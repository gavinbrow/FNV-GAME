"""Capture 128 post-positive 825d production objects for later private verification."""
import argparse,datetime,hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-operators-825d';sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as locks
BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='7689a05cc64e094a726f8d8261378e4cdcbad790f7b05a73295a4439d01da4bf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--ack-positive-terminal',action='store_true');a=ap.parse_args();out=a.out.resolve()
 if not a.ack_positive_terminal or not out.is_relative_to((M/'out').resolve()) or not out.name.startswith('phase2-') or out.exists():raise ValueError('fresh private archive and terminal-positive acknowledgment required')
 if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN:raise ValueError('recipe or cohort preflight differs')
 m=json.loads((P/'manifest.json').read_text());rows=m['units']
 if len(rows)!=128 or len({x['unit'] for x in rows})!=128 or sum(len(x['functions']) for x in rows)!=2580 or sum(len(x['eh_tails']) for x in rows)!=88:raise ValueError('cohort scope differs')
 guards=locks.acquire_guard()
 try:
  if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN:raise ValueError('inputs changed after locking')
  out.mkdir();records=[]
  for row in rows:
   i=row['unit'];source=RN/('pinned-build/obj_v3/%04d.obj'%i);target=out/('%04d.obj'%i)
   if not source.is_file():raise ValueError('production object missing '+str(i))
   before=source.stat();digest=sha(source);shutil.copyfile(source,target);after=source.stat()
   if before.st_size!=after.st_size or before.st_mtime_ns!=after.st_mtime_ns or target.stat().st_size!=before.st_size or sha(target)!=digest or sha(source)!=digest:raise ValueError('production object changed while capturing '+str(i))
   records.append({'unit':i,'sha256':digest,'size':before.st_size,'source_mtime_ns':before.st_mtime_ns})
  if sha(F/'build/units.json')!=BASE:raise ValueError('recipe changed during capture')
  result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'recipe_sha256':BASE,'cohort_manifest_sha256':PIN,'objects':records,'scope':'actual 825d post-positive production objects; no compilation','limitations':['capture must be run only after the positive build terminates and before control builds','object capture does not establish function, EH, ownership or final image correctness']};(out/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({'objects':len(records),'manifest_sha256':sha(out/'manifest.json')}))
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':main()
