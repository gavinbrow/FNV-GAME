"""Prepare isolated production-path mirror trees; never compile or touch shared inputs."""
import argparse,copy,hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';AUDIT=M/'out/phase2-tescontainer-production-labels'
OLD='a7470e7f0f8c59ea4b201a1e1f72bb552d3bbd00596db2fdc4911b94b6c18a56';NEW='e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576'
INCLUDE=re.compile(rb'^[ \t]*#[ \t]*include[ \t]*(["<])([^">\r\n]+)[">]',re.M)
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 if sha(old)!=OLD or sha(new)!=NEW or current!=new:raise ValueError('unreviewed recipe transition')
 a=json.loads(old);b=json.loads(new)
 if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a if k!='units') or len(a['units'])!=len(b['units']):raise ValueError('recipe schema changed')
 if [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]!=[980]:raise ValueError('unexpected changed units')
 u=copy.deepcopy(a['units'][980]);changes=[('$SG4917','$SG4918','0x0101c178'),('$SG4919','$SG4920','0x01012058'),('$SG4925','$SG4926','0x0101c140'),('$SG4927','$SG4928','0x0101c140')]
 for prev,post,va in changes:
  if u['symbols'].pop(prev,None)!=va or post in u['symbols']:raise ValueError('unexpected literal key transition')
  u['symbols'][post]=va
 if u!=b['units'][980]:raise ValueError('unit980 transition differs')
 return b

def logical(path):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] not in ('src','include'):raise ValueError('invalid logical path')
 return p.as_posix()

def walk(root,source,overrides):
 """Enumerate syntactic quoted includes, preserving nested parent search order."""
 edges=[];missing=[];files={};seen=set()
 def visit(name,parents):
  name=logical(name);key=(name,tuple(parents))
  if key in seen:return
  if name in parents:return
  seen.add(key);p=root/name
  if not p.is_file():raise ValueError('missing logical source '+name)
  data=overrides.get(name,p.read_bytes());files[name]=sha(data)
  for style,n in INCLUDE.findall(data):
   inc=n.decode('ascii');line=data[:data.find(style+n)].count(b'\n')+1 if style+n in data else None
   if style==b'<':missing.append({'from':name,'include':inc,'kind':'angle-system-or-unresolved'});continue
   dirs=[Path(name).parent]+[Path(x).parent for x in reversed(parents)]+[Path('include')];target=None
   for d in dirs:
    candidate=(root/d/inc).resolve()
    try:r=candidate.relative_to(root.resolve()).as_posix();logical(r)
    except ValueError:continue
    if r in overrides or candidate.is_file():target=r;break
   if target is None:missing.append({'from':name,'include':inc,'kind':'quoted-system-or-unresolved'});continue
   edges.append({'from':name,'include':inc,'resolved':target});visit(target,parents+[name])
 visit(source,[])
 return {'files':files,'edges':edges,'unresolved':missing}

def prepare(source, overrides, out):
 source=logical(source);unitdata=transition((AUDIT/'units.original').read_bytes(),(AUDIT/'units.generated').read_bytes(),(F/'build/units.json').read_bytes())
 if not any(u['source']==source for u in unitdata['units']):raise ValueError('source not in recipe')
 if out.exists():raise FileExistsError('refusing overwrite')
 try:out.resolve().relative_to((M/'out').resolve())
 except ValueError:raise ValueError('output must be private m3/out')
 if not out.name.startswith('phase2-'):raise ValueError('private output name required')
 for k in overrides:logical(k)
 for k in overrides:
  if not (F/k).is_file():raise ValueError('override destination not an existing project file '+k)
 base=walk(F,source,{});candidate=walk(F,source,overrides)
 if set(overrides)-set(candidate['files']):raise ValueError('override not reachable from candidate source')
 out.mkdir(parents=False)
 for tag,graph in [('original',base),('candidate',candidate)]:
  target=out/tag
  for path,digest in graph['files'].items():
   b=overrides[path] if tag=='candidate' and path in overrides else (F/path).read_bytes()
   if sha(b)!=digest:raise ValueError('input changed while reading')
   dst=target/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
 meta={'schema_version':1,'source':source,'units_sha256':NEW,'reviewed_units_sha256':OLD,'production_include_order':['/I<mirror>/include'],'overrides':{k:sha(v) for k,v in overrides.items()},'original_inputs':{k:sha((F/k).read_bytes()) for k in sorted(set(base['files'])|set(candidate['files']))},'original':base,'candidate':candidate,'limitations':['syntactic include scan does not evaluate preprocessor or macro includes','angle and unresolved quoted includes require compiler/SDK validation','MSVC search includes enclosing headers; compiler include trace must validate actual resolution','private-object literal labels are not accepted without actual production-object comparison']}
 (out/'mirror-manifest.json').write_text(json.dumps(meta,indent=2));return meta

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--override',action='append',default=[]);a=p.parse_args();overrides={}
 for item in a.override:
  if '=' not in item:raise ValueError('override syntax logical=private_file')
  k,v=item.split('=',1);k=logical(k)
  if k in overrides:raise ValueError('duplicate override')
  overrides[k]=Path(v).read_bytes()
 m=prepare(a.source,overrides,a.out);print(json.dumps({'source':m['source'],'original_files':len(m['original']['files']),'candidate_files':len(m['candidate']['files']),'original_unresolved':len(m['original']['unresolved']),'candidate_unresolved':len(m['candidate']['unresolved'])}))
if __name__=='__main__':main()
