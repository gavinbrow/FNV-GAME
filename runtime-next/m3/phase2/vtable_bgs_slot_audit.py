"""Inventory source-recipe evidence for each observed BGSE virtual prefix slot."""
import json,hashlib
from pathlib import Path
M=Path(__file__).resolve().parent.parent; O=M/'out/phase2-bgsencounterzone-six-override'; B=M/'out/phase2-bgsencounterzone-combined'; D=M/'out/phase2-bgsencounterzone-slot-audit.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=O/'class-metadata-comparison-v2.json';b=B/'slot-source-leads-v2.json';v=json.loads(a.read_text())['tables'][0]['slots'];s=json.loads(b.read_text())['tables'][0]['slots']
 if len(v)!=78 or len(s)!=78:raise ValueError('unexpected observed prefix')
 rows=[]
 for x,y in zip(v,s):
  if x['index']!=y['slot_index'] or x['reference_target']!=y['reference_target']:raise ValueError('slot evidence mismatch')
  refs=y.get('function_recipe_candidates',[]);tf=[z for z in refs if z['source']=='src/fallout_shared/tesform.cpp'];local=[z for z in refs if z['source']=='src/bgsencounterzone.cpp'];status='matched' if x['match'] else 'local_candidate' if local else 'tesform_candidate' if tf else 'other_or_unresolved'
  rows.append({'index':x['index'],'reference_target':x['reference_target'],'emitted_symbol':x['symbol'],'resolved_target':x['resolved_target'],'status':status,'tesform_functions':[z['symbol'] for z in tf],'local_functions':[z['symbol'] for z in local],'other_function_count':len(refs)-len(tf)-len(local)})
 if D.exists():raise FileExistsError(D)
 D.write_text(json.dumps({'scope':'78 observed slots only; recipe reverse matches are leads, not semantic identity','inputs':{'class_metadata_sha256':sha(a),'source_leads_sha256':sha(b)},'slots':rows},indent=2)+'\n');print({k:sum(x['status']==k for x in rows) for k in ('matched','local_candidate','tesform_candidate','other_or_unresolved')})
if __name__=='__main__':main()
