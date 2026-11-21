"""Freeze shared-model private mirrors; compilation remains a separate lane."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-psa-implicit-proposal';O=M/'out/phase2-bgsbodypart-shared-model-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 manifest=json.loads((O/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text())
 for n,v in manifest['outputs'].items():
  if sha((O/n).read_bytes())!=v:raise ValueError('mirror changed '+n)
 meta['native_source_sha256']=manifest['outputs']['620/bgsbodypart.cpp'];meta['candidate_header_sha256']=manifest['outputs']['620/bgsbodypart_decls.h'];meta['shared_header_sha256']=manifest['outputs']['620/PSAModel_shared.h'];meta['621_header_sha256']=manifest['outputs']['621/bgsbodypartdata.h']
 shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 driver=(P/'lane.py').read_text();changes=[('out/phase2-bgsbodypart-psa-implicit-proposal','out/phase2-bgsbodypart-shared-model-proposal'),("for k in ('621.cpp', '621.h'):","for k in ('621.cpp',):"),
 ("if digest(outputs['620.h']) != meta['candidate_header_sha256']:","if digest(outputs['621.h']) != meta['621_header_sha256']: raise ValueError('621 header changed')\n    for i in ('620','621'):\n        if digest(OUT/i/'PSAModel_shared.h') != meta['shared_header_sha256']: raise ValueError('shared model header changed')\n    if digest(outputs['620.h']) != meta['candidate_header_sha256']:"),
 ("meta = load()\n    for row in f['include_closure'].values():","meta = load()\n    for i in ('620','621'):\n        if digest(OUT/i/'PSAModel_shared.h') != meta['shared_header_sha256']: raise ValueError('shared model header changed')\n    for row in f['include_closure'].values():")]
 for a,b in changes:
  if driver.count(a)!=1:raise ValueError('driver anchor mismatch')
  driver=driver.replace(a,b,1)
 (O/'lane.py').write_text(driver,encoding='utf8');print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes())}))
if __name__=='__main__':main()
