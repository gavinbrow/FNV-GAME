"""Conservative include-closure scope for the public NiMemObject key fixture."""
import hashlib,json,sys,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';D=M/'out/phase2-nirefobject-classkey-fixture';OUT=M/'out/phase2-nirefobject-classkey-consumers.json';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';TARGET={'include/layout_support.h','include/NiMemObject.h'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve historical scope')
 rp=F/'build/units.json';raw=rp.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=BASE:raise ValueError('recipe changed')
 u=json.loads(raw)['units'];fixture=json.loads((D/'manifest.json').read_text());cache={};rows=[]
 def declarations(rel):
  if rel not in cache:
   data=(F/rel).read_text(encoding='utf-8-sig',errors='replace');r=[]
   for z in re.finditer(r'\b(class|struct)\s+NiMemObject\s*([;{])',data):r.append({'line':data.count('\n',0,z.start())+1,'keyword':z.group(1),'kind':'forward' if z.group(2)==';' else 'definition'})
   cache[rel]=r
  return cache[rel]
 for i,x in enumerate(u):
  graph=core.walk(F,x['source'],{});hit=sorted(TARGET.intersection(graph['files']))
  if hit:
   views=[{'path':rel,'declarations':declarations(rel)} for rel in graph['files'] if declarations(rel)]
   rows.append({'unit':i,'source':x['source'],'functions':len(x['functions']),'eh_tails':len(x.get('eh_tails',[])),'target_headers':hit,'quoted_project_closure':graph['files'],'declared_views':views,'unresolved_includes':graph['unresolved']})
  if i%250==0:print('processed',i,'of',len(u),flush=True)
 if sha(rp)!=BASE:raise ValueError('recipe changed during scope scan')
 OUT.write_text(json.dumps({'recipe_sha256':sha(rp),'fixture_manifest_sha256':sha(D/'manifest.json'),'target_headers':sorted(TARGET),'recipe_units_scanned':len(u),'affected_units':len(rows),'mapped_functions':sum(x['functions'] for x in rows),'recipe_eh_tails':sum(x['eh_tails'] for x in rows),'units':rows,'limits':['syntactic quoted-include closure overapproximation: inactive branches and shared guards not evaluated','first-declaration order, namespaces, macro-generated includes and conditional definitions are not established by token matches','compiler preprocessing and include traces are required for each affected context','independent class/struct definitions are not merged or reclassified']},indent=2));print('RESULT',len(rows),sum(x['functions'] for x in rows),flush=True)
if __name__=='__main__':main()
