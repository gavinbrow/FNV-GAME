def main():
    import os, sys
    saved_path = list(sys.path)
    saved_argv = list(sys.argv)
    saved_env = dict(os.environ)
    saved_bytecode = sys.dont_write_bytecode
    try:
        import sys,json,tempfile,subprocess,copy
        from pathlib import Path
        h=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(h)); import gen_m3 as g; import compile_units_v3 as cu
        from compare import Coff
        import splice
        attrs = ("GEN", "SELF", "obj_path", "compile_obj", "refbytes", "sec_of", "NEG8V", "NEG8P", "ANYNEG")
        saved_attrs = {key: getattr(g, key) for key in attrs}
        saved_manifest = splice.MANIFEST
        saved_render_stat = g.RENDER_STAT.copy()
        try:
            rows=json.loads((h/'inventory/b8_other_names_accepted.json').read_text())['entries']; selection=[dict(x['selection'],generated_name='M3_%08x'%x['selection']['va'],batch=8) for x in rows]
            entries=g.build_entries(selection); assert all(e['name'].startswith('M3_') and e['sym'] is None and e['batch']==8 for e in entries)
            # Add synthetic zero arrays and W objects for both sections, avoiding original bytes.
            orig_ref,orig_sec=g.refbytes,g.sec_of
            fake={0x02000000:'.data',0x02000010:'.rdata',0x02000020:'.data',0x02000030:'.rdata'}
            g.refbytes=lambda va,n: bytes(n) if va in fake else orig_ref(va,n)
            g.sec_of=lambda va: fake.get(va) or orig_sec(va)
            zeros=[{'va':x,'tc':'A','et':'E','size':4,'file_backed':True,'generated_name':'M3_%08x'%x,'batch':8} for x in list(fake)[:2]]+ [{'va':x,'tc':'W','size':4,'runs':[['B',4]],'kind':'test','align':4,'named':False,'file_backed':True,'batch':8} for x in list(fake)[2:]]
            entries+=g.build_entries(zeros)
            ptrs=[x for x in json.loads((h/'batch3_selection.json').read_text())['entries'] if x['tc']=='P']; ptr=ptrs[0]; ptr2=next(x for x in ptrs if x['tgt']==ptr['tgt'] and x['ptr']!=ptr['ptr']);entries+=g.build_entries([ptr,ptr2])
            with tempfile.TemporaryDirectory(prefix='b8_gen_review_') as tmp:
             t=Path(tmp); obj=t/'m3.obj'; src=t/'m3.cpp';src.write_text(g.cpp(entries),encoding='utf8');tc=cu.find_toolchains()['sp1'];vc=Path(tc['vc']);env=cu.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);env['TMP']=env['TEMP']=str(t)
             r=subprocess.run([str(vc/'bin/cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy',str(src),'/Fo'+str(obj)],cwd=t,env=env,text=True,capture_output=True,errors='replace');assert r.returncode==0,r.stdout+'\n'+r.stderr
             g.obj_path=lambda k:str(obj); bad=g.check(entries);assert not bad,bad
             c=Coff(str(obj));assert all(e['sym'] and e['sym'].startswith('?M3_') for e in entries[:-2]); print('PASS:',len(rows),'accepted heads, four zero fixtures, two pointers; actual g.check matched bytes, sections, relocations and sym mapping')
            # Execute exactly the mutation branches from the source, without main/shared outputs.
            branches=(h/'gen_m3.py').read_text().split('    if NEG8V:\n',1)[1].split('    if NEG7V:\n',1)[0]; import textwrap; code=textwrap.dedent('    if NEG8V:\n'+branches)
            for flag in ('NEG8V','NEG8P'):
             es=copy.deepcopy(entries); env2={'entries':es,'NEG8V':flag=='NEG8V','NEG8P':flag=='NEG8P','fmt':g.fmt,'TLO':g.TLO,'THI':g.THI}
             try:
              exec(code,env2); changed=next(e for e in es if e.get('negctl'))
              with tempfile.TemporaryDirectory(prefix='b8_ctl_review_') as tmp:
               t=Path(tmp); src=t/'control.cpp'; obj=t/'control.obj';src.write_text(g.cpp(es),encoding='utf8');env['TMP']=env['TEMP']=str(t)
               proc=subprocess.run([str(vc/'bin/cl.exe'),'/c','/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy',str(src),'/Fo'+str(obj)],cwd=t,env=env,text=True,capture_output=True,errors='replace');assert proc.returncode==0,proc.stdout+proc.stderr
               c=Coff(str(obj))
               try:
                raw,rel,sec,fl,st=splice.slice_entry(c,changed); print('CONTROL',flag,'section',sec,'bytes',raw.hex(),'relocs',rel)
               except ValueError as exc: print('CONTROL',flag,'not file-backed:',exc)
             except Exception as exc: print('FAIL mutation',flag,type(exc).__name__,str(exc))

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
