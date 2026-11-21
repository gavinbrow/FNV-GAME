"""Compose reviewed private source hypotheses and provisional recipe bindings."""
import copy,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core,tescontainer_install
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-combined-825d';A=R/'phase2-nimem-adapter-using-v2';G=R/'phase2-nimem-global-placement-v2';T=R/'phase2-tesfile-recordtype-825d';B=R/'phase2-nimem-provisional-bindings-133';U=R/'phase2-nimem-unit200-normal-new-v3';O=R/'phase2-nimem-next-source-composed'
PINS={P/'manifest.json':'6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3',A/'manifest.json':'ec90e9a5d649e5841c04d5ad194b07d17eca8c5a12a267d40faed73ed95739e3',G/'manifest.json':'085f79dfe40efd9276219ed27320f8761d77dc17fff7e979fd088882b9403678',T/'manifest.json':'45425a3ac83c34c3709240e07e069138e37265298570644735a790ca4688fc30',B/'manifest.json':'237f37f7978f2765e3793c2fec3e7c8f05289b6e02852effb4894b12993afe6f',U/'source-owner-replay.json':'6acfb2049b12049418545c7dc8b813735b1341c134baaf5c9d4580a06db59af3',R/'phase2-nimem-adapter-using-v2-773-literal-proof.json':'252c94b618e4c149874920cae6210ce8e33cbdac178cafbd52f7d004bc01e8ad'}
BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 for p,h in PINS.items():
  if sha(p.read_bytes())!=h:raise ValueError('parent evidence changed '+str(p))
 raw=(F/'build/units.json').read_bytes()
 if sha(raw)!=BASE:raise ValueError('recipe changed')
 old=json.loads(raw);am=json.loads((A/'manifest.json').read_bytes());gm=json.loads((G/'manifest.json').read_bytes());tm=json.loads((T/'manifest.json').read_bytes());bm=json.loads((B/'manifest.json').read_bytes());u200=json.loads((U/'source-owner-replay.json').read_bytes());proof=json.loads((R/'phase2-nimem-adapter-using-v2-773-literal-proof.json').read_bytes())
 if sha((B/'units.generated').read_bytes())!=bm['candidate_recipe_sha256'] or sha((T/'0.original').read_bytes())!=BASE:raise ValueError('recipe parent changed')
 data={}
 for rel,h in am['source_payload_sha256'].items():
  b=(A/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('adapter payload changed '+rel)
  data[rel]=b
 for item in gm['files']:
  rel=item['path']
  if rel.endswith('speedtreeleafshader.cpp'):continue
  if rel in data or sha((F/rel).read_bytes())!=item['before_sha256']:raise ValueError('placement source overlap/drift')
  b=(G/'payload'/rel).read_bytes()
  if sha(b)!=item['after_sha256']:raise ValueError('placement payload changed')
  data[rel]=b
 rel='src/bsshader/speedtreeleafshader.cpp';b=(U/'candidate'/rel).read_bytes()
 if rel in data or sha(b)!='5096a3e1b9b5ff785130e874afe2d0dafc9867d3c63a0186bfb688a685d5915b':raise ValueError('unit200 source mismatch')
 data[rel]=b
 item=next(x for x in tm['files'] if x['path'].endswith('/tesfile.cpp'));rel=item['path'];b=(T/item['generated']).read_bytes()
 if rel in data or sha((F/rel).read_bytes())!=item['old_sha256'] or sha(b)!=item['new_sha256']:raise ValueError('995 source overlap/drift')
 data[rel]=b
 for item in am['adapter_changes']:
  if sha((F/item['path']).read_bytes())!=item['before_sha256']:raise ValueError('adapter preimage changed')
 recipe=(B/'units.generated').read_bytes();current=json.loads(recipe);tes=json.loads((T/'0.generated').read_bytes())
 if current['units'][995]!=old['units'][995]:raise ValueError('995 recipe overlaps previous edits')
 recipe=tescontainer_install.replace_unit(recipe,995,tes['units'][995]);current=json.loads(recipe)
 for i in (200,773):
  unit=copy.deepcopy(current['units'][i]);symbols=unit['symbols']
  additions=proof['unit_local_bindings'] if i==773 else {u200['owner_2734']['source_native_symbol']:u200['owner_2734']['address'],u200['owner_1664']['source_native_symbol']:u200['owner_1664']['address']}
  for name,value in additions.items():symbols[name]=value
  recipe=tescontainer_install.replace_unit(recipe,i,unit);current=json.loads(recipe)
 changed_units=[]
 for i,(a,b) in enumerate(zip(old['units'],current['units'])):
  if a!=b:
   if {k:v for k,v in a.items() if k!='symbols'}!={k:v for k,v in b.items() if k!='symbols'} and i not in (1664,2734):raise ValueError('unreviewed recipe field change '+str(i))
   changed_units.append(i)
 scope=[]
 for i,u in enumerate(old['units']):
  original=core.walk(F,u['source'],{});candidate=core.walk(F,u['source'],data)
  touched=sorted(k for k in set(original['files'])|set(candidate['files']) if original['files'].get(k)!=candidate['files'].get(k))
  if touched or i in changed_units:scope.append({'unit':i,'source':u['source'],'flags':u['flags'],'compiler':u['compiler'],'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[])),'source_changes':touched,'recipe_changed':i in changed_units,'original':original,'candidate':candidate})
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(recipe)
 for rel,b in data.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 result={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(recipe),'parent_sha256':{str(k.relative_to(R)):v for k,v in PINS.items()},'source_payload_sha256':{k:sha(v) for k,v in data.items()},'recipe_changed_units':changed_units,'affected_units':scope,'limits':['private provisional composition only; no source installation','recipe literal labels are fixture-specific and must be rederived from actual production objects','source and recipe overlap checked; newly composed closures require fresh joint proof','unit 995 outside-owner EH contribution and earlier unresolved baseline EH remain separately gated','class layout, generated metadata, ODR, image and runtime gates remain open']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({'source_files':len(data),'affected_units':len(scope),'recipe_units':changed_units,'manifest_sha256':sha((O/'manifest.json').read_bytes())}))
if __name__=='__main__':main()
