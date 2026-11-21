"""Stage native NiMemObject operator definitions at the existing allocator owners."""
import copy,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core,tescontainer_install
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-nimemobject-native-operators-v2';A=M/'out/phase2-nimem-allocator-return';B=M/'out/phase2-nimemobject-allocation-api';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';NEWSYM='??2NiMemObject@@SAPAXI@Z';DELSYM='??3NiMemObject@@SAXPAXI@Z';ALLOC='src/staging/blk_00aa0000_o2.cpp';DELETE='src/gamebryo2.2/corelibs/nisystem/nimemobject_o2_variant_iso_variant.cpp';HDR='include/NiMemObject.h'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior proposal')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);u=doc['units'];ap=json.loads((A/'manifest.json').read_text());proof=json.loads((A/'comparison.json').read_text());bp=json.loads((B/'independent-review.json').read_text());am=json.loads((B/'manifest.json').read_text())
 if sha((F/DELETE).read_bytes())!='55387e3f60c9ab215fe03c2dac8c270dbbe3480a65c89df3e0ecb260567fb2e3' or sha((A/'comparison.json').read_bytes())!='ebd293989e581f17b314e6e26951b86da93797c83a96719be9f42a1ebe6ce3e6' or sha((B/'independent-review.json').read_bytes())!='348d4cb118492cd18cc19c31e9a7ce4ee5102ecbb653211c250eb657d467997f':raise ValueError('owner or evidence preimage changed')
 if sha(raw)!=BASE or ap['base_recipe_sha256']!=BASE or proof['strict_functions']!=43 or proof['target_size']!=62 or bp['recipe_sha256']!=BASE or am['recipe_sha256']!=BASE:raise ValueError('pinned proof differs')
 if sha((F/ALLOC).read_bytes())!=ap['before_source_sha256'] or sha((A/'source.generated').read_bytes())!=ap['after_source_sha256'] or sha((F/HDR).read_bytes())!=am['before_sha256'] or sha((B/'header.generated').read_bytes())!=am['after_sha256']:raise ValueError('source preimages differ')
 if len(u[1664]['functions'])!=3 or len(u[2734]['functions'])!=43 or u[1664]['source']!=DELETE or u[2734]['source']!=ALLOC:raise ValueError('owner units differ')
 expected=[(1664,'0x00aa1460',34,'?FUN_00aa1460@@YAXPAXI@Z',DELSYM),(2734,'0x00aa13e0',62,'?FUN_00aa13e0@@YAXH@Z',NEWSYM)]
 for i,addr,size,old,new in expected:
  found=[(j,f) for j,z in enumerate(u) for f in z['functions'] if int(f['address'],16)<int(addr,16)+size and int(addr,16)<int(f['address'],16)+f['size']]
  if len(found)!=1 or found[0][0]!=i or found[0][1]['address']!=addr or found[0][1]['size']!=size or found[0][1]['symbol']!=old:raise ValueError('overlapping owner')
 allocate=(A/'source.generated').read_bytes();deallocate=(F/DELETE).read_bytes();header=(B/'header.generated').read_bytes();anl=b'\r\n' if b'\r\n' in allocate else b'\n';dnl=b'\r\n' if b'\r\n' in deallocate else b'\n'
 edits=[(b'void* __cdecl FUN_00aa13e0(unsigned int value)',b'void* NiMemObject::operator new(unsigned int value)'),(b'#include "../../include/layout_support.h"',b'#include "../../include/layout_support.h"'+anl+b'#include "NiMemObject.h"')]
 for a,b in edits:
  if allocate.count(a)!=1:raise ValueError('allocation anchor differs')
  allocate=allocate.replace(a,b,1)
 for a,b in [(b'void FUN_00aa1460(void* memory, unsigned int size)',b'void NiMemObject::operator delete(void* memory, unsigned int size)'),(b'#include "nimemobject_decls.h"',b'#include "nimemobject_decls.h"'+dnl+b'#include "NiMemObject.h"')]:
  if deallocate.count(a)!=1:raise ValueError('deallocation anchor differs')
  deallocate=deallocate.replace(a,b,1)
 overrides={ALLOC:allocate,DELETE:deallocate,HDR:header};new=raw
 for i,addr,size,old,sym in expected:
  v=copy.deepcopy(u[i]);f=next(f for f in v['functions'] if f['address']==addr);f['symbol']=sym;new=tescontainer_install.replace_unit(new,i,v)
 nd=json.loads(new)
 if [i for i,(a,b) in enumerate(zip(u,nd['units'])) if a!=b]!=[1664,2734] or any(doc[k]!=nd[k] for k in doc if k!='units'):raise ValueError('recipe scope differs')
 for i in (1664,2734):
  if [(x['address'],x['size']) for x in u[i]['functions']]!=[(x['address'],x['size']) for x in nd['units'][i]['functions']]:raise ValueError('function extents differ')
 mirrors={}
 for i in (1664,2734):
  source=u[i]['source'];a=core.walk(F,source,{});b=core.walk(F,source,overrides);mirrors[str(i)]={'source':source,'original':a,'candidate':b,'functions':len(u[i]['functions']),'eh_tails':len(u[i].get('eh_tails',[]))}
  if HDR not in b['files']:raise ValueError('canonical API header absent')
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(new)
 for rel,data in overrides.items():
  p=O/'payload'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 for i,m in mirrors.items():
  d=O/i
  for tag in ('original','candidate'):
   for rel,digest in m[tag]['files'].items():
    data=overrides[rel] if tag=='candidate' and rel in overrides else (F/rel).read_bytes()
    if sha(data)!=digest:raise ValueError('closure input changed')
    p=d/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  mm={'schema_version':1,'source':m['source'],'units_sha256':BASE,'original_inputs':m['original']['files'],'original':m['original'],'candidate':m['candidate'],'production_include_order':['/I<mirror>/include'],'limits':['private native operator owner hypothesis; no live edits']};(d/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 evidence={'allocation_return_comparison_sha256':sha((A/'comparison.json').read_bytes()),'allocation_api_review_sha256':sha((B/'independent-review.json').read_bytes()),'allocation_manifest_sha256':sha((A/'manifest.json').read_bytes()),'api_manifest_sha256':sha((B/'manifest.json').read_bytes())}
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(new),'source_payload_sha256':{k:sha(v) for k,v in overrides.items()},'evidence_sha256':evidence,'owners':[{'unit':i,'address':addr,'size':size,'old':old,'candidate':sym,'flags':u[i]['flags']} for i,addr,size,old,sym in expected],'mirrors':mirrors,'legacy_call_bindings':{'pointer_return_FUN_00aa13e0':sum('?FUN_00aa13e0@@YAPAXI@Z' in z.get('symbols',{}) for z in u),'void_FUN_00aa1460':sum('?FUN_00aa1460@@YAXPAXI@Z' in z.get('symbols',{}) for z in u)},'api_header_lexical_consumer_units':am['lexical_consumer_count'],'additional_owner_units':[1664,2734],'limits':['private native operator owner hypothesis, not live source/recipe','legacy caller symbols retain existing field bindings; normal linker and global name ownership require explicit proof','class kind-only 750-cohort is separate and untouched','all 126 header consumers plus two newly including owners need function/EH, new/delete, first declaration and production placement proof','allocator virtual operation names, failure semantics, weak fallback and final image/runtime remain open']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'owners':[1664,2734],'functions':46,'header_existing_consumers':am['lexical_consumer_count'],'candidate_recipe_sha256':sha(new)}))
if __name__=='__main__':main()
