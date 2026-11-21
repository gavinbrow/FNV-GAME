"""Stage one class-definition core and three context-preserving wrappers."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-baseformcomponent-core';A=M/'out/phase2-baseformcomponent-audit-v2.json';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';sys.path.insert(0,str(H));import rtti_class_registry as registry
WRAPPERS=['include/BaseFormComponent.h','src/fallout_shared/BaseFormComponent.h','src/fallout_shared/tesresponse_component.h'];CORE='include/BaseFormComponent_core.h';INCLUDE=re.compile(rb'^[ \t]*#[ \t]*include[ \t]*(["<])([^">\r\n]+)[">]',re.M)
def sha(b):return hashlib.sha256(b).hexdigest()
def block(data):
 text=data.decode('utf-8-sig');clean=registry.clean(text);found=[x for x in registry.DECL.finditer(clean) if x.group(1)=='class' and x.group(2)=='BaseFormComponent']
 if len(found)!=1:raise ValueError('expected one class definition')
 m=found[0];pos=m.end();depth=1
 while depth and pos<len(clean):depth+=(clean[pos]=='{')-(clean[pos]=='}');pos+=1
 if depth or text[pos:pos+1]!=';':raise ValueError('unterminated class')
 return text[m.start():pos+1]
def walk(root,source,overrides):
 files={};edges=[];missing=[];visited=set()
 def visit(rel,parents):
  key=(rel,tuple(parents))
  if key in visited or rel in parents:return
  visited.add(key);p=root/rel
  if rel in overrides:data=overrides[rel]
  elif p.is_file():data=p.read_bytes()
  else:raise ValueError('missing input '+rel)
  files[rel]=sha(data)
  for style,raw in INCLUDE.findall(data):
   name=raw.decode('ascii',errors='replace')
   if style==b'<':missing.append({'from':rel,'name':name,'kind':'system-angle'});continue
   target=None
   for directory in [Path(rel).parent]+[Path(x).parent for x in reversed(parents)]+[Path('include')]:
    q=(root/directory/name).resolve()
    try:relative=q.relative_to(root.resolve()).as_posix()
    except ValueError:continue
    if relative in overrides or q.is_file():target=relative;break
   if target is None:missing.append({'from':rel,'name':name,'kind':'quoted-unresolved'});continue
   edges.append({'from':rel,'name':name,'resolved':target});visit(target,parents+[rel])
 visit(source,[])
 return {'files':dict(sorted(files.items())),'edges':edges,'unresolved':missing}
def main():
 units=(F/'build/units.json').read_bytes()
 if sha(units)!=D:raise ValueError('recipe changed')
 audit=json.loads(A.read_bytes())
 if audit['units_sha256']!=D:raise ValueError('scope audit is stale')
 rows={x['path']:x for x in audit['definitions']};
 for name in WRAPPERS:
  x=rows[name]
  if not x['canonical_body_exact'] or sha((F/name).read_bytes())!=x['sha256']:raise ValueError('wrapper evidence changed '+name)
 canonical=block((F/WRAPPERS[0]).read_bytes());normalized=' '.join(canonical.split())
 for name in WRAPPERS:
  if ' '.join(block((F/name).read_bytes()).split())!=normalized:raise ValueError('wrapper class body differs '+name)
 if (F/CORE).exists():raise ValueError('new core target already exists')
 core=('#ifndef FNV_BASEFORMCOMPONENT_CORE_H\n#define FNV_BASEFORMCOMPONENT_CORE_H\n'+canonical.replace('\r\n','\n')+'\n#endif\n').encode();overrides={CORE:core}
 for name in WRAPPERS:
  old=(F/name).read_bytes().decode('utf-8-sig');b=block((F/name).read_bytes())
  if old.count(b)!=1:raise ValueError('ambiguous wrapper body')
  new=old.replace(b,'#include "BaseFormComponent_core.h"',1).encode();overrides[name]=new
  # Every original byte outside the class block remains exactly in place.
  if new.decode()!=old.replace(b,'#include "BaseFormComponent_core.h"',1):raise ValueError('unrelated wrapper edit')
 wanted=set()
 for name in WRAPPERS:wanted.update(x['unit'] for x in rows[name]['consumer_units'])
 if len(wanted)!=241:raise ValueError('affected lexical cohort changed')
 unitdoc=json.loads(units)['units'];units_out=[];other_global={x['path'] for x in audit['definitions'] if x['path'] not in WRAPPERS}
 for i in sorted(wanted):
  u=unitdoc[i];base=walk(F,u['source'],{});candidate=walk(F,u['source'],overrides)
  if not any(x in base['files'] for x in WRAPPERS):raise ValueError('affected unit lacks wrapper '+str(i))
  if CORE not in candidate['files']:raise ValueError('candidate missing core '+str(i))
  if set(candidate['files'])!=set(base['files'])|{CORE}:raise ValueError('unexpected closure change '+str(i))
  changed=[k for k in base['files'] if base['files'][k]!=candidate['files'][k]]
  if any(k not in WRAPPERS for k in changed):raise ValueError('non-wrapper content changed '+str(i))
  units_out.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':[{'address':f['address'],'symbol':f['symbol'],'size':f['size']} for f in u['functions']],'eh_tails':u.get('eh_tails',[]),'original':base,'candidate':candidate,'other_lexical_global_bfc_views':sorted(set(base['files'])&other_global)})
 if O.exists():raise FileExistsError('refusing overwrite')
 O.mkdir();files=[]
 for i,name in enumerate(WRAPPERS):
  (O/('%d.original'%i)).write_bytes((F/name).read_bytes());(O/('%d.generated'%i)).write_bytes(overrides[name]);files.append({'path':name,'old_sha256':sha((F/name).read_bytes()),'new_sha256':sha(overrides[name]),'original':'%d.original'%i,'generated':'%d.generated'%i})
 (O/'3.generated').write_bytes(core);files.append({'path':CORE,'old_sha256':None,'new_sha256':sha(core),'original':None,'generated':'3.generated'})
 report={'schema_version':1,'base_units_sha256':D,'scope_audit_sha256':sha(A.read_bytes()),'files':files,'affected_unit_count':len(units_out),'mapped_function_count':sum(len(x['functions']) for x in units_out),'units':units_out,'limits':['syntactic quoted-include closures overapproximate inactive branches and do not expand macros','system include resolution and actual preprocessor guards require compiler /showIncludes traces','wrapper-local pack and size assertions are preserved, so divergent ambient packing remains unresolved','additional global and namespace views are not merged','all affected functions, EH tails, production literal labels and full image gates are required before integration']}
 (O/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps({'files':len(files),'affected_units':len(units_out),'mapped_functions':report['mapped_function_count'],'other_bfc_view_units':sum(bool(x['other_lexical_global_bfc_views']) for x in units_out)}))
if __name__=='__main__':main()
