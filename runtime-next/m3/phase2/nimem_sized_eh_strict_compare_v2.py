"""Fail-closed source-owner and composed-baseline checks for units149/172/194."""
import argparse,copy,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
SPEC={149:('phase2-nimem-149-194-sized-eh-v1','dca9aece504241d985be62def30a1e2eb67ad08cf2bab3dc9eac8ee167fa0948','sized_eh_manifest_sha256',{'src/bsshader/debugshader_local.h'},'0x00bd23f0'),194:('phase2-nimem-149-194-sized-eh-v1','dca9aece504241d985be62def30a1e2eb67ad08cf2bab3dc9eac8ee167fa0948','sized_eh_manifest_sha256',{'src/bsshader/shadowscenenode_fog_decls.h'},'0x00b54110'),172:('phase2-nimem-172-geometry-eh-v2','81578c458637063ed0aa5c21cca199eb580f7b525563bdd90a80dc907b5a0a8d','geometry_eh_manifest_sha256',{'src/bsshader/imagespacemanager_geometry.h','src/bsshader/imagespacemanager.cpp'},'0x00b8c3b0')}
ARCHIVE={149:'038aebf9581380e7bc9aa0d822257419b3db7311424a8e7bb7fcecba15bc2b1e',194:'3af5f589857c7aabc5f22d40891a9831b241bf7da01b96c1b9f9e62c0460498b',172:'2fbcab5d2fd3b3b387129cb8ba6cfc4bf51b2071f21c2b4bfb2b1e4d3191e5d0'}
BASELINE={149:('67e11a9ccdfa923a5831aeb29fcac0cc1b699c95a92818d41ef7bea9218d04bc','bb606f99f0b817ca01c4f5b0d73f0cc18a652a8e3e31022204e6548524e6425e','bd5fbdd4bc5df3ef833189c6bc0683013b30812bd61012b84ecd2cb10d253edd'),172:('06f57c6f136a64acd4f0b00f9a330ff6c3b4d7e15916e7d44e9fabe813c42ebd','6dc59a338675634490502ce4bca7565b416c868d76c15f9889f6499c4944fd2e','af610dc5cf4f46e592e2c2c0a3bc22ada4b2469677a3b401d4a4fb7cd6d9ae21'),194:('edad46c0bbf8ab4232d850cedf6d6072c4433790dccf40cc9191947e9db7f568','834f93e4e58441da0f15f182f81ea7e205404f1b8bc3818f6b64195f0c194127','a60092e1811f4d81215bbee3644fceff4761487e121f8df59d8d937d68c8a5d2')}
EXPECTED={149:(0xf2c310,18),172:(0xf2954f,18),194:(0xf26d90,15)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--production-object',type=Path,required=True);ap.add_argument('--production-object-sha256',required=True);a=ap.parse_args();d=a.out.resolve();prod=a.production_object.resolve();name,pin,key,changed,parent=SPEC[a.unit];out=d/'strict-sized-eh-comparison-v2.json'
 if out.exists() or not d.is_relative_to((M/'out').resolve()) or not prod.is_relative_to((M/'out').resolve()):raise ValueError('fresh private paths required')
 if sha(R/name/'manifest.json')!=pin or sha(R/'phase2-nimem-psys-pointer-binding-v1/units.generated')!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or a.production_object_sha256.lower()!=ARCHIVE[a.unit] or sha(prod)!=ARCHIVE[a.unit] or sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('proposal, archive or reference differs')
 proof=R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json'
 if sha(proof)!='6acfb2049b12049418545c7dc8b813735b1341c134baaf5c9d4580a06db59af3':raise ValueError('source-owner proof differs')
 source=json.loads(proof.read_text())
 for rel,h in source['inputs'].items():
  if sha(F.parent/Path(rel))!=h:raise ValueError('source-owner proof input differs')
 units=json.loads((R/'phase2-nimem-psys-pointer-binding-v1/units.generated').read_text())['units'];u=units[a.unit]
 for n,addr in [('owner_2734','0x00aa13e0'),('owner_1664','0x00aa1460')]:
  x=source[n]
  if x['address']!=addr or x['functions_matched']!=x['functions_total']:raise ValueError('owner not source-proven')
 baseline=R/('phase2-nimem-combined-825d-run/unit-%04d'%a.unit);bm=json.loads((baseline/'mirror-manifest.json').read_text());br=json.loads((baseline/'compile-result.json').read_text());mm=d/'mirror-manifest.json';m=json.loads(mm.read_text());run=json.loads((d/'compile-result.json').read_text())
 if m[key]!=pin or run['unit_index']!=a.unit or run['mirror_manifest_sha256']!=sha(mm) or run['flags']!=u['flags'] or br['flags']!=u['flags'] or br['mirror_manifest_sha256']!=sha(baseline/'mirror-manifest.json'):raise ValueError('mirror or flags differ')
 agraph=m['candidate']['files'];bgraph=bm['candidate']['files'];diff={k for k in set(agraph)|set(bgraph) if agraph.get(k)!=bgraph.get(k)}
 if diff!=changed:raise ValueError('candidate vs composed baseline source delta differs')
 baseline_row=next(x for x in br['outcomes'] if x['tag']=='candidate');bp=baseline/'candidate.obj'
 if (sha(baseline/'mirror-manifest.json'),sha(baseline/'compile-result.json'),sha(bp))!=BASELINE[a.unit] or baseline_row['rc'] or not baseline_row['trace_valid'] or sha(bp)!=baseline_row['object_sha256']:raise ValueError('composed baseline object differs')
 objects={'production':Coff(str(prod)),'composed_baseline':Coff(str(bp))}
 for row in run['outcomes']:
  p=d/(row['tag']+'.obj')
  if row['rc'] or not row['trace_valid'] or sha(p)!=row['object_sha256']:raise ValueError('fixture object differs')
  objects[row['tag']]=Coff(str(p))
 if set(objects)!={'production','composed_baseline','original','candidate'}:raise ValueError('object set incomplete')
 candidate=copy.deepcopy(u);candidate['symbols']['??3NiMemObject@@SAXPAXI@Z']=source['owner_1664']['address'];candidate['symbols']['??2NiMemObject@@SAPAXI@Z']=source['owner_2734']['address'];pe=Pe(paths.REF_IMAGE);results={}
 for tag,c in objects.items():
  spec=candidate if tag=='candidate' else u;r=compare(c,pe,spec);sections,inf,errors=eh_sections(c,pe,spec,r,recipe_names(units));tails,bad,_,_,conf=eh_tails([spec],[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}],pe)
  results[tag]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'sections':sections,'eh_errors':errors,'bad_tails':bad,'conflicts':conf,'inferred_names':len(inf)}
 pairs=[]
 for f in u['functions']:
  x,xr=relocated(objects['composed_baseline'],f['symbol'],f['size'],{});y,yr=relocated(objects['candidate'],f['symbol'],f['size'],{})
  if x!=y or xr!=yr:pairs.append({'address':f['address'],'bytes_equal':x==y,'baseline_relocations':xr,'candidate_relocations':yr})
 baseline_failed=[x for x in results['composed_baseline']['sections'] if not x[2]];candidate_failed=[x for x in results['candidate']['sections'] if not x[2]];target_before=[x for x in baseline_failed if x[3]==parent];target_after=[x for x in candidate_failed if x[3]==parent]
 allowed_old='?FUN_00aa13e0@@YAPAXI@Z';allowed_new='??2NiMemObject@@SAPAXI@Z'
 def allowed_pair(x):
  if not x['bytes_equal'] or len(x['baseline_relocations'])!=len(x['candidate_relocations']):return False
  for a0,b0 in zip(x['baseline_relocations'],x['candidate_relocations']):
   if a0==b0:continue
   if a.unit!=172 or x['address']!=parent or a0[:2]!=b0[:2] or a0[3:]!=b0[3:] or a0[2]!=allowed_old or b0[2]!=allowed_new:return False
  return True
 candidate_row=next(x for x in run['outcomes'] if x['tag']=='candidate');codes=lambda row:Counter(re.findall(r'(?i)\bwarning\s+(C\d+)', '\n'.join(row['warnings'])))
 expected_start,expected_size=EXPECTED[a.unit];target_evidence=[x for x in results['candidate']['sections'] if x[0]==expected_start and x[1]==expected_start+expected_size and x[3]==parent and x[2]]
 gates={'all_candidate_functions_match':results['candidate']['matches']==len(u['functions']),'all_parent_bytes_equal':all(x['bytes_equal'] for x in pairs),'all_relocation_changes_source_owned':all(allowed_pair(x) for x in pairs),'target_previously_fails':bool(target_before),'target_now_clear':len(target_evidence)==1 and not target_after,'no_new_failed_sections':all(x in baseline_failed for x in candidate_failed),'no_new_eh_errors':all(x in results['composed_baseline']['eh_errors'] for x in results['candidate']['eh_errors']),'no_new_bad_tails':all(k in results['composed_baseline']['bad_tails'] and results['composed_baseline']['bad_tails'][k]==v for k,v in results['candidate']['bad_tails'].items()),'no_new_conflicts':results['candidate']['conflicts']<=results['composed_baseline']['conflicts'],'no_new_warning_codes':not (codes(candidate_row)-codes(baseline_row)),'owner_symbols_proven':True}
 out.write_text(json.dumps({'unit':a.unit,'proposal_sha256':pin,'reference_sha256':sha(Path(paths.REF_IMAGE)),'source_owner_proof_sha256':sha(proof),'baseline_object_sha256':sha(bp),'source_delta':sorted(diff),'results':results,'mapped_pair_differences':pairs,'gates':gates,'limits':['all relocations are retained for independent review; equal counts do not prove identical failed fields','actual installation and generated metadata/ODR and final image remain separate']},indent=2));print(json.dumps({'unit':a.unit,'gates':gates,'pair_differences':len(pairs)}))
 if not all(gates.values()):raise SystemExit(1)
if __name__=='__main__':main()
