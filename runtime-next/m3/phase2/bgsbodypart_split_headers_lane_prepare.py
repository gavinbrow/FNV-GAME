"""Prepare private five-header lane from grouped prototype comparator."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-shared-body-proposal';O=M/'out/phase2-bgsbodypart-split-headers-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((O/'manifest.json').read_text());prior=json.loads((P/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text())
 for n,v in m['outputs'].items():
  if sha((O/n).read_bytes())!=v:raise ValueError('split mirror changed '+n)
 meta['candidate_header_sha256']=m['outputs']['620/bgsbodypart_decls.h'];meta['621_header_sha256']=m['outputs']['621/bgsbodypartdata.h']
 names=('FileEntryList_native.h','TESModel_native.h','TESModelPSA_native.h','BodyPartInfo_native.h','BGSBodyPart_native.h')
 for name in names:
  if m['outputs']['620/'+name]!=m['outputs']['621/'+name]:raise ValueError('split header mismatch')
 meta['split_header_sha256']={name:m['outputs']['620/'+name] for name in names}
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8');shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 m['caller_source_sha256']=prior['caller_source_sha256'];m['local_support_sha256']=prior['local_support_sha256'];(O/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf8');digest=sha((O/'manifest.json').read_bytes())
 driver=(P/'lane.py').read_text();changes=[('out/phase2-bgsbodypart-shared-body-proposal','out/phase2-bgsbodypart-split-headers-proposal'),(sha((P/'manifest.json').read_bytes()),digest),
 ("if digest(OUT/i/'PSAModel_shared.h') != meta['shared_header_sha256']: raise ValueError('shared model header changed')\n        if digest(OUT/i/'BGSBodyPart_shared.h') != meta['body_header_sha256']: raise ValueError('shared body header changed')",
  "for name, expected in meta['split_header_sha256'].items():\n            if digest(OUT/i/name) != expected: raise ValueError('split header changed: '+name)")]
 for a,b in changes:
  n=2 if a.startswith("if digest(OUT/i/") else 1
  if driver.count(a)!=n:raise ValueError('lane anchor mismatch')
  driver=driver.replace(a,b)
 (O/'lane.py').write_text(driver,encoding='utf8');print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes()),'manifest_sha256':digest}))
if __name__=='__main__':main()
