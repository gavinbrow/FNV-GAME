"""Compare isolated hierarchy hypothesis against unit code and original RTTI graph."""
import copy,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;RN=M3.parent;PROJECT=RN.parent;OUT=M3/'out/phase2-hkp-destructor-v2';BASE=M3/'out/phase2-hkp-constraint-viewer'
sys.path[:0]=[str(PROJECT/'fnv_decomp/tools'),str(RN),str(HERE)]
from compare import Coff,Pe,compare
import paths,rtti_hierarchy_analysis as hierarchy,rtti_hkp_viewer_compare as oldcompare,rtti_hkp_hierarchy_overlay as transform


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def translated(name):
    if name.startswith('??_C@'):return name
    maps=list(transform.MAP)+[(transform.base.OLD,transform.base.NEW,4)]
    for old,new,_ in sorted(maps,key=lambda row:-len(row[0])):name=name.replace(old,new)
    return name

def base_name(symbol):
    m=re.fullmatch(r'\?\?_R0\?AV(.+)@@@8',symbol)
    if not m:raise ValueError('unexpected base type symbol: '+symbol)
    return '.?AV'+m.group(1)+'@@'

def main():
    output=OUT/'coff-hierarchy-comparison.json'
    if output.exists():raise FileExistsError('refusing overwrite')
    manifest=json.loads((OUT/'manifest.json').read_text());result=json.loads((OUT/'compile-result.json').read_text());base_result=json.loads((BASE/'compile-result.json').read_text());obj=OUT/'2501.hierarchy.obj';baseline=BASE/'2501.original.obj';units=PROJECT/'fnv_decomp/build/units.json'
    if result['rc'] or not result['object_present'] or sha(obj)!=result['object_sha256']:raise ValueError('hierarchy object mismatch')
    orig=next(x for x in base_result['outcomes'] if x['source']=='original')
    if orig['rc'] or sha(baseline)!=orig['object_sha256'] or sha(units)!=manifest['units_sha256']:raise ValueError('baseline or unit hash mismatch')
    unit=json.loads(units.read_text())['units'][2501]
    if len(unit['functions'])!=16:raise ValueError('unexpected function count')
    translated_keys={};normalization={}
    for name,value in unit['symbols'].items():
        new=translated(name)
        if new in translated_keys and translated_keys[new]!=value:raise ValueError('translated symbol collision')
        translated_keys[new]=value
        if new in normalization and normalization[new]!=name:raise ValueError('ambiguous reverse mapping')
        normalization[new]=name
    mapped=copy.deepcopy(unit);mapped['symbols']=translated_keys
    mapped['functions']=[dict(f,symbol=translated(f['symbol']),fold_aliases=[translated(x) for x in f.get('fold_aliases',[])]) for f in unit['functions']]
    original=Coff(str(baseline));current=Coff(str(obj));rows=[]
    for f,new in zip(unit['functions'],mapped['functions']):
        try:
            a,ar=oldcompare.relocated(original,f['symbol'],f['size'],{});b,br=oldcompare.relocated(current,new['symbol'],new['size'],normalization)
            rows.append({'address':f['address'],'original_symbol':f['symbol'],'overlay_symbol':new['symbol'],'code_bytes_equal':a==b,'normalized_relocations_equal':ar==br,'original_relocation_count':len(ar),'overlay_relocation_count':len(br)})
        except (ValueError,KeyError,IndexError) as exc:rows.append({'address':f['address'],'original_symbol':f['symbol'],'overlay_symbol':new['symbol'],'error':str(exc)})
    try:
        reports=compare(current,Pe(paths.REF_IMAGE),mapped)
        refs=[{'address':x['address'],'verdict':x['verdict'],'error_count':len(x['errors']),'byte_difference_count':len(x['byte_differences']),'failed_relocations':sum(not r.get('match') for r in x['relocations'])} for x in reports]
    except Exception as exc:refs={'fatal':type(exc).__name__+': '+str(exc)}
    original_graph=hierarchy.original();new_graph=hierarchy.overlay(obj); rb=original_graph['hierarchy']['bases'];nb=new_graph['hierarchy']['bases'];facts=[]
    for i in range(max(len(rb),len(nb))):
        a=rb[i] if i<len(rb) else None;b=nb[i] if i<len(nb) else None
        facts.append({'index':i,'reference_name':a['type_name'] if a else None,'overlay_name':base_name(b['type_symbol']) if b else None,
                      'name_equal':bool(a and b and a['type_name']==base_name(b['type_symbol'])),
                      'contained_count_equal':bool(a and b and a['contained_bases']==b['contained_bases']),
                      'pmd_equal':bool(a and b and a['pmd']==b['pmd']),'attributes_equal':bool(a and b and a['attributes']==b['attributes'])})
    graph={'reference_base_count':len(rb),'overlay_base_count':len(nb),'signature_equal':original_graph['hierarchy']['signature']==new_graph['hierarchy']['signature'],
           'hierarchy_attributes_equal':original_graph['hierarchy']['attributes']==new_graph['hierarchy']['attributes'],
           'locator_offsets_equal':sorted(x['offset'] for x in original_graph['locators'])==sorted(x['offset'] for x in new_graph['locators']),'base_records':facts,
           'scope':'Compares numeric fields and decorated type names only; relocation target placements, full vtables, alias collisions, and game behavior not established.'}
    data={'schema_version':1,'scope':'One isolated candidate; reference-guided metadata hypothesis, not native source identity proof','object_sha256':sha(obj),'unit_functions':rows,'reference_comparator':refs,'graph':graph}
    with output.open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    print(json.dumps({'functions':len(rows),'raw_equal':sum(r.get('code_bytes_equal',False) for r in rows),'normalized_relocs_equal':sum(r.get('normalized_relocations_equal',False) for r in rows),'missing':sum('error' in r for r in rows),
                      'reference_base_count':len(rb),'overlay_base_count':len(nb),'base_records_match':sum(all(x[k] for k in ('name_equal','contained_count_equal','pmd_equal','attributes_equal')) for x in facts),'reference_comparison':{'match':sum(x['verdict']=='match' for x in refs),'wip':sum(x['verdict']!='match' for x in refs)} if isinstance(refs,list) else refs}))

if __name__=='__main__':main()
