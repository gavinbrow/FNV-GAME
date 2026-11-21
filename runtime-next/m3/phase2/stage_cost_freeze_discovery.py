"""Prepare and inspect the minimal private production-helper watch fix."""
import hashlib,importlib.util,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;SRC=H/'run_frozen.py';O=M/'out/phase2-cost-freeze-discovery-v2'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 old=SRC.read_bytes();anchor=b"files = [name for name in files if name in ('library_overlay.py', 'run_frozen.py')]"
 replacement=b"files = [name for name in files if name in ('library_overlay.py', 'cost245_records.py', 'run_frozen.py')]"
 if old.count(anchor)!=1:raise ValueError('watch-list anchor mismatch')
 old_comment=b'# explicitly imported library hook and this wrapper are inputs.';new_comment=b'# explicitly imported production helpers and this wrapper are inputs.'
 if old.count(old_comment)!=1:raise ValueError('watch-list comment anchor mismatch')
 new=old.replace(anchor,replacement,1).replace(old_comment,new_comment,1)
 O.mkdir(exist_ok=False);(O/'run_frozen.original.py').write_bytes(old);(O/'run_frozen.candidate.py').write_bytes(new)
 spec=importlib.util.spec_from_file_location('private_cost_freeze',O/'run_frozen.candidate.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
 paths=module.paths_to_watch(ROOT,[]);wanted=[H/n for n in ('library_overlay.py','cost245_records.py','run_frozen.py')];excluded=[H/n for n in ('next_data_artifact_audit.py','next_data_library_replay.py','stage_cost_freeze_discovery.py')]
 if any(x.resolve() not in paths for x in wanted) or any(x.resolve() in paths for x in excluded):raise ValueError('actual watch membership failed')
 manifest={'scope':'private freeze-discovery proposal; no live edit','path':'runtime-next/m3/phase2/run_frozen.py','old_sha256':sha(old),'new_sha256':sha(new),'old_payload':'run_frozen.original.py','new_payload':'run_frozen.candidate.py',
  'actual_membership':{'watched_count':len(paths),'included':[str(x.relative_to(ROOT)) for x in wanted],'excluded':[str(x.relative_to(ROOT)) for x in excluded]},
  'limitations':['v3 used an explicit helper watch; this candidate has not been installed','fresh default gate must validate automatic catalog and full inputs']}
 (O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print(json.dumps({'old_sha256':sha(old),'new_sha256':sha(new),'watch_count':len(paths),'manifest_sha256':sha((O/'manifest.json').read_bytes())}))
if __name__=='__main__':main()
