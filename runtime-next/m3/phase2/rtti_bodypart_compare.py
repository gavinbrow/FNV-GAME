"""Compare private BGSBodyPart object, preserving the 15-function gates."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;PROJECT=RN.parent;OUT=M/'out/phase2-bgsbodypart-slot0'
sys.path[:0]=[str(PROJECT/'fnv_decomp/tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_viewer_compare as helpers,class_metadata_compare as cm


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def make_unit(unit,metadata):
    changes={r['before']:r['after'] for r in metadata['proposed_function_symbol_changes']}
    if len(changes)!=1:raise ValueError('expected one source symbol change')
    new=copy.deepcopy(unit)
    new['functions']=[dict(f,symbol=changes.get(f['symbol'],f['symbol']),fold_aliases=[changes.get(s,s) for s in f.get('fold_aliases',[])]) for f in unit['functions']]
    if sum(a['symbol']!=b['symbol'] for a,b in zip(unit['functions'],new['functions']))!=1:raise ValueError('expected remapped function count differs')
    symbols={}
    for k,v in unit['symbols'].items():
        target=changes.get(k,k)
        if target in symbols and symbols[target]!=v:raise ValueError('symbol remap collision')
        symbols[target]=v
    new['symbols']=symbols
    return new,{after:before for before,after in changes.items()}


def normalization_for_function(symbol,normalization):
    return dict(normalization)


def main():
    targets=[OUT/'unit-overlay-v2.json',OUT/'coff-comparison-v2.json',OUT/'class-metadata-comparison-v2.json']
    if any(p.exists() for p in targets):raise FileExistsError('refusing overwrite')
    metadata=json.loads((OUT/'manifest.json').read_text());compiled=json.loads((OUT/'compile-result.json').read_text());units_path=PROJECT/'fnv_decomp/build/units.json'
    if sha(units_path)!=metadata['input_sha256']['units']:raise ValueError('unit recipe changed')
    units=json.loads(units_path.read_text())['units'];unit=units[620]
    if len(unit['functions'])!=15:raise ValueError('unexpected unit function count')
    objects={tag:OUT/('0620.%s.obj'%tag) for tag in ('original','combined')};results={r['source']:r for r in compiled['outcomes']}
    for tag,p in objects.items():
        if tag not in results or results[tag]['rc'] or not results[tag]['object_present'] or sha(p)!=results[tag]['object_sha256']:raise ValueError('compiled object mismatch: '+tag)
    mapped,normalization=make_unit(unit,metadata);original=Coff(str(objects['original']));combined=Coff(str(objects['combined']));facts=[]
    for f,new in zip(unit['functions'],mapped['functions']):
        try:
            normal=normalization_for_function(f['symbol'],normalization)
            a,ar=helpers.relocated(original,f['symbol'],f['size'],{});b,br=helpers.relocated(combined,new['symbol'],new['size'],normal)
            facts.append({'address':f['address'],'original_symbol':f['symbol'],'overlay_symbol':new['symbol'],'code_bytes_equal':a==b,'normalized_relocations_equal':ar==br,'original_relocation_count':len(ar),'overlay_relocation_count':len(br)})
        except (ValueError,KeyError,IndexError) as exc:facts.append({'address':f['address'],'original_symbol':f['symbol'],'overlay_symbol':new['symbol'],'error':str(exc)})
    pe=Pe(paths.REF_IMAGE);reports={}
    for tag,c,spec in [('original',original,unit),('combined',combined,mapped)]:
        try:
            rows=compare(c,pe,spec)
            reports[tag]=[{'address':r['address'],'verdict':r['verdict'],'error_count':len(r['errors']),'byte_difference_count':len(r['byte_differences']),'failed_relocations':sum(not x.get('match') for x in r['relocations'])} for r in rows]
        except Exception as exc:reports[tag]={'fatal':type(exc).__name__+': '+str(exc)}
    general={'scope':'private 15-function comparison; no complete ABI or ownership claim',
             'object_hashes':{k:sha(v) for k,v in objects.items()},'functions':facts,'reference_comparator':reports}
    for p,data in zip(targets[:2],(mapped,general)):
        with p.open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    print(json.dumps({'functions':len(facts),'code_equal':sum(x.get('code_bytes_equal',False) for x in facts),'normalized_relocations_equal':sum(x.get('normalized_relocations_equal',False) for x in facts),'reference_summary':{k:({'match':sum(x['verdict']=='match' for x in v),'other':sum(x['verdict']!='match' for x in v)} if isinstance(v,list) else v) for k,v in reports.items()}}))

if __name__=='__main__':main()
