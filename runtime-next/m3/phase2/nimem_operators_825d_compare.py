"""Strict source/operator consumer audit; never normalizes code differences."""
import argparse,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-operators-825d';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True,type=int);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--production-object',required=True,type=Path);ap.add_argument('--production-object-sha256',required=True);a=ap.parse_args();d=a.out.resolve();prod=a.production_object.resolve()
 if not d.is_relative_to((M/'out').resolve()) or not prod.is_relative_to((M/'out').resolve()):raise ValueError('private input/output required')
 out=d/'comparison.json'
 if out.exists():raise FileExistsError('preserve output')
 meta=json.loads((P/'manifest.json').read_text());oldp=P/'units.original';newp=P/'units.generated';mm=d/'mirror-manifest.json';m=json.loads(mm.read_text());run=json.loads((d/'compile-result.json').read_text())
 if sha(F/'build/units.json')!=BASE or sha(oldp)!=BASE or sha(newp)!=meta['candidate_recipe_sha256'] or m['unit']!=a.unit or run['unit_index']!=a.unit or run['mirror_manifest_sha256']!=sha(mm) or sha(prod)!=a.production_object_sha256.lower():raise ValueError('input identity differs')
 old=json.loads(oldp.read_text())['units'];new=json.loads(newp.read_text())['units'];specs={'production':old[a.unit],'original':old[a.unit],'candidate':new[a.unit]};pe=Pe(paths.REF_IMAGE);objs={'production':Coff(str(prod))}
 for z in run['outcomes']:
  p=d/(z['tag']+'.obj')
  if z['rc'] or not z['trace_valid'] or sha(p)!=z['object_sha256']:raise ValueError('compile object differs')
  objs[z['tag']]=Coff(str(p))
 if set(objs)!={'production','original','candidate'}:raise ValueError('missing object pair')
 results={};eh={};generated={}
 for tag,c in objs.items():
  try:
   r=compare(c,pe,specs[tag]);sec,inf,errors=eh_sections(c,pe,specs[tag],r,recipe_names(new if tag=='candidate' else old));results[tag]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match']};eh[tag]={'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()},'errors':errors}
  except (ValueError,KeyError,IndexError) as e:results[tag]={'fatal':type(e).__name__+': '+str(e)};eh[tag]={'eh_sections':[],'eh_inferred':{},'errors':['function prerequisite failed']}
  facts=[]
  for name,group in c.by_name.items():
   if not ('NiMemObject' in name or name.startswith(('??_G','??_E'))):continue
   for x in group:
    if x['section']<=0:continue
    s=c.sections[x['section']];data=s['data'][x['value']:];facts.append({'symbol':name,'section':s['name'],'size':len(data),'tail_sha256':hashlib.sha256(data).hexdigest(),'relocations':[(off-x['value'],kind,c.symbols[j]['name']) for off,j,kind in s['relocs'] if off>=x['value']]})
  generated[tag]=facts
 prior={x['address']:x for x in specs['original']['functions']};pair=[]
 for f in specs['candidate']['functions']:
  try:
   z=prior[f['address']];a0,ar=relocated(objs['original'],z['symbol'],z['size'],{});b0,br=relocated(objs['candidate'],f['symbol'],f['size'],{})
   if a0!=b0 or ar!=br:pair.append({'address':f['address'],'original_symbol':z['symbol'],'candidate_symbol':f['symbol'],'bytes_equal':a0==b0,'original_relocations':ar,'candidate_relocations':br})
  except (ValueError,KeyError,IndexError) as e:pair.append({'address':f['address'],'error':str(e)})
 out.write_text(json.dumps({'unit':a.unit,'production_object_sha256':sha(prod),'mirror_manifest_sha256':sha(mm),'compile_result_sha256':sha(d/'compile-result.json'),'reference':results,'ordinary_eh':eh,'mapped_function_pair_differences':pair,'generated_operator_and_deleting_sections':generated,'compiler_warnings':{x['tag']:x['warnings'] for x in run['outcomes']},'limitations':['differences and source baseline failures remain explicit; no alias or opcode normalization','unmapped deleting wrappers require ownership and semantic review','actual source installation, reference image, global linker/COMDAT and runtime remain separate']},indent=2));print(json.dumps({'unit':a.unit,'matches':{k:v.get('matches') for k,v in results.items()},'pair_differences':len(pair)}))
if __name__=='__main__':main()
