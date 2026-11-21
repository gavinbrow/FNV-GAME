"""Record source- and COFF-backed NiRefObject metadata/owner leads."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';DEST=O/'phase2-nirefobject-native-evidence.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from class_metadata_compare import ObjectRecords
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if DEST.exists():raise FileExistsError('preserve prior evidence')
 recipe=F/'build/units.json';doc=json.loads(recipe.read_text());units=doc['units'];census=O/'phase2-class-census/census-6757.json';x=json.loads(census.read_text());typ=next(z for z in x['classes'] if z['type_name']=='.?AVNiRefObject@@');table=next(z for z in x['vtables'] if z['vtable_va']==0x101dce4);hier=next(z for z in x['hierarchies'] if z['va']==table['locator']['hierarchy_va'])
 if typ['type_descriptor_va']!=0x11854e0 or table['contiguous_code_pointer_prefix_targets']!=[0x4968e0,0xcfcc20] or len(hier['bases'])!=2:raise ValueError('reference metadata differs')
 obj=RN/'pinned-build/obj_v3.bak-20261116/1503.obj';c=Coff(str(obj));tables=ObjectRecords(c).tables('.?AVNiRefObject@@')
 if len(tables)!=1:raise ValueError('native class table absent')
 g=tables[0]['locator']['graph'];v=g['bases'];ref=hier['bases']
 if [z['type_name'] for z in v]!=['.?AVNiRefObject@@','.?AVNiMemObject@@'] or [z['pmd'] for z in v]!=[[0,-1,0],[4,-1,0]]:raise ValueError('unexpected emitted graph')
 if [z['type_name'] for z in ref]!=['.?AVNiRefObject@@','.?AUNiMemObject@@']:raise ValueError('unexpected original class key')
 pe=Pe(paths.REF_IMAGE);spec=copy.deepcopy(units[1503]);spec['functions']=[{'address':'0x00a5d3d0','symbol':'??1NiRefObject@@UAE@XZ','size':18}];rows=compare(c,pe,spec)
 if len(rows)!=1 or rows[0]['verdict']!='match':raise ValueError('native destructor not strict')
 fallback=c.named('??_GNiRefObject@@UAEPAXI@Z');fbsize=len(c.sections[fallback['section']]['data'])-fallback['value']
 if fbsize!=42:raise ValueError('native deleting wrapper extent changed')
 owners={}
 for address in ('0x004968e0','0x00496910','0x00cfcc20','0x00a5d3d0'):
  found=[{'unit':i,'source':u['source'],'symbol':f['symbol'],'size':f['size']} for i,u in enumerate(units) for f in u['functions'] if f['address']==address]
  if len(found)!=1:raise ValueError('owner ambiguous '+address)
  owners[address]=found[0]
 sources=['include/NiRefObject.h','include/NiMemObject.h','src/fallout_shared/animation.cpp','src/gamebryo2.2/corelibs/nimain/nirefobject.cpp','src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp','src/staging/blk_00a40000_o2.cpp']
 OUT=DEST;OUT.write_text(json.dumps({'scope':'reference RTTI and native source/object owner leads; no full native class or placement claim','recipe_sha256':sha(recipe),'census_sha256':sha(census),'object1503_sha256':sha(obj),'reference_sha256':sha(Path(paths.REF_IMAGE)),'source_sha256':{s:sha(F/s) for s in sources},'type_descriptor_va':'0x011854e0','table_va':'0x0101dce4','locator_va':'0x01107a6c','reference_slot_prefix':['0x004968e0','0x00cfcc20'],'reference_graph':[{'name':z['type_name'],'pmd':z['pmd'],'attributes':z['attributes']} for z in ref],'emitted_graph':v,'graph_mismatch':'public class NiMemObject emits .?AV; original descriptor is .?AU','source_owners':owners,'object1503_native_destructor_reference':'0x00a5d3d0','object1503_destructor_bytes_strict':18,'object1503_deleting_wrapper_bytes':fbsize,'reference_deleting_wrapper_bytes':46,'counter_reference_va':'0x011f4400','limits':['source constructor inline and independent emitted owner not established','original 0x00496910 and optimized 0x00a5d3d0 are distinct function bodies','observed pointer prefix is not a verified complete vtable extent','source global class/struct choice and all consuming closures need review','weak fallback/ICF/link placement and runtime are unproved']},indent=2));print('PASS reference graph comparison and native optimized destructor match; base class key mismatch remains')
if __name__=='__main__':main()
