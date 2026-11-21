"""Read-only scoped BaseFormComponent declaration and consumer audit."""
import collections,functools,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';sys.path.insert(0,str(H));import rtti_class_registry as reg
S=M/'out/phase2-scoped-registry/BaseFormComponent-scopes-phase2.json';O=M/'out/phase2-baseformcomponent-audit-v2.json';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 raw=(F/'build/units.json').read_bytes()
 if sha(raw)!=D:raise ValueError('recipe changed')
 units=json.loads(raw)['units'];scope=json.loads(S.read_text());defs=[x for x in scope['definitions'] if x['category']=='global'];canonical=next(x for x in defs if x['path']=='include/BaseFormComponent.h');group=canonical['lexical_token_sha256'];targets={}
 for x in defs:
  path=x['path'];data=(F/path).read_bytes();lines=data.decode('utf-8-sig',errors='replace').splitlines();line=x['line'];prior='\n'.join(lines[:line-1]);pragmas=re.findall(r'^\s*#\s*pragma\s+pack\s*\(([^)]*)\)',prior,re.M);depth=[]
  for p in pragmas:
   p=' '.join(p.split())
   if p.startswith('push'):depth.append(p)
   elif p.startswith('pop') and depth:depth.pop()
   else:depth.append('untracked:'+p)
  after='\n'.join(lines[line-1:line+20]);size=bool(re.search(r'(?:FNV_STATIC_ASSERT|typedef\s+char\s+\w+).*?sizeof\s*\(\s*BaseFormComponent\s*\).*?(?:0x0*4|\b4\b)',after,re.S));quoted=re.findall(rb'^[ \t]*#[ \t]*include[ \t]*"([^"\r\n]+)"',data,re.M)
  cleaned=reg.clean(data.decode('utf-8-sig',errors='replace'));matches=[z for z in reg.DECL.finditer(cleaned) if z.group(2)=='BaseFormComponent' and cleaned.count('\n',0,z.start())+1==line]
  if len(matches)!=1:raise ValueError('ambiguous declaration '+path)
  z=matches[0];pos=z.end();level=1
  while level and pos<len(cleaned):level+=(cleaned[pos]=='{')-(cleaned[pos]=='}');pos+=1
  if level:raise ValueError('unbalanced class '+path)
  body=cleaned[z.end():pos-1];exact=x['lexical_token_sha256']==group
  category='canonical-four-method-body' if exact else 'pure-virtual-or-abstract' if re.search(r'=\s*0\s*;',body) else 'declares-destructor' if re.search(r'~\s*BaseFormComponent\s*\(',body) else 'declares-constructor' if re.search(r'\bBaseFormComponent\s*\(',body) else 'renamed-method-view' if 'InitializeComponent' in body else 'other-different-view'
  targets[path]={'path':path,'line':line,'sha256':sha(data),'keyword':x['keyword'],'classification':category,'canonical_body_exact':exact,'active_pack_pragmas':depth,'ambient_pack_unknown':not depth,'nearby_size_4_assert':size,'quoted_includes':[z.decode('ascii',errors='replace') for z in quoted],'conditional_directives':x['conditional_directives'],'consumer_units':[]}
 INC=re.compile(rb'^[ \t]*#[ \t]*include[ \t]*"([^"\r\n]+)"',re.M)
 @functools.lru_cache(None)
 def includes(path):
  p=Path(path);deps=[];un=[]
  for raw in INC.findall(p.read_bytes()):
   n=raw.decode('ascii',errors='replace');q=next((z.resolve() for z in (p.parent/n,F/'include'/n) if z.is_file()),None)
   if q is None:un.append(n)
   else:deps.append(q)
  return deps,un
 target_abs={(F/k).resolve():k for k in targets};collisions=[]
 for i,u in enumerate(units):
  todo=[(F/u['source']).resolve()];seen=set();missing=set()
  while todo:
   p=todo.pop()
   if p in seen or not p.is_file():continue
   seen.add(p);d,m=includes(str(p));todo.extend(d);missing.update(m)
  found=[target_abs[p] for p in seen if p in target_abs]
  for name in found:targets[name]['consumer_units'].append({'unit':i,'source':u['source'],'functions':len(u['functions']),'quoted_missing':sorted(missing)})
  if len(found)>1:collisions.append({'unit':i,'source':u['source'],'definitions':sorted(found),'note':'lexical include overlap; guards/branches may prevent actual duplicate definitions'})
 exact=[v for v in targets.values() if v['canonical_body_exact']]
 output={'schema_version':2,'units_sha256':sha(raw),'scoped_registry_sha256':sha(S.read_bytes()),'global_definitions':len(defs),'namespace_definitions':sum(x['category']=='namespace' for x in scope['definitions']),'canonical_body_exact_count':len(exact),'classification_counts':dict(collections.Counter(x['classification'] for x in targets.values())),'canonical_token_sha256':group,'definitions':list(targets.values()),'lexical_overlap_consumers':collisions,'limits':['categories use first applicable lexical signal and are not mutually exclusive semantically','exact body tokens mean method signatures/access/class-key match; surrounding pack and preprocessing remain separate','quoted include closure is an over-approximation and does not evaluate macros/conditionals or system includes','absence of a nearby assertion does not disprove four-byte layout','self-contained header requires auditing transitive users of layout_support, not only BaseFormComponent uses','not proof of native identity, ABI, ODR or object equivalence']}
 O.write_text(json.dumps(output,indent=2));print(json.dumps({'global':len(defs),'namespace':output['namespace_definitions'],'exact_body':len(exact),'overlap_units':len(collisions)}))
if __name__=='__main__':main()
