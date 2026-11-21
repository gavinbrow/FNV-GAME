"""Audit one NiMemObject kind mirror without borrowing baseline bindings."""
import argparse,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from class_metadata_compare import ObjectRecords
from rtti_hkp_viewer_compare import relocated
import paths
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True,type=int);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--production-object-sha256',required=True);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()):raise ValueError('private output required')
 report=out/'comparison.json'
 if report.exists():raise FileExistsError('preserve prior evidence')
 recipe=F/'build/units.json';mm=out/'mirror-manifest.json';m=json.loads(mm.read_text());run=json.loads((out/'compile-result.json').read_text());prod=M/('out/phase2-nimem-kind-production-archive/%04d.obj'%a.unit)
 if sha(recipe)!=BASE or m['unit']!=a.unit or run['unit_index']!=a.unit or run['mirror_manifest_sha256']!=sha(mm) or sha(prod)!=a.production_object_sha256.lower():raise ValueError('input identity differs')
 units=json.loads(recipe.read_text())['units'];spec=units[a.unit];pe=Pe(paths.REF_IMAGE);names=recipe_names(units);objs={'production':Coff(str(prod))};rows={};eh={};facts={}
 for record in run['outcomes']:
  f=out/(record['tag']+'.obj')
  if record['rc'] or not record['trace_valid'] or sha(f)!=record['object_sha256']:raise ValueError('compile invalid')
  objs[record['tag']]=Coff(str(f))
 if set(objs)!={'production','original','candidate'}:raise ValueError('missing object')
 for tag,c in objs.items():
  try:
   r=compare(c,pe,spec);rows[tag]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'verdict':x['verdict'],'errors':x['errors'],'unmatched_relocations':[{'offset':z['offset'],'symbol':z['symbol']} for z in x['relocations'] if not z.get('match')]} for x in r if x['verdict']!='match']}
   sec,inf,errors=eh_sections(c,pe,spec,r,names);eh[tag]={'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()},'errors':errors}
  except (ValueError,KeyError,IndexError) as e:rows[tag]={'fatal':type(e).__name__+': '+str(e)};eh[tag]={'eh_sections':[],'eh_inferred':{},'errors':['comparison prerequisite failed']}
  symbols=[]
  for name,group in c.by_name.items():
   if 'NiMemObject' in name:symbols.append({'name':name,'definitions':sum(x['section']>0 for x in group),'undefined':sum(x['section']==0 for x in group)})
  graphs=[]
  try:
   for t in ObjectRecords(c).tables('.?AVNiRefObject@@'):graphs.append({'symbol':t['symbol'],'locator':t['locator'],'slots':[x['symbol']['name'] for x in t['slots']]})
  except Exception as e:graphs=[{'error':type(e).__name__+': '+str(e)}]
  facts[tag]={'nimem_symbols':symbols,'niref_graphs':graphs}
 pair=[]
 for f in spec['functions']:
  try:
   a0,ar=relocated(objs['original'],f['symbol'],f['size'],{});b0,br=relocated(objs['candidate'],f['symbol'],f['size'],{})
   if a0!=b0 or ar!=br:pair.append({'address':f['address'],'bytes_equal':a0==b0,'relocation_changes':[{'original':list(x),'candidate':list(y)} for x,y in zip(ar,br) if x!=y],'original_relocations':len(ar),'candidate_relocations':len(br)})
  except (ValueError,KeyError,IndexError) as e:pair.append({'address':f['address'],'error':type(e).__name__+': '+str(e)})
 result={'unit':a.unit,'recipe_sha256':BASE,'production_object_sha256':sha(prod),'mirror_manifest_sha256':sha(mm),'compile_result_sha256':sha(out/'compile-result.json'),'strict_reference':rows,'ordinary_eh':eh,'mapped_function_pair_differences':pair,'emitted_classkey_evidence':facts,'compiler_classkey_warnings':{x['tag']:x['class_key_warnings'] for x in run['outcomes']},'limits':['unit-only strict baseline; unresolved failures are not borrowed or normalized','compiled RTTI/symbol evidence does not establish first declaration in translation units that do not emit those records','global ordinary EH inference conflicts and outside owners require cohort union','no production recipe or source changes']}
 report.write_text(json.dumps(result,indent=2));print(json.dumps({'unit':a.unit,'reference_matches':{k:v.get('matches') for k,v in rows.items()},'pair_differences':len(pair),'classkey_warnings':sum(len(x) for x in result['compiler_classkey_warnings'].values())}))
if __name__=='__main__':main()
