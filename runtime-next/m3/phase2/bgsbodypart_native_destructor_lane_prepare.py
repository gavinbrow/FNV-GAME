"""Freeze private native destructor mirrors for an independently queued compiler."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-split-headers-proposal';O=M/'out/phase2-bgsbodypart-native-destructor-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((O/'manifest.json').read_text());old=json.loads((P/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text())
 for n,v in m['outputs'].items():
  if sha((O/n).read_bytes())!=v:raise ValueError('input changed '+n)
 meta['native_source_sha256']=m['outputs']['620/bgsbodypart.cpp'];meta['split_header_sha256']['BGSBodyPart_native.h']=m['outputs']['620/BGSBodyPart_native.h']
 if m['outputs']['621/BGSBodyPart_native.h']!=meta['split_header_sha256']['BGSBodyPart_native.h']:raise ValueError('class headers differ')
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8');shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 m['caller_source_sha256']=old['caller_source_sha256'];m['local_support_sha256']=old['local_support_sha256'];(O/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf8')
 driver=(P/'lane.py').read_text();changes=[('out/phase2-bgsbodypart-split-headers-proposal','out/phase2-bgsbodypart-native-destructor-proposal'),(sha((P/'manifest.json').read_bytes()),sha((O/'manifest.json').read_bytes())),
 ("if f['address']=='0x005e3be0': f['symbol']='??0TESModelPSA@@QAE@XZ'", "if f['address']=='0x005e3be0': f['symbol']='??0TESModelPSA@@QAE@XZ'\n                if f['address']=='0x005e3c60': f['symbol']='??1BGSBodyPart@@QAE@XZ'"),
 ("native=('??0TESModelPSA@@QAE@XZ' if f['address']=='0x005e3be0'", "native=('??1BGSBodyPart@@QAE@XZ' if f['address']=='0x005e3c60' else '??0TESModelPSA@@QAE@XZ' if f['address']=='0x005e3be0'")]
 for a,b in changes:
  if driver.count(a)!=1:raise ValueError('lane anchor mismatch')
  driver=driver.replace(a,b,1)
 (O/'lane.py').write_text(driver,encoding='utf8');print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes())}))
if __name__=='__main__':main()
