"""Index joint evidence and replay unchanged source objects against final recipe."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';OUT=R/'phase2-nimem-next-source-proof-index.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 pm=P/'manifest.json';joint=R/'phase2-nimem-next-source-joint-ten/progress.json';prior=R/'phase2-nimem-combined-825d-run/progress.json';oldscope=R/'phase2-nimem-combined-825d/manifest.json'
 if sha(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53' or sha(P/'units.generated')!='13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876':raise ValueError('composed input differs')
 proposal=json.loads(pm.read_text());new=json.loads((P/'units.generated').read_text())['units'];j=json.loads(joint.read_text());pr=json.loads(prior.read_text());sc=json.loads(oldscope.read_text());priorrows={x['unit']:x for x in sc['combined_api_units']+sc['fresh_kind_only_units']};affected={x['unit']:x for x in proposal['affected_units']};fresh={128,129,191,200,620,773,995,1203,1271,1598}
 if len(priorrows)!=133 or len(affected)!=752 or {x['unit'] for x in j['units']}!=fresh:raise ValueError('scope incomplete')
 same=sorted(i for i in priorrows if i not in fresh and affected[i]['candidate']==priorrows[i]['candidate'])
 if len(same)!=125:raise ValueError('source-identical cohort changed')
 pe=Pe(paths.REF_IMAGE);rows=[];prior_results={x['unit']:x for x in pr['units']}
 for i in same:
  d=R/('phase2-nimem-combined-825d-run/unit-%04d'%i);run=json.loads((d/'compile-result.json').read_text());outcome=next(x for x in run['outcomes'] if x['tag']=='candidate');obj=d/'candidate.obj'
  if outcome['rc'] or not outcome['trace_valid'] or sha(obj)!=outcome['object_sha256'] or sha(d/'comparison.json')!=prior_results[i]['comparison_sha256']:raise ValueError('prior object differs '+str(i))
  c=Coff(str(obj));r=compare(c,pe,new[i]);sections,inferred,errors=eh_sections(c,pe,new[i],r,recipe_names(new))
  rows.append({'unit':i,'candidate_object_sha256':sha(obj),'prior_comparison_sha256':sha(d/'comparison.json'),'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'eh_sections':len(sections),'failed_eh_sections':sum(not x[2] for x in sections),'eh_errors':errors,'eh_inferred_names':len(inferred),'recipe_changed':i in proposal['recipe_changed_units']})
 freshrows=[]
 for row in j['units']:
  i=row['unit'];d=R/('phase2-nimem-next-source-composed-u%04d'%i);comparison=d/'comparison.json';compile_=d/'compile-result.json';coff=d/'coff-sections-raw.json';run=json.loads(compile_.read_text());candidate=next(x for x in run['outcomes'] if x['tag']=='candidate')
  if sha(comparison)!=row['comparison_sha256'] or sha(coff)!=row['coff_sections_sha256'] or sha(d/'candidate.obj')!=candidate['object_sha256']:raise ValueError('joint object evidence changed '+str(i))
  report=json.loads(comparison.read_text());raw=json.loads(coff.read_text());freshrows.append({'unit':i,'candidate_object_sha256':sha(d/'candidate.obj'),'comparison_sha256':sha(comparison),'raw_sections_sha256':sha(coff),'reference':report['reference'],'ordinary_eh':{'failed':row['eh_failed'],'errors':row['eh_errors']},'pair_differences':report['mapped_function_pair_differences'],'normalized_sections':raw['kind_normalized_pair'],'generated_operator_and_deleting_sections':report['generated_operator_and_deleting_sections']})
 proofs=[R/'phase2-nimem-provisional-bindings-133/manifest.json',R/'phase2-nimem-adapter-using-v2-773-literal-proof.json',R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json',R/'phase2-tesfile-recordtype-825d/manifest.json',R/'phase2-nimem-next-source-composed-u0620/independent-psa-section-review.json']
 index={'proposal_sha256':sha(pm),'recipe_sha256':sha(P/'units.generated'),'joint_progress_sha256':sha(joint),'prior_progress_sha256':sha(prior),'reference_sha256':sha(Path(paths.REF_IMAGE)),'supporting_proof_sha256':{str(p.relative_to(R)):sha(p) for p in proofs},'partition':{'prior133':133,'new_context_units':[620,995],'reused_kind_only':617,'total':752,'prior_source_identical_replayed':125,'prior_changed_source_recompiled':8},'recipe_changed_units':proposal['recipe_changed_units'],'source_identical_replay':rows,'joint_results':freshrows,'joint_eh_union':j['ordinary_eh_union'],'limits':['all source-backed fixture bindings remain provisional until production object label and ownership verification','unit191 retains eight preexisting ordinary EH failures','unit995 source corrects original global target; 0xeeeb50 tail requires separately proved outside owner 2634','unit620 exact 16-section PSA review does not prove placement or ownership','generated/deleting wrappers and other emitted COMDAT ownership, full ODR, image and runtime remain open']}
 OUT.write_text(json.dumps(index,indent=2));print(json.dumps({'replayed':len(rows),'functions':sum(x['functions'] for x in rows),'matches':sum(x['matches'] for x in rows),'eh_failures':sum(x['failed_eh_sections'] for x in rows),'eh_errors':sum(len(x['eh_errors']) for x in rows),'sha256':sha(OUT)}))
if __name__=='__main__':main()
