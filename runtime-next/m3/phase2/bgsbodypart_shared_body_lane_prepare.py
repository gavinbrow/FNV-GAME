"""Prepare private shared BGSBodyPart lane; no compiler invocation."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-shared-model-v2';O=M/'out/phase2-bgsbodypart-shared-body-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((O/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text())
 for n,d in m['outputs'].items():
  if sha((O/n).read_bytes())!=d:raise ValueError('mirror input changed: '+n)
 meta['candidate_header_sha256']=m['outputs']['620/bgsbodypart_decls.h'];meta['621_header_sha256']=m['outputs']['621/bgsbodypartdata.h'];meta['body_header_sha256']=m['outputs']['620/BGSBodyPart_shared.h']
 if m['outputs']['621/BGSBodyPart_shared.h']!=meta['body_header_sha256']:raise ValueError('shared body headers differ')
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8');shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 # Preserve caller evidence and layout support provenance from the reviewed v2.
 prior=json.loads((P/'manifest.json').read_text());m['caller_source_sha256']=prior['caller_source_sha256'];m['local_support_sha256']=prior['local_support_sha256']
 (O/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf8');provenance_sha=sha((O/'manifest.json').read_bytes())
 driver=(P/'lane.py').read_text();a='out/phase2-bgsbodypart-shared-model-v2';b='out/phase2-bgsbodypart-shared-body-proposal'
 changes=[(a,b),('bcbdceaf8933016e23aa0a85e1016b3194920fb239e4f830cc152a0b9e708e80',provenance_sha),
  ("if digest(OUT/i/'PSAModel_shared.h') != meta['shared_header_sha256']: raise ValueError('shared model header changed')", "if digest(OUT/i/'PSAModel_shared.h') != meta['shared_header_sha256']: raise ValueError('shared model header changed')\n        if digest(OUT/i/'BGSBodyPart_shared.h') != meta['body_header_sha256']: raise ValueError('shared body header changed')"),
  ("if f['address']=='0x005e3be0': f['symbol']='??0TESModelPSA@@QAE@XZ'", "if f['address']=='0x005e3be0': f['symbol']='??0TESModelPSA@@QAE@XZ'\n                if f['address']=='0x005e45e0': f['symbol']='?QueueResourceLoad@BGSBodyPart@@UAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z'"),
  ("native='??0TESModelPSA@@QAE@XZ' if index==620 and f['address']=='0x005e3be0' else f['symbol']", "native=('??0TESModelPSA@@QAE@XZ' if f['address']=='0x005e3be0' else '?QueueResourceLoad@BGSBodyPart@@UAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z' if f['address']=='0x005e45e0' else f['symbol']) if index==620 else f['symbol']")]
 for a,b in changes:
  n=2 if a.startswith("if digest(OUT/i/'PSAModel_shared.h')") else 1
  if driver.count(a)!=n:raise ValueError('driver anchor count '+str(driver.count(a)))
  driver=driver.replace(a,b)
 (O/'lane.py').write_text(driver,encoding='utf8');print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes()),'manifest_sha256':provenance_sha}))
if __name__=='__main__':main()
