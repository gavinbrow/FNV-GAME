"""Prepare all private NiRef inline cohort mirrors and frozen archives; no compiler."""
import copy,hashlib,json,shutil,sys,datetime
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';P=O/'phase2-nimem-next-source-composed';I=O/'phase2-niref-primary-inline-fixture';C=O/'phase2-nimem-calendar-binding-v1';D=O/'phase2-niref-inline-cohort';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core,tescontainer_install
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if D.exists():raise FileExistsError(D)
 pins={P/'manifest.json':'c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53',I/'manifest.json':'84940ae66aefdbb57cb06d7b7f6b051825e3d601766b3532149fc0e808eca89a',I/'quoted-consumer-scope.json':'5cbab83684e2aa43882809c1cd8e1dc278c24e4604baec0d88d93aa511649340',I/'source-atomic-owner-replay.json':'7f6f16230f85ec2f371fa7d0624b089df995167ee2f4561f9d0c81537a978555',C/'manifest.json':'1b15812e89bd4167f7a10032d20e775721f351473d47721cc12269169b68858e'}
 for p,v in pins.items():
  if h(p)!=v:raise ValueError('pinned evidence changed '+str(p))
 if h(F/'build/units.json')!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68':raise ValueError('live recipe differs')
 old=(P/'units.generated').read_bytes();cal=(C/'units.generated').read_bytes();a=json.loads(old);b=json.loads(cal)
 if h(P/'units.generated')!='13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876' or h(C/'units.original')!=h(P/'units.generated') or h(C/'units.generated')!='92b5d4058d196208672a6479f1d5e33414c2e022172fa3f3674d1d8e12ede9b8':raise ValueError('calendar lineage changed')
 if [i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]!=[368]:raise ValueError('calendar scope')
 x,y=a['units'][368],b['units'][368];name='?GetDayOfMonth@Calendar@@QAEHXZ'
 if any(x[k]!=y[k] for k in x if k!='symbols') or {k for k in x['symbols'].keys()|y['symbols'].keys() if x['symbols'].get(k)!=y['symbols'].get(k)}!={name} or y['symbols'][name]!='0x00867d60':raise ValueError('calendar non-binding edit')
 fixture=j(I/'manifest.json');oldfixture=j(I/'units.original')['units'];newfixture=j(I/'units.generated')['units']
 if a['units'][612]!=oldfixture[612] or a['units'][1503]!=oldfixture[1503]:raise ValueError('fixture parent differs')
 unit=copy.deepcopy(newfixture[612]);sym='?NiAtomicSubtract@@YAIAAI@Z'
 if sym in unit['symbols']:raise ValueError('helper unexpectedly bound')
 unit['symbols'][sym]='0x004019a0';new=tescontainer_install.replace_unit(cal,612,unit);newdoc=json.loads(new)
 if [i for i,(x,y) in enumerate(zip(b['units'],newdoc['units'])) if x!=y]!=[612] or any(unit[k]!=b['units'][612][k] for k in ('source','flags','compiler')):raise ValueError('candidate scope')
 scope=j(I/'quoted-consumer-scope.json')
 if scope['units_scanned']!=2995 or scope['affected_units']!=119 or scope['affected_functions']!=2080 or scope['errors']:raise ValueError('scope incomplete')
 parent=j(P/'manifest.json');ov={}
 for rel,digest in parent['source_payload_sha256'].items():
  p=P/'payload'/rel
  if h(p)!=digest:raise ValueError('parent source changed')
  ov[rel]=p.read_bytes()
 candidate=dict(ov)
 for rel,digest in fixture['modified_source_sha256'].items():
  p=I/'overrides'/rel
  if h(p)!=digest:raise ValueError('fixture source changed')
  candidate[rel]=p.read_bytes()
 archives=[(O/'phase2-nimem-operators-825d-production-archive','25e303cfcef7555e59437901586e1085cec1df91b6487d9acb1bee6e12a30bdc'),(O/'phase2-nimem-kind-production-archive','62a67ba7b952e0b04f52c019652e035214dee8ffb425daedfbbf099ebf0967e5')];idx=[]
 for p,digest in archives:
  if h(p/'manifest.json')!=digest:raise ValueError('production archive changed')
  idx.append({x['unit']:x for x in j(p/'manifest.json')['objects']})
 # Capture only pinned archive objects, never mutable obj_v3; unit612 is 6757 archive with unchanged 825d recipe.
 old6757=j(O/'phase2-eh-1047-ownership-archive/units.json')['units'];live=j(F/'build/units.json')['units']
 if old6757[612]!=live[612]:raise ValueError('612 recipe changed')
 D.mkdir();(D/'units.original').write_bytes(cal);(D/'units.generated').write_bytes(new);rows=[]
 for entry in scope['units']:
  i=entry['unit'];u=b['units'][i];source=u['source'];orig=core.walk(F,source,ov);cand=core.walk(F,source,candidate)
  if orig!=entry['original'] or cand!=entry['candidate'] or any(u[k]!=entry[k] for k in ('source','flags','compiler')):raise ValueError('scope/mirror drift '+str(i))
  archive,record=(archives[1][0],idx[1][i]) if i==612 else (archives[0][0],idx[0][i]);p=archive/('%04d.obj'%i)
  if h(p)!=record['sha256']:raise ValueError('production object changed')
  d=D/('unit-%04d'%i);d.mkdir();shutil.copyfile(p,d/'production.obj')
  for tag,g,overrides in (('original',orig,ov),('candidate',cand,candidate)):
   for rel,digest in g['files'].items():
    data=overrides[rel] if rel in overrides else (F/rel).read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('mirror file changed '+rel)
    q=d/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  row={'unit':i,'source':source,'flags':u['flags'],'compiler':u['compiler'],'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[])),'original':orig,'candidate':cand,'production_object_sha256':h(d/'production.obj'),'archive_manifest_sha256':archives[1 if i==612 else 0][1],'production_scope':'6757 unchanged-unit archive' if i==612 else '825d archive; not private 38-source parent'}
  (d/'mirror-manifest.json').write_text(json.dumps(row,indent=2));rows.append({'unit':i,'mirror_manifest_sha256':h(d/'mirror-manifest.json'),'production_object_sha256':h(d/'production.obj')})
 result={'status':'PRIVATE prepared; no compiler run','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':{str(p.relative_to(R)).replace('\\','/'):v for p,v in pins.items()},'parent_recipe_sha256':h(C/'units.generated'),'candidate_recipe_sha256':h(D/'units.generated'),'units':rows,'scope_count':119,'function_count':2080,'limits':['production archives are 825d or unchanged 6757 unit612, not private parent compilation','both 119 parent/candidate contexts require fresh compile and include trace','612 G46 and1503 G44 provider conflict remains unresolved; no weak binding or forced provider','source, link/image and runtime gates remain']}
 (D/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({'manifest_sha256':h(D/'manifest.json'),'candidate_recipe_sha256':h(D/'units.generated'),'units':len(rows)}))
if __name__=='__main__':main()
