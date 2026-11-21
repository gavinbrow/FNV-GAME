"""Compare private BGSE combined object, preserving the normal 24-function gates."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;PROJECT=RN.parent;OUT=M/'out/phase2-bgsencounterzone-six-override'
sys.path[:0]=[str(PROJECT/'fnv_decomp/tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_viewer_compare as helpers,class_metadata_compare as cm


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def make_unit(unit,metadata):
    changes={r['before']:r['after'] for r in metadata['proposed_function_symbol_changes']}
    if len(changes)!=9:raise ValueError('expected nine distinct source symbol changes')
    new=copy.deepcopy(unit)
    new['functions']=[dict(f,symbol=changes.get(f['symbol'],f['symbol']),fold_aliases=[changes.get(s,s) for s in f.get('fold_aliases',[])]) for f in unit['functions']]
    if sum(a['symbol']!=b['symbol'] for a,b in zip(unit['functions'],new['functions']))!=9:raise ValueError('expected remapped function count differs')
    alias=metadata['proposed_external_symbol_alias'];name=alias['after'];va=alias['address']
    values={x['address'] for x in alias['independent_unit_evidence']}
    if values!={va} or len(alias['independent_unit_evidence'])<2:raise ValueError('external alias evidence ambiguous')
    symbols={}
    for k,v in unit['symbols'].items():
        target=changes.get(k,k)
        if target in symbols and symbols[target]!=v:raise ValueError('symbol remap collision')
        symbols[target]=v
    if name in symbols and symbols[name]!=va:raise ValueError('base destructor alias collision')
    symbols[name]=va;new['symbols']=symbols
    normalize={after:before for before,after in changes.items()}
    # The constructor/destructor use distinct named vtable keys which this
    # original unit independently maps to the same address. This is only a
    # relocation-target normalization, not proof that the vtables are equal.
    old_vtable='??_7FUN_00525ce0@@6B@';new_vtable='??_7BGSEncounterZone@@6B@'
    if old_vtable not in unit['symbols'] or unit['symbols'].get(old_vtable)!=unit['symbols'].get(new_vtable):
        raise ValueError('co-addressed vtable key evidence absent')
    return new,normalize


def normalization_for_function(symbol,normalization):
    result=dict(normalization)
    if symbol=='??1FUN_00525ce0@@UAE@XZ':
        result['??_7BGSEncounterZone@@6B@']='??_7FUN_00525ce0@@6B@'
        result['??1TESForm@@UAE@XZ']='??1Base5a@@UAE@XZ'
    return result


def main():
    targets=[OUT/'unit-overlay-v2.json',OUT/'coff-comparison-v2.json',OUT/'class-metadata-comparison-v2.json']
    if any(p.exists() for p in targets):raise FileExistsError('refusing overwrite')
    metadata=json.loads((OUT/'manifest.json').read_text());compiled=json.loads((OUT/'compile-result.json').read_text());units_path=PROJECT/'fnv_decomp/build/units.json'
    if sha(units_path)!=metadata['input_sha256']['units']:raise ValueError('unit recipe changed')
    units=json.loads(units_path.read_text())['units'];unit=units[2]
    if len(unit['functions'])!=24:raise ValueError('unexpected unit function count')
    objects={tag:OUT/('0002.%s.obj'%tag) for tag in ('original','combined')};results={r['source']:r for r in compiled['outcomes']}
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
    census_path=M/'out/phase2-class-census/census-v2.json';census=json.loads(census_path.read_text())
    if census['inputs']['units_sha256']!=metadata['input_sha256']['units']:raise ValueError('census recipe hash mismatch')
    class_result=cm.compare_class(objects['combined'],mapped,units,census,'.?AVBGSEncounterZone@@')
    class_result['inputs']={'unit_index':2,'units_sha256':metadata['input_sha256']['units'],'census_sha256':sha(census_path),'source_overlay_sha256':metadata['source_overlay_sha256'],'header_overlay_sha256':metadata['header_overlay_sha256']}
    general={'scope':'private 24-function original/combined comparison; proposed source-based unit alias only; full ABI and ownership not established',
             'object_hashes':{k:sha(v) for k,v in objects.items()},'functions':facts,'reference_comparator':reports,'proposed_external_alias':metadata['proposed_external_symbol_alias'],
             'vtable_relocation_normalization':{'old':'??_7FUN_00525ce0@@6B@','new':'??_7BGSEncounterZone@@6B@','address':unit['symbols']['??_7BGSEncounterZone@@6B@'],'scope':'unit source keys map to same reference address; no emitted slot-equivalence claim'}}
    for p,data in zip(targets,(mapped,general,class_result)):
        with p.open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    tables=class_result['tables'];print(json.dumps({'function_count':len(facts),'code_equal':sum(x.get('code_bytes_equal',False) for x in facts),'normalized_relocs_equal':sum(x.get('normalized_relocations_equal',False) for x in facts),'missing':sum('error' in x for x in facts),
      'reference_summary':{k:({'match':sum(x['verdict']=='match' for x in v),'wip':sum(x['verdict']!='match' for x in v)} if isinstance(v,list) else v) for k,v in reports.items()},'emitted_tables':len(tables),'graph_matches':sum(t.get('graph_fields_equal',False) for t in tables),'slots':sum(t.get('emitted_slot_count',0) for t in tables),'matched_slots':sum(s['match'] for t in tables for s in t.get('slots',[]))}))

if __name__=='__main__':main()
