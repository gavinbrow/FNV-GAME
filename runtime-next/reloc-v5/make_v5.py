# builds assemble_v5.py from build-v4/assemble_v4.py (v4 itself is not modified)
s = open('C:/Projects/Decompilation/runtime-next/build-v4/assemble_v4.py', encoding='utf-8').read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old[:60], s.count(old))
    s = s.replace(old, new)

rep('"""assemble_v4: true-strict', '"""assemble_v5 (copy of v4 + fixes, see NOTES.md): true-strict')
rep("sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV))", "sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV)); sys.path.insert(0, str(HERE))")
# --- worker: tsec log, ___ImageBase, SECREL accounting, optional callee fixups
rep("_log = []\n", "_log = []\n_tsec = {}\nFIX = {}\n")
rep("""        src, exp = orig_rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        _log.append(""", """        src, exp = orig_rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        if src is None and tsym['name'] == '___ImageBase': src, exp = 'linker-imagebase', (A.G['pe'].base + addend) & M32
        if FIX and src == 'a' and field_va in FIX: src, exp = 'a-fixup', FIX[field_va]
        _tsec[field_va] = tsym['section']
        _log.append(""")
rep("""            if raw is not None and exp is not None and kind in (6, 7, 0x14):""", """            if raw is not None and exp is not None and kind == 0x0B:
                try: st = 'agree' if (pe.secrel(exp) & M32) == struct.unpack('<I', raw)[0] else 'disagree'
                except ValueError: st = 'borrow'
            elif raw is not None and exp is not None and kind in (6, 7, 0x14):""")
rep("""def init4(*a):
    A.init(*a)""", """def init4(*a):
    A.init(*a)
    import os as _os
    if _os.environ.get('FNV_V5_FIXUPS') == '1':
        FIX.update({int(k): v for k, v in json.loads((HERE / 'callee_fixups.json').read_text())['fixups'].items()})""")
rep("""    _log.clear()
""", """    _log.clear(); _tsec.clear()
""")
rep("    out['rl'] = [tuple(e) for e in _log]\n", "    out['rl'] = [tuple(e) for e in _log]; out['tsec'] = dict(_tsec)\n")
# --- CRT
LIB = 'C:/Projects/Decompilation/FNV/tools/vc2008/VC/lib'
i = s.index('    crt, crt_rej, nmatch = run_crt4('); j = s.index(chr(10), i)
NL = chr(10)
s = s[:i] + ('    import crt5' + NL + '    dsecs = [(pe.base + rva, bytes(orig[raw:raw + rsz])) for (rva, vs, rsz, raw) in pe.sections[1:] if rsz]' + NL + "    crt, crt_rej, nmatch, crt5stat = crt5.run_crt5(BE, units, pe, cover, TEXT_VA, rs, ref, Path('%s'), ehm, dsecs)" % LIB) + s[j:]
rep("    crt_stat = collections.Counter(matched=nmatch,", "    crt_stat = collections.Counter(matched=nmatch,")
open('assemble_v5.py', 'w', encoding='utf-8').write(s)
print('ok')
