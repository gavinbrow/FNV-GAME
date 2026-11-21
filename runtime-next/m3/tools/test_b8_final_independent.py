def main():
    import os, sys
    saved_path = list(sys.path)
    saved_argv = list(sys.argv)
    saved_env = dict(os.environ)
    saved_bytecode = sys.dont_write_bytecode
    try:
        import sys,json,tempfile,subprocess,os,hashlib
        from pathlib import Path
        h=Path(__file__).resolve().parents[1];sys.path.insert(0,str(h));import gen_m3 as g;import splice;import compile_units_v3 as cu
        from compare import Coff
        attrs = ("GEN", "SELF", "obj_path", "compile_obj", "refbytes", "sec_of", "NEG8V", "NEG8P", "ANYNEG")
        saved_attrs = {key: getattr(g, key) for key in attrs}
        saved_manifest = splice.MANIFEST
        saved_render_stat = g.RENDER_STAT.copy()
        try:
            f=h/'batch8_final_selection.json';raw=f.read_bytes();assert hashlib.sha256(raw).hexdigest()=='42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7'
            j=json.loads(raw);sel=j['entries'][-j['added']['entries']:];assert len(sel)==64 and sum((4 if e['tc']=='P' else g.TYPES[e['tc']][1] if e['tc'] in g.TYPES else e['size']) for e in sel)==36597
            for va,n in [(0x103ae48,165),(0x103aef0,163)]:
             matches=[e for e in sel if e['va']==va];assert len(matches)==1 and matches[0]['tc']=='A' and matches[0]['size']==n and matches[0]['partial']
            tc=cu.find_toolchains()['sp1'];vc=Path(tc['vc']);env=cu.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None)
            with tempfile.TemporaryDirectory(prefix='b8_final_independent_') as tmp:
             t=Path(tmp);g.GEN=str(t);g.SELF=str(t/'selected.json');Path(g.SELF).write_text(json.dumps({'entries':sel}));splice.MANIFEST=str(t/'manifest.json');g.obj_path=lambda k:str(t/('m3_data.obj' if k==0 else 'm3_data_%d.obj'%k));os.environ['FNV_M3_SEL']='selected.json';sys.argv=['gen_m3.py'];env['TMP']=env['TEMP']=str(t)
             def compile_fixture(entries):
              for k in sorted({e.get('obj',0) for e in entries}):
               src=t/('m3_%d.cpp'%k); obj=Path(g.obj_path(k));src.write_text(g.cpp([e for e in entries if e.get('obj',0)==k]),encoding='utf8');p=subprocess.run([str(vc/'bin/cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy',str(src),'/Fo'+str(obj)],cwd=t,env=env,text=True,capture_output=True,errors='replace');assert p.returncode==0,p.stdout+'\n'+p.stderr
             g.compile_obj=compile_fixture
             for mode in ('positive','b8v','b8p'):
              g.NEG8V=mode=='b8v';g.NEG8P=mode=='b8p';g.ANYNEG=mode!='positive';g.main();man=json.loads(Path(splice.MANIFEST).read_text());log=json.loads((t/'m3_gen.log.json').read_text());assert log['selected']==log['kept']==64 and not log['dropped'];assert len(man['entries'])==64
              changes=[e for e in man['entries'] if e.get('negctl')];assert len(changes)==(0 if mode=='positive' else 1)
              if changes:
               e=changes[0];data,rel,sec,flags,storage=splice.slice_entry(Coff(g.obj_path(e.get('obj',0))),e);assert sec==e['section'] and storage==2
               if mode=='b8v':assert data.hex()!=e['ref'];print(mode,'changed',e['name'],'old',e['ref'],'new',data.hex())
               else:assert len(rel)==1 and splice.resolve(rel[0][1])+rel[0][2] != int.from_bytes(bytes.fromhex(e['ref']),'little');print(mode,'changed',e['name'],'target',rel[0][1])
              else:print(mode,'all 64 selected and matched')
        finally:
            for key, value in saved_attrs.items():
                setattr(g, key, value)
            splice.MANIFEST = saved_manifest
            g.RENDER_STAT.clear()
            g.RENDER_STAT.update(saved_render_stat)
    finally:
        sys.path[:] = saved_path
        sys.argv[:] = saved_argv
        os.environ.clear()
        os.environ.update(saved_env)
        sys.dont_write_bytecode = saved_bytecode


if __name__ == "__main__":
    main()
