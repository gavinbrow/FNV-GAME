import os,tempfile,subprocess,json,hashlib
from pathlib import Path
import gen_m3 as G
import b8_records as R
import compile_units_v3 as CU
from compare import Coff
sel=json.load(open('inventory/b8_command_prefix_selection.json'))['entries']
entries=[R.build_entry(r,G) for r in sel]; ext={}; structs=[]; defs=[]
for e in entries:
 s,d=R.render_entry(e,ext); structs.append(s); defs.append(d)
assert len(set(structs))==1
source='\n'.join([structs[0]]+[ext[x] for x in sorted(ext)]+defs)+'\n'
tc=CU.find_toolchains()['sp1']; vc=Path(tc['vc']); env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None)
with tempfile.TemporaryDirectory(prefix='b8records_') as t:
 src=Path(t)/'record.cpp'; obj=Path(t)/'record.obj'; src.write_text(source); env['TMP']=env['TEMP']=t
 p=subprocess.run([str(vc/'bin'/'cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/I'+os.path.join(G.PROJ,'fnv_decomp','include'),str(src),'/Fo'+str(obj)],cwd=t,env=env,capture_output=True,text=True,errors='replace'); print('compile',p.returncode,p.stdout,p.stderr); assert p.returncode==0
 c=Coff(str(obj)); assert not any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s)
 for e in entries:
  syms=[s['name'] for s in c.symbols.values() if e['name'] in s['name'] and s['section']>0]; assert len(syms)==1; e['sym']=syms[0]
  data,rel,sec,flags,storage=G.splice.slice_entry(c,e); assert sec==e['section'] and storage==2
  err=G.check_elems(e,data,rel,{}); assert err is None,err
  print(hex(e['va']),e['size'],'relocations',len(rel),'reference sha256',hashlib.sha256(bytes.fromhex(e['ref'])).hexdigest(),'PASS')
# Rejections of wrong bounds, full-extent assertion, and invalid name.
for changes in ({'n':641},{'partial':False},{'generated_name':'DAT_01190910'}):
 bad=dict(sel[0],**changes)
 try: R.build_entry(bad,G)
 except ValueError: pass
 else: raise AssertionError('unsafe selection accepted: '+str(changes))
print('invalid candidate rejections PASS')
