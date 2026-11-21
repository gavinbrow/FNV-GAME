"""Compare all paired TESForm and BGSE mapped functions and BGSE RTTI slots."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;O=M/'out/phase2-tesform-paired-closure';T=M/'out/phase2-tesform-base-slots';B=M/'out/phase2-bgsencounterzone-six-override';F=P/'fnv_decomp'
sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_viewer_compare as helpers,rtti_bgse_six_compare as bg,class_metadata_compare as cm
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tes_unit(u,meta):
 changes={x['before']:x['after'] for x in meta['proposed_function_symbol_changes']}
 if len(changes)!=2:raise ValueError('expected two remaps')
 out=copy.deepcopy(u);count=0
 for f in out['functions']:
  if f['symbol'] in changes:f['symbol']=changes[f['symbol']];count+=1
  f['fold_aliases']=[changes.get(x,x) for x in f.get('fold_aliases',[])]
 if count!=2:raise ValueError('function remap mismatch')
 symbols={}
 for k,v in u['symbols'].items():
  k=changes.get(k,k)
  if k in symbols and symbols[k]!=v:raise ValueError('symbol collision')
  symbols[k]=v
 for x in meta['proposed_function_symbol_changes']:
  if x['after'] in symbols and symbols[x['after']]!=x['address']:raise ValueError('symbol address collision')
  symbols[x['after']]=x['address']
 out['symbols']=symbols;return out,{v:k for k,v in changes.items()}
def main():
 if sha(O/'closure-manifest.json')!='55e56bc5b2ee85b07fffcaa5322b4dc135ad526fce5f78598421f1be1b1f5e0a':raise ValueError('closure manifest changed')
 report=O/'comparison.json';graph=O/'bgs-class-metadata.json'
 if report.exists() or graph.exists():raise FileExistsError('refusing overwrite')
 closure=json.loads((O/'closure-manifest.json').read_text());tm=json.loads((T/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text());compiled=json.loads((O/'compile-result.json').read_text());units_path=F/'build/units.json';census_path=M/'out/phase2-class-census/census-current.json'
 for p,d in [(units_path,closure['units_sha256']),(T/'manifest.json',closure['tes_manifest_sha256']),(B/'manifest.json',closure['bgs_manifest_sha256']),(census_path,closure['census_sha256'])]:
  if sha(p)!=d:raise ValueError('pinned input mismatch')
 objs={x['source']:O/(x['source']+'.obj') for x in compiled['outcomes']}
 if set(objs)!={'tes_original','tes_overlay','bgs_original','bgs_overlay'}:raise ValueError('incomplete compile')
 for x in compiled['outcomes']:
  if x['rc'] or not x['object_present'] or sha(objs[x['source']])!=x['object_sha256']:raise ValueError('bad object')
 units=json.loads(units_path.read_text())['units'];tu=units[998];bu=units[2]
 if len(tu['functions'])!=128 or len(bu['functions'])!=24:raise ValueError('function count')
 mt,nt=tes_unit(tu,tm);mb,nb=bg.make_unit(bu,bm)
 for x in tm['proposed_function_symbol_changes']:
  if x['after'] in mb['symbols'] and mb['symbols'][x['after']]!=x['address']:raise ValueError('BGSE alias collision')
  mb['symbols'][x['after']]=x['address']
 pe=Pe(paths.REF_IMAGE);out={}
 for label,u,mapping,norm in [('tes',tu,mt,nt),('bgs',bu,mb,nb)]:
  original=Coff(str(objs[label+'_original']));overlay=Coff(str(objs[label+'_overlay']));facts=[]
  for old,new in zip(u['functions'],mapping['functions']):
   try:
    norm2=bg.normalization_for_function(old['symbol'],norm) if label=='bgs' else norm
    a,ar=helpers.relocated(original,old['symbol'],old['size'],{});b,br=helpers.relocated(overlay,new['symbol'],new['size'],norm2)
    facts.append({'address':old['address'],'old':old['symbol'],'new':new['symbol'],'bytes_equal':a==b,'relocations_equal':ar==br})
   except (ValueError,KeyError,IndexError) as e:facts.append({'address':old['address'],'error':str(e)})
  refs={}
  for tag,obj,spec in [('original',original,u),('overlay',overlay,mapping)]:
   try:refs[tag]=[{'address':r['address'],'verdict':r['verdict'],'error_count':len(r['errors']),'byte_difference_count':len(r['byte_differences']),'failed_relocations':sum(not x.get('match') for x in r['relocations'])} for r in compare(obj,pe,spec)]
   except Exception as e:refs[tag]={'fatal':type(e).__name__+': '+str(e)}
  out[label]={'functions':facts,'reference':refs}
 census=json.loads(census_path.read_text())
 if census['inputs']['units_sha256']!=closure['units_sha256']:raise ValueError('census recipe mismatch')
 class_result=cm.compare_class(objs['bgs_overlay'],mb,units,census,'.?AVBGSEncounterZone@@')
 report.write_text(json.dumps(out,indent=2));graph.write_text(json.dumps(class_result,indent=2));print(json.dumps({k:{'functions':len(v['functions']),'bytes_equal':sum(x.get('bytes_equal',False) for x in v['functions']),'relocations_equal':sum(x.get('relocations_equal',False) for x in v['functions'])} for k,v in out.items()}))
if __name__=='__main__':main()
