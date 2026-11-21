"""Extend the private BFC core proposal to the TESObjectWEAP exact-body wrapper."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-bfc-core-weapon-extension';OLD=M/'out/phase2-baseformcomponent-core';AUD=M/'out/phase2-baseformcomponent-audit-v2.json';TRANS=M/'out/phase2-bfc-core-rebase-6757.json';WRAP='src/fallout_shared/tesobjectweap_BaseFormComponent.h';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve previous experiment')
 raw=(F/'build/units.json').read_bytes();m=json.loads((OLD/'manifest.json').read_text());a=json.loads(AUD.read_text());t=json.loads(TRANS.read_text());doc=json.loads(raw)
 if sha(raw)!=BASE or t['new_recipe_sha256']!=BASE or t['old_cohort_manifest_sha256']!=sha((OLD/'manifest.json').read_bytes()):raise ValueError('recipe transition proof mismatch')
 row=next(x for x in a['definitions'] if x['path']==WRAP)
 if not row['canonical_body_exact'] or row['ambient_pack_unknown']!=True or [x['unit'] for x in row['consumer_units']]!=[1097] or sha((F/WRAP).read_bytes())!=row['sha256']:raise ValueError('wrapper evidence differs')
 canonical=core.block((F/'include/BaseFormComponent.h').read_bytes());w=(F/WRAP).read_bytes();b=core.block(w)
 if ' '.join(b.split())!=' '.join(canonical.split()):raise ValueError('class body differs')
 text=w.decode('utf-8-sig');new=text.replace(b,'#include "BaseFormComponent_core.h"',1).encode()
 if text.count(b)!=1:raise ValueError('ambiguous class')
 overrides={WRAP:new}
 for x in m['files']:
  candidate=(OLD/x['generated']).read_bytes()
  if sha(candidate)!=x['new_sha256']:raise ValueError('existing core payload changed')
  if x['old_sha256'] is None:
   if (F/x['path']).exists():raise ValueError('new core already exists')
  elif sha((F/x['path']).read_bytes())!=x['old_sha256']:raise ValueError('old core wrapper differs')
  overrides[x['path']]=candidate
 oldunits={x['unit'] for x in m['units']};wanted=oldunits|{1097}
 if len(oldunits)!=241 or len(wanted)!=242:raise ValueError('cohort scope changed')
 units=[]
 for i in sorted(wanted):
  u=doc['units'][i];before=core.walk(F,u['source'],{});after=core.walk(F,u['source'],overrides)
  if set(after['files'])!=set(before['files'])|{'include/BaseFormComponent_core.h'}:raise ValueError('unexpected closure delta '+str(i))
  changes=[k for k in before['files'] if before['files'][k]!=after['files'][k]]
  if any(k not in overrides for k in changes):raise ValueError('unreviewed content delta')
  units.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':before,'candidate':after,'changed_wrappers':changes})
  if i==1097 and WRAP not in changes:raise ValueError('additional wrapper absent')
 O.mkdir();(O/'weapon.original').write_bytes(w);(O/'weapon.generated').write_bytes(new)
 for item in m['files']:
  for key in ('original','generated'):
   name=item[key]
   if name is not None:(O/name).write_bytes((OLD/name).read_bytes())
 report={'schema_version':1,'base_units_sha256':sha(raw),'prior_core_manifest_sha256':sha((OLD/'manifest.json').read_bytes()),'scoped_audit_sha256':sha(AUD.read_bytes()),'transition_audit_sha256':sha(TRANS.read_bytes()),'new_wrapper':WRAP,'new_wrapper_old_sha256':sha(w),'new_wrapper_new_sha256':sha(new),'files':m['files']+[{'path':WRAP,'old_sha256':sha(w),'new_sha256':sha(new),'original':'weapon.original','generated':'weapon.generated'}],'units':units,'scope':'existing private four-file proposal plus one exact-body global wrapper','limitations':['syntactic closure only; preprocessing guard and pack histories need proof','ambient pack remains unproved and unchanged','not a native global ODR or ABI identity claim','all affected units, recipe EH tails, metadata, production labels and full-image/runtime gates remain required']}
 (O/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps({'units':len(units),'functions':sum(len(x['functions']) for x in units),'eh_tails':sum(len(x['eh_tails']) for x in units),'unit1097_functions':len(doc['units'][1097]['functions'])}))
if __name__=='__main__':main()
