"""Preflight native NiMemObject operator proposal across reviewed 825d transition."""
import copy,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core,tescontainer_install
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimemobject-native-operators-v2';T=M/'out/phase2-source-integration6757-transaction-v2';S=M/'out/phase2-nirefobject-classkey-consumers.json';O=M/'out/phase2-nimem-operators-825d';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';OLD='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';TPIN='9422dd1642f66ddca78a1b161b040cdb55847afd3ad447fbf66e86a6ed47e9da'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior evidence')
 raw=(F/'build/units.json').read_bytes();before=(T/'0.original').read_bytes();after=(T/'0.candidate').read_bytes();tx=json.loads((T/'manifest.json').read_text());p=json.loads((P/'manifest.json').read_text());scope=json.loads(S.read_text())
 if sha(raw)!=BASE or raw!=after or sha(before)!=OLD or sha((T/'manifest.json').read_bytes())!=TPIN or p['base_recipe_sha256']!=OLD or scope['recipe_sha256']!=OLD:raise ValueError('unreviewed transition')
 a=json.loads(before);b=json.loads(after);proposed=json.loads((P/'units.generated').read_bytes());indices=[i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]
 if indices!=[253,370,425,620,2909] or any(a[k]!=b[k] for k in a if k!='units') or any(a['units'][i]!=b['units'][i] for i in (1664,2734)):raise ValueError('semantic transition differs')
 changed={x['path']:x for x in tx['files'] if x['path']!='build/units.json'}
 for rel,x in changed.items():
  q=F/rel
  if not q.exists() or sha(q.read_bytes())!=x['new_sha256']:raise ValueError('transaction payload differs '+rel)
  if x['original'] is not None and sha((T/x['original']).read_bytes())!=x['old_sha256']:raise ValueError('transaction preimage differs')
 overrides={}
 for rel,digest in p['source_payload_sha256'].items():
  q=P/'payload'/rel
  if sha(q.read_bytes())!=digest:raise ValueError('operator payload changed '+rel)
  overrides[rel]=q.read_bytes()
 for i in (1664,2734):
  for rel,digest in p['mirrors'][str(i)]['original']['files'].items():
   if sha((F/rel).read_bytes())!=digest:raise ValueError('owner closure differs '+rel)
 generated=raw
 for i in (1664,2734):generated=tescontainer_install.replace_unit(generated,i,proposed['units'][i])
 nd=json.loads(generated)
 if [i for i,(x,y) in enumerate(zip(b['units'],nd['units'])) if x!=y]!=[1664,2734] or any(b[k]!=nd[k] for k in b if k!='units'):raise ValueError('candidate recipe scope differs')
 rows=[x for x in scope['units'] if 'include/NiMemObject.h' in x['target_headers']];wanted={x['unit'] for x in rows}|{1664,2734}
 if len(rows)!=126 or len(wanted)!=128:raise ValueError('consumer scope differs')
 oldrows={x['unit']:x for x in rows};details=[];transitions=[]
 for i in sorted(wanted):
  u=b['units'][i];original=core.walk(F,u['source'],{});candidate=core.walk(F,u['source'],overrides)
  if i in oldrows:
   prior=oldrows[i]['quoted_project_closure'];same=set(prior)&set(original['files']);diff=[q for q in same if prior[q]!=original['files'][q]];added=sorted(set(original['files'])-set(prior));removed=sorted(set(prior)-set(original['files']))
   if any(q not in changed for q in diff) or any(q not in changed for q in added):raise ValueError('unreviewed closure transition '+str((i,diff,added)))
   if diff or added or removed:transitions.append({'unit':i,'changed_existing':diff,'added':added,'removed':removed})
  if 'include/NiMemObject.h' not in candidate['files']:raise ValueError('candidate does not reach API '+str(i))
  actual=[q for q in set(original['files'])&set(candidate['files']) if original['files'][q]!=candidate['files'][q]]
  if any(q not in overrides for q in actual):raise ValueError('unexpected candidate source delta '+str(i))
  details.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':u['functions'],'eh_tails':u.get('eh_tails',[]),'original':original,'candidate':candidate,'changed_inputs':actual})
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(generated)
 for rel,data in overrides.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(generated),'old_recipe_sha256':OLD,'transition_manifest_sha256':TPIN,'prior_operator_manifest_sha256':sha((P/'manifest.json').read_bytes()),'prior_consumer_scope_sha256':sha(S.read_bytes()),'source_payload_sha256':{k:sha(v) for k,v in overrides.items()},'recipe_units_changed':[1664,2734],'source_transition_affected_consumers':transitions,'units':details,'limits':['private preflight only; no source, recipe, or compiler actions','750-unit kind-only proposal is separate and not included','all 128 units require production flags, actual traces, strict functions, ordinary EH, new/delete and weak/COMDAT review','legacy FUN caller symbol resolution and actual production/whole image remain open']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'units':len(details),'functions':sum(len(x['functions']) for x in details),'eh_tails':sum(len(x['eh_tails']) for x in details),'transition_affected':len(transitions),'recipe_sha256':sha(generated)}))
if __name__=='__main__':main()
