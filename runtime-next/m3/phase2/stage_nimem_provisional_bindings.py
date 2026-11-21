"""Compose source-local provisional 133-fixture bindings; never install."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path[:0]=[str(H),str(R/'fnv_decomp/tools'),str(R/'runtime-next')]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
import paths,tescontainer_install
O=M/'out';D=O/'phase2-nimem-combined-825d-run';BASE=O/'phase2-nimem-combined-825d';DEST=O/'phase2-nimem-provisional-bindings-133';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if DEST.exists():raise FileExistsError(DEST)
 p1=D/'independent-four-pool-binding-replay.json';p2=D/'independent-509-592-binding-replay.json';p3=O/'phase2-nimem-combined-eh-label-diagnostic-v2.json';pins={p1:'2d68df5b986869bc58ace57b79bb1b6cee9f540556b1320dee4c884e64f92e0f',p2:'231dfdb0def50f1e20d128b5472305b7b86f353ea8283c88bb482d94b94d4b7c'}
 for p,v in pins.items():
  if h(p)!=v:raise ValueError('proof changed '+str(p))
 raw=(BASE/'units.generated').read_bytes()
 if hashlib.sha256(raw).hexdigest()!='fcf06f28918cd1280dc61a6cd61b96a17ce1418024482a34ed637e5babfcb9c2':raise ValueError('base recipe differs')
 base=json.loads(raw);updates={};source={}
 def add(i,name,target,label):
  if not name.startswith('$SG') and (i,name) not in [(592,'?ReadBytes@FUN_00462d80_shell@@QAEIPAXI@Z'),(592,'?FUN_004720a0@@YIHPAD@Z')]:raise ValueError('unsupported binding '+name)
  if name in updates.setdefault(i,{}) and updates[i][name]!=target:raise ValueError('binding conflict')
  updates[i][name]=target;source.setdefault(i,{})[name]=label
 for x in j(p1)['units']:
  if h(D/('unit-%04d'%x['unit'])/'candidate.obj')!=x['object_sha256']:raise ValueError('four replay object changed')
  for k,v in x['bindings'].items():add(x['unit'],k,v,'same-unit archived pool and original strict source map')
 for x in j(p2)['units']:
  i=x['unit']
  if h(D/('unit-%04d'%i)/'candidate.obj')!=x['checks']['candidate']['object_sha256']:raise ValueError('baseline replay object changed')
  for k,v in x['candidate_pool_bindings'].items():add(i,k,v,'same-unit pool with source-backed baseline')
  for k,v in x['source_bound_baseline'].items():
   if not k.startswith('$SG'):add(i,k,v,'unique external source definition')
 for key,x in j(p3)['units'].items():
  i=int(key);d=D/('unit-%04d'%i)
  if i not in (548,721,722,726) or h(d/'original.obj')!=x['original_sha256'] or h(d/'candidate.obj')!=x['candidate_sha256'] or x['issues'] or x['unmatched'] or x['eh_failed'] or x['eh_errors']:raise ValueError('EH diagnostic not clean')
  for k,v in x['bindings'].items():add(i,k,v,'same-unit relocation field and archived source literal')
 if sorted(updates)!=[147,392,509,548,592,703,721,722,725,726]:raise ValueError('scope mismatch')
 encoded=raw;changes={}
 for i in sorted(updates):
  unit=copy.deepcopy(json.loads(encoded)['units'][i]);changes[str(i)]={k:{'before':unit['symbols'].get(k),'after':v,'evidence':source[i][k]} for k,v in sorted(updates[i].items()) if unit['symbols'].get(k)!=v};unit['symbols'].update(updates[i]);encoded=tescontainer_install.replace_unit(encoded,i,unit)
 result=json.loads(encoded);units=result['units'];changed=[i for i,(a,b) in enumerate(zip(base['units'],units)) if a!=b]
 if any(any(base['units'][i][k]!=units[i][k] for k in base['units'][i] if k!='symbols') for i in changed):raise ValueError('changed non-symbol unit field')
 for i in (1664,2734):
  if base['units'][i]!=units[i]:raise ValueError('native operator source ownership changed')
 pe=Pe(paths.REF_IMAGE);review={}
 for i in sorted(updates):
  c=Coff(str(D/('unit-%04d'%i)/'candidate.obj'));r=compare(c,pe,units[i]);sec,inf,err=eh_sections(c,pe,units[i],r,recipe_names(units));review[str(i)]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'eh_sections':len(sec),'eh_failed':sum(not x[2] for x in sec),'eh_errors':err,'inferred_names':{k:hex(v) for k,v in inf.items()}}
 DEST.mkdir();(DEST/'units.original').write_bytes(raw);(DEST/'units.generated').write_bytes(encoded)
 out={'status':'PRIVATE PROVISIONAL fixture-specific bindings; not installation-ready','base_recipe_sha256':hashlib.sha256(raw).hexdigest(),'candidate_recipe_sha256':h(DEST/'units.generated'),'source_recipe_825d_sha256':base and h(BASE/'units.original'),'changed_units':changed,'symbol_changes':changes,'proof_sha256':{str(p.relative_to(R)).replace('\\','/'):h(p) for p in (p1,p2,p3)},'fixture_replay':review,'operator_source_owners':['0x00aa1460 unit1664 sized delete','0x00aa13e0 unit2734 operator new'],'limitations':['not production-ready: proposed placement/adapter source fixes may change SG names','no field-only immediate proof has been applied unit-wide','inferred EH names are not added to recipe','operator/vtable metadata, weak COMDAT provider and full image/runtime gates remain','actual post-source-change compilation and exact source pool proof required']}
 (DEST/'manifest.json').write_text(json.dumps(out,indent=2));print(json.dumps({'manifest':h(DEST/'manifest.json'),'recipe':h(DEST/'units.generated'),'units':changed,'bindings':sum(map(len,changes.values())),'results':{k:(v['matches'],v['functions'],v['eh_failed'],len(v['eh_errors'])) for k,v in review.items()}}))
if __name__=='__main__':main()
