"""Stage native NiRef destructor/wrapper hypothesis above a private 38-source proposal."""
import copy,hashlib,json,sys
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';P=O/'phase2-nimem-next-source-composed';T=O/'phase2-niref-primary-owner-fixture';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core,tescontainer_install
PIN='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';RPIN='13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876'
h=lambda b:hashlib.sha256(b).hexdigest()
def readtext(data):return data.decode('utf-8-sig')
def replace_once(text,old,new):
 old=old.replace('\n','\r\n') if '\r\n' in text else old;new=new.replace('\n','\r\n') if '\r\n' in text else new
 if text.count(old)!=1:raise ValueError('source anchor not unique')
 return text.replace(old,new,1)
def main():
 if T.exists():raise FileExistsError(T)
 if h((P/'manifest.json').read_bytes())!=PIN or h((P/'units.generated').read_bytes())!=RPIN or h((F/'build/units.json').read_bytes())!=BASE:raise ValueError('baseline changed')
 m=json.loads((P/'manifest.json').read_bytes());ov={}
 for rel,digest in m['source_payload_sha256'].items():
  data=(P/'payload'/rel).read_bytes()
  if h(data)!=digest:raise ValueError('parent source differs '+rel)
  ov[rel]=data
 def baseline(rel):return ov[rel] if rel in ov else (F/rel).read_bytes()
 decl='src/fallout_shared/animation_decls.h';src='src/fallout_shared/animation.cpp';opt='src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp'
 x=readtext(baseline(decl));old='''class NiMemObject\n{\n  public:\n    static void* operator new(unsigned int);\n    static void operator delete(void*, unsigned int);\n};''';x=replace_once(x,old,'#include "../../include/NiRefObject.h"');ov[decl]=x.encode()
 x=readtext(baseline(src));old='''void __fastcall FUN_00496910(int** apObject)\n{\n    *apObject = &vftable_NiRefObject;\n    FinishScriptRunLock((void*)&DAT_011f4400);\n}''';x=replace_once(x,old,'''NiRefObject::~NiRefObject()\n{\n    FinishScriptRunLock((void*)&ms_lObjectCount);\n}''');ov[src]=x.encode()
 x=readtext(baseline(opt));old='''inline NiRefObject::~NiRefObject()\n{\n    NiAtomicSubtract(ms_lObjectCount);\n}\n''';x=replace_once(x,old,'');ov[opt]=x.encode()
 orig=(P/'units.generated').read_bytes();doc=json.loads(orig);u=copy.deepcopy(doc['units'][612]);v=doc['units'][1503]
 if len(u['functions'])!=154 or len(v['functions'])!=11:raise ValueError('unit scope changed')
 for address,oldname,newname,size in [('0x00496910','?FUN_00496910@@YIXPAPAH@Z','??1NiRefObject@@UAE@XZ',33),('0x004968e0','?FUN_004968e0@FUN_004968e0_shell@@QAEPAXI@Z','??_GNiRefObject@@UAEPAXI@Z',46)]:
  z=[f for f in u['functions'] if f['address']==address]
  if len(z)!=1 or z[0]['symbol']!=oldname or z[0]['size']!=size:raise ValueError('owner differs')
  z[0]['symbol']=newname
 for sym,target in [('?ms_lObjectCount@NiRefObject@@2IA','0x011f4400'),('??_7NiRefObject@@6B@','0x0101dce4')]:
  if sym in u['symbols'] and u['symbols'][sym]!=target:raise ValueError('existing binding conflict')
  u['symbols'][sym]=target
 recipe=tescontainer_install.replace_unit(orig,612,u);after=json.loads(recipe)
 spans=lambda x:Counter((f['address'],f['size']) for q in x['units'] for f in q['functions'])
 if spans(doc)!=spans(after) or any(doc['units'][i]!=after['units'][i] for i in range(len(doc['units'])) if i!=612) or any(doc['units'][612][k]!=u[k] for k in ('source','flags','compiler')):raise ValueError('scope changed')
 mirrors={}
 for i in (612,1503):
  source=doc['units'][i]['source'];origov={k:(P/'payload'/k).read_bytes() for k in m['source_payload_sha256']};a=core.walk(F,source,origov);b=core.walk(F,source,ov);mirrors[str(i)]={'source':source,'original':a,'candidate':b,'flags':doc['units'][i]['flags'],'functions':len(doc['units'][i]['functions']),'eh_tails':len(doc['units'][i].get('eh_tails',[]))}
  if 'include/NiRefObject.h' not in b['files']:raise ValueError('canonical header not reached '+str(i))
 T.mkdir();(T/'units.original').write_bytes(orig);(T/'units.generated').write_bytes(recipe)
 for rel in (decl,src,opt):
  q=T/'overrides'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(ov[rel])
 for i,z in mirrors.items():
  for tag in ('original','candidate'):
   dataov={k:(P/'payload'/k).read_bytes() for k in m['source_payload_sha256']} if tag=='original' else ov
   for rel,digest in z[tag]['files'].items():
    data=dataov[rel] if rel in dataov else (F/rel).read_bytes()
    if h(data)!=digest:raise ValueError('source capture changed')
    q=T/i/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  q=T/i/'mirror-manifest.json';q.write_text(json.dumps({'schema_version':1,'unit':int(i),'source':z['source'],'original_inputs':z['original']['files'],'original':z['original'],'candidate':z['candidate'],'flags':z['flags'],'parent_manifest_sha256':PIN,'baseline':'private 38-source proposal, not live installed source','production_include_order':['/I<mirror>/include']},indent=2))
 facts={'status':'private uncompiled native source hypothesis','parent_manifest_sha256':PIN,'parent_recipe_sha256':RPIN,'live_recipe_sha256':BASE,'candidate_recipe_sha256':h(recipe),'functions_global_address_size_multiset_unchanged':True,'modified_sources':{x:h(ov[x]) for x in (decl,src,opt)},'baseline_source_sha256':{x:h(baseline(x)) for x in (decl,src,opt)},'mirrors':mirrors,'counter_source_contract':{'counter_symbol':'?ms_lObjectCount@NiRefObject@@2IA','mapped_va':'0x011f4400','existing_source_unit':1503,'status':'declared storage reference and source mapping; no definition/initializer claim'},'atomic_helper':{'source_unit':633,'mapped_va':'0x004019a0','source_function':'WaitForSingleObjectEx(long*)','source_behavior':'InterlockedDecrement','612_existing_source_view':'FinishScriptRunLock(void*)'},'prior_object_paths':{'612':'runtime-next/m3/out/phase2-nimem-kind-production-archive/0612.obj','1503':'runtime-next/m3/out/phase2-nimem-operators-825d-production-archive/1503.obj'},'limitations':['fixture hypothesis only; no compilation or source installation','compiler may not emit G wrapper or may produce different helper call; do not force aliases','1503 optimized 0x00a5d3d0 18-byte source owner remains unchanged in recipe','legacy surrogate source wrapper remains unplaced only in hypothetical mapping','public NiRef class duplicate views, all consumers, RTTI/weak/COMDAT and complete image/runtime remain open']}
 (T/'manifest.json').write_text(json.dumps(facts,indent=2));print(json.dumps({'manifest_sha256':h((T/'manifest.json').read_bytes()),'candidate_recipe_sha256':h(recipe),'closures':{i:[len(z['original']['files']),len(z['candidate']['files'])] for i,z in mirrors.items()}}))
if __name__=='__main__':main()
