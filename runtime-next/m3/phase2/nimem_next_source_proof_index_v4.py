"""Classify replay changes by direction without conflating fixes and regressions."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent/'out';B=R/'phase2-nimem-next-source-proof-index-v3.json';O=R/'phase2-nimem-next-source-proof-index-v4.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve history')
 if sha(B)!='069605dfa01cffb2205b973b1a052759bef4714a96cd9070616c16f759778db4':raise ValueError('index changed')
 j=json.loads(B.read_text());j.pop('source_identical_replay_regression_units');changed=[];regress=[]
 for x in j['source_identical_replay']:
  before=(x['prior_candidate_strict_matches'],x['prior_candidate_eh_failed'],x['prior_candidate_eh_error_count']);after=(x['matches'],x['failed_eh_sections'],len(x['eh_errors']))
  if before!=after:changed.append({'unit':x['unit'],'before':before,'after':after})
  if after[0]<before[0] or after[1]>before[1] or after[2]>before[2]:regress.append(x['unit'])
 j['parent_index_sha256']=sha(B);j['source_identical_replay_changed_counts']=changed;j['source_identical_replay_regression_units']=regress
 O.write_text(json.dumps(j,indent=2));print(json.dumps({'count_changes':len(changed),'regressions':regress,'sha256':sha(O)}))
if __name__=='__main__':main()
