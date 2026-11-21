"""Classify unmerged NiMemObject definition leads within affected closures."""
import collections,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';I=M/'out/phase2-nimemobject-coherent-kind-consumers.json';O=M/'out/phase2-nimemobject-coherent-kind-identity-blockers.json';sys.path.insert(0,str(H));import rtti_scoped_registry as scoped
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve evidence')
 x=json.loads(I.read_text());target=set(x['target_headers']);usage=collections.defaultdict(list)
 for u in x['units']:
  for v in u['declared_views']:
   if v['path'] not in target:usage[v['path']].append(u['unit'])
 rows=[]
 for rel in sorted(usage):
  p=F/rel;text=p.read_text(encoding='utf-8-sig',errors='replace');defs=scoped.scopes(text,'NiMemObject');rows.append({'path':rel,'source_sha256':sha(p),'consuming_units':usage[rel],'definitions':defs,'status':'unmerged; class identity, prior declarations and conditional branch activity unresolved'})
 O.write_text(json.dumps({'consumer_scope_sha256':sha(I),'paths':len(rows),'affected_units_with_extra_lexical_views':len({i for r in rows for i in r['consuming_units']}),'definitions':sum(len(r['definitions']) for r in rows),'categories':dict(collections.Counter(d['category'] for r in rows for d in r['definitions'])),'files':rows,'limits':['brace and preprocessor heuristic; zero definitions can mean forward declarations or unknown parsing','class/struct token equality does not prove ABI/ODR identity','conditional activation and first declaration require actual preprocessing','no unrelated views are modified']},indent=2));print('paths',len(rows),'definitions',sum(len(r['definitions']) for r in rows))
if __name__=='__main__':main()
