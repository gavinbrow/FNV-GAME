"""Correct TESFile collision in private shared model mirrors; never compiles."""
import hashlib,json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';P=M/'out/phase2-bgsbodypart-shared-model-proposal';O=M/'out/phase2-bgsbodypart-shared-model-v2'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 manifest=json.loads((P/'manifest.json').read_text());meta=json.loads((P/'lane-manifest.json').read_text());units=(F/'build/units.json').read_bytes();u=json.loads(units)['units']
 for i,src,count in ((620,'src/fallout_shared/bgsbodypart.cpp',15),(621,'src/fallout_shared/bgsbodypartdata.cpp',10)):
  if u[i]['source']!=src or len(u[i]['functions'])!=count:raise ValueError('unit shape changed')
 for name,digest in manifest['outputs'].items():
  if sha((P/name).read_bytes())!=digest:raise ValueError('prior mirror changed '+name)
 h=(P/'620/bgsbodypart_decls.h').read_bytes()
 old=b'class TESFile\n{\n  public:\n    unsigned int GetChunkID();\n    unsigned int GetChunkSize();\n    bool NextChunk();\n    bool GetChunkData(void*, unsigned int);\n    bool IsEndianConversionRequired();\n};\n'
 if h.count(old)!=1:raise ValueError('TESFile declaration mismatch')
 h=h.replace(old,b'// TESFile definition and chunk methods come from the shared layout_support.h.\n',1)
 O.mkdir(exist_ok=False)
 for name in ('620','621'):(O/name).mkdir()
 for name in manifest['outputs']:
  target=O/name;target.write_bytes(h if name=='620/bgsbodypart_decls.h' else (P/name).read_bytes())
 meta['input_sha256']['units']=sha(units);meta['candidate_header_sha256']=sha(h)
 for key,src in (('620.cpp','src/fallout_shared/bgsbodypart.cpp'),('620.h','src/fallout_shared/bgsbodypart_decls.h'),('621.cpp','src/fallout_shared/bgsbodypartdata.cpp'),('621.h','src/fallout_shared/bgsbodypartdata.h')):
  if sha((F/src).read_bytes())!=meta['input_sha256'][key]:raise ValueError('live source changed '+src)
 (O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 driver=(P/'lane.py').read_text();oldpath='out/phase2-bgsbodypart-shared-model-proposal';newpath='out/phase2-bgsbodypart-shared-model-v2'
 if driver.count(oldpath)!=1:raise ValueError('lane path mismatch')
 (O/'lane.py').write_text(driver.replace(oldpath,newpath),encoding='utf8')
 provenance={'description':'v2 replaces unit620 local TESFile definition with existing fallout_shared/layout_support.h guarded TESFile definition; retains one shared model header',
    'units_sha256':sha(units),'outputs':{name:sha((O/name).read_bytes()) for name in manifest['outputs']},
    'caller_source_sha256':{p:sha((F/p).read_bytes()) for p in ('src/fallout_shared/bipedanim.cpp','src/fallout_shared/bipedanim_decls.h')},
    'local_support_sha256':sha((F/'src/fallout_shared/layout_support.h').read_bytes()),
    'qualification':'slot7 TESModelTextureSwap* nonconst follows bipedanim source; separate const source view remains unresolved',
    'limitations':['uncompiled; actual include trace, all 15+10 functions, EH/RTTI/eight slots/weak aliases still require proof','BGSBodyPart declarations not unified']}
 (O/'manifest.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
 print(json.dumps({'units_sha256':sha(units),'driver_sha256':sha((O/'lane.py').read_bytes()),'header_sha256':sha(h)}))
if __name__=='__main__':main()
