"""Prepare a private six-byte W-tail fixture; does not compile or alter selection."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;OUT=M/'out/phase2-hkp-hierarchy-v1';sys.path.insert(0,str(M));import gen_m3 as g


def main():
    plan=json.loads((OUT/'owner-split-proposal.json').read_text());src=OUT/'tail-fixture.cpp';meta=OUT/'tail-fixture.json'
    if src.exists() or meta.exists():raise FileExistsError('refusing overwrite')
    e=g.build_entries([plan['remaining_w']])[0];body=g.cpp([e]).encode('utf8')
    with src.open('xb') as f:f.write(body)
    record={'schema_version':1,'selection':plan['remaining_w'],'source_sha256':hashlib.sha256(body).hexdigest(),
            'expected_tail_relocation':plan['tail_relocation'],'status':'prepared only; no selection or byte coverage change'}
    with meta.open('x',encoding='utf8') as f:json.dump(record,f,indent=2)
    print(json.dumps({'source_sha256':record['source_sha256'],'status':record['status']}))

if __name__=='__main__':main()
