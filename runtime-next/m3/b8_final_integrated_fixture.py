import os,json,tempfile,subprocess,hashlib
from pathlib import Path
import gen_m3 as G
import compile_units_v3 as CU
from compare import Coff
selpath='batch8_final_selection.json'; rawsel=open(selpath,'rb').read(); print('selection sha256',hashlib.sha256(rawsel).hexdigest()); assert hashlib.sha256(rawsel).hexdigest()=='42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7'
allsel=json.loads(rawsel)['entries']; old=json.load(open('batch7_selection.json'))['entries']; assert allsel[:len(old)]==old
new=allsel[len(old):]; print('new',len(new)); assert len(new)==64
entries=G.build_entries(new); assert sum(e['size'] for e in entries)==36597
srcdata=G.cpp(entries); tc=CU.find_toolchains()['sp1']; assert tc['ok']; vc=Path(tc['vc']); env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None)
with tempfile.TemporaryDirectory(prefix='b8final_') as temp:
 src=Path(temp)/'m3.cpp'; obj=Path(temp)/'m3.obj'; src.write_text(srcdata); env['TMP']=env['TEMP']=temp
 p=subprocess.run([str(vc/'bin'/'cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/I'+os.path.join(G.PROJ,'fnv_decomp','include'),str(src),'/Fo'+str(obj)],cwd=temp,env=env,capture_output=True,text=True,errors='replace'); print('compile',p.returncode,p.stdout,p.stderr); assert p.returncode==0
 c=Coff(str(obj)); assert not any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s); assert not any(s['name'].startswith(('??__E','$E')) for s in c.symbols.values())
 syms={}
 for s in c.symbols.values():
  m=G.splice.SYM_RE.match(s['name'])
  if m and s['section']>0:
   va=int(m.group(1),16); assert va not in syms; syms[va]=s['name']
 for e in entries:
  e['sym']=syms.get(e['va']); assert e['sym'],e['name']
 tab=G.splice.name_table(entries); counts={}; reltotal=0
 for e in entries:
  data,rel,sec,flags,storage=G.splice.slice_entry(c,e); assert storage==2 and sec==e['section'] and len(data)==e['size'],e['name']
  if e['tc'] in ('A','T','X','R'): err=G.check_elems(e,data,rel,tab)
  elif e.get('ptr'): err=G.check_ptr(e,data,rel)
  elif e['tc']=='W': err=G.check_g(e,data,rel,tab)
  else: err=None if not rel and data==bytes.fromhex(e['ref']) else 'scalar mismatch'
  assert err is None,(e['name'],err)
  counts[e['tc']]=counts.get(e['tc'],0)+1; reltotal+=len(rel)
 print('PASS entries',len(entries),'bytes',sum(e['size'] for e in entries),'types',counts,'relocs',reltotal,'R relocs',sum(len(e.get('fields',[])) for e in entries if e['tc']=='R'),'P',sum(bool(e.get('ptr')) for e in entries))
