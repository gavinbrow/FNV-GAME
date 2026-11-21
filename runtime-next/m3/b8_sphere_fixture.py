import os,tempfile,subprocess,sys,json,hashlib
from pathlib import Path
import gen_m3 as G
import compile_units_v3 as CU
from compare import Coff
selection={'va':0x1187ac8,'tc':'A','et':'N','size':2688,'generated_name':'M3_01187ac8','partial':True,'align':8}
e=G.build_entries([selection])[0]; e['name']=selection['generated_name']
vcinfo=CU.find_toolchains()['sp1']; assert vcinfo['ok']; vc=Path(vcinfo['vc']); env=CU.make_env(vc,Path(vcinfo['sdk']) if vcinfo['sdk']!='None' else None)
with tempfile.TemporaryDirectory(prefix='b8sphere_') as temp:
 src=Path(temp)/'sphere.cpp'; obj=Path(temp)/'sphere.obj'; src.write_text(G.cpp([e]))
 env['TMP']=env['TEMP']=temp
 cmd=[str(vc/'bin'/'cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/I'+os.path.join(G.PROJ,'fnv_decomp','include'),str(src),'/Fo'+str(obj)]
 p=subprocess.run(cmd,cwd=temp,env=env,capture_output=True,text=True,errors='replace'); print('compile',p.returncode,p.stdout,p.stderr); assert p.returncode==0
 coff=Coff(str(obj)); syms=[s['name'] for s in coff.symbols.values() if 'M3_01187ac8' in s['name'] and s['section']>0]; print('symbols',syms); assert len(syms)==1
 e['sym']=syms[0]; data,rel,sec,flags,storage=G.splice.slice_entry(coff,e); err=G.check_elems(e,data,rel,{})
 assert sec=='.data' and storage==2 and err is None and not rel
 assert not any(s['name'].startswith('.CRT$XC') for s in coff.sections[1:] if s)
 print('result',len(data),'match',data==bytes.fromhex(e['ref']),'section',sec,'negative_zero',sum(data[i:i+8]==bytes.fromhex('0000000000000080') for i in range(0,len(data),8)),'sha256',hashlib.sha256(data).hexdigest())
 print('selection',json.dumps(selection))
