"""Create private implicit-destructor compile mirrors without invoking compiler."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent; P=M/'out/phase2-bgsbodypart-psa-hierarchy-proposal'; O=M/'out/phase2-bgsbodypart-psa-implicit-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 proposal=json.loads((O/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text());src=(O/'bgsbodypart.cpp').read_bytes();hdr=(O/'bgsbodypart_decls.h').read_bytes()
 if sha(src)!=proposal['source_sha256'] or sha(hdr)!=proposal['header_sha256']:raise ValueError('proposal changed')
 for n in ('620','621'):(O/n).mkdir(exist_ok=False)
 (O/'620/bgsbodypart.cpp').write_bytes(src);(O/'620/bgsbodypart_decls.h').write_bytes(hdr)
 for n in ('bgsbodypartdata.cpp','bgsbodypartdata.h'):shutil.copyfile(P/'621'/n,O/'621'/n)
 shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 meta['native_source_sha256']=sha(src);meta['candidate_header_sha256']=sha(hdr)
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 driver=(P/'lane.py').read_text();a='out/phase2-bgsbodypart-psa-hierarchy-proposal';b='out/phase2-bgsbodypart-psa-implicit-proposal'
 if driver.count(a)!=1:raise ValueError('driver changed')
 (O/'lane.py').write_text(driver.replace(a,b),encoding='utf8')
 print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes()),'source_sha256':sha(src),'header_sha256':sha(hdr)}))
if __name__=='__main__':main()
