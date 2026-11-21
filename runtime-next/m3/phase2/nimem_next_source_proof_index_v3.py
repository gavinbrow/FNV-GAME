"""Attach independently pinned transitive proofs and explicit baseline deltas."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;R=M/'out';B=R/'phase2-nimem-next-source-proof-index-v2.json';O=R/'phase2-nimem-next-source-proof-index-v3.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior index')
 if sha(B)!='4c599eb544131876b385824c21e001994fc11f602895fbdde7b7f8b8f445391d':raise ValueError('index differs')
 j=json.loads(B.read_text());m=json.loads((R/'phase2-nimem-provisional-bindings-133/manifest.json').read_text());root=R.parent.parent.parent;proofs={}
 for name,h in m['proof_sha256'].items():
  p=root/name
  if sha(p)!=h:raise ValueError('provisional proof changed '+name)
  proofs[name]=h
 outside=R/'phase2-tesfile-recordtype-global/eh-outside-owner-proof.json';psa=R/'phase2-nimem-next-source-composed-u0620/independent-psa-section-review.json';q=json.loads(psa.read_text())
 if q['section_count']!=16 or not all(x['equal'] for x in q['sections']):raise ValueError('620 PSA section evidence not exact')
 rows=j['source_identical_replay'];regress=[x['unit'] for x in rows if x['matches']!=x['prior_candidate_strict_matches'] or x['failed_eh_sections']!=x['prior_candidate_eh_failed'] or len(x['eh_errors'])!=x['prior_candidate_eh_error_count']]
 j['parent_index_sha256']=sha(B);j['transitive_proof_sha256']=proofs;j['unit995_outside_owner_proof_sha256']=sha(outside);j['unit620_psa_exact_sections']=16;j['source_identical_replay_regression_units']=regress
 O.write_text(json.dumps(j,indent=2));print(json.dumps({'regression_units':regress,'transitive_proofs':len(proofs),'outside_owner_sha256':sha(outside),'sha256':sha(O)}))
if __name__=='__main__':main()
