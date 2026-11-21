"""Split the private grouped prototype into one class per private header."""
import hashlib,json,re
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-shared-body-proposal';O=M/'out/phase2-bgsbodypart-split-headers-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def class_block(s,name):
 matches=list(re.finditer(r'\bclass\s+'+re.escape(name)+r'(?:\s*:[^\n]+)?\n\{',s))
 if len(matches)!=1:raise ValueError('ambiguous '+name)
 start=matches[0].start();end=s.index('\n};',start)+3
 return s[start:end]
def guard(name,includes,body,checks=''):
 g='FNV_EXPERIMENT_'+name.upper()+'_H'
 return '#ifndef '+g+'\n#define '+g+'\n'+includes+'\n#pragma pack(push, 4)\n'+body+'\n#pragma pack(pop)\n'+checks+'\n#endif\n'
def main():
 m=json.loads((P/'manifest.json').read_text())
 for name,digest in m['outputs'].items():
  if sha((P/name).read_bytes())!=digest:raise ValueError('prototype changed '+name)
 model=(P/'620/PSAModel_shared.h').read_text().replace('\r\n','\n');body=(P/'620/BGSBodyPart_shared.h').read_text().replace('\r\n','\n')
 en=body[body.index('enum IO_TASK_PRIORITY\n'):body.index('\n#pragma pack(push, 4)')]
 infostart=body.index('#pragma pack(push, 4)\nclass BodyPartInfo');partstart=body.index('#pragma pack(push, 4)\nclass BGSBodyPart',infostart)
 infochunk=body[infostart:partstart];infocheck=infochunk[infochunk.index('FNV_STATIC_ASSERT('):].strip()
 partchunk=body[partstart:body.rindex('\n#endif')];partcheck=partchunk[partchunk.index('FNV_STATIC_ASSERT('):].strip()
 headers={
  'FileEntryList_native.h':guard('fileentrylist','#include "layout_support.h"\nclass BSFileEntry;',class_block(model,'FileEntryList'),'FNV_STATIC_ASSERT(sizeof(FileEntryList) == 8);'),
  'TESModel_native.h':guard('tesmodel','#include "BaseFormComponent.h"\n#include "FileEntryList_native.h"\nclass TESFile;\nclass TESModelTextureSwap;',class_block(model,'TESModel'),'FNV_STATIC_ASSERT(sizeof(TESModel) == 24);'),
  'TESModelPSA_native.h':guard('tesmodelpsa','#include "TESModel_native.h"',class_block(model,'TESModelPSA'),'FNV_STATIC_ASSERT(sizeof(TESModelPSA) == 24);'),
  'BodyPartInfo_native.h':guard('bodypartinfo','#include "NiPoint3.h"\nclass BGSDebris;\nclass BGSExplosion;\nclass BGSImpactDataSet;',class_block(body,'BodyPartInfo'),infocheck),
  'BGSBodyPart_native.h':guard('bgsbodypart','#include "TESModelPSA_native.h"\n#include "BodyPartInfo_native.h"\nclass TESForm;\nclass TESFile;\nclass QueuedFile;\n'+en,class_block(body,'BGSBodyPart'),partcheck)}
 O.mkdir(exist_ok=False)
 for unit in ('620','621'):
  d=O/unit;d.mkdir()
  for name,content in headers.items():(d/name).write_bytes(content.encode())
  for name in (('bgsbodypart.cpp','bgsbodypart_decls.h') if unit=='620' else ('bgsbodypartdata.cpp','bgsbodypartdata.h')):
   data=(P/unit/name).read_bytes()
   if name.endswith('.h'):
    if data.count(b'#include "BGSBodyPart_shared.h"')!=1:raise ValueError('include anchor')
    data=data.replace(b'#include "BGSBodyPart_shared.h"',b'#include "BGSBodyPart_native.h"')
   (d/name).write_bytes(data)
 files={str(p.relative_to(O)).replace('\\','/'):sha(p.read_bytes()) for unit in ('620','621') for p in (O/unit).iterdir()}
 (O/'manifest.json').write_text(json.dumps({'status':'private uncompiled one-class-per-header prototype','input_manifest_sha256':sha((P/'manifest.json').read_bytes()),'outputs':files,'limitations':['class method names and slot7 const qualification remain unresolved','original source headers and recipes untouched','all 15+10 functions, include closure, graph, EH, weak and placement still require checks']},indent=2),encoding='utf8')
 print(json.dumps({'class_headers':len(headers),'files':len(files),'manifest_sha256':sha((O/'manifest.json').read_bytes())}))
if __name__=='__main__':main()
