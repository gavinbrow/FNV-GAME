"""Run all NiMemObject kind cohort units on an exclusive verifier lane."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';S=M/'out/phase2-nimemobject-coherent-kind-consumers.json';K=M/'out/phase2-nimemobject-coherent-kind/manifest.json';sys.path[:0]=[str(H),str(F/'tools'),str(RN)];import rtti_tesform_bindings_transaction as locks
from compare import Pe
from build_and_match import eh_tails
import paths
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SH='c45dad435c9c172c149afa1fb4054ae5844f59299e1a1dcb6ffaa1e3ca2bc67f';KH='5e4610cd17372885861964b9e25238925b5d69f8c0f2287065107fee7ac445d6';ARCH=M/'out/phase2-nimem-kind-production-archive';AH='62a67ba7b952e0b04f52c019652e035214dee8ffb425daedfbbf099ebf0967e5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--ack-serialized-lane',action='store_true');a=ap.parse_args();out=a.out.resolve()
 if not a.ack_serialized_lane or not out.is_relative_to((M/'out').resolve()) or not out.name.startswith('phase2-') or out.exists():raise ValueError('fresh private output and serialized-lane acknowledgment required')
 if sha(F/'build/units.json')!=BASE or sha(S)!=SH or sha(K)!=KH or sha(ARCH/'manifest.json')!=AH:raise ValueError('recipe/scope/proposal/archive differs')
 scope=json.loads(S.read_text());units=json.loads((F/'build/units.json').read_text())['units'];rows=scope['units']
 if len(rows)!=750 or scope['mapped_functions']!=26446 or scope['recipe_eh_tails']!=866:raise ValueError('cohort counts differ')
 tools=[H/x for x in ('nimem_kind_cohort_prepare.py','nimem_kind_cohort_compile.py','nimem_kind_cohort_compare.py')];toolhash={p.name:sha(p) for p in tools};guards=locks.acquire_guard()
 try:
  if sha(F/'build/units.json')!=BASE or sha(S)!=SH or sha(K)!=KH or sha(ARCH/'manifest.json')!=AH:raise ValueError('inputs changed after lock')
  archive=json.loads((ARCH/'manifest.json').read_text())
  if archive['recipe_sha256']!=BASE or len(archive['objects'])!=750:raise ValueError('archive scope differs')
  inventory={x['unit']:x for x in archive['objects']}
  if len(inventory)!=750 or set(inventory)!={x['unit'] for x in rows}:raise ValueError('archive unit set differs')
  objects={}
  for x in rows:
   i=x['unit'];p=ARCH/('%04d.obj'%i);entry=inventory[i]
   if not p.exists() or p.stat().st_size!=entry['size'] or sha(p)!=entry['sha256']:raise ValueError('archived production object differs '+str(i))
   objects[str(i)]=entry['sha256']
  out.mkdir();(out/'units.snapshot.json').write_bytes((F/'build/units.json').read_bytes());logs=out/'logs';logs.mkdir()
  result={'recipe_sha256':BASE,'scope_sha256':SH,'kind_manifest_sha256':KH,'tools_sha256':toolhash,'production_archive_manifest_sha256':AH,'production_object_sha256':objects,'total_units':750,'total_functions':26446,'requested_recipe_eh_tails':866,'units':[],'status':'running','limits':['unit-only baselines and class-key warnings are retained, never borrowed','compiled records reveal emitted class keys but do not prove absent first declarations','ordinary EH union requires all successful reports and outside-owner checks','final object ownership, packing and production/full-image gates remain separate']}
  def save():
   p=out/'progress.tmp';p.write_text(json.dumps(result,indent=2));os.replace(p,out/'progress.json')
  def command(i,label,args):
   log=logs/('%04d-%s.log'%(i,label))
   with log.open('xb') as f:r=subprocess.run([sys.executable]+[str(z) for z in args],cwd=F.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
   return {'rc':r.returncode,'log':str(log.relative_to(out))}
  save()
  for x in rows:
   i=x['unit'];d=out/('unit-%04d'%i);entry={'unit':i,'functions':x['functions'],'eh_tails':x['eh_tails']}
   try:
    if any(sha(p)!=toolhash[p.name] for p in tools) or sha(F/'build/units.json')!=BASE:raise ValueError('tool or recipe changed')
    if objects[str(i)] is None:raise ValueError('production object missing')
    entry['prepare']=command(i,'prepare',[tools[0],'--unit',i,'--out',d])
    if entry['prepare']['rc']:raise ValueError('mirror preparation failed')
    entry['compile']=command(i,'compile',[tools[1],'--unit',i,'--out',d])
    if entry['compile']['rc']:raise ValueError('compile or include trace failed')
    entry['compare']=command(i,'compare',[tools[2],'--unit',i,'--out',d,'--production-object-sha256',objects[str(i)]])
    if entry['compare']['rc']:raise ValueError('comparison execution failed')
    report=json.loads((d/'comparison.json').read_text());entry['comparison_sha256']=sha(d/'comparison.json');entry['strict_matches']={k:v.get('matches') for k,v in report['strict_reference'].items()};entry['pair_differences']=len(report['mapped_function_pair_differences']);entry['classkey_warning_count']=sum(len(v) for v in report['compiler_classkey_warnings'].values());entry['eh_errors']={k:len(v['errors']) for k,v in report['ordinary_eh'].items()};entry['failed_eh_sections']={k:sum(not z[2] for z in v['eh_sections']) for k,v in report['ordinary_eh'].items()};entry['status']='pass' if all(v==x['functions'] for v in entry['strict_matches'].values()) and not entry['pair_differences'] and not entry['classkey_warning_count'] and not any(entry['eh_errors'].values()) and not any(entry['failed_eh_sections'].values()) else 'review-required'
   except Exception as e:entry['status']='failed';entry['error']=str(e)
   result['units'].append(entry);save();print(json.dumps({'unit':i,'status':entry['status']}),flush=True)
  done={'production':[],'original':[],'candidate':[]}
  for entry in result['units']:
   p=out/('unit-%04d'%entry['unit'])/'comparison.json'
   if p.exists():
    r=json.loads(p.read_text())
    for tag in done:done[tag].append(r['ordinary_eh'][tag])
  pe=Pe(paths.REF_IMAGE);result['ordinary_eh_union']={}
  for tag in done:
   tails,bad,inferred,_,conflicts=eh_tails([units[x['unit']] for x in rows],done[tag],pe)
   result['ordinary_eh_union'][tag]={'requested_unique_tail_count':len(tails),'bad':bad,'inferred_tails':len(inferred),'conflicts':conflicts,'contributing_unit_reports':len(done[tag]),'complete_scope':len(done[tag])==len(rows)}
  result['status']='function-and-eh-pass-metadata-review-required' if all(x['status']=='pass' for x in result['units']) and all(not x['bad'] and not x['conflicts'] and x['complete_scope'] for x in result['ordinary_eh_union'].values()) else 'complete-review-required';save()
 finally:
  for p in reversed(guards):p.unlink()
 if result['status']=='complete-review-required':raise SystemExit(1)
if __name__=='__main__':main()
