import glob,os
H=r'C:\Projects\Decompilation\runtime-next\link-v2'
objs=sorted(glob.glob(H+r'\obj_rw\*.obj'))+sorted(glob.glob(H+r'\obj_contrib_rw\*.obj'))+sorted(glob.glob(H+r'\data_out\*.obj'))+sorted(glob.glob(H+r'\crt_obj\*.obj'))+[H+r'\resources.obj']
libs=sorted(glob.glob(H+r'\implibs2\*.lib'))+['kernel32.lib','user32.lib','gdi32.lib','advapi32.lib','shell32.lib','ole32.lib','oleaut32.lib','winmm.lib','comctl32.lib','wsock32.lib','ws2_32.lib','xinput.lib','version.lib','d3d9.lib','libcmt.lib','libcpmt.lib']
opts=['/NOLOGO','/OUT:'+H+r'\FalloutNV_linked.exe','/SUBSYSTEM:WINDOWS','/ENTRY:WinMainCRTStartup','/FIXED:NO','/MACHINE:X86','/OPT:REF','/OPT:NOICF','/NODEFAULTLIB','/MAP:'+H+r'\linked.map','/INCREMENTAL:NO']
BS=chr(92)
extra=[l.strip() for f in ('opts_extra.txt','opts_imp.txt') if os.path.exists(H+BS+f) for l in open(H+BS+f) if l.strip()]
open(H+r'\link.rsp','w').write('\n'.join(opts+extra+['"%s"'%o for o in objs]+libs)+'\n')
print(len(objs),'objects')
