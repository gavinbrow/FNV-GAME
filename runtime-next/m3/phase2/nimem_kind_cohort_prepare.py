"""Create minimal source mirrors for one pinned NiMemObject kind cohort unit."""
import argparse,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';K=M/'out/phase2-nimemobject-coherent-kind';S=M/'out/phase2-nimemobject-coherent-kind-consumers.json';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';KH='5e4610cd17372885861964b9e25238925b5d69f8c0f2287065107fee7ac445d6';SH='c45dad435c9c172c149afa1fb4054ae5844f59299e1a1dcb6ffaa1e3ca2bc67f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True,type=int);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 if sha(K/'manifest.json')!=KH or sha(S)!=SH or sha(F/'build/units.json')!=BASE:raise ValueError('pinned manifest, scope, or recipe differs')
 k=json.loads((K/'manifest.json').read_text());scope=json.loads(S.read_text());u=json.loads((F/'build/units.json').read_text())['units'];row=next((z for z in scope['units'] if z['unit']==a.unit),None)
 if row is None or u[a.unit]['source']!=row['source'] or len(u[a.unit]['functions'])!=row['functions'] or len(u[a.unit].get('eh_tails',[]))!=row['eh_tails']:raise ValueError('unit scope differs')
 overrides={}
 for x in k['files']:
  before=F/x['path'];after=K/x['generated']
  if sha(before)!=x['before_sha256'] or sha(after)!=x['after_sha256']:raise ValueError('payload preimage changed '+x['path'])
  overrides[x['path']]=after.read_bytes()
 original=core.walk(F,row['source'],{});candidate=core.walk(F,row['source'],overrides)
 if original['files']!=row['quoted_project_closure'] or set(original['files'])!=set(candidate['files']):raise ValueError('source closure differs')
 changed=[q for q in original['files'] if original['files'][q]!=candidate['files'][q]]
 if not changed or any(q not in overrides for q in changed):raise ValueError('unexpected candidate closure delta')
 out.mkdir(parents=True)
 for tag,graph in (('original',original),('candidate',candidate)):
  for rel,digest in graph['files'].items():
   data=overrides[rel] if tag=='candidate' and rel in overrides else (F/rel).read_bytes()
   if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('file changed '+rel)
   p=out/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 m={'source':row['source'],'unit':a.unit,'units_sha256':BASE,'scope_sha256':SH,'kind_manifest_sha256':KH,'original_inputs':original['files'],'original':original,'candidate':candidate,'changed_headers':changed,'production_include_order':['/I<mirror>/include'],'limitations':['quoted include graph does not evaluate guard conditions or first declaration','preprocessed type records and compiler warnings must be inspected']}
 (out/'mirror-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'unit':a.unit,'files':len(original['files']),'changed_headers':len(changed)}))
if __name__=='__main__':main()
