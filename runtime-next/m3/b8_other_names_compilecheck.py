import json,sys,tempfile,subprocess
from pathlib import Path
h=Path(__file__).resolve().parent; sys.path.insert(0,str(h)); import gen_m3 as g; import splice
import compile_units_v3 as cu
from compare import Coff
p=h/'inventory/b8_other_names_accepted.json'; data=json.loads(p.read_text()); entries=g.build_entries([x['selection'] for x in data['entries']])
for e in entries: e['name']=e['name'].replace('DAT_','M3_',1);e['sym']=e['sym'].replace('DAT_','M3_',1)
tc=cu.find_toolchains()['sp1']; assert tc.get('ok');vc=Path(tc['vc']);env=cu.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None)
with tempfile.TemporaryDirectory(prefix='b8_other_names_') as tmp:
 t=Path(tmp); src=t/'heads.cpp';obj=t/'heads.obj';src.write_text(g.cpp(entries),encoding='utf8');env['TMP']=env['TEMP']=str(t)
 cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy',str(src),'/Fo'+str(obj)]
 proc=subprocess.run(cmd,cwd=t,env=env,capture_output=True,text=True,errors='replace');
 if proc.returncode: raise RuntimeError(proc.stdout+'\n'+proc.stderr)
 coff=Coff(str(obj)); assert not any(s['name'].startswith('.CRT$XC') for s in coff.sections[1:] if s); assert not any(s['name'].startswith(('??__E','$E')) for s in coff.symbols.values())
 for e,row in zip(entries,data['entries']):
  raw,rel,sec,flags,storage=splice.slice_entry(coff,e)
  assert raw.hex()==row['reference_hex'] and not rel and sec==row['section'] and storage==2,(e['name'],raw.hex(),rel,sec,storage)
  row['validation']['isolated_vc2008_object_bytes_section_storage_relocations']=True
  row['tested_emission']={'name':e['name'],'coff_symbol':e['sym'],'compiler':'VC2008 SP1','flags':'/MT /Od /Oy- /GS /EHsc /Gy'}
data['scope'] += ' Isolated exact candidate M3-named scalar definitions compiled and checked through splice.slice_entry; full integrated build remains outstanding.'
data['selection_ready_for_compile']=False;data['selection_ready_for_integration']=True
p.write_text(json.dumps(data,indent=2),encoding='utf8');print('PASS isolated object:',len(entries),'entries',sum(e['size'] for e in entries),'bytes')
