"""Recheck compiled PSA candidate and write private, narrow recipe proposal."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;FN=ROOT/'fnv_decomp';O=M/'out/phase2-bgsbodypart-psa-implicit-proposal'
sys.path[:0]=[str(FN/'tools'),str(M.parent),str(M)]
from compare import Coff,Pe,compare
import paths,gen_m3 as G
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 run=json.loads((O/'lane-compile.json').read_text());rows={(x['unit'],x['tag']):x for x in run['outcomes']}
 if len(rows)!=4:raise ValueError('four objects required')
 for (unit,tag),r in rows.items():
  if r['rc'] or sha(O/('%04d.%s.obj'%(unit,tag)))!=r['object_sha256']:raise ValueError('object evidence mismatch')
 saved=json.loads((O/'lane-comparison.json').read_text());control=saved['621']['reference']['mirror']
 if not isinstance(control,list) or len(control)!=10 or any(x['verdict']!='match' for x in control):raise ValueError('unit 621 control mismatch')
 units=json.loads((FN/'build/units.json').read_text())['units'];u=copy.deepcopy(units[620]);f=[f for f in u['functions'] if f['address']=='0x005e3be0']
 if len(f)!=1:raise ValueError('constructor mapping')
 before=f[0]['symbol'];f[0]['symbol']='??0TESModelPSA@@QAE@XZ'
 bindings={'??_7TESModelPSA@@6B@':'0x0104540c','??1TESModel@@UAE@XZ':'0x00489070'}
 for k,v in bindings.items():
  if k in u['symbols'] and u['symbols'][k]!=v:raise ValueError('binding conflict')
  u['symbols'][k]=v
 c=Coff(str(O/'0620.mirror.obj'));ref=Pe(paths.REF_IMAGE);result=compare(c,ref,u)
 if len(result)!=15 or any(x['verdict']!='match' for x in result):raise ValueError('strict function match failed')
 proofs=[]
 for name,va,size,targets in [('??1TESModelPSA@@UAE@XZ',0x51b950,19,[0x489070]),('??_GTESModelPSA@@UAEPAXI@Z',0x5e3c30,44,[0x51b950,0x401030])]:
  sym=c.named(name);sec=c.sections[sym['section']];data=bytearray(sec['data'][sym['value']:sym['value']+size]);original=G.refbytes(va,size);found=[]
  for off,idx,kind in sec['relocs']:
   if not sym['value']<=off<sym['value']+size:continue
   x=off-sym['value']
   if kind!=20 or x+4>size:raise ValueError('unexpected destructor relocation')
   target=va+x+4+struct.unpack_from('<i',original,x)[0];found.append(target);data[x:x+4]=original[x:x+4]
  if bytes(data)!=original or found!=targets:raise ValueError('destructor reference mismatch')
  proofs.append({'symbol':name,'reference_va':hex(va),'size':size,'nonrelocated_bytes_equal':True,'reference_rel32_targets':[hex(x) for x in found]})
 weak=[(i,s) for i,s in c.symbols.items() if s['name']=='??_ETESModelPSA@@UAEPAXI@Z' and s['storage']==105]
 if len(weak)!=1:raise ValueError('weak symbol ambiguous')
 symptr=struct.unpack_from('<I',c.data,8)[0];index,kind=struct.unpack_from('<II',c.data,symptr+(weak[0][0]+1)*18)
 if kind!=2 or c.symbols[index]['name']!='??_GTESModelPSA@@UAEPAXI@Z':raise ValueError('unexpected weak alias')
 v=c.named('??_7TESModelPSA@@6B@');sec=c.sections[v['section']];slots=[{'offset':off-v['value'],'symbol':c.symbols[idx]['name']} for off,idx,kind in sec['relocs'] if off>=v['value']]
 output={'status':'private narrow proposal; no placement or full-table acceptance','inputs':{'units_sha256':sha(FN/'build/units.json'),'compiled_object_sha256':sha(O/'0620.mirror.obj'),'compile_report_sha256':sha(O/'lane-compile.json'),'comparison_sha256':sha(O/'lane-comparison.json')},
         'function_check':{'candidate_620_strict_matches':15,'count':15,'previous_621_strict_matches':10,'previous_621_count':10},
         'recipe_changes':{'constructor_before':before,'constructor_after':f[0]['symbol'],'bindings':bindings},'implicit_destructor_bodies':proofs,
         'weak_alias':{'symbol':weak[0][1]['name'],'fallback':c.symbols[index]['name'],'characteristics':kind},'emitted_slots':slots,
         'remaining':['eighth original code pointer ownership and complete table extent unresolved','all slot targets and complete RTTI graph must be independently checked','no runtime placement or image validation','native getter/setter source signatures remain hypotheses']}
 p=O/'integration-candidate.json'
 with p.open('x',encoding='utf8') as q:json.dump(output,q,indent=2)
 print(json.dumps({'candidate':str(p),'sha256':sha(p)}))
if __name__=='__main__':main()
