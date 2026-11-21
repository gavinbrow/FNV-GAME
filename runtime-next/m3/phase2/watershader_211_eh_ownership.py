"""Trace unit211's original and candidate EH action ownership without rebinding."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';OUT=R/'phase2-watershader-211-eh-ownership.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve old evidence')
 obj=R/'phase2-nimem-combined-825d-run/unit-0211/candidate.obj';recipe=R/'phase2-nimem-psys-pointer-binding-v1/units.generated';source=F/'src/bsshader/watershader.cpp';header=F/'include/AutoMemContext.h';owner=F/'src/bscore/memoryusagetracker.cpp'
 pins={obj:'7a883d30d2f3a19cfe5241f26e484fa54c9d00c4fe692fc08fd878643f7de4da',recipe:'5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad',source:'0fb67f7563d989f10faa12a88ea005da7083d6e84b7a0c04d6db3f1c9ca97363',header:'95c90ddd12fd4b76b62187317713d77ec2ee3250b7f772116adfb0d342fabf1b',owner:'3b91b792c66735cd9d633539d2d0f305ec30801586a0fae84970a3bdbaa17760'}
 for p,h in pins.items():
  if sha(p)!=h:raise ValueError('input changed '+str(p))
 units=json.loads(recipe.read_text())['units'];u=units[211];c=Coff(str(obj));pe=Pe(paths.REF_IMAGE);rows=compare(c,pe,u);parent=next(x for x in rows if x['address']=='0x00b827c0')
 if parent['verdict']!='match' or parent['size']!=5647:raise ValueError('parent not strict')
 fninfo=struct.unpack('<9I',pe.read(0x01175a04,36));state,action=struct.unpack('<II',pe.read(fninfo[2],8))
 if fninfo[:3]!=(0x19930522,1,0x011759fc) or (state,action)!=(0xffffffff,0x00f29180):raise ValueError('reference unwind graph differs')
 funclet=pe.read(action,11)
 if funclet[:6]!=bytes.fromhex('8d8db8efffff') or funclet[6]!=0xe9:raise ValueError('reference funclet differs')
 target=(action+11+struct.unpack_from('<i',funclet,7)[0])&0xffffffff
 if target!=0x00404ee0:raise ValueError('original cleanup target differs')
 s=c.named('__unwindfunclet$?FUN_00b827c0@WaterShaderLoader@@QAEXXZ$0');sec=c.sections[s['section']];d=sec['data'][s['value']:s['value']+11]
 if d[:6]!=bytes.fromhex('8d8db4efffff') or d[6]!=0xe9:raise ValueError('candidate funclet differs')
 rs=[c.symbols[j]['name'] for off,j,k in sec['relocs'] if off==s['value']+7 and k==0x14]
 if rs!=['??1WaterShaderMemScope@@QAE@XZ']:raise ValueError('candidate cleanup target differs')
 x=c.named('__ehfuncinfo$?FUN_00b827c0@WaterShaderLoader@@QAEXXZ');xs=c.sections[x['section']];xr=[c.symbols[j]['name'] for off,j,k in xs['relocs'] if off==x['value']+8]
 if xr!=['__unwindtable$?FUN_00b827c0@WaterShaderLoader@@QAEXXZ']:raise ValueError('candidate unwind table differs')
 facts={'candidate_object_sha256':sha(obj),'reference_sha256':sha(Path(paths.REF_IMAGE)),'source_sha256':sha(source),'native_header_sha256':sha(header),'native_destructor_source_sha256':sha(owner),'parent':'0x00b827c0','parent_size':5647,'parent_strict_verdict':parent['verdict'],'reference_handler':'0x00f2918b','reference_funcinfo':'0x01175a04','reference_unwind_table':'0x011759fc','reference_action':'0x00f29180','reference_frame_displacement':-0x1048,'reference_destructor':'0x00404ee0','reference_destructor_owner_unit':47,'candidate_frame_displacement':-0x104c,'candidate_destructor':rs[0],'candidate_unwind_table':xr[0],'source_lifetime':'WaterShaderMemScope is two words; public AutoMemContext header asserts one word','limits':['reference destructor source identity is recipe-supported; owner object strict replay remains separate','strict parent and matching unwind association do not establish cross-view ABI or stack semantics by themselves','source change requires fresh full parent, frame, all EH and generated metadata proof']}
 OUT.write_text(json.dumps(facts,indent=2));print(sha(OUT))
if __name__=='__main__':main()
