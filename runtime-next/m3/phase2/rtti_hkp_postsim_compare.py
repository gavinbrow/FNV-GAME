"""Compare the hkp post-simulation prototype against 16 original functions and RTTI."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;PROJECT=RN.parent;OUT=M/'out/phase2-hkp-postsim-v3';BASE=M/'out/phase2-hkp-constraint-viewer'
sys.path[:0]=[str(PROJECT/'fnv_decomp/tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_hierarchy_compare as hc,rtti_hkp_viewer_compare as vc,class_metadata_compare as cm


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def make_unit(unit,m):
 method=m['proposed_method'];helper=m['proposed_helper_alias'];new=copy.deepcopy(unit);mapping={}
 for key,value in unit['symbols'].items():
  target=hc.translated(key)
  if target in mapping and mapping[target]!=value:raise ValueError('translated source symbol collision')
  mapping[target]=value
 if unit['symbols'].get(helper['before'])!=helper['address']:raise ValueError('source helper alias changed')
 if helper['after'] in mapping and mapping[helper['after']]!=helper['address']:raise ValueError('candidate helper collision')
 mapping[helper['after']]=helper['address'];new['symbols']=mapping
 funcs=[];matched=0
 for f in unit['functions']:
  symbol=method['after'] if f['symbol']==method['before'] else hc.translated(f['symbol'])
  if f['symbol']==method['before']:
   if f['address']!=method['address'] or f['size']!=method['size']:raise ValueError('candidate method changed')
   matched+=1
  funcs.append(dict(f,symbol=symbol,fold_aliases=[hc.translated(x) for x in f.get('fold_aliases',[])]))
 if matched!=1:raise ValueError('candidate function absent or ambiguous')
 new['functions']=funcs
 normalization={hc.translated(k):k for k in unit['symbols']}
 for f in unit['functions']:
  normalization[hc.translated(f['symbol'])]=f['symbol']
 normalization[method['after']]=method['before'];normalization[helper['after']]=helper['before']
 return new,normalization


def main():
 targets=[OUT/'unit-overlay.json',OUT/'coff-postsim-comparison.json',OUT/'class-metadata-comparison.json']
 if any(p.exists() for p in targets):raise FileExistsError('refusing overwrite')
 m=json.loads((OUT/'manifest.json').read_text());result=json.loads((OUT/'compile-result.json').read_text());units_path=PROJECT/'fnv_decomp/build/units.json';raw=units_path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=m['units_sha256']:raise ValueError('unit digest changed')
 original=BASE/'2501.original.obj';compiled=OUT/'2501.hierarchy.obj';baseline=json.loads((BASE/'compile-result.json').read_text())
 original_result=next(x for x in baseline['outcomes'] if x['source']=='original')
 if sha(original)!=original_result['object_sha256'] or result['rc'] or sha(compiled)!=result['object_sha256']:raise ValueError('object hash mismatch')
 units=json.loads(raw)['units'];unit=units[2501];mapped,normalization=make_unit(unit,m);old=Coff(str(original));new=Coff(str(compiled));facts=[]
 for f,n in zip(unit['functions'],mapped['functions']):
  try:
   a,ar=vc.relocated(old,f['symbol'],f['size'],{});b,br=vc.relocated(new,n['symbol'],n['size'],normalization)
   facts.append({'address':f['address'],'before':f['symbol'],'after':n['symbol'],'code_bytes_equal':a==b,'normalized_relocations_equal':ar==br})
  except (ValueError,KeyError,IndexError) as exc:facts.append({'address':f['address'],'error':str(exc)})
 try:
  rs=compare(new,Pe(paths.REF_IMAGE),mapped)
  refs=[{'address':r['address'],'verdict':r['verdict'],'errors':len(r['errors']),'byte_differences':len(r['byte_differences']),'failed_relocations':sum(not x.get('match') for x in r['relocations'])} for r in rs]
 except Exception as exc:refs={'fatal':type(exc).__name__+': '+str(exc)}
 census_path=M/'out/phase2-class-census/census-v2.json';census=json.loads(census_path.read_text())
 if census['inputs']['units_sha256']!=m['units_sha256']:raise ValueError('census unit digest mismatch')
 class_result=cm.compare_class(compiled,mapped,units,census,'.?AVhkpConstraintViewer@@')
 class_result['inputs']={'unit_index':2501,'units_sha256':m['units_sha256'],'census_sha256':sha(census_path),'overlay_sha256':m['new_overlay_sha256']}
 details={'scope':'private source method move hypothesis, no global ABI or ownership proof','functions':facts,'reference_comparator':refs,'proposed_helper_alias':m['proposed_helper_alias']}
 for p,data in zip(targets,(mapped,details,class_result)):
  with p.open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
 tables=class_result['tables'];print(json.dumps({'functions':len(facts),'raw_equal':sum(x.get('code_bytes_equal',False) for x in facts),'normalized_relocations_equal':sum(x.get('normalized_relocations_equal',False) for x in facts),'missing':sum('error' in x for x in facts),'reference':{'match':sum(x['verdict']=='match' for x in refs),'wip':sum(x['verdict']!='match' for x in refs)} if isinstance(refs,list) else refs,'tables':len(tables),'graph_matches':sum(x.get('graph_fields_equal',False) for x in tables),'slots_matched':sum(y['match'] for x in tables for y in x.get('slots',[]))}))

if __name__=='__main__':main()
