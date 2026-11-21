"""Bounded recipe-unit include census for private inline NiRef candidate."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';P=M/'out/phase2-nimem-next-source-composed';D=M/'out/phase2-niref-primary-inline-fixture';OUT=D/'quoted-consumer-scope.json';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 pp=P/'manifest.json';fp=D/'manifest.json';recipe=D/'units.original'
 if h(pp)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53' or h(fp)!='84940ae66aefdbb57cb06d7b7f6b051825e3d601766b3532149fc0e808eca89a' or h(recipe)!='13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876':raise ValueError('snapshot changed')
 m=j(pp);ov={}
 for k,v in m['source_payload_sha256'].items():
  p=P/'payload'/k
  if h(p)!=v:raise ValueError('parent payload changed')
  ov[k]=p.read_bytes()
 cand=dict(ov)
 for rel in ('include/NiRefObject.h','src/fallout_shared/animation.cpp','src/fallout_shared/animation_decls.h','src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp'):
  p=D/'overrides'/rel;data=p.read_bytes()
  if hashlib.sha256(data).hexdigest()!=j(fp)['modified_source_sha256'][rel]:raise ValueError('fixture payload changed')
  cand[rel]=data
 rows=[];errors=[];units=j(recipe)['units']
 for i,u in enumerate(units):
  try:
   a=core.walk(F,u['source'],ov);b=core.walk(F,u['source'],cand)
   changes=sorted(k for k in set(a['files'])|set(b['files']) if a['files'].get(k)!=b['files'].get(k))
   if changes:rows.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[])),'changed_files':changes,'original':a,'candidate':b})
  except Exception as e:errors.append({'unit':i,'source':u['source'],'error':type(e).__name__+': '+str(e)})
 out={'scope':'all 2995 recipe units, static quoted-project-include over-approximation; proposed private parent and inline candidate','parent_sha256':h(pp),'fixture_sha256':h(fp),'recipe_sha256':h(recipe),'units_scanned':len(units),'affected_units':len(rows),'affected_functions':sum(x['functions'] for x in rows),'affected_eh_tails':sum(x['eh_tails'] for x in rows),'errors':errors,'units':rows,'limitations':['quoted static closure is not preprocessor or compiler include-trace proof','every affected unit requires fresh source and behavior review','ODR, duplicate class views, COMDAT ownership and final image remain separate']}
 OUT.write_text(json.dumps(out,indent=2));print(json.dumps({'scope_sha256':h(OUT),'units':len(rows),'functions':out['affected_functions'],'errors':len(errors)}))
if __name__=='__main__':main()
