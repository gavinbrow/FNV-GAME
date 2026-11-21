"""Freeze actual successful compiler cohort and audit one weak primary; read-only."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;RN=M.parent;sys.path.insert(0,str(H));import vtable_search_library as V
OUT=M/'out/phase2-vtable-bgse-search';O=RN/'pinned-build/obj_v3';L=RN/'pinned-build/logs/compile_v3.jsonl';U=P/'fnv_decomp/build/units.json';TARGET='??_EBGSEncounterZone@@UAEPAXI@Z'; SUB=M/'out/phase2-bgsencounterzone-six-override/0002.combined.obj';LIB=P/'FNV/tools/vc2008/VC/lib'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 lh=digest(L);uh=digest(U); rows=[json.loads(x) for x in L.read_text().splitlines() if x.strip()];units=json.loads(U.read_bytes())['units']
 ids=[r['index'] for r in rows];
 if len(ids)!=len(set(ids)) or set(ids)!=set(range(len(units))):raise ValueError('compile log does not cover recipe')
 for r in rows:
  if r['source']!=units[r['index']]['source']:raise ValueError('compile log source mismatch')
 good=sorted(r['index'] for r in rows if r['status']=='ok' and r['rc']==0);skipped=[{'index':r['index'],'status':r['status'],'rc':r['rc']} for r in rows if r['index'] not in set(good)]
 if 2 not in good:raise ValueError('candidate unit missing')
 actual=[(i,O/('%04d.obj'%i)) for i in good]
 if any(not p.is_file() for _,p in actual):raise ValueError('successful unit object missing')
 old={i:digest(p) for i,p in actual};sh=digest(SUB);objects=[(i,SUB if i==2 else p,sh if i==2 else old[i]) for i,p in actual]
 names=['libcmt.lib','libcpmt.lib'];ars=[(n,LIB/n,digest(LIB/n)) for n in names];result=V.prove_absent(TARGET,ars,names,objects,good)
 if digest(L)!=lh or digest(U)!=uh or digest(SUB)!=sh or any(digest(p)!=old[i] for i,p in actual) or any(digest(p)!=h for _,p,h in ars):raise ValueError('cohort changed during scan')
 OUT.mkdir(parents=False,exist_ok=False);manifest={'scope':'successful compile-v3 recipe cohort; unit2 replaced by independent BGSE six-override object; excludes failed/filtered units and other possible linker inputs','primary':TARGET,'recipe_sha256':uh,'compile_log_sha256':lh,'successful_unit_count':len(good),'total_recipe_units':len(units),'excluded':skipped,'substitution':{'index':2,'original_object_sha256':old[2],'replacement_sha256':sh},'objects':[{'index':i,'sha256':old[i]} for i in good],'archives':[{'name':n,'sha256':h} for n,p,h in ars],'result':result,'limitations':['conditional on captured compile log and supplied CRT archive list','no proof of all possible game/linker providers, archive extraction behavior, fallback placement, or full ABI']}
 (OUT/'cohort-proof.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'successful':len(good),'excluded':len(skipped),'archive_count':len(ars),'strong_primary_count':result['strong_primary_count']}))
if __name__=='__main__':main()
