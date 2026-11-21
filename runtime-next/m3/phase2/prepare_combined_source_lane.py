"""Prepare seven private combined mirrors and preserve current production objects; no compile."""
import hashlib,json,shutil,sys,datetime
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';S=M/'out/phase2-source-integration6757';O=M/'out/phase2-source-integration6757-lane';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError(O)
 proposal=S/'manifest.json';pin='81547b70a3471f423953800494083534349dab885afba119b525b6e522b37a41'
 if sha(proposal)!=pin:raise ValueError('proposal changed')
 m=json.loads(proposal.read_text());raw=F/'build/units.json'
 if sha(raw)!=m['base_recipe_sha256'] or sha(S/'units.generated')!=m['candidate_recipe_sha256']:raise ValueError('recipe changed')
 overrides={k:(S/'payload'/k).read_bytes() for k in m['source_files']}
 for name,row in m['source_files'].items():
  p=F/name
  if (sha(p) if p.exists() else None)!=row['preimage'] or hashlib.sha256(overrides[name]).hexdigest()!=row['candidate']:raise ValueError('source input changed '+name)
 for name,digest in m['evidence_sha256'].items():
  if sha(R/name)!=digest:raise ValueError('proposal evidence changed '+name)
 units=json.loads(raw.read_text())['units'];O.mkdir();created=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for i in (253,370,425,620,621,2909,2910):
  dst=O/str(i);dst.mkdir();saved=m['closure'][str(i)];source=units[i]['source']
  for tag,ov in (('original',{}),('candidate',overrides)):
   actual=core.walk(F,source,ov)
   if actual!=saved[tag]:raise ValueError('include graph changed '+str(i)+' '+tag)
   for rel,digest in actual['files'].items():
    data=ov.get(rel,(F/rel).read_bytes() if (F/rel).exists() else None)
    if data is None or hashlib.sha256(data).hexdigest()!=digest:raise ValueError('closure data changed')
    p=dst/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  production=R/'runtime-next/pinned-build/obj_v3'/('%04d.obj'%i)
  if not production.is_file():raise FileNotFoundError(production)
  shutil.copyfile(production,dst/'production-baseline.obj')
  if sha(production)!=sha(dst/'production-baseline.obj'):raise ValueError('object changed while copying')
  mm={'source':source,'original_inputs':saved['original']['files'],'original':saved['original'],'candidate':saved['candidate'],'proposal_sha256':pin,'recipe_sha256':m['base_recipe_sha256'],'candidate_recipe_sha256':m['candidate_recipe_sha256'],'production_object_sha256':sha(production),'production_source':str(production),'production_mtime_ns':production.stat().st_mtime_ns,'capture_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  (dst/'mirror-manifest.json').write_text(json.dumps(mm,indent=2),encoding='utf8');created.append({'unit':i,'manifest_sha256':sha(dst/'mirror-manifest.json'),'production_object_sha256':mm['production_object_sha256']})
 summary={'capture_started_utc':start,'capture_finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'proposal_sha256':pin,'captured':created,'provenance_limit':'current production object files copied with observed mtime/hash; establish accepted-build identity separately before treating them as accepted objects','compile_not_run':True}
 (O/'capture.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':main()
