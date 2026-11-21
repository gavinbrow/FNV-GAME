import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-skyobject-destructor-v1'
sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_viewer_compare as helper,class_metadata_compare as cm
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=O/'comparison.json';graph=O/'class-metadata.json'
 if out.exists() or graph.exists():raise FileExistsError('refusing overwrite')
 meta=json.loads((O/'manifest.json').read_text());comp=json.loads((O/'compile-result.json').read_text());up=F/'build/units.json';cpath=M/'out/phase2-class-census/census-current.json'
 if sha(up)!=meta['input_sha256']['units'] or sha(cpath)!='e7ae33cc2404a8d9628ad2148bcd9292479f5a0964caa2405433f2b6053bf333':raise ValueError('pinned inputs changed')
 units=json.loads(up.read_text())['units'];unit=units[925];mapped=copy.deepcopy(unit);remap={x['before']:x['after'] for x in meta['proposed_function_symbol_changes']};normal={v:k for k,v in remap.items()}
 for a in meta['proposed_external_aliases']:
  old,new,va=a['old'],a['new'],a['address']
  if unit['symbols'].get(old)!=va or sum(x.get('symbols',{}).get(new)==va for x in units)<2:raise ValueError('alias evidence changed')
  mapped['symbols'][new]=va;normal[new]=old
 for f in mapped['functions']:f['symbol']=remap.get(f['symbol'],f['symbol'])
 for x in meta['proposed_function_symbol_changes']:mapped['symbols'][x['after']]=x['address']
 objects={x['source']:O/('0925.'+x['source']+'.obj') for x in comp['outcomes']}
 if set(objects)!={'original','combined'}:raise ValueError('incomplete compile')
 for x in comp['outcomes']:
  if x['rc'] or sha(objects[x['source']])!=x['object_sha256']:raise ValueError('bad object')
 a=Coff(str(objects['original']));b=Coff(str(objects['combined']));facts=[]
 for x,y in zip(unit['functions'],mapped['functions']):
  try:
   n=dict(normal)
   if x['address']=='0x0063f8d0':n['??_7SkyObject@@6B@']='??_7FUN_0063f8d0@@6B@'
   c,cr=helper.relocated(a,x['symbol'],x['size'],{});d,dr=helper.relocated(b,y['symbol'],y['size'],n)
   facts.append({'address':x['address'],'bytes_equal':c==d,'relocations_equal':cr==dr})
  except (ValueError,KeyError,IndexError) as e:facts.append({'address':x['address'],'error':str(e)})
 pe=Pe(paths.REF_IMAGE);ref={}
 for k,obj,spec in [('original',a,unit),('combined',b,mapped)]:
  try:ref[k]=[{'address':r['address'],'verdict':r['verdict'],'errors':len(r['errors']),'byte_differences':len(r['byte_differences']),'failed_relocations':sum(not z.get('match') for z in r['relocations'])} for r in compare(obj,pe,spec)]
  except Exception as e:ref[k]={'fatal':type(e).__name__+': '+str(e)}
 census=json.loads(cpath.read_text());g=cm.compare_class(objects['combined'],mapped,units,census,'.?AVSkyObject@@')
 out.write_text(json.dumps({'functions':facts,'reference':ref,'notes':'function-body comparison does not prove deleting destructor or exception handler conformance'},indent=2));graph.write_text(json.dumps(g,indent=2));print(json.dumps(facts))
if __name__=='__main__':main()
