"""Compare one private overlay COFF to its original unit and reference, read-only."""
import copy,hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; M3=HERE.parent;RN=M3.parent;PROJECT=RN.parent;OUT=M3/'out/phase2-hkp-constraint-viewer'
sys.path[:0]=[str(PROJECT/'fnv_decomp/tools'),str(RN),str(M3)]
from compare import Coff,Pe,compare
import paths
OLD='FUN_00d698b0';NEW='hkpConstraintViewer'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def relocated(coff,symbol,size,normalization):
    sy=coff.named(symbol);sec=coff.sections[sy['section']];start=sy['value'];data=sec['data'][start:start+size]
    if len(data)!=size:raise ValueError('short code section: '+symbol)
    rel=[]
    for off,index,kind in sec['relocs']:
        if start<=off<start+size:
            if off+4>start+size:raise ValueError('relocation crosses function boundary')
            target=coff.symbols[index]['name'];target=normalization.get(target,target)
            rel.append((off-start,kind,target,int.from_bytes(data[off-start:off-start+4],'little')))
    return data,sorted(rel)


def main():
    output=OUT/'coff-comparison-v2.json'
    if output.exists():raise FileExistsError('refusing to overwrite prior comparison')
    manifest=json.loads((OUT/'manifest.json').read_text());compile_result=json.loads((OUT/'compile-result.json').read_text());units_path=PROJECT/'fnv_decomp/build/units.json'
    if sha(units_path)!=manifest['units_sha256']:raise ValueError('unit recipe changed')
    results={x['source']:x for x in compile_result['outcomes']};objs={k:OUT/('2501.%s.obj'%k) for k in ('original','overlay')}
    for k,p in objs.items():
        if k not in results or results[k]['rc'] or sha(p)!=results[k]['object_sha256']:raise ValueError('object differs from compile result')
    original=Coff(str(objs['original']));overlay=Coff(str(objs['overlay']));unit=json.loads(units_path.read_text())['units'][2501]
    if len(unit['functions'])!=16:raise ValueError('unit function count changed')
    mapped=copy.deepcopy(unit)
    mapped['functions']=[dict(f,symbol=f['symbol'].replace(OLD,NEW),fold_aliases=[x.replace(OLD,NEW) for x in f.get('fold_aliases',[])]) for f in unit['functions']]
    translated={}
    for k,v in unit['symbols'].items():
        name=k.replace(OLD,NEW)
        if name in translated and translated[name]!=v:raise ValueError('remapped unit symbol collision')
        translated[name]=v
    mapped['symbols']=translated
    normalization={}
    for old in list(unit['symbols']) + [f['symbol'] for f in unit['functions']] + [x for f in unit['functions'] for x in f.get('fold_aliases',[])]:
        new=old.replace(OLD,NEW)
        if new in normalization and normalization[new]!=old: raise ValueError('ambiguous normalized symbol')
        normalization[new]=old
    facts=[]
    for old,new in zip(unit['functions'],mapped['functions']):
        a,ar=relocated(original,old['symbol'],old['size'],{});b,br=relocated(overlay,new['symbol'],new['size'],normalization)
        facts.append({'address':old['address'],'original_symbol':old['symbol'],'overlay_symbol':new['symbol'],
                      'code_bytes_equal':a==b,'normalized_relocations_equal':ar==br,'original_relocation_count':len(ar),'overlay_relocation_count':len(br)})
    pe=Pe(paths.REF_IMAGE); checked={}
    for tag,coff,spec in [('original',original,unit),('overlay',overlay,mapped)]:
        try:
            reports=compare(coff,pe,spec)
            checked[tag]=[{'address':r['address'],'verdict':r['verdict'],'error_count':len(r['errors']),'byte_difference_count':len(r['byte_differences']),
                           'relocation_count':len(r['relocations']),'failed_relocations':sum(not x.get('match') for x in r['relocations'])} for r in reports]
        except Exception as exc:checked[tag]={'fatal':type(exc).__name__+': '+str(exc)}
    td=overlay.named('??_R0?AVhkpConstraintViewer@@@8');section=overlay.sections[td['section']];start=td['value'];data=section['data'][start:]; ref=pe.read(0x011b616c,len(data));rels=[(off-start,kind,overlay.symbols[idx]['name']) for off,idx,kind in section['relocs'] if start<=off<start+len(data)]
    unmasked_equal=all(data[i]==ref[i] for i in range(len(data)) if not any(off<=i<off+4 for off,_,_ in rels))
    all_units=json.loads(units_path.read_text())['units']
    typeinfo_targets={int(v,0) for u in all_units for k,v in u.get('symbols',{}).items() if k=='??_7type_info@@6B@'}
    if len(typeinfo_targets)!=1: raise ValueError('type_info vtable mapping is not unique')
    typeinfo_target=next(iter(typeinfo_targets))
    expected=(typeinfo_target+int.from_bytes(data[:4],'little')) & 0xffffffff
    relocation_matches=(rels==[(0,6,'??_7type_info@@6B@')] and expected==int.from_bytes(ref[:4],'little'))
    out={'scope':'unit-local original-vs-overlay and reference comparator; no placement or runtime guarantee','source_sha256':manifest['source_sha256'],'overlay_sha256':manifest['overlay_sha256'],
         'functions':facts,'reference_comparator':checked,'rtti_type_descriptor':{'symbol':td['name'],'coff_section':section['name'],'symbol_offset':start,
         'section_tail_bytes':len(data),'relocations':[{'offset':off,'kind':kind,'symbol':name} for off,kind,name in rels],
         'reference_va':'0x011b616c','nonrelocated_bytes_match_reference':unmasked_equal,'resolved_relocation_matches_reference':relocation_matches,
         'typeinfo_target_va':hex(typeinfo_target),'extent_warning':'section tail is not independent proof of original descriptor extent; W owner includes a further relocation at +36'}}
    with output.open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'functions':len(facts),'code_bytes_equal':sum(x['code_bytes_equal'] for x in facts),'normalized_relocations_equal':sum(x['normalized_relocations_equal'] for x in facts),'descriptor':out['rtti_type_descriptor'],'reference_summary':{k:({z:sum(x['verdict']==z for x in v) for z in ('match','wip')} if isinstance(v,list) else v) for k,v in checked.items()}}))

if __name__=='__main__':main()
