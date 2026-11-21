"""Run the 128-unit native operator cohort on a serialized verifier lane."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-operators-825d';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='7689a05cc64e094a726f8d8261378e4cdcbad790f7b05a73295a4439d01da4bf';sys.path[:0]=[str(H),str(F/'tools'),str(RN)];import rtti_tesform_bindings_transaction as locks
from compare import Pe
from build_and_match import eh_tails
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);p.add_argument('--archive-manifest-sha256',required=True);p.add_argument('--ack-serialized-lane',action='store_true');a=p.parse_args();out=a.out.resolve();archive=a.archive.resolve();am=archive/'manifest.json'
 if not a.ack_serialized_lane or out.exists() or not out.is_relative_to((M/'out').resolve()) or not out.name.startswith('phase2-') or not archive.is_relative_to((M/'out').resolve()):raise ValueError('fresh private paths and serialized lane required')
 if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or sha(am)!=a.archive_manifest_sha256.lower():raise ValueError('pinned input differs')
 proposal=json.loads((P/'manifest.json').read_text());items=proposal['units'];old=json.loads((P/'units.original').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units']
 if len(items)!=128 or sum(len(x['functions']) for x in items)!=2580 or sum(len(x['eh_tails']) for x in items)!=88:raise ValueError('cohort scope differs')
 inventory=json.loads(am.read_text());entries={x['unit']:x for x in inventory['objects']}
 if inventory['recipe_sha256']!=BASE or len(entries)!=len(inventory['objects']) or not {x['unit'] for x in items}<=set(entries):raise ValueError('archive provenance differs')
 tools=[H/x for x in ('nimem_operators_825d_prepare.py','nimem_operators_825d_compile.py','nimem_operators_825d_compare.py')];toolhash={x.name:sha(x) for x in tools};guards=locks.acquire_guard()
 try:
  if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or sha(am)!=a.archive_manifest_sha256.lower():raise ValueError('input changed after lock')
  for x in items:
   i=x['unit'];obj=archive/('%04d.obj'%i);entry=entries[i]
   if not obj.exists() or obj.stat().st_size!=entry['size'] or sha(obj)!=entry['sha256']:raise ValueError('archived object differs '+str(i))
  out.mkdir();logs=out/'logs';logs.mkdir();result={'status':'running','recipe_sha256':BASE,'proposal_sha256':PIN,'archive_manifest_sha256':sha(am),'tool_sha256':toolhash,'unit_count':128,'function_count':2580,'requested_recipe_eh_tails':88,'units':[],'limits':['private API effects, generated/deleting code and source baseline failures require independent review','no automatic normalization or unsupported function aliases','listed EH coverage does not clear other located section failures','first declaration/packing, weak/COMDAT/linker and full image/runtime remain separate']}
  def save():
   q=out/'progress.tmp';q.write_text(json.dumps(result,indent=2));os.replace(q,out/'progress.json')
  def command(i,label,args):
   log=logs/('%04d-%s.log'%(i,label))
   with log.open('xb') as f:r=subprocess.run([sys.executable]+[str(x) for x in args],cwd=F.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
   return {'rc':r.returncode,'log':str(log.relative_to(out))}
  save()
  for x in items:
   i=x['unit'];d=out/('unit-%04d'%i);entry={'unit':i,'functions':len(x['functions']),'eh_tails':len(x['eh_tails'])}
   try:
    if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or any(sha(t)!=toolhash[t.name] for t in tools):raise ValueError('inputs changed')
    entry['prepare']=command(i,'prepare',[tools[0],'--unit',i,'--out',d])
    if entry['prepare']['rc']:raise ValueError('mirror preparation failed')
    entry['compile']=command(i,'compile',[tools[1],'--unit',i,'--out',d])
    if entry['compile']['rc']:raise ValueError('compiler or trace failed')
    entry['compare']=command(i,'compare',[tools[2],'--unit',i,'--out',d,'--production-object',archive/('%04d.obj'%i),'--production-object-sha256',entries[i]['sha256']])
    if entry['compare']['rc']:raise ValueError('comparison execution failed')
    r=json.loads((d/'comparison.json').read_text());entry['comparison_sha256']=sha(d/'comparison.json');entry['strict_matches']={k:v.get('matches') for k,v in r['reference'].items()};entry['pair_differences']=len(r['mapped_function_pair_differences']);entry['warning_count']=sum(len(v) for v in r['compiler_warnings'].values());entry['eh_errors']={k:len(v['errors']) for k,v in r['ordinary_eh'].items()};entry['failed_eh_sections']={k:sum(not y[2] for y in v['eh_sections']) for k,v in r['ordinary_eh'].items()};entry['status']='pass' if all(v==entry['functions'] for v in entry['strict_matches'].values()) and not entry['pair_differences'] and not entry['warning_count'] and not any(entry['eh_errors'].values()) and not any(entry['failed_eh_sections'].values()) else 'review-required'
   except Exception as e:entry['status']='failed';entry['error']=str(e)
   result['units'].append(entry);save();print(json.dumps({'unit':i,'status':entry['status']}),flush=True)
  done={'production':[],'original':[],'candidate':[]}
  for x in result['units']:
   q=out/('unit-%04d/comparison.json'%x['unit'])
   if q.exists():
    r=json.loads(q.read_text())
    for tag in done:done[tag].append(r['ordinary_eh'][tag])
  pe=Pe(paths.REF_IMAGE);result['ordinary_eh_union']={}
  for tag in done:
   units=new if tag=='candidate' else old;tails,bad,inferred,_,conflicts=eh_tails([units[x['unit']] for x in items],done[tag],pe);result['ordinary_eh_union'][tag]={'requested_unique_tails':len(tails),'bad':bad,'inferred_tails':len(inferred),'conflicts':conflicts,'reports':len(done[tag]),'complete_scope':len(done[tag])==len(items)}
  result['status']='function-and-eh-pass-metadata-review-required' if all(x['status']=='pass' for x in result['units']) and all(not x['bad'] and not x['conflicts'] and x['complete_scope'] for x in result['ordinary_eh_union'].values()) else 'complete-review-required';save()
 finally:
  for q in reversed(guards):q.unlink()
 if result['status']=='complete-review-required':raise SystemExit(1)
if __name__=='__main__':main()
