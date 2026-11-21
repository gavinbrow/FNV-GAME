"""Index the pinned BFC cohort proofs; this does not perform ordinary EH/ownership checks."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;O=M/'out';S=O/'phase2-baseformcomponent-core';R=O/'phase2-bfc-core-cohort-retry-v2';OUT=O/'phase2-bfc-core-proof-index.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve historical index')
 mp=S/'manifest.json';bp=S/'root-baseline-audit.json';progress=R/'progress.json';m=json.loads(mp.read_text());b=json.loads(bp.read_text());p=json.loads(progress.read_text());rows=[]
 if sha(mp)!='93f5e6c6392d35a3524cbf78ebcfbf9fba27ad83607f7617f82c7697449e32ec' or sha(bp)!='7937cbaeb95552461704f20563221f7d559762f876961178c91470fad698a1df':raise ValueError('pinned audit mismatch')
 for x in m['units']:
  i=x['unit'];pr=next(z for z in p['units'] if z['unit']==i);retry=pr['prepare'].get('status','').endswith('retry') or (pr['prepare'].get('rc')==0);d=O/('phase2-bfc-core-u%04d%s'%(i,'-retry' if retry else ''))
  if not (d/'compile-result.json').exists():
   d=O/('phase2-bfc-core-u%04d-retry'%i)
  c=json.loads((d/'compile-result.json').read_text());mm=d/'mirror-manifest.json'
  if c['unit_index']!=i or c['mirror_manifest_sha256']!=sha(mm):raise ValueError('mirror mismatch '+str(i))
  for z in c['outcomes']:
   if z['rc'] or not z['trace_valid'] or sha(d/(z['tag']+'.obj'))!=z['object_sha256']:raise ValueError('compile result mismatch')
  n='comparison-cohort-v2.json' if pr['status']=='function-and-named-eh-pass' else 'comparison-cohort-v3.json' if i==721 else 'comparison-cohort-v5.json' if i in (253,388,396,623) else 'comparison-cohort-v4.json';q=d/n;v=json.loads(q.read_text());nf=len(x['functions'])
  if v['unit']!=i or v['production_obj_sha256']!=b['object_sha256'][str(i)] or v['functions']!=nf or any(v[k]!=nf for k in ('production_reference_matches','mirror_original_reference_matches','mirror_candidate_reference_matches')):raise ValueError('function evidence mismatch '+str(i))
  rows.append({'unit':i,'functions':nf,'ordinary_recipe_eh_tails':len(x['eh_tails']),'named_eh_sections_equal':v['eh_named_section_tails_equal'],'production_object_sha256':v['production_obj_sha256'],'mirror_manifest_sha256':sha(mm),'compile_result_sha256':sha(d/'compile-result.json'),'objects':{z['tag']:z['object_sha256'] for z in c['outcomes']},'report':str(q.relative_to(M)).replace('\\','/'),'report_sha256':sha(q),'comparison':n})
 if len(rows)!=241 or sum(x['functions'] for x in rows)!=5817 or sum(x['ordinary_recipe_eh_tails'] for x in rows)!=367:raise ValueError('scope differs')
 pins={str(z.relative_to(M)).replace('\\','/'):sha(z) for z in (mp,bp,progress,*[S/n for n in ('external-binding-evidence.json','local-string-evidence-v2.json','local-string-evidence-v3.json','archived-immediate-evidence.json')])}
 OUT.write_text(json.dumps({'scope':'index only: 241 units, 5817 strict function comparisons; named EH equality is supplementary','pinned_inputs':pins,'recipe_sha256':m['base_units_sha256'],'units':rows,'ordinary_eh_recipe_tail_count':367,'ordinary_eh_status':'NOT VERIFIED by indexed function/named-section reports','remaining':['ordinary recipe EH tails and placement/ownership','generated data, RTTI/vtables, thunks, weak symbols, initializers','packing/ODR and preprocessed wrapper context','production-label rederivation, full image/relocation and runtime controls']},indent=2));print('indexed',len(rows),'units',sum(x['functions'] for x in rows),'functions')
if __name__=='__main__':main()
