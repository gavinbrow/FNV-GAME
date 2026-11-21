"""Snapshot actual V7/M3 provider artifacts for two exact deleting-dtor primaries."""
import json,hashlib,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;sys.path.insert(0,str(H));import vtable_search_library as S
OUT=M/'out/phase2-vtable-provider-closure.json';U=P/'fnv_decomp/build/units.json';L=RN/'pinned-build/logs/compile_v3.jsonl';V=RN/'build-v7';G=M/'gen';LIB=P/'FNV/tools/vc2008/VC/lib'
TARGETS=['??_EBGSEncounterZone@@UAEPAXI@Z','??_ETESModelPSA@@UAEPAXI@Z']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 manifests=[U,L,V/'ehvariants_w2.json',V/'contrib_pieces.json',G/'m3_manifest.json']; before={str(x):sha(x) for x in manifests};units=json.loads(U.read_bytes())['units'];log=[json.loads(x) for x in L.read_text().splitlines() if x.strip()]
 if len(log)!=len(units) or {x['index'] for x in log}!=set(range(len(units))):raise ValueError('incomplete compile cohort')
 paths=[];excluded=[]
 for row in log:
  i=row['index']
  if row['source']!=units[i]['source']:raise ValueError('source mismatch')
  if row['status']=='ok' and row['rc']==0:paths.append(('recipe',str(i),RN/'pinned-build/obj_v3'/('%04d.obj'%i)))
  else:excluded.append({'unit':i,'status':row['status'],'rc':row['rc']})
 variants=json.loads((V/'ehvariants_w2.json').read_bytes())
 for x in variants:paths.append(('eh_variant',str(x['unit']),V/x['obj']))
 c=json.loads((V/'contrib_pieces.json').read_bytes());ids=sorted({x['target_id'] for k in ('pieces','eh') for x in c[k]})
 if any(Path(i).name!=i for i in ids):raise ValueError('invalid contribution id')
 paths.extend(('contribution',i,V/'obj'/(i+'.obj')) for i in ids)
 gm=json.loads((G/'m3_manifest.json').read_bytes());groups=sorted({x.get('obj',0) for x in gm['entries']})
 for i in groups:paths.append(('m3_generated',str(i),G/('m3_data.obj' if i==0 else 'm3_data_%d.obj'%i)))
 names=['libcmt.lib','libcpmt.lib'];archives=[(n,LIB/n) for n in names];missing=[{'kind':k,'id':i} for k,i,p in paths if not p.is_file()];present=[(k,i,p,sha(p)) for k,i,p in paths if p.is_file()];archives_sha=[(n,p,sha(p)) for n,p in archives];hits={n:[] for n in TARGETS};errors=[]
 for k,i,p,h in present:
  try:
   data=p.read_bytes()
   if hashlib.sha256(data).hexdigest()!=h:raise ValueError('object changed')
   for n in TARGETS:
    for hit in S.scan_coff(data,n.encode()):hits[n].append({'kind':k,'id':i,'symbol_record':hit})
  except Exception as e:errors.append({'kind':k,'id':i,'error':type(e).__name__+': '+str(e)})
 for name,p,h in archives_sha:
  data=p.read_bytes();S.validate_archive_indexes(data)
  for ix,(member,blob) in enumerate(S.archive_members(data)):
   if member in ('/','//','/SYM64/'):continue
   for n in TARGETS:
    for hit in S.scan_coff(blob,n.encode()):hits[n].append({'kind':'archive','archive':name,'member_index':ix,'symbol_record':hit})
 if any(sha(p)!=h for k,i,p,h in present) or any(sha(p)!=h for n,p,h in archives_sha) or any(sha(Path(p))!=h for p,h in before.items()):raise ValueError('inputs changed during scan')
 counts={k:sum(x[0]==k for x in present) for k in ('recipe','eh_variant','contribution','m3_generated')}
 out={'scope':'snapshot of compiled successful recipe objects, configured EH variant, contribution-object artifacts referenced by verified pieces, generated M3 partitions and two V7 CRT archives; exact primary names only','targets':TARGETS,'counts':counts,'excluded_recipe':excluded,'missing':missing,'scan_errors':errors,'strong_definitions':hits,'manifests_sha256':before,'objects':[{'kind':k,'id':i,'sha256':h} for k,i,p,h in present],'archives':[{'name':n,'sha256':h} for n,p,h in archives_sha],'assumptions':['default FNV_EH_VARIANTS=1; archived build environment must establish actual toggle','contribution pieces are data snapshots; source objects may not be current without provenance binding','M3 partitions only those in current generated manifest','V7 overlay/ICF maps and import rules can supply a name without an object definition','object-provider closure is not equivalent to MSVC archive-search semantics'],'status':'complete snapshot' if not missing and not excluded and not errors else 'incomplete snapshot'}
 OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'counts':counts,'missing':len(missing),'excluded':len(excluded),'errors':len(errors),'hits':{n:len(v) for n,v in hits.items()}}))
if __name__=='__main__':main()
