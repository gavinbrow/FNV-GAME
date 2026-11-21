"""Private compiler experiment comparing debug hkBool class and current PC typedef view."""
from pathlib import Path
import argparse,hashlib,json,sqlite3,subprocess,sys
R=Path(__file__).resolve().parents[3];sys.path[:0]=[str(R/'runtime-next/m3/phase2'),str(R/'fnv_decomp/tools')]
from atlas_evidence_query import query
import rtti_tesform_bindings_transaction as locks
from compare import Coff
import capstone

def run(out):
 assert not out.exists();out.mkdir(parents=True);card=query(R/'runtime-next/m3/out/non-ai-continuation-20261119/atlas-index/index.json',job='P2N19-C-011B0310');definition=card['definitions'];assert len(definition)==1
 methods=next(m['overloads'] for m in definition[0]['members'] if m['member_name']=='castRay');assert len(methods)==2
 header=R/'fnv_decomp/include/havok/hkBase.h';raw=header.read_bytes();assert b'typedef char hkBool;' in raw
 db=R/'runtime-next/m3/out/non-ai-benchmark-20261119/atlas/fnv-source-atlas-data-0.5.0/fnv-source-atlas.sqlite';c=sqlite3.connect(db.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
 support=c.execute("select t.tag_kind,t.size_value,f.member_name,f.rendered_type,f.member_offset_value from codeview_tag_layouts t join codeview_tag_member_uses u using(tag_layout_id) join codeview_field_members f using(field_member_id) where t.display_name='hkBool' and t.is_forward_reference=0 and f.member_kind='data_member'").fetchall();assert support==[('class','1','m_bool','char','0')]
 decls=[]
 for m in reversed(methods):
  ret,args=m['rendered_type'].split(' __cdecl hkaRaycastInterface::*(');assert ret=='hkBool';decls.append('virtual hkBool castRay('+args[:-1]+');')
 cl=R/'FNV/tools/vc2008/VC/bin/cl.exe';results=[];guards=locks.acquire_guard()
 try:
  assert not (R/'runtime-next/direct-v1/harness.lock').exists()
  for label,decl in [('debug_class','class hkBool { char m_bool; };'),('pc_typedef_view','typedef char hkBool;')]:
   source='class hkVector4; '+decl+'\nclass hkaRaycastInterface { public: virtual ~hkaRaycastInterface();\n'+'\n'.join(decls)+'\n};\nvoid Invoke(hkaRaycastInterface* p,const hkVector4& a,const hkVector4& b,unsigned int f,float& t,hkVector4& n){p->castRay(a,b,f,t,n); }\n'
   src=out/(label+'.cpp');src.write_text(source);obj=out/(label+'.obj');cmd=[str(cl),'/nologo','/c','/Od','/GR','/EHsc','/Fo'+str(obj),str(src)];cp=subprocess.run(cmd,cwd=out,capture_output=True,text=True);(out/(label+'.log')).write_text(cp.stdout+cp.stderr);assert cp.returncode==0,cp.stdout+cp.stderr
   coff=Coff(str(obj));symbol=next(s for s in coff.symbols.values() if s['name'].startswith('?Invoke@@') and s['section']>0);code=coff.sections[symbol['section']]['data'][symbol['value']:];md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);ins=[{'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(code,0)];hidden=any(i['mnemonic']=='lea' and '[ebp - 1]' in i['operands'] for i in ins);arg_start=next(n for n,i in enumerate(ins) if i['mnemonic']=='mov' and '[ebp +' in i['operands']);pushes=sum(i['mnemonic']=='push' for i in ins[arg_start:next(n for n,i in enumerate(ins) if i['mnemonic']=='call')]);results.append({'view':label,'command':cmd,'hidden_return_storage_address':hidden,'argument_push_instructions_before_virtual_call':pushes,'instructions':ins,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(obj.read_bytes()).hexdigest()})
 finally:
  for path in reversed(guards):path.unlink()
 assert results[0]['hidden_return_storage_address'] and not results[1]['hidden_return_storage_address'];assert results[0]['argument_push_instructions_before_virtual_call']==results[1]['argument_push_instructions_before_virtual_call']+1
 result={'scope':'Original compiler behavior for two evidence-backed type views, not an original-PC caller match','hkBool_debug_record':support,'current_header_sha256':hashlib.sha256(raw).hexdigest(),'results':results,'conclusion':'Equal 1-byte storage does not imply equal return ABI. Do not copy Xbox hkBool return signatures into current PC typedef contexts. Native caller/definition proof remains required.','native_class_accepted':False};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps([{k:r[k] for k in ('view','hidden_return_storage_address','argument_push_instructions_before_virtual_call')} for r in results]))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.out.resolve())
