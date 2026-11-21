import os,sys,tempfile,subprocess,struct,json,hashlib
from pathlib import Path
exec(open('b8_types_certify.py').read().split('accepted=[];')[0])
import compile_units_v3 as CU
from compare import Coff
cases=[(0x1190910,640),(0x118e8e0,192)]
refs={}
for base,count in cases:
 for x in sorted(z for z in drel if base<=z<base+count*40):
  target=struct.unpack('<I',refbytes(x,4))[0]; refs[target]='M3F' if G.TLO<=target<G.THI else 'M3D'
# Fixed layout is sourced from CommandDescription and the 40-byte ScriptFunctionInfo view;
# members 0x10 and 0x24 are opaque words, and 0x18..0x20 are opaque pointer storage.
L=['struct CommandRecordView { const char* name; const char* alternate; unsigned int opcode; const char* description; unsigned int opaque10; void* parameters; void* opaque18; void* opaque1c; void* opaque20; unsigned int opaque24; };','typedef char VerifySize[sizeof(CommandRecordView)==40 ? 1 : -1];']
for tv,kind in sorted(refs.items()): L.append('extern "C" '+('void '+kind+'_%08x(void);'%tv if kind=='M3F' else 'char '+kind+'_%08x;'%tv))
for base,count in cases:
 L.append('CommandRecordView M3_%08x[%d] = {'%(base,count))
 for i in range(count):
  a=base+i*40; parts=[]
  for off in range(0,40,4):
   site=a+off; v=struct.unpack('<I',refbytes(site,4))[0]
   if off in (0,4,12,20,24,28,32):
    if site in drel: parts.append('(%s)&%s_%08x'%('const char*' if off in (0,4,12) else 'void*',refs[v],v))
    else:
     assert v==0; parts.append('0')
   else: assert site not in drel; parts.append('0x%08xu'%v)
  L.append('{'+','.join(parts)+'},')
 L.append('};')
vcinfo=CU.find_toolchains()['sp1']; assert vcinfo['ok']; vc=Path(vcinfo['vc']); env=CU.make_env(vc,Path(vcinfo['sdk']) if vcinfo['sdk']!='None' else None)
out=[]
with tempfile.TemporaryDirectory(prefix='b8cmd_') as t:
 src=Path(t)/'commands.cpp'; obj=Path(t)/'commands.obj'; src.write_text('\n'.join(L)+'\n'); env['TMP']=env['TEMP']=t
 cmd=[str(vc/'bin'/'cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/I'+os.path.join(PROJ,'fnv_decomp','include'),str(src),'/Fo'+str(obj)]
 p=subprocess.run(cmd,cwd=t,env=env,capture_output=True,text=True,errors='replace'); print('compile',p.returncode,p.stdout,p.stderr); assert p.returncode==0
 c=Coff(str(obj)); assert not any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s)
 for base,count in cases:
  name='M3_%08x'%base; syms=[s['name'] for s in c.symbols.values() if name in s['name'] and s['section']>0]; assert len(syms)==1
  e=dict(sym=syms[0],size=count*40); data,rel,sec,flags,storage=G.splice.slice_entry(c,e); raw=refbytes(base,count*40)
  assert sec=='.data' and storage==2 and len(data)==len(raw)
  expected=sorted(x-base for x in drel if base<=x<base+len(raw)); assert [x[0] for x in rel]==expected
  mask=bytearray(len(raw))
  for off,sym,add in rel:
   target=G.splice.resolve(sym); orig=struct.unpack('<I',raw[off:off+4])[0]; assert target==orig and add==0 and data[off:off+4]==b'\0'*4
   mask[off:off+4]=b'\1'*4
  assert all(mask[i] or data[i]==raw[i] for i in range(len(raw)))
  rec={'va':base,'size':len(raw),'records':count,'record_size':40,'section':sec,'symbol':syms[0],'relocations':len(rel),'reference_sha256':hashlib.sha256(raw).hexdigest(),'partial':True,'unresolved':'complete original array extent, exact pointer/function types and source symbol identity; opaque fields intentionally retained'}
  out.append(rec); print(json.dumps(rec))
with open('inventory/b8_command_prefix_fixture.json','w') as f: json.dump({'schema_version':1,'scope':'isolated compiler evidence, no generator support or selection; per-record source views and opaque pointer storage','records':out},f,indent=2)

