"""Extend the preserved replay index with recipe-binding and raw metadata provenance."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;R=M/'out';BASE=R/'phase2-nimem-next-source-proof-index.json';P=R/'phase2-nimem-next-source-composed';OUT=R/'phase2-nimem-next-source-proof-index-v2.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior index')
 if sha(BASE)!='6ac411ee15415e7c19ddde68af73af9c58a608d58471e677a7c723159c51d8c9':raise ValueError('replay index changed')
 j=json.loads(BASE.read_text());old=json.loads((P/'units.original').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units'];prior=json.loads((R/'phase2-nimem-combined-825d-run/progress.json').read_text());oldrows={x['unit']:x for x in prior['units']};joint={x['unit']:x for x in j['joint_results']};replayed={x['unit']:x for x in j['source_identical_replay']}
 for i,row in replayed.items():
  d=R/('phase2-nimem-combined-825d-run/unit-%04d'%i);comp=json.loads((d/'comparison.json').read_text());raw=d/'coff-sections-raw.json'
  if sha(d/'candidate.obj')!=row['candidate_object_sha256'] or sha(d/'comparison.json')!=row['prior_comparison_sha256']:raise ValueError('prior evidence drift')
  row['prior_candidate_strict_matches']=oldrows[i]['strict_matches']['candidate'];row['prior_candidate_eh_failed']=oldrows[i]['failed_eh_sections']['candidate'];row['prior_candidate_eh_error_count']=oldrows[i]['eh_errors']['candidate'];row['generated_operator_and_deleting_sections']=comp['generated_operator_and_deleting_sections'];row['raw_sections_sha256']=sha(raw)
 proofs={
  'provisional_122':R/'phase2-nimem-provisional-bindings-133/manifest.json',
  'unit773_literals':R/'phase2-nimem-adapter-using-v2-773-literal-proof.json',
  'unit200_and_operator_owners':R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json',
  'unit995_global_and_literals':R/'phase2-tesfile-recordtype-825d/manifest.json'}
 bindings=[]
 for i in j['recipe_changed_units']:
  if i in (200,1664,2734):proof='unit200_and_operator_owners'
  elif i==773:proof='unit773_literals'
  elif i==995:proof='unit995_global_and_literals'
  else:proof='provisional_122'
  a=old[i].get('symbols',{});b=new[i].get('symbols',{});changes={k:{'before':a.get(k),'after':b.get(k)} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)}
  af=old[i]['functions'];bf=new[i]['functions'];function_symbol_changes=[{'address':x['address'],'before':x['symbol'],'after':y['symbol']} for x,y in zip(af,bf) if x['symbol']!=y['symbol']]
  evidence=joint.get(i,replayed.get(i))
  if evidence is None:raise ValueError('changed unit has no candidate object '+str(i))
  bindings.append({'unit':i,'symbol_changes':changes,'function_symbol_changes':function_symbol_changes,'source_proof':proof,'source_proof_sha256':sha(proofs[proof]),'candidate_object_sha256':evidence['candidate_object_sha256']})
 for p in proofs.values():
  if not p.is_file():raise ValueError('missing proof')
 j['parent_index_sha256']=sha(BASE);j['changed_recipe_binding_evidence']=bindings
 j['limits'].append('source-identical replay used final recipe but retained preexisting baseline failures; production source-label rebinding remains separate')
 OUT.write_text(json.dumps(j,indent=2));print(json.dumps({'changed_units':len(bindings),'prior_raw_metadata_units':len(replayed),'sha256':sha(OUT)}))
if __name__=='__main__':main()
