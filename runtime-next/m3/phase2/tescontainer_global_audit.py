"""Read-only TESContainer global declaration and quoted-include recipe audit."""
import collections,functools,hashlib,json,re,sys,types
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';sys.path.insert(0,str(H));import rtti_class_registry as R
# In-memory correction only: do not let directive whitespace consume line breaks.
p=H/'rtti_scoped_registry.py';text=p.read_text().replace("r'(?m)^\\s*#.*$'", "r'(?m)^[ \\t]*#.*$'");scope=types.ModuleType('scoped_local');scope.__file__=str(p);exec(compile(text,str(p),'exec'),scope.__dict__)
legacy=json.load(open(M/'out/phase2-scoped-registry/TESContainer-scopes.json'));units_path=F/'build/units.json';units_raw=units_path.read_bytes();units=json.loads(units_raw)['units'];files=sorted({x['path'] for x in legacy['definitions']});targets={};
for path in files:
 raw=(F/path).read_bytes();src=raw.decode('utf-8-sig',errors='replace');clean=R.clean(src)
 for x in scope.scopes(src,'TESContainer'):
  if x['category']!='global':continue
  matches=[z for z in R.DECL.finditer(clean) if z.group(2)=='TESContainer' and clean.count('\n',0,z.start())+1==x['line']]
  if len(matches)!=1:raise ValueError('ambiguous declaration '+path)
  q=matches[0];i=q.end();depth=1
  while depth and i<len(clean):depth+=(clean[i]=='{')-(clean[i]=='}');i+=1
  if depth:raise ValueError('unbalanced declaration '+path)
  body=clean[q.end():i-1];decls=[' '.join(z.split()) for z in body.split(';') if '(' in z and ')' in z]
  method_names=[]
  for declaration in decls:
   match=re.search(r'(~?[A-Za-z_]\w*)\s*\(',declaration)
   if match:method_names.append(match.group(1))
  targets[path]={'path':path,'line':x['line'],'sha256':hashlib.sha256(raw).hexdigest(),'keyword':q.group(1),'base_form_component':'BaseFormComponent' in clean[q.start():q.end()],'method_names':method_names,'virtual_declaration_count':sum('virtual' in z.split() for z in decls),'conditional_directives':x['conditional_directives']}
assert len(targets)==25
INC=re.compile(rb'^[ \t]*#[ \t]*include[ \t]*"([^"\r\n]+)"',re.M)
@functools.lru_cache(None)
def includes(path):
 p=Path(path);out=[];missing=[]
 for b in INC.findall(p.read_bytes()):
  try:n=b.decode('ascii')
  except UnicodeDecodeError:missing.append('<non-ascii>');continue
  q=next((z.resolve() for z in (p.parent/n,F/'include'/n) if z.is_file()),None)
  if q is None:missing.append(n)
  else:out.append(q)
 return tuple(out),tuple(missing)
P=F.resolve();target_abs={str((F/x).resolve()):x for x in targets};unresolved=collections.Counter()
for i,u in enumerate(units):
 root=(F/u['source']).resolve()
 if not root.is_file():continue
 seen=set();todo=[root];missing=set()
 while todo:
  p=todo.pop()
  if p in seen:continue
  seen.add(p);v,b=includes(str(p));todo.extend(v);missing.update(b)
 unresolved[i]=len(missing)
 for p in seen:
  key=target_abs.get(str(p))
  if key is not None:targets[key].setdefault('recipe_units',[]).append({'unit':i,'source':u['source'],'mapped_functions':[{'address':f['address'],'symbol':f.get('symbol')} for f in u['functions']],'unresolved_quoted_include_count':len(missing)})
for x in targets.values():x.setdefault('recipe_units',[])
out={'schema_version':1,'units_sha256':hashlib.sha256(units_raw).hexdigest(),'canonical_header_sha256':targets['include/TESContainer.h']['sha256'],'global_definition_count':len(targets),'definitions':list(targets.values()),'limitations':['Quoted-include lexical closure only; preprocessor conditions, macro includes and angle-bracket SDK includes are not evaluated.','Potential unit users are an over-approximation for inactive quoted includes and can miss macro-generated includes.','Class declarations and signature spelling do not establish ABI compatibility or emitted object equivalence.']};(H/'tescontainer_global_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print('definitions',len(targets),'recipe joins',sum(len(x['recipe_units']) for x in targets.values()))
