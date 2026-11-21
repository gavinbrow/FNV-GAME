"""Stage canonical TESModelPSA native owner in private unit-2909 mirrors."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-bgsbodypart-native-destructor-rebase6757';O=M/'out/phase2-psa-owner-2909';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core,tescontainer_install
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SRC='src/tesobjecttree.cpp';HDR='src/TESObjectTREE.h';NATIVE='??1TESModelPSA@@UAE@XZ';OLD='?FUN_0051b950@FUN_0051b950_shell@@QAEXXZ'
def sha(x):return hashlib.sha256(x).hexdigest()
def replace_class(text,anchor,include):
 anchor=anchor.replace('\n','\r\n') if '\r\n' in text else anchor
 if text.count(anchor)!=1:raise ValueError('ambiguous class '+anchor)
 start=text.index(anchor);p=text.index('{',start)+1;depth=1
 while depth and p<len(text):depth+=(text[p]=='{')-(text[p]=='}');p+=1
 if depth or text[p:p+1]!=';':raise ValueError('class boundary differs')
 return text[:start]+include+text[p+1:]
def main():
 if O.exists():raise FileExistsError('preserve private output')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);u=doc['units'][2909]
 if sha(raw)!=BASE or u['source']!=SRC or len(u['functions'])!=45 or doc['units'][2910]['source']!='src/tesobjecttree_o2_variant.cpp':raise ValueError('recipe scope differs')
 owner=[f for f in u['functions'] if f['address']=='0x0051b950']
 if len(owner)!=1 or owner[0]['symbol']!=OLD or owner[0]['size']!=19 or u['symbols'].get('??1TESModel@@QAE@XZ')!='0x00489070':raise ValueError('owner changed')
 b=(F/HDR).read_bytes();t=b.decode('utf-8-sig');t=replace_class(t,'class FileEntryList\n{','#include "FileEntryList_native.h"');t=replace_class(t,'class TESModel : public BaseFormComponent\n{','#include "TESModel_native.h"');newhdr=t.encode()
 old=(F/SRC).read_bytes();txt=old.decode('utf-8-sig');block='struct FUN_0051b950_shell : TESModel\n{\n    void FUN_0051b950();\n};\n\n// @fnv 0x0051b950\nvoid FUN_0051b950_shell::FUN_0051b950()\n{\n    TESModel::~TESModel();\n}'
 nl='\r\n' if '\r\n' in txt else '\n';block=block.replace('\n',nl)
 if txt.count(block)!=1 or txt.count('#include "TESObjectTREE.h"')!=1:raise ValueError('source owner differs')
 txt=txt.replace('#include "TESObjectTREE.h"','#include "TESObjectTREE.h"'+nl+'#include "TESModelPSA_native.h"',1).replace(block,'// @fnv 0x0051b950'+nl+'TESModelPSA::~TESModelPSA()'+nl+'{}',1);newsrc=txt.encode()
 ov={HDR:newhdr,SRC:newsrc}
 for n in ('FileEntryList_native.h','TESModel_native.h','TESModelPSA_native.h'):
  data=(D/'620'/n).read_bytes()
  if n=='TESModelPSA_native.h':
   anchor=b'    TESModelPSA();'
   if data.count(anchor)!=1:raise ValueError('PSA header changed')
   data=data.replace(anchor,anchor+b'\n    virtual ~TESModelPSA();',1)
  rel='include/'+n
  if (F/rel).exists():raise ValueError('native header already exists')
  ov[rel]=data
 candidate=copy.deepcopy(u);next(x for x in candidate['functions'] if x['address']=='0x0051b950')['symbol']=NATIVE;candidate['symbols']['??1TESModel@@UAE@XZ']='0x00489070';newrecipe=tescontainer_install.replace_unit(raw,2909,candidate);decoded=json.loads(newrecipe)
 if [i for i,(a,b) in enumerate(zip(doc['units'],decoded['units'])) if a!=b]!=[2909] or any(doc[k]!=decoded[k] for k in doc if k!='units'):raise ValueError('recipe difference outside owner')
 mirrors={}
 for i in (2909,2910):
  source=doc['units'][i]['source'];a=core.walk(F,source,{});b=core.walk(F,source,ov);mirrors[str(i)]={'source':source,'original':a,'candidate':b,'functions':len(doc['units'][i]['functions']),'eh_tails':len(doc['units'][i].get('eh_tails',[]))}
  if HDR not in a['files'] or 'include/TESModel_native.h' not in b['files']:raise ValueError('TESModel context not reached')
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(newrecipe)
 for rel,data in ov.items():
  q=O/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 for i,m in mirrors.items():
  for tag in ('original','candidate'):
   for rel,digest in m[tag]['files'].items():
    data=ov[rel] if tag=='candidate' and rel in ov else (F/rel).read_bytes()
    if sha(data)!=digest:raise ValueError('file changed')
    q=O/i/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 for i,m in mirrors.items():
  mm={'schema_version':1,'source':m['source'],'units_sha256':sha(raw),'original_inputs':m['original']['files'],'original':m['original'],'candidate':m['candidate'],'production_include_order':['/I<mirror>/include'],'limits':['TESModel native virtual contract changes previous TESObjectTREE view: ABI/ODR and all affected code must be independently proved','explicit PSA destructor changes earlier 620/621 candidate: fresh paired object/RTTI/COMDAT proof required','private source and recipe proposal only; no live writes or compiler execution']}
  (O/i/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 result={'base_recipe_sha256':sha(raw),'candidate_recipe_sha256':sha(newrecipe),'parent_bgs_manifest_sha256':sha((D/'manifest.json').read_bytes()),'owner_unit':2909,'owner_address':'0x0051b950','source_symbol':OLD,'candidate_symbol':NATIVE,'owner_size':19,'files':{k:sha(v) for k,v in ov.items()},'mirrors':mirrors,'dependent_units':[620,621,2909,2910],'limits':['TESModel native virtual contract changes previous TESObjectTREE view: ABI/ODR and all affected code must be independently proved','explicit PSA destructor changes earlier 620/621 candidate: fresh paired object/RTTI/COMDAT proof required','private source and recipe proposal only; no live writes or compiler execution']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({'owner_functions':45,'variant_functions':1,'owner_eh_tails':5,'mirror_files':[len(mirrors[str(i)]['candidate']['files']) for i in (2909,2910)]}))
if __name__=='__main__':main()
