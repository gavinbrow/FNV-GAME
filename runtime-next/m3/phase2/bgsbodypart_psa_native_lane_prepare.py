"""Stage a native-constructor lane from the previously reviewed private driver."""
import hashlib,json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent; M=H.parent
OLD=M/'out/phase2-bgsbodypart-psa-proposal'; NEW=M/'out/phase2-bgsbodypart-psa-native-proposal'

def main():
    manifest=json.loads((NEW/'manifest.json').read_text())
    source=(NEW/'bgsbodypart.cpp').read_bytes();header=(NEW/'bgsbodypart_decls.h').read_bytes()
    if hashlib.sha256(source).hexdigest()!=manifest['output_sha256']['source'] or hashlib.sha256(header).hexdigest()!=manifest['output_sha256']['header']:raise ValueError('native proposal changed')
    meta=json.loads((OLD/'manifest.json').read_text())
    for name in ('620','621'):(NEW/name).mkdir(exist_ok=False)
    (NEW/'620/bgsbodypart.cpp').write_bytes(source)
    (NEW/'620/bgsbodypart_decls.h').write_bytes(header)
    shutil.copyfile(OLD/'621/bgsbodypartdata.cpp',NEW/'621/bgsbodypartdata.cpp')
    shutil.copyfile(OLD/'621/bgsbodypartdata.h',NEW/'621/bgsbodypartdata.h')
    meta['native_source_sha256']=hashlib.sha256(source).hexdigest()
    (NEW/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    driver=(H/'bgsbodypart_psa_lane.py').read_text(encoding='utf8')
    replacements=[("H = Path(__file__).resolve().parent","H = Path(__file__).resolve().parents[2] / 'phase2'"),
       ("out/phase2-bgsbodypart-psa-proposal","out/phase2-bgsbodypart-psa-native-proposal"),
       ("OUT / 'manifest.json'","OUT / 'lane-manifest.json'"),
       ("OUT/'manifest.json'","OUT/'lane-manifest.json'"),
       ("for k in ('620.cpp', '621.cpp', '621.h'):","for k in ('621.cpp', '621.h'):"),
       ("if digest(outputs['620.h']) != meta['candidate_header_sha256']:","if digest(outputs['620.cpp']) != meta['native_source_sha256']: raise ValueError('native source changed')\n    if digest(outputs['620.h']) != meta['candidate_header_sha256']:"),
       ("a,ar=relocated(cs['original'],f['symbol'],f['size'],{})\n                b,br=relocated(cs['mirror'],f['symbol'],f['size'],aliases)",
        "a,ar=relocated(cs['original'],f['symbol'],f['size'],{})\n                native='??0TESModelPSA@@QAE@XZ' if index==620 and f['address']=='0x005e3be0' else f['symbol']\n                b,br=relocated(cs['mirror'],native,f['size'],aliases)"),
       ("mapped=copy.deepcopy(unit)\n        for native,old in aliases.items():", 
        "mapped=copy.deepcopy(unit)\n        if index==620:\n            for f in mapped['functions']:\n                if f['address']=='0x005e3be0': f['symbol']='??0TESModelPSA@@QAE@XZ'\n        for native,old in aliases.items():")]
    for old,new in replacements:
        if driver.count(old)!=(2 if old=="OUT/'manifest.json'" else 1):raise ValueError('driver template changed: '+old)
        driver=driver.replace(old,new)
    (NEW/'lane.py').write_text(driver,encoding='utf8')
    print(json.dumps({'lane':str(NEW/'lane.py'),'lane_sha256':hashlib.sha256(driver.encode()).hexdigest()}))
if __name__=='__main__':main()
