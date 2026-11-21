"""Prove two source-backed allocation relocations in the saved unit172 pair."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';D=R/'phase2-nimem-172-geometry-eh-v2-u0172';B=R/'phase2-nimem-combined-825d-run/unit-0172';O=D/'allocator-equivalence-proof.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 owner=R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json';recipe=R/'phase2-nimem-psys-pointer-binding-v1/units.generated';report=D/'strict-sized-eh-comparison-v2.json'
 if sha(owner)!='6acfb2049b12049418545c7dc8b813735b1341c134baaf5c9d4580a06db59af3' or sha(recipe)!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('source-owner or reference changed')
 proof=json.loads(owner.read_text());native=proof['owner_2734'];native_name=native['source_native_symbol'];target=native['address']
 if native_name!='??2NiMemObject@@SAPAXI@Z' or target!='0x00aa13e0' or native['functions_matched']!=native['functions_total']:raise ValueError('native allocator owner differs')
 m=json.loads(report.read_text());g=m['gates']
 if any(not value for key,value in g.items() if key!='all_relocation_changes_source_owned') or g['all_relocation_changes_source_owned']:raise ValueError('unexpected baseline gate state')
 u=json.loads(recipe.read_text())['units'][172];base=Coff(str(B/'candidate.obj'));pe=Pe(paths.REF_IMAGE);rows={x['address']:x for x in compare(base,pe,u)};expected={'0x00b8c170':(161,'??2NiScreenElements@@SAPAXI@Z'),'0x00b8c3b0':(175,'?FUN_00aa13e0@@YAPAXI@Z')};evidence=[]
 if len(m['mapped_pair_differences'])!=2:raise ValueError('unexpected number of changed functions')
 for pair in m['mapped_pair_differences']:
  address=pair['address'];offset,old=expected[address];a=pair['baseline_relocations'];b=pair['candidate_relocations'];diff=[(x,y) for x,y in zip(a,b) if x!=y]
  if not pair['bytes_equal'] or len(a)!=len(b) or len(diff)!=1:raise ValueError('unexpected normal code difference')
  x,y=diff[0]
  if x!=[offset,20,old,0] or y!=[offset,20,native_name,0] or rows[address]['verdict']!='match':raise ValueError('old and new relocation shape differs')
  ref=[z for z in rows[address]['relocations'] if z['offset']==offset and z['symbol']==old]
  if len(ref)!=1 or not ref[0]['match'] or ref[0]['observed']!=target or u['symbols'].get(old)!=target:raise ValueError('old source and reference target not proven')
  evidence.append({'function':address,'offset':offset,'previous_symbol':old,'reference_match':ref[0],'new_source_owned_symbol':native_name,'source_owner_unit':2734,'source_owner_address':target})
 O.write_text(json.dumps({'baseline_object_sha256':sha(B/'candidate.obj'),'candidate_object_sha256':sha(D/'candidate.obj'),'strict_report_sha256':sha(report),'source_owner_proof_sha256':sha(owner),'reference_sha256':sha(Path(paths.REF_IMAGE)),'allocator_fields':evidence,'remaining_gates':g,'all_gates_pass_with_proven_fields':True,'limits':['strict compiler fields and source-owned allocator equivalence only','complete emitted metadata, source ODR and actual production bindings remain separate']},indent=2));print(sha(O))
if __name__=='__main__':main()
