import re
P = r'C:\path\to\Decompilation\runtime-next\m3\gen_m3.py'
s = open(P, encoding='utf-8').read()
g = open(r'C:\path\to\Decompilation\runtime-next\m3\b7_gcode.py', encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new, cnt)


rep("Self-check: every kept definition's bytes", """Batch 7: FNV_M3_SEL=batch7_selection.json (b7_select.py writes it: batch4 + generic typed objects 'G' for namespaced-only globals, scalar-declared tables, undeclared tails).
Env:   FNV_M3_NEGCTL=b7v (first new object with a dword run: first dword +1) / b7p (first new object with a pointer cell: retargeted); both exempt from the self-check.
Entries beyond batch 4 are compiled into extra objects m3_data_<k>.obj (a COFF section holds at most 65535 relocations); entry['obj'] = k.
Self-check: every kept definition's bytes""")
rep("NEG4P = os.environ.get('FNV_M3_NEGCTL') == 'b4p'\n", "NEG4P = os.environ.get('FNV_M3_NEGCTL') == 'b4p'\nNEG7V = os.environ.get('FNV_M3_NEGCTL') == 'b7v'      # batch 7 negative controls: a value / a pointer inside the new generic objects\nNEG7P = os.environ.get('FNV_M3_NEGCTL') == 'b7p'\nANYNEG = NEG or NEGP or NEG4V or NEG4P or NEG7V or NEG7P\n")
rep("\ndef build_entries(sel):\n    out = []\n    for r in sel:\n        va, tc = r['va'], r['tc']; n = sec_of(va)\n",
    "\n" + g + "\ndef build_entries(sel):\n    out = []\n    for r in sel:\n        va, tc = r['va'], r['tc']; n = sec_of(va)\n"
    "        if tc == 'G':        # batch 7: generic typed object (run descriptors frozen in the selection, items re-derived from the reference bytes)\n"
    "            raw = refbytes(va, r['size']); runs = [list(x) for x in r['runs']]; items = g_items(va, raw, runs); nm = ('DAT_%08x' if r.get('named') else 'M3_%08x') % va\n"
    "            e = dict(sym=None, name=nm, ns=r.get('ns') or '', va=va, size=r['size'], type='M3S', tc='G', section=n, kind=r['kind'], ref=raw.hex(), align=r['align'], runs=runs, items=items, decl=r.get('decl'), head=r.get('head'))\n"
    "            g_fields(e); out.append(e); continue\n")

# cpp(): G entries (struct + namespaced definitions), restricted to the entries of one object
rep("""def cpp(entries):
    L = ['// M3 phase 1: generated DAT_ globals (gen_m3.py). Do not edit.']
    ents = sorted(entries, key=lambda x: x['va']); starts = [x['va'] for x in ents]
    ext = {}; hostdecl = {}; defs = []; RENDER_STAT.clear()
""", """def cpp(entries):
    L = ['// M3 phase 1: generated DAT_ globals (gen_m3.py). Do not edit.']
    gents = [e for e in entries if e['tc'] == 'G']; entries = [e for e in entries if e['tc'] != 'G']
    ents = sorted(entries, key=lambda x: x['va']); starts = [x['va'] for x in ents]
    ext = {}; hostdecl = {}; defs = []; RENDER_STAT.clear()
""")
rep("""    L += [ext[k] for k in sorted(ext)]
    for va in sorted(hostdecl):
        ty, nm = tyname(hostdecl[va]); L.append('extern %s %s;' % (ty, nm))
    return '\\n'.join(L + defs) + '\\n'
""", """    gdef = {}; gstruct = []
    for e in gents:
        sd, ini = g_render(e, ext); gstruct.append(sd)
        gdef.setdefault(e['ns'], []).append('%sstruct M3S_%08x %s = %s;' % ('extern const ' if e['section'] == '.rdata' else '', e['va'], e['name'], ini))
    L += [ext[k] for k in sorted(ext)]
    for va in sorted(hostdecl):
        ty, nm = tyname(hostdecl[va]); L.append('extern %s %s;' % (ty, nm))
    if gstruct: L += ['#pragma pack(push, 1)'] + gstruct + ['#pragma pack(pop)']
    for ns in sorted(gdef):
        if ns: defs += ['namespace %s {' % ns] + gdef[ns] + ['}']
        else: defs += gdef[ns]
    return '\\n'.join(L + defs) + '\\n'
""")

