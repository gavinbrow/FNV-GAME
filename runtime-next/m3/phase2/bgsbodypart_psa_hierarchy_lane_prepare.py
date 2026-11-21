"""Prepare private hierarchy mirrors and lane; compiler is invoked separately."""
import hashlib,json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';N=M/'out/phase2-bgsbodypart-psa-native-proposal';O=M/'out/phase2-bgsbodypart-psa-hierarchy-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 meta=json.loads((N/'lane-manifest.json').read_text());m=json.loads((O/'manifest.json').read_text());header=(O/'bgsbodypart_decls.h').read_bytes()
 if sha(header)!=m['output_header_sha256']:raise ValueError('hierarchy header changed')
 units=(F/'build/units.json').read_bytes();u=json.loads(units)['units']
 for i,source,count in ((620,'src/fallout_shared/bgsbodypart.cpp',15),(621,'src/fallout_shared/bgsbodypartdata.cpp',10)):
  if u[i]['source']!=source or len(u[i]['functions'])!=count:raise ValueError('unit mismatch')
 meta['input_sha256']['units']=sha(units);meta['candidate_header_sha256']=sha(header)
 # Explicit native destructor triggers an emitted deleting destructor for review.
 source=(O/'bgsbodypart.cpp').read_bytes()+b'\r\nTESModelPSA::~TESModelPSA() {}\r\n'
 meta['native_source_sha256']=sha(source)
 for n in ('620','621'):(O/n).mkdir(exist_ok=False)
 (O/'620/bgsbodypart.cpp').write_bytes(source);(O/'620/bgsbodypart_decls.h').write_bytes(header)
 for n in ('bgsbodypartdata.cpp','bgsbodypartdata.h'):shutil.copyfile(N/'621'/n,O/'621'/n)
 shutil.copyfile(N/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 driver=(N/'lane.py').read_text();a='out/phase2-bgsbodypart-psa-native-proposal';b='out/phase2-bgsbodypart-psa-hierarchy-proposal'
 if driver.count(a)!=1:raise ValueError('lane path mismatch')
 (O/'lane.py').write_text(driver.replace(a,b),encoding='utf8')
 print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes()),'source_sha256':sha(source),'units_sha256':sha(units)}))
if __name__=='__main__':main()
