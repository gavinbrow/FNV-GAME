"""Prepare a private unified BGSBodyPart/BodyPartInfo header for units 620/621."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-shared-model-v2';O=M/'out/phase2-bgsbodypart-shared-body-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def one(s,a,b):
 if s.count(a)!=1:raise ValueError('ambiguous anchor '+a[:45])
 return s.replace(a,b,1)
def main():
 proof=json.loads((P/'manifest.json').read_text());a=(P/'620/bgsbodypart_decls.h').read_text().replace('\r\n','\n');b=(P/'621/bgsbodypartdata.h').read_text().replace('\r\n','\n')
 for n in ('620/bgsbodypart_decls.h','621/bgsbodypartdata.h','620/PSAModel_shared.h','621/PSAModel_shared.h'):
  if sha((P/n).read_bytes())!=proof['outputs'][n]:raise ValueError('input changed '+n)
 enum_start=b.index('enum IO_TASK_PRIORITY\n');enum_end=b.index('\n#include "PSAModel_shared.h"',enum_start);en=b[enum_start:enum_end]
 body_start=b.index('#pragma pack(push, 4)\nclass BodyPartInfo');body_end=b.index('#pragma pack(push, 4)\nclass BGSBodyPartData',body_start);classes=b[body_start:body_end]
 classes=one(classes,'class BodyPartInfo\n{\n  public:\n','class BodyPartInfo\n{\n  public:\n    BodyPartInfo();\n    void SwapEndianFields();\n    void Initialize();\n')
 classes=one(classes,'    void InitItem(TESForm* parent);','    void InitItem(TESForm* parent);\n    unsigned int FUN_005e3fc0();\n    void FUN_00994ef0(BGSImpactDataSet*);\n    void FUN_005e3d20();')
 shared='''#ifndef FNV_EXPERIMENT_SHARED_BGSPART_H
#define FNV_EXPERIMENT_SHARED_BGSPART_H
#include "PSAModel_shared.h"
#include "NiPoint3.h"
class TESForm;
class TESFile;
class BGSDebris;
class BGSExplosion;
class BGSImpactDataSet;
class QueuedFile;
'''+en+'\n'+classes+'\n#endif\n'
 s=a.index('enum IO_TASK_PRIORITY\n');e=a.index('\nclass ModelLoader',s);a=a[:s]+'#include "BGSBodyPart_shared.h"\nextern "C" NiPoint3 NiPoint3_ZERO;\n'+a[e:]
 s=a.index('class BGSBodyPart\n{');e=a.index('\nclass Queueable18',s);a=a[:s]+a[e:]
 s=b.index('enum IO_TASK_PRIORITY\n');e=b.index('\n#pragma pack(push, 4)\nclass BGSPreloadable',s);b=b[:s]+'#include "BGSBodyPart_shared.h"\n'+b[e:]
 s=b.index('#pragma pack(push, 4)\nclass BodyPartInfo');e=b.index('#pragma pack(push, 4)\nclass BGSBodyPartData',s);b=b[:s]+b[e:]
 O.mkdir(exist_ok=False)
 for n in ('620','621'):(O/n).mkdir()
 for n in ('620','621'):
  (O/n/'PSAModel_shared.h').write_bytes((P/n/'PSAModel_shared.h').read_bytes());(O/n/'BGSBodyPart_shared.h').write_bytes(shared.encode())
 (O/'620/bgsbodypart_decls.h').write_bytes(a.encode());(O/'621/bgsbodypartdata.h').write_bytes(b.encode())
 for n in ('620/bgsbodypart.cpp','621/bgsbodypartdata.cpp'):(O/n).write_bytes((P/n).read_bytes())
 outputs={str(p.relative_to(O)).replace('\\','/'):sha(p.read_bytes()) for n in ('620','621') for p in (O/n).iterdir()}
 report={'status':'private uncompiled full shared class hypothesis','outputs':outputs,'input_manifest_sha256':sha((P/'manifest.json').read_bytes()),
  'decisions':['typed BodyPartInfo pointers follow 621 declarations and 620 dynamic_cast assignment evidence','slot0 is virtual QueueResourceLoad as independently observed reference table',
   'BGSBodyPart destructor is nonvirtual as 621 source; separate unit620 FUN_005e3c60_cls destructor adapter is intentionally preserved',
   'NiPoint3 uses existing include/NiPoint3.h while NiPoint3_ZERO external source symbol is retained'],
  'required':['all15+10 functions, ctor and destructor EH','eight slots and full graph/weak aliases','pointer field type names require broader semantic proof','full link placement and runtime controls']}
 (O/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'shared_header_sha256':sha(shared.encode()),'outputs':len(outputs)}))
if __name__=='__main__':main()
