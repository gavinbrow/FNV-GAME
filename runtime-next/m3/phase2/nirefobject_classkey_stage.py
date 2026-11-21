"""Stage a private NiMemObject class-key test for two existing NiRefObject consumers."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-nirefobject-classkey-fixture';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';FILES=('include/layout_support.h','include/NiMemObject.h')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior fixture')
 raw=(F/'build/units.json').read_bytes();u=json.loads(raw)['units']
 if sha(raw)!=BASE:raise ValueError('recipe changed')
 old={x:(F/x).read_bytes() for x in FILES};ov={}
 for path,needle,replacement in ((FILES[0],b'class NiMemObject;',b'struct NiMemObject;'),(FILES[1],b'class NiMemObject\r\n',b'struct NiMemObject\r\n')):
  b=old[path]
  if needle not in b and path==FILES[1]:needle=b'class NiMemObject\n';replacement=b'struct NiMemObject\n'
  if b.count(needle)!=1:raise ValueError('class key occurrence differs '+path)
  ov[path]=b.replace(needle,replacement,1)
 units=[]
 for i in (1484,1503):
  q=u[i];a=core.walk(F,q['source'],{});b=core.walk(F,q['source'],ov)
  if not set(FILES)<=set(a['files']) or set(a['files'])!=set(b['files']):raise ValueError('scope differs')
  units.append({'unit':i,'source':q['source'],'compiler':q['compiler'],'flags':q['flags'],'functions':len(q['functions']),'eh_tails':len(q.get('eh_tails',[])),'original':a,'candidate':b})
 O.mkdir()
 for rel in FILES:
  for tag,data in [('original',old[rel]),('candidate',ov[rel])]:
   p=O/'payload'/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 for x in units:
  d=O/str(x['unit'])
  for tag in ('original','candidate'):
   for rel,digest in x[tag]['files'].items():
    b=ov[rel] if tag=='candidate' and rel in ov else (F/rel).read_bytes()
    if sha(b)!=digest:raise ValueError('input changed')
    p=d/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  mm={'schema_version':1,'source':x['source'],'units_sha256':BASE,'original_inputs':x['original']['files'],'original':x['original'],'candidate':x['candidate'],'production_include_order':['/I<mirror>/include'],'limits':['two-unit private class-key hypothesis; no class ownership or ODR claim']};(d/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 out={'recipe_sha256':BASE,'changes':[{'path':x,'before_sha256':sha(old[x]),'after_sha256':sha(ov[x])} for x in FILES],'units':units,'scope':'two-unit private experiment only; public include and forward-declaration contexts are not exhaustively enumerated','limits':['layout_support.h is broadly shared; full affected closure and all preceding declarations must be inventoried before any integration','check /showIncludes and class key order, exact RTTI graph/PMD and all functions/EH','no forced emission, compiler, live source or recipe changes']}
 (O/'manifest.json').write_text(json.dumps(out,indent=2));print(json.dumps({'units':[1484,1503],'functions':sum(x['functions'] for x in units),'files':len(FILES)}))
if __name__=='__main__':main()
