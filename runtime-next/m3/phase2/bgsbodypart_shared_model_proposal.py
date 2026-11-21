"""Prepare a private two-unit shared model header, without compilation."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-psa-slot7-typed-proposal';ROOT=M.parent.parent;F=ROOT/'fnv_decomp';O=M/'out/phase2-bgsbodypart-shared-model-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def one(s,a,b):
 if s.count(a)!=1:raise ValueError('ambiguous anchor: '+a[:45])
 return s.replace(a,b,1)
def main():
 manifest=json.loads((P/'manifest.json').read_text());h=(P/'bgsbodypart_decls.h').read_bytes();source=(P/'bgsbodypart.cpp').read_bytes()
 if sha(h)!=manifest['header_sha256'] or sha(source)!=manifest['source_sha256']:raise ValueError('typed input changed')
 h=h.decode('ascii').replace('\r\n','\n');start=h.index('template <class T> class BSStringT');end=h.index('\nclass ModelLoader',start)
 model=h[h.index('class TESModel : public BaseFormComponent',start):end]
 psa_start=h.index('class TESModelPSA : public TESModel');psa_end=h.index('\nextern "C" void* memset',psa_start)
 psa=h[psa_start:psa_end]
 shared='''#ifndef FNV_EXPERIMENT_SHARED_PSAMODEL_H
#define FNV_EXPERIMENT_SHARED_PSAMODEL_H
#include "BaseFormComponent.h"
class TESFile;
class BSFileEntry;
class TESModelTextureSwap;
#pragma pack(push, 4)
class FileEntryList
{
  public:
    unsigned char m_ucFileEntryCount, layoutPadding1[3];
    BSFileEntry** m_ppFileEntries;
};
'''+model+'\n'+psa+'''
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(FileEntryList) == 8);
FNV_STATIC_ASSERT(sizeof(TESModel) == 24);
FNV_STATIC_ASSERT(sizeof(TESModelPSA) == 24);
#endif
'''
 # Replace the local BSStringT, BFC, FileEntryList and TESModel together, using
 # the canonical BaseFormComponent/layout_support definitions in both units.
 h=h[:start]+'#include "PSAModel_shared.h"\n'+h[end:]
 psa_start=h.index('class TESModelPSA : public TESModel');psa_end=h.index('\nextern "C" void* memset',psa_start);h=h[:psa_start]+h[psa_end:]
 other=(F/'src/fallout_shared/bgsbodypartdata.h').read_text(encoding='utf8').replace('\r\n','\n')
 a=other.index('#pragma pack(push, 4)\nclass FileEntryList');b=other.index('#pragma pack(push, 4)\nclass BGSPreloadable',a)
 other=other[:a]+'#include "PSAModel_shared.h"\n'+other[b:]
 a=other.index('#pragma pack(push, 4)\nclass TESModelPSA');b=other.index('#pragma pack(push, 4)\nclass BodyPartInfo',a);other=other[:a]+other[b:]
 O.mkdir(exist_ok=False)
 for n in ('620','621'):(O/n).mkdir()
 for n,data in [('620/bgsbodypart.cpp',source),('620/bgsbodypart_decls.h',h.encode()),('621/bgsbodypartdata.cpp',(F/'src/fallout_shared/bgsbodypartdata.cpp').read_bytes()),('621/bgsbodypartdata.h',other.encode()),('620/PSAModel_shared.h',shared.encode()),('621/PSAModel_shared.h',shared.encode())]:(O/n).write_bytes(data)
 files={str(p.relative_to(O)).replace('\\','/'):sha(p.read_bytes()) for p in (O/'620').iterdir()};files.update({str(p.relative_to(O)).replace('\\','/'):sha(p.read_bytes()) for p in (O/'621').iterdir()})
 out={'status':'private uncompiled shared TESModel hypothesis; BGSBodyPart class remains separate', 'outputs':files,
      'source_callers':['src/fallout_shared/bipedanim_decls.h:368','src/fallout_shared/bipedanim.cpp:2101','src/fallout_shared/bipedanim.cpp:2421'],
      'reference_caller':'0x004aeff5 slot +0x1c; 0x004af00a ApplyTextureSwaps 0x0048afe0',
      'remaining':['slot7 nonconst source view differs from another const source view','BGSBodyPart declarations still require separate reconciliation',
       'layout_support types may expose collisions or code changes; compiler gate required','all native function, RTTI, EH, weak alias and table checks required']}
 (O/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'outputs':files}))
if __name__=='__main__':main()
