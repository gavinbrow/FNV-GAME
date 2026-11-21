"""Prepare an uncompiled implicit PSA destructor experiment."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent; P=M/'out/phase2-bgsbodypart-psa-hierarchy-proposal'; O=M/'out/phase2-bgsbodypart-psa-implicit-proposal'
def main():
 h=(P/'620/bgsbodypart_decls.h').read_bytes();s=(P/'620/bgsbodypart.cpp').read_bytes()
 old=b'    virtual ~TESModelPSA();';body=b'\r\nTESModelPSA::~TESModelPSA() {}\r\n'
 if h.count(old)!=1 or s.count(body)!=1:raise ValueError('unexpected hierarchy input')
 h=h.replace(old,b'',1);s=s.replace(body,b'\r\n',1)
 O.mkdir(exist_ok=False);(O/'bgsbodypart.cpp').write_bytes(s);(O/'bgsbodypart_decls.h').write_bytes(h)
 sha=lambda b:hashlib.sha256(b).hexdigest()
 (O/'manifest.json').write_text(json.dumps({'status':'private uncompiled implicit destructor hypothesis','input_source_sha256':sha((P/'620/bgsbodypart.cpp').read_bytes()),'input_header_sha256':sha((P/'620/bgsbodypart_decls.h').read_bytes()),'source_sha256':sha(s),'header_sha256':sha(h),'requirements':['compare actual destructor and deleting wrapper against reference','inspect weak aliases, RTTI, all 15+10 mapped functions and EH','do not conflate declaration with source recovery']},indent=2),encoding='utf8')
 print(json.dumps({'source_sha256':sha(s),'header_sha256':sha(h)}))
if __name__=='__main__':main()
