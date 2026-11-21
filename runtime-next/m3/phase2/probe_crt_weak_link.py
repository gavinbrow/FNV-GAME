"""Exercise MSVC2008 LINK weak-CRT resolution with actual libraries; never runs the executables."""
from pathlib import Path
import argparse,subprocess,sys,json,hashlib,re,struct
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'runtime-next/m3/phase2'));import rtti_tesform_bindings_transaction as locks
import pefile

def run(out):
 assert not out.exists();out.mkdir(parents=True);vc=R/'FNV/tools/vc2008/VC';src=out/'fixture.cpp';src.write_text('#include <typeinfo>\nextern "C" { const type_info* volatile selectedType=0; void ProbeEntry(){ selectedType=&typeid(int); } } int main(){ ProbeEntry(); return 0; }\n');asm=out/'strong-control.asm';asm.write_text('.386\n.model flat\nPUBLIC ??_Etype_info@@UAEPAXI@Z\n.code\n??_Etype_info@@UAEPAXI@Z PROC\nxor eax,eax\nret 4\n??_Etype_info@@UAEPAXI@Z ENDP\nEND\n');commands=[]
 def execute(cmd,log):
  commands.append(cmd);cp=subprocess.run(cmd,cwd=out,capture_output=True,text=True);(out/log).write_text(cp.stdout+cp.stderr);return cp.returncode
 guards=locks.acquire_guard()
 try:
  assert not (R/'runtime-next/direct-v1/harness.lock').exists()
  rc=execute([str(vc/'bin/cl.exe'),'/nologo','/c','/MT','/GR','/Od','/I'+str(vc/'include'),'/Fo'+str(out/'fixture.obj'),str(src)],'compile.log');assert rc==0,'compile failed'
  rc=execute([str(vc/'bin/ml.exe'),'/nologo','/c','/Fo'+str(out/'strong-control.obj'),str(asm)],'assemble.log');assert rc==0,'assemble failed'
  results=[]
  for variant,extra in [('fallback',[]),('strong-control',[str(out/'strong-control.obj')])]:
   image=out/(variant+'.exe');mp=out/(variant+'.map');cmd=[str(vc/'bin/link.exe'),'/NOLOGO','/INCREMENTAL:NO','/OPT:NOREF','/OPT:NOICF','/SUBSYSTEM:CONSOLE','/MACHINE:X86','/OUT:'+str(image),'/MAP:'+str(mp),'/LIBPATH:'+str(vc/'lib'),'/LIBPATH:'+str(vc/'PlatformSDK/Lib'),str(out/'fixture.obj')]+extra+['libcmt.lib','libcpmt.lib','kernel32.lib','user32.lib','advapi32.lib'];rc=execute(cmd,variant+'.log');assert rc==0,variant+' link failed'
   symbols={m.group(1):int(m.group(2),16) for m in re.finditer(r'^\s+[0-9A-Fa-f]{4}:[0-9A-Fa-f]+\s+(\S+)\s+([0-9A-Fa-f]{8})\b',mp.read_text(),re.M)};vft=symbols['??_7type_info@@6B@'];g=symbols['??_Gtype_info@@UAEPAXI@Z'];pe=pefile.PE(str(image));target=struct.unpack('<I',pe.get_data(vft-pe.OPTIONAL_HEADER.ImageBase,4))[0];e=symbols.get('??_Etype_info@@UAEPAXI@Z')
   if variant=='fallback':assert target==g
   else:assert e is not None and target==e and e!=g
   results.append({'variant':variant,'vft_address':hex(vft),'target':hex(target),'G_address':hex(g),'E_address':hex(e) if e else None,'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'map_sha256':hashlib.sha256(mp.read_bytes()).hexdigest()})
 finally:
  for p in reversed(guards):p.unlink()
 result={'scope':'Own fixture links using actual CRT libraries; executables never run. Establishes linker behavior under these exact inputs, not all project weak symbols.','pass':True,'results':results,'commands':commands,'limits':['Production input symbol closure and source ownership require separate checks','No blanket E->G alias is authorized','No game function bodies reconstructed or production helper modified']};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(results))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.out.resolve())
