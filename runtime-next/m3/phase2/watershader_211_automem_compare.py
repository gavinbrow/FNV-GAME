"""Compare saved unit211 lifetime hypothesis and independently saved owners."""
import argparse,copy,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-watershader-211-automem-v1';Q=R/'phase2-nimem-psys-pointer-binding-v1';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import nimem_kind_section_review as metadata
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--production-object',type=Path,required=True);ap.add_argument('--production-sha256',required=True);ap.add_argument('--owner47',type=Path,required=True);ap.add_argument('--owner47-sha256',required=True);ap.add_argument('--owner781',type=Path,required=True);ap.add_argument('--owner781-sha256',required=True);a=ap.parse_args();d=a.out.resolve();out=d/'automem-comparison.json'
 if out.exists() or not d.is_relative_to((M/'out').resolve()) or any(not p.resolve().is_relative_to((M/'out').resolve()) for p in (a.production_object,a.owner47,a.owner781)):raise ValueError('fresh private evidence required')
 if sha(P/'manifest.json')!='f241acd5a38a00fcdd25ed8597716f9b8aedd371a44f6c2f157145584c2392d4' or sha(Q/'units.generated')!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('pinned proposal/reference differs')
 capture=R/'phase2-watershader-211-owner-v2-capture';capture_manifest=capture/'manifest.json';owner_replay=capture/'strict-owner-replay.json'
 if sha(capture_manifest)!='0c1a42787fa3bfd556904d4a47d14ec6ebadfd503e42da0f7a1b9724017fb7c4' or sha(owner_replay)!='fe422d5fbf45d4bc8faf3377d644ed726ee78dba2e8fce73ea2e868a962e7bb2':raise ValueError('source owner provenance differs')
 for path,h,expected in ((a.production_object,a.production_sha256,'dd7183bd3875b66d84547eff62dd8faf7b4ba41ac8227e6e07ed296bf62c35ad'),(a.owner47,a.owner47_sha256,'a9af6d85be4102328d7223453acc88fde09896db9c5a449fcda30b875aec0b6c'),(a.owner781,a.owner781_sha256,'f60820b423032feb27e4e5aa895d89c8937a80b87153bb815985100069ddb76b')):
  if h.lower()!=expected or sha(path)!=expected:raise ValueError('archive object differs')
 mm=d/'mirror-manifest.json';m=json.loads(mm.read_text());run=json.loads((d/'compile-result.json').read_text())
 baseline=R/'phase2-nimem-combined-825d-run/unit-0211';bm=baseline/'mirror-manifest.json';br=json.loads((baseline/'compile-result.json').read_text());brow=next(x for x in br['outcomes'] if x['tag']=='candidate');bp=baseline/'candidate.obj';bg=json.loads(bm.read_text())['candidate']['files'];ng=m['candidate']['files'];delta={k for k in set(bg)|set(ng) if bg.get(k)!=ng.get(k)}
 if m['automem_manifest_sha256']!=sha(P/'manifest.json') or run['unit_index']!=211 or run['mirror_manifest_sha256']!=sha(mm) or br['mirror_manifest_sha256']!=sha(bm) or (sha(bm),sha(baseline/'compile-result.json'),sha(bp))!=('d8c4e8eaa5a614dcd0c06423881ffef7cc882679e3f4d22505167bbeb1b5bedf','4fa84194ad66b289ec3b883a1391abe50fdb06c487b5ee6adedf428d878bd883','7a883d30d2f3a19cfe5241f26e484fa54c9d00c4fe692fc08fd878643f7de4da') or brow['rc'] or not brow['trace_valid'] or sha(bp)!=brow['object_sha256'] or delta!={'src/bsshader/watershader.cpp'}:raise ValueError('mirror or composed baseline differs')
 units=json.loads((Q/'units.generated').read_text())['units'];pe=Pe(paths.REF_IMAGE);owners={}
 if run['flags']!=units[211]['flags'] or br['flags']!=units[211]['flags']:raise ValueError('production flags differ')
 for i,path,address in ((47,a.owner47,'0x00404ee0'),(781,a.owner781,'0x00404f70')):
  c=Coff(str(path));rows=compare(c,pe,units[i]);r=next(x for x in rows if x['address']==address)
  if r['verdict']!='match':raise ValueError('source owner fails strict reference '+address)
  owners[str(i)]={'object_sha256':sha(path),'function':r,'all_matches':sum(x['verdict']=='match' for x in rows),'all_functions':len(rows)}
 if units[47]['symbols'].get('?Leave@AutoMemContext@@QAEXXZ')!='0x00404f70':raise ValueError('owner dtor Leave source map differs')
 specs={'production':units[211],'composed_baseline':units[211],'original':units[211],'candidate':copy.deepcopy(units[211])};specs['candidate']['symbols']['??1AutoMemContext@@QAE@XZ']='0x00404ee0';objects={'production':Coff(str(a.production_object)),'composed_baseline':Coff(str(bp))}
 for x in run['outcomes']:
  p=d/(x['tag']+'.obj')
  if x['rc'] or not x['trace_valid'] or sha(p)!=x['object_sha256']:raise ValueError('saved object mismatch')
  objects[x['tag']]=Coff(str(p))
 if set(objects)!={'production','composed_baseline','original','candidate'}:raise ValueError('object pair missing')
 results={}
 for tag,c in objects.items():
  r=compare(c,pe,specs[tag]);sec,inf,errors=eh_sections(c,pe,specs[tag],r,recipe_names(units));tails,bad,_,_,conf=eh_tails([specs[tag]],[{'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}],pe)
  path=a.production_object if tag=='production' else bp if tag=='composed_baseline' else d/(tag+'.obj')
  results[tag]={'object_sha256':sha(path),'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors'],'byte_differences':x['byte_differences']} for x in r if x['verdict']!='match'],'sections':sec,'eh_errors':errors,'bad_tails':bad,'conflicts':conf}
 pairs=[]
 for f in units[211]['functions']:
  x,xr=relocated(objects['composed_baseline'],f['symbol'],f['size'],{});y,yr=relocated(objects['candidate'],f['symbol'],f['size'],{})
  if x!=y or xr!=yr:pairs.append({'address':f['address'],'bytes_equal':x==y,'original_relocations':xr,'candidate_relocations':yr})
 sym=objects['candidate'].named('__unwindfunclet$?FUN_00b827c0@WaterShaderLoader@@QAEXXZ$0');sec=objects['candidate'].sections[sym['section']];disp=sec['data'][sym['value']:sym['value']+6];refs=[objects['candidate'].symbols[j]['name'] for o,j,k in sec['relocs'] if o==sym['value']+7 and k==20];before=[x for x in results['composed_baseline']['sections'] if not x[2]];after=[x for x in results['candidate']['sections'] if not x[2]]
 candidate_row=next(x for x in run['outcomes'] if x['tag']=='candidate');codes=lambda x:Counter(re.findall(r'(?i)\bwarning\s+(C\d+)', '\n'.join(x['warnings'])));target=[x for x in results['candidate']['sections'] if x[0]==0xf29180 and x[1]==0xf2918b and x[2] and x[3]=='0x00b827c0']
 gates={'all_functions_match':results['candidate']['matches']==len(units[211]['functions']),'all_normal_bytes_and_relocations_equal':not pairs,'reference_frame_displacement':disp==bytes.fromhex('8d8db8efffff'),'source_owned_destructor':refs==['??1AutoMemContext@@QAE@XZ'],'previous_failure_present':any(x[3]=='0x00b827c0' for x in before),'target_failure_cleared':len(target)==1 and not any(x[3]=='0x00b827c0' for x in after),'no_new_eh_failures':all(x in before for x in after),'no_new_eh_errors':all(x in results['composed_baseline']['eh_errors'] for x in results['candidate']['eh_errors']),'no_new_bad_tails':all(k in results['composed_baseline']['bad_tails'] and results['composed_baseline']['bad_tails'][k]==v for k,v in results['candidate']['bad_tails'].items()),'no_new_conflicts':results['candidate']['conflicts']<=results['composed_baseline']['conflicts'],'no_new_warning_codes':not (codes(candidate_row)-codes(brow))}
 ra=metadata.records(objects['composed_baseline']);rb=metadata.records(objects['candidate']);aa=metadata.aux(objects['composed_baseline']);ab=metadata.aux(objects['candidate']);metadata_summary={'normalized_only_baseline_sections':sum((ra-rb).values()),'normalized_only_candidate_sections':sum((rb-ra).values()),'weak_comdat_equal':aa==ab,'normalization':'NiMemObject RTTI class-key only; AutoMemContext code/metadata remains unnormalized'}
 out.write_text(json.dumps({'manifest_sha256':sha(P/'manifest.json'),'candidate_recipe_sha256':sha(Q/'units.generated'),'owner_capture_sha256':sha(capture_manifest),'owner_replay_sha256':sha(owner_replay),'owner_checks':owners,'local_candidate_binding':{'??1AutoMemContext@@QAE@XZ':'0x00404ee0'},'results':results,'mapped_pair_differences':pairs,'funclet_destructor_refs':refs,'metadata_summary':metadata_summary,'gates':gates,'limits':['full parent byte/relocation and EH results retained; no funclet aliasing','owner781 is separately named surrogate; native Leave identity and broader ODR remain open','stack-frame/local-object associations and generated metadata require independent review']},indent=2));print(json.dumps({'gates':gates,'pair_differences':len(pairs)}))
 if not all(gates.values()):raise SystemExit(1)
if __name__=='__main__':main()
