"""Capture completed production owners under the active source freeze; no compiler."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';OUT=R/'phase2-watershader-211-owner-v2-capture';FREEZE=R/'phase2-psa-w103-v2-positive-freeze/inputs-before.json';LOG=RN/'pinned-build/logs/compile_v3.jsonl';OBJ=RN/'pinned-build/obj_v3';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior capture')
 recipe=(F/'build/units.json').read_bytes();freeze_raw=FREEZE.read_bytes();log_raw=LOG.read_bytes()
 if sha(recipe)!=BASE:raise ValueError('recipe changed')
 freeze=json.loads(freeze_raw);units=json.loads(recipe)['units'];logrows=[json.loads(x) for x in log_raw.splitlines() if x.strip()];objects={};records=[];closures={}
 for i in (47,781):
  u=units[i];matches=[x for x in logrows if x.get('index')==i]
  if len(matches)!=1 or matches[0].get('status')!='ok' or matches[0].get('rc')!=0 or matches[0].get('source')!=u['source'] or matches[0].get('compiler')!=u['compiler']:raise ValueError('compile log differs '+str(i))
  closure=core.walk(F,u['source'],{});closures[i]=closure
  for rel,h in closure['files'].items():
   path=(F/rel).resolve();entry=freeze.get(str(path))
   if not entry or entry['sha256']!=h or sha(path.read_bytes())!=h:raise ValueError('source freeze mismatch '+rel)
  obj=OBJ/('%04d.obj'%i);b=obj.read_bytes();objects[i]=b;records.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'size':len(b),'object_sha256_start':sha(b),'compile_log_row':matches[0],'closure':closure})
 OUT.mkdir()
 for i,b in objects.items():(OUT/('%04d.obj'%i)).write_bytes(b)
 for row in records:
  i=row['unit'];row['object_sha256_end']=sha((OBJ/('%04d.obj'%i)).read_bytes())
  if row['object_sha256_end']!=row['object_sha256_start'] or sha((OUT/('%04d.obj'%i)).read_bytes())!=row['object_sha256_start']:raise ValueError('object changed during capture')
  if core.walk(F,row['source'],{})!=closures[i]:raise ValueError('closure changed during capture')
 if sha((F/'build/units.json').read_bytes())!=BASE or sha(FREEZE.read_bytes())!=sha(freeze_raw) or sha(LOG.read_bytes())!=sha(log_raw):raise ValueError('freeze or log changed during capture')
 (OUT/'manifest.json').write_text(json.dumps({'recipe_sha256':BASE,'freeze_sha256':sha(freeze_raw),'freeze_entries':len(freeze),'compile_log_sha256':sha(log_raw),'objects':records,'limits':['capture after compile while harness active, not a proof of final linked ownership','source closure is quoted-project lexical inventory; system includes/toolchain provenance follow compile log','start/end hashes detect capture races but not historical producer identity']},indent=2));print(sha((OUT/'manifest.json').read_bytes()))
if __name__=='__main__':main()