# compile_obj(): one object per group
rep("""def compile_obj(entries):
    import compile_units_v3 as CU
""", """def obj_path(k): return splice.OBJ if k == 0 else splice.objpath(splice.OBJ, k)


def compile_obj(entries):
    \"\"\"compile every object group (entry['obj']) with the unit compiler; objects in parallel. -> None (raises on failure)\"\"\"
    import glob
    for f in glob.glob(os.path.join(GEN, 'm3_data_*.obj')): os.remove(f)
    groups = collections.defaultdict(list)
    for e in entries: groups[e.get('obj', 0)].append(e)
    procs = []
    for k in sorted(groups): procs.append((k, compile_one(groups[k], k)))
    for k, p in procs:
        out, err = p.communicate()
        if p.returncode or not os.path.exists(obj_path(k)): raise SystemExit('m3 compile failed (object %d):\\n' % k + out[-2000:] + err[-2000:])


def compile_one(entries, k):
    import compile_units_v3 as CU
""")
rep("""    src = os.path.join(GEN, 'm3_data.cpp'); open(src, 'w').write(cpp(entries))
    if os.path.exists(splice.OBJ): os.remove(splice.OBJ)
    r = subprocess.run([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo', '/MT', '/Od', '/Oy-', '/GS', '/EHsc', '/Gy', '/I' + os.path.join(PROJ, 'fnv_decomp', 'include'),
                        src, '/Fo' + splice.OBJ], cwd=GEN, env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    if r.returncode or not os.path.exists(splice.OBJ): raise SystemExit('m3 compile failed:\\n' + r.stdout[-2000:] + r.stderr[-2000:])
""", """    src = os.path.join(GEN, 'm3_data.cpp' if k == 0 else 'm3_data_%d.cpp' % k); open(src, 'w').write(cpp(entries))
    if os.path.exists(obj_path(k)): os.remove(obj_path(k))
    tk = os.path.join(tmp, str(k)); os.makedirs(tk, exist_ok=True); env['TMP'] = env['TEMP'] = tk
    return subprocess.Popen([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo', '/MT', '/Od', '/Oy-', '/GS', '/EHsc', '/Gy', '/I' + os.path.join(PROJ, 'fnv_decomp', 'include'),
                             src, '/Fo' + obj_path(k)], cwd=GEN, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace', stdin=subprocess.DEVNULL)
""")

# check(): per object, G entries, symbol discovery with namespaces
rep("""def check(entries):
    from compare import Coff
    c = Coff(splice.OBJ); bad = {}
    if any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s) or any(s['name'].startswith(('??__E', '$E')) for s in c.symbols.values()):
        raise SystemExit('dynamic initializer in the m3 object')
    symmap = {}
    for sy in c.symbols.values():
        m = re.match(r'\\?DAT_([0-9a-f]{8})@@3', sy['name'])
        if m and sy['section'] > 0: symmap[int(m.group(1), 16)] = sy['name']
    for e in entries:
        if e.get('sym') is None: e['sym'] = symmap.get(e['va'])
    tab = splice.name_table([e for e in entries if e.get('sym')])
    for e in entries:
        if (NEG or NEGP or NEG4V or NEG4P) and e.get('negctl'): continue
        if not e.get('sym'): bad[e['name']] = 'symbol not defined in the object'; continue
""", """def check(entries):
    from compare import Coff
    bad = {}; cs = {}; symmap = {}
    for k in sorted({e.get('obj', 0) for e in entries}):
        c = cs[k] = Coff(obj_path(k))
        if any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s) or any(s['name'].startswith(('??__E', '$E')) for s in c.symbols.values()):
            raise SystemExit('dynamic initializer in the m3 object %d' % k)
        for sy in c.symbols.values():
            m = splice.SYM_RE.match(sy['name'])
            if m and sy['section'] > 0: symmap[int(m.group(1), 16)] = sy['name']
    for e in entries:
        if e.get('sym') is None: e['sym'] = symmap.get(e['va'])
    tab = splice.name_table([e for e in entries if e.get('sym')])
    for e in entries:
        c = cs[e.get('obj', 0)]
        if ANYNEG and e.get('negctl'): continue
        if not e.get('sym'): bad[e['name']] = 'symbol not defined in the object'; continue
""")
rep("""        elif e['tc'] in ('A', 'T', 'X'):
            r = check_elems(e, data, rel, tab)
            if r: bad[e['name']] = r
""", """        elif e['tc'] == 'G':
            r = check_g(e, data, rel, tab)
            if r: bad[e['name']] = r
        elif e['tc'] in ('A', 'T', 'X'):
            r = check_elems(e, data, rel, tab)
            if r: bad[e['name']] = r
""")

