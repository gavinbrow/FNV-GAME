"""Run the BFC cohort serially; report all failures without weakening baselines."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';S=M/'out/phase2-baseformcomponent-core';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
MAN='93f5e6c6392d35a3524cbf78ebcfbf9fba27ad83607f7617f82c7697449e32ec';AUDIT='7937cbaeb95552461704f20563221f7d559762f876961178c91470fad698a1df';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--ack-serialized-lane',action='store_true');a=ap.parse_args()
 if not a.ack_serialized_lane:raise ValueError('explicit serialized compiler lane required')
 out=a.out.resolve()
 try:out.relative_to((M/'out').resolve())
 except ValueError:raise ValueError('output outside private m3/out')
 if not out.name.startswith('phase2-') or out.exists():raise ValueError('private unique output required')
 mp=S/'manifest.json';bp=S/'root-baseline-audit.json'
 if sha(mp)!=MAN or sha(bp)!=AUDIT or sha(F/'build/units.json')!=D:raise ValueError('cohort, baseline audit or recipe changed')
 m=json.loads(mp.read_text());baseline=json.loads(bp.read_text());units=m['units']
 if len(units)!=241 or m['mapped_function_count']!=5817 or baseline['recipe_sha256']!=D or baseline['manifest_sha256']!=MAN:raise ValueError('cohort scope mismatch')
 for x in units:
  i=x['unit'];p=RN/('pinned-build/obj_v3/%04d.obj'%i)
  if sha(p)!=baseline['object_sha256'].get(str(i)):raise ValueError('production object changed %d'%i)
 guards=locks.acquire_guard()
 try:
  # Recheck after locking; no compiler should touch production objects during this run.
  if sha(F/'build/units.json')!=D:raise ValueError('recipe changed after locking')
  for x in units:
   i=x['unit'];p=RN/('pinned-build/obj_v3/%04d.obj'%i)
   if sha(p)!=baseline['object_sha256'][str(i)]:raise ValueError('production object changed after locking %d'%i)
  out.mkdir();logs=out/'logs';logs.mkdir();result={'cohort_manifest_sha256':MAN,'baseline_audit_sha256':AUDIT,'recipe_sha256':D,'total_units':241,'total_functions':5817,'units':[],'status':'running','limitations':['baseline comparator is unit-only and fails closed; no cross-unit local-label binding','named EH section checks do not replace full ordinary EH-tail/ownership checks','RTTI/vtables, all generated sections, production label reproof and full image remain separate']}
  env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
  def save():
   tmp=out/'progress.tmp';tmp.write_text(json.dumps(result,indent=2));os.replace(tmp,out/'progress.json')
  def command(i,label,args):
   log=logs/('%04d-%s.log'%(i,label))
   with log.open('xb') as f:r=subprocess.run([sys.executable]+[str(z) for z in args],cwd=P,env=env,stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,timeout=1800)
   return {'rc':r.returncode,'log':str(log.relative_to(out))}
  save()
  for x in units:
   i=x['unit'];mirror=M/('out/phase2-bfc-core-u%04d'%i);row={'unit':i,'functions':len(x['functions']),'baseline_unit_only_matches':next(q['unit_only_matches'] for q in baseline['units'] if q['unit']==i)}
   try:
    if mirror.exists():
     mm=json.loads((mirror/'mirror-manifest.json').read_text())
     if mm.get('bfc_cohort_manifest_sha256')!=MAN or mm['source']!=x['source'] or mm['units_sha256']!=D:raise ValueError('preexisting mirror mismatch')
     row['prepare']={'status':'reused pinned mirror'}
    else:
     row['prepare']=command(i,'prepare',[H/'baseformcomponent_core_mirror.py','--unit',str(i)])
     if row['prepare']['rc']:raise ValueError('mirror preparation failed')
    cr=mirror/'compile-result.json'
    if cr.exists():
     c=json.loads(cr.read_text());rr={z['tag']:z for z in c['outcomes']}
     if c['unit_index']!=i or c['mirror_manifest_sha256']!=sha(mirror/'mirror-manifest.json') or set(rr)!={'original','candidate'} or any(rr[t]['rc'] or not rr[t]['trace_valid'] or sha(mirror/(t+'.obj'))!=rr[t]['object_sha256'] for t in rr):raise ValueError('preexisting compile invalid')
     row['compile']={'status':'reused pinned objects'}
    else:
     row['compile']=command(i,'compile',[H/'rtti_mirror_compile_d569.py','--out',mirror])
     if row['compile']['rc']:raise ValueError('mirror compilation failed')
    comparison=mirror/'comparison-cohort.json'
    if comparison.exists():raise ValueError('cohort comparison already exists; manual review required')
    row['compare']=command(i,'compare',[H/'baseformcomponent_core_compare.py','--unit',str(i),'--production-object-sha256',baseline['object_sha256'][str(i)],'--report','comparison-cohort.json'])
    if row['compare']['rc']:raise ValueError('strict comparison failed')
    q=json.loads(comparison.read_text());n=len(x['functions'])
    if q['functions']!=n or any(q[k]!=n for k in ('production_reference_matches','mirror_original_reference_matches','mirror_candidate_reference_matches')):raise ValueError('comparison counts differ')
    row['status']='function-and-named-eh-pass'
   except Exception as exc:row['status']='failed';row['error']=str(exc)
   result['units'].append(row);save();print(json.dumps({'unit':i,'status':row['status'],'error':row.get('error')}),flush=True)
  result['status']='complete-with-failures' if any(x['status']!='function-and-named-eh-pass' for x in result['units']) else 'function-and-named-eh-pass';save()
 finally:
  for p in reversed(guards):p.unlink()
 if result['status']!='function-and-named-eh-pass':raise SystemExit(1)
if __name__=='__main__':main()
