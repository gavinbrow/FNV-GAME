"""Capture W103 run evidence before the next compiler; fail closed on missing artifacts."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[3]; M=R/'runtime-next/m3'; P=M/'out/phase2-psa-w103-optin-package'; h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('run',choices=('positive','p2rv','p2rp','repeat'));ap.add_argument('--suite',choices=('v3','v4'),default='v3');a=ap.parse_args();d=M/('out/phase2-psa-w103-'+a.suite+'-'+a.run);e=d/'evidence';freeze=Path(str(d)+'-freeze');m=json.loads((P/'manifest.json').read_bytes());f=json.loads((freeze/'result.json').read_bytes());assert f['command_rc']==0 and f['input_freeze_passed'] and not f['final_digest_changes'] and not f['observed_metadata_changes'];before=json.loads((freeze/'inputs-before.json').read_bytes());sel=(P/'selection.json').resolve();assert before[str(sel)]['sha256']==m['selection_sha256'];assert h(R/'fnv_decomp/build/units.json')==m['recipe_sha256'];e.mkdir(exist_ok=True)
 files={}
 def copy(src,name):
  src=Path(src);dst=e/name
  if dst.exists():raise FileExistsError(dst)
  data=src.read_bytes();dst.write_bytes(data);files[name]={'source':str(src),'sha256':hashlib.sha256(data).hexdigest()}
 for name in ('m3_manifest.json','dv1_pieces.json','m3_data.obj','m3_data_1.obj','m3_data_2.obj','m3_data_3.obj'):copy(R/'runtime-next/layout-v2/snapshot/m3'/name,name)
 for name in ('m3_gen.log.json','dv1_log.json','skip_ranges.json'):copy(M/'gen'/name,name)
 for src,name in [(P/'selection.json','selection.json'),(M/'phase2/library_candidates.json','library_candidates.json'),(R/'fnv_decomp/build/units.json','units.json'),(R/'runtime-next/pinned-build/obj_v3/0620.obj','0620.obj'),(R/'runtime-next/pinned-build/logs/compile_v3.jsonl','compile_v3.jsonl'),(R/'runtime-next/pinned-build/logs/compile_v3_summary.json','compile_v3_summary.json'),(R/'runtime-next/data-v3/out/manifest.json','data-v3-manifest.json'),(R/'runtime-next/data-v3/symbolic.json','data-v3-symbolic.json'),(R/'runtime-next/layout-v2/build/image_G.json','layout-image.json'),(R/'runtime-next/layout-v2/build/map_G.npz','layout-map.npz')]:copy(src,name)
 log=json.loads((e/'m3_gen.log.json').read_bytes());assert log['selected']==log['kept']==8269 and not log['dropped'];dv=json.loads((e/'dv1_log.json').read_bytes());assert dv['library_opt_in']['selected']==405 and dv['library_opt_in']['bytes']==16730
 for name,digest in json.loads((d/'build-summary.json').read_bytes())['provenance']['data_v1_scratch_sha256'].items():assert h(e/'data-v1-scratch'/name)==digest
 (e/'capture-manifest.json').open('x').write(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':a.run,'frozen_selection_sha256':m['selection_sha256'],'files':files},indent=2));print('PASS frozen selection, 8269 retained, library405 and scratch hashes; archived',len(files))
if __name__=='__main__':main()