# main(): negctl, obj partition, manifest, log
rep("""    entries = build_entries(sel)
    for e in entries:
        if e['tc'] in ('T', 'X'): set_fields(e)
""", """    entries = build_entries(sel)
    for e in entries:
        if e['tc'] in ('T', 'X'): set_fields(e)
    partition(entries)
    if NEG7V:
        e = next(x for x in entries if x['tc'] == 'G' and any(c == 'U' for c, n in x['runs'])); k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'U')
        raw = e['items'][k][0]; v = (struct.unpack('<I', raw)[0] + 1) & 0xffffffff; e['items'][k][0] = struct.pack('<I', v); e['negctl'] = True
        print('NEGATIVE CONTROL (b7 value): %s run %d element 0 is now %08x (reference bytes %s)' % (e['name'], k, v, raw.hex()))
    if NEG7P:
        gs = [x for x in entries if x['tc'] == 'G' and x['tgts']]; e = gs[0]; t0 = e['tgts'][0]; code0 = TLO <= t0 < THI
        alt = next(t for x in gs for t in x['tgts'] if (TLO <= t < THI) == code0 and t != t0)
        k = next(i for i, (c, n) in enumerate(e['runs']) if c == 'P' and any(s for s, v in e['items'][i])); j = next(i for i, (s, v) in enumerate(e['items'][k]) if s)
        e['items'][k][j] = (True, alt); g_fields(e); e['negctl'] = True
        print('NEGATIVE CONTROL (b7 pointer): %s run %d cell %d now points to %08x instead of %08x' % (e['name'], k, j, alt, t0))
""")
rep("""    json.dump(dict(entries=[{k: v for k, v in e.items() if k not in ('elems', 'els', 'init')} if e['tc'] in ('A', 'T', 'X') else e for e in entries], negctl=NEG or NEGP or NEG4V or NEG4P), open(splice.MANIFEST, 'w'), indent=0)""",
    """    json.dump(dict(entries=[{k: v for k, v in e.items() if k not in ('elems', 'els', 'init', 'items')} if e['tc'] in ('A', 'T', 'X', 'G') else e for e in entries], negctl=ANYNEG, objs=sorted({e.get('obj', 0) for e in entries})), open(splice.MANIFEST, 'w'), indent=0)""")
rep("negctl=NEG or NEGP or NEG4V or NEG4P, kinds=", "negctl=ANYNEG, kinds=")
rep("table_pointer_fields=sum(len(e.get('fields', [])) for e in entries if e['tc'] in ('T', 'X'))", "table_pointer_fields=sum(len(e.get('fields', [])) for e in entries if e['tc'] in ('T', 'X')), g_pointer_fields=sum(len(e.get('fields', [])) for e in entries if e['tc'] == 'G'), objs=len({e.get('obj', 0) for e in entries}), kind_relocs=dict(sum((collections.Counter({e.get('kind', ''): len(e.get('fields', []))}) for e in entries if e['tc'] == 'G'), collections.Counter()))")

# partition(): before main
rep("\ndef main():\n", """
def partition(entries, max_relocs=30000, max_entries=2500):
    \"\"\"batch 7: the first 1,948 (batch 4) entries stay in object 0 (compiled exactly as before); the generic objects go to objects 1..n (<= max_relocs relocations and max_entries entries each, one COFF
    section holds at most 65535 relocations)\"\"\"
    k = 1; nr = 0; ne = 0
    for e in entries:
        if e['tc'] != 'G': e['obj'] = 0; continue
        r = len(e['fields'])
        if ne and (nr + r > max_relocs or ne >= max_entries): k += 1; nr = 0; ne = 0
        e['obj'] = k; nr += r; ne += 1


def main():
""")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
