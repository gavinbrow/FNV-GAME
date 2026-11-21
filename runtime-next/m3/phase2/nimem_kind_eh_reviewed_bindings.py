"""Recompute archived 6757 cohort EH with reviewed non-immediate local maps."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out/phase2-nimem-kind-cohort-run';A=M/'out/phase2-nimem-kind-production-archive';B=M/'out/phase2-nimem-kind-source-bindings-final.json';OUT=M/'out/phase2-nimem-kind-eh-reviewed-bindings.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve report')
 progress=R/'progress.json';p=json.loads(progress.read_text());mp=json.loads(B.read_text());rp=R/'units.snapshot.json';units=json.loads(rp.read_text())['units'];inventory={x['unit']:x for x in json.loads((A/'manifest.json').read_text())['objects']}
 if p['status']!='complete-review-required' or len(p['units'])!=750 or sha(rp)!=p['recipe_sha256'] or sha(A/'manifest.json')!=p['production_archive_manifest_sha256']:raise ValueError('archive run not complete/pinned')
 pe=Pe(paths.REF_IMAGE);names=recipe_names(units);done={'production':[],'original':[],'candidate':[]};details=[];specs=[];removed=0
 for item in p['units']:
  i=item['unit'];d=R/('unit-%04d'%i);q=d/'comparison.json';mm=d/'mirror-manifest.json';run=json.loads((d/'compile-result.json').read_text())
  if item['status']=='failed' or sha(q)!=item['comparison_sha256'] or run['unit_index']!=i or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('cohort report incomplete '+str(i))
  spec=copy.deepcopy(units[i]);mapping=mp['units'].get(str(i),{})
  for n,z in mapping.items():
   if z['evidence']=='same-unit-strict-archive-immediate':removed+=1;continue
   spec['symbols'][n]=z['target']
  if i==995:
   for n in ('$SG7025','$SG8028','$SG8627','$SG8632'):spec['symbols'].pop(n,None)
  specs.append(spec);entry={'unit':i,'functions':len(spec['functions']),'requested_eh_tails':len(spec.get('eh_tails',[]))}
  checks={'production':(A/('%04d.obj'%i),inventory[i]['sha256'])}
  for z in run['outcomes']:
   if z['rc'] or not z['trace_valid']:raise ValueError('compile evidence invalid')
   checks[z['tag']]=(d/(z['tag']+'.obj'),z['object_sha256'])
  if set(checks)!=set(done):raise ValueError('missing object')
  for tag,(path,digest) in checks.items():
   if sha(path)!=digest:raise ValueError('object changed '+str((i,tag)))
   c=Coff(str(path));r=compare(c,pe,spec);sec,inf,errors=eh_sections(c,pe,spec,r,names);failed=[{'start':'0x%08x'%x[0],'end':'0x%08x'%x[1],'parent':x[3],'inferred':x[4]} for x in sec if not x[2]]
   done[tag].append({'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}});entry[tag]={'strict_matches':sum(x['verdict']=='match' for x in r),'function_failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'located_sections':len(sec),'failed_sections':failed,'errors':errors,'inferred_name_count':len(inf)}
  details.append(entry)
 summary={}
 for tag in done:
  tails,bad,inferred,names_count,conf=eh_tails(specs,done[tag],pe);summary[tag]={'requested_unique_tails':len(tails),'bad_tails':bad,'inferred_tails':inferred,'inferred_name_count':names_count,'conflicts':conf,'unit_error_count':sum(len(x[tag]['errors']) for x in details),'failed_section_count':sum(len(x[tag]['failed_sections']) for x in details),'function_failure_count':sum(len(x[tag]['function_failures']) for x in details)}
 OUT.write_text(json.dumps({'scope':'unchanged ordinary EH oracle; same-unit SG and unique strong-external diagnostic bindings only','progress_sha256':sha(progress),'recipe_sha256':sha(rp),'archive_manifest_sha256':sha(A/'manifest.json'),'source_binding_map_sha256':sha(B),'reference_sha256':sha(Path(paths.REF_IMAGE)),'field_scoped_immediate_bindings_excluded':removed,'995_known_false_literal_aliases_excluded':True,'summary':summary,'units':details,'limits':['44 field-scoped immediate proofs excluded from unit-wide diagnostic maps','unit 995 historical source still contains three false literal/global aliases; candidate fix is not substituted','passing tails do not clear other failed located sections','global inferred-name conflicts and final object ownership remain separate']},indent=2));print(json.dumps({k:{'tails':v['requested_unique_tails'],'bad':len(v['bad_tails']),'inferred':len(v['inferred_tails']),'conflicts':v['conflicts'],'errors':v['unit_error_count'],'failed_sections':v['failed_section_count'],'function_failures':v['function_failure_count']} for k,v in summary.items()}))
if __name__=='__main__':main()
