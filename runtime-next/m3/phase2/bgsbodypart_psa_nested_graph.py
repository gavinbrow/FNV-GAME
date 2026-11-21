"""Compare original and candidate PSA RTTI nested base hierarchies, read-only."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;O=M/'out/phase2-bgsbodypart-psa-implicit-proposal'
sys.path[:0]=[str(H),str(M),str(M.parent),str(ROOT/'fnv_decomp/tools')]
from class_metadata_compare import ObjectRecords
from native_class_inventory import Records
from compare import Coff
import paths,gen_m3 as G
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 obj=O/'0620.mirror.obj';c=Coff(str(obj));o=ObjectRecords(c);ref=Records(Path(paths.REF_IMAGE).read_bytes(),G.SEC,G.ORIG_SET)
 original=ref.locator(0x110fbe8);cg=o.locator(o.location(c.named('??_R4TESModelPSA@@6B@')))
 if (cg['subobject_offset'],cg['constructor_displacement'])!=(original['subobject_offset'],original['constructor_displacement']):raise ValueError('COL displacement mismatch')
 keys=('type_name','contained_bases','pmd','attributes','preorder_parent_index')
 strip=lambda bs:[{k:q[k] for k in keys} for q in bs]
 root=ref.hierarchy(original['hierarchy_va'])
 if cg['graph']!={'attributes':root['attributes'],'bases':strip(root['bases'])}:raise ValueError('root graph mismatch')
 units=json.loads((ROOT/'fnv_decomp/build/units.json').read_bytes())['units'];ti={int(v,0) for u in units for k,v in u.get('symbols',{}).items() if k=='??_7type_info@@6B@'}
 if ti!={0x10f1ee0}:raise ValueError('type_info source map ambiguous')
 result=[]
 for b in root['bases']:
  expected={' .?AVTESModelPSA@@':'TESModelPSA',' .?AVTESModel@@':'TESModel',' .?AVBaseFormComponent@@':'BaseFormComponent'}[' '+b['type_name']]
  child=ref.hierarchy(b['hierarchy_va']);ours=o.hierarchy(o.location(c.named('??_R3'+expected+'@@8')))
  if ours!={'attributes':child['attributes'],'bases':strip(child['bases'])} or ref.pointer(b['type_descriptor_va'])!=0x10f1ee0:raise ValueError('nested RTTI mismatch')
  result.append({'type_name':b['type_name'],'reference_descriptor_va':hex(b['descriptor_va']),'reference_type_descriptor_va':hex(b['type_descriptor_va']),
                 'reference_nested_hierarchy_va':hex(b['hierarchy_va']),'type_info_target':'0x010f1ee0','nested_graph_equal':True,'nested_bases':strip(child['bases'])})
 output={'scope':'nested relocated RTTI structure; candidate records not placed','object_sha256':sha(obj),'units_sha256':sha(ROOT/'fnv_decomp/build/units.json'),
         'reference_locator':'0x0110fbe8','reference_hierarchy':hex(original['hierarchy_va']),'root_graph_equal':True,'bases':result}
 p=O/'nested-graph-evidence.json'
 with p.open('x',encoding='utf8') as f:json.dump(output,f,indent=2)
 print(json.dumps({'output':str(p),'sha256':sha(p),'bases':len(result)}))
if __name__=='__main__':main()
