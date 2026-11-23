r"""Batch 10 step B build mode (FNV_M3_DATASRC=1): compile m3/datasrc/*.cpp (the data as source) instead of regenerating placeholders from the reference.
Reads datasrc/index.json (addresses, sizes, objects, expected relocation sites -> target VAs, hash of the non-pointer bytes); never opens the reference image.
Same outputs as gen_m3.py (m3\gen: m3_data*.obj, m3_manifest.json, skip_ranges.json, m3_gen.log.json).
Env: FNV_M3_DATASRC_DIR=<dir>  use another copy of the datasrc directory (default m3\datasrc)
     FNV_M3_NEGCTL=dsv|dsp     negative controls for an edited datasrc copy (a literal / a pointer): objects that fail the self-check are exempt, the round trip must fail."""
import os, sys, json, re, hashlib, subprocess, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
sys.path.insert(0, os.path.join(PROJ, 'runtime-next', 'pinned-build'))
import splice
GEN = splice.GEN
DIR = os.path.abspath(os.environ.get('FNV_M3_DATASRC_DIR') or os.path.join(HERE, 'datasrc'))
NEG = os.environ.get('FNV_M3_NEGCTL') in ('dsv', 'dsp')
M32 = 0xffffffff


def obj_path(k): return splice.OBJ if k == 0 else splice.objpath(splice.OBJ, k)


def compile_all(files, jobs=8):
    import compile_units_v3 as CU
    from pathlib import Path
    tc = CU.find_toolchains()['sp1']; assert tc.get('ok'), tc
    vc = Path(tc['vc']); env = CU.make_env(vc, Path(tc['sdk']) if tc['sdk'] != 'None' else None)
    tmp = os.path.join(GEN, 'tmp'); os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(GEN):
        if re.fullmatch(r'm3_data(_\d+)?\.(obj|cpp)', f): os.remove(os.path.join(GEN, f))
    pend = list(files); run = []; fail = []
    while pend or run:
        while pend and len(run) < jobs:
            k, fn = pend.pop(0); e2 = dict(env); tk = os.path.join(tmp, str(k)); os.makedirs(tk, exist_ok=True); e2['TMP'] = e2['TEMP'] = tk
            p = subprocess.Popen([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo', '/MT', '/Od', '/Oy-', '/GS', '/EHsc', '/Gy', '/I' + os.path.join(PROJ, 'fnv_decomp', 'include'),
                                  os.path.join(DIR, fn), '/Fo' + obj_path(k)], cwd=GEN, env=e2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace', stdin=subprocess.DEVNULL)
            run.append((k, p))
        k, p = run.pop(0); out, err = p.communicate()
        if p.returncode or not os.path.exists(obj_path(k)): fail.append('object %d: %s %s' % (k, out[-1500:], err[-1500:]))
    if fail: raise SystemExit('datasrc compile failed:\n' + '\n'.join(fail))


def check(entries, externs):
    from compare import Coff
    cs = {}; byname = {e['name']: e['va'] for e in entries}; symmap = {}; bad = {}
    for k in sorted({e['obj'] for e in entries}):
        c = cs[k] = Coff(obj_path(k))
        if any(s['name'].startswith('.CRT$XC') for s in c.sections[1:] if s) or any(s['name'].startswith(('??__E', '$E')) for s in c.symbols.values()):
            raise SystemExit('dynamic initializer in datasrc object %d' % k)
        for sy in c.symbols.values():
            if sy['section'] <= 0: continue
            m = splice.SYM_RE.match(sy['name'])
            if m: symmap[int(m.group(1), 16)] = sy['name']
            elif sy['name'].startswith('_') and sy['name'][1:] in byname: symmap[byname[sy['name'][1:]]] = sy['name']
    for e in entries: e['sym'] = symmap.get(e['va'])
    tab = splice.name_table([e for e in entries if e['sym']])
    for n, v in externs.items(): tab[n] = v; tab['_' + n] = v
    for e in entries:
        if not e['sym']: bad[e['name']] = 'symbol not defined in the object'; continue
        try: data, rel, sname, fl, st = splice.slice_entry(cs[e['obj']], e)
        except Exception as ex: bad[e['name']] = 'symbol: %s' % ex; continue
        r = None
        if st != 2: r = 'storage %d' % st
        elif sname != e['section']: r = 'section %s != %s' % (sname, e['section'])
        elif len(data) != e['size']: r = 'size %d != %d' % (len(data), e['size'])
        elif [x[0] for x in rel] != [x[0] for x in e['_relocs']]: r = 'reloc sites %s != index %s' % ([x[0] for x in rel][:6], [x[0] for x in e['_relocs']][:6])
        else:
            buf = bytearray(data)
            for (off, nm, add), (o2, tv) in zip(rel, e['_relocs']):
                t = splice.resolve(nm, tab)
                if t is None: r = 'offset %d: unresolvable target %s' % (off, nm); break
                if (t + add) & M32 != tv: r = 'offset %d: target %x + addend %d != %x' % (off, t, add, tv); break
                buf[off:off + 4] = b'\0\0\0\0'
            if r is None and hashlib.sha256(bytes(buf)).hexdigest() != e['_h']: r = 'non-pointer bytes differ from the datasrc index'
        if r:
            if NEG: e['negctl'] = True; print('NEGATIVE CONTROL (datasrc edit) detected in %s (va %08x): %s' % (e['name'], e['va'], r)); continue
            bad[e['name']] = r
    return bad


def main():
    idx = json.load(open(os.path.join(DIR, 'index.json')))
    entries = []
    for d in idx['entries']:
        e = dict(sym=None, name=d['name'], va=d['va'], size=d['size'], section=d['section'], tc=d['tc'], kind=d['kind'], type=d['kind'], obj=d['obj'],
                 fields=[[o, '', 0] for o, tv in d['relocs']], _relocs=d['relocs'], _h=d['h'], datasrc=True)
        if d.get('align'): e['align'] = d['align']
        if d.get('file_backed'): e['file_backed'] = True
        entries.append(e)
    compile_all([tuple(x) for x in idx['files']])
    bad = check(entries, idx.get('externs', {}))
    if bad: raise SystemExit('datasrc objects failed the self-check: %s' % dict(list(bad.items())[:20]))
    man = [{k: v for k, v in e.items() if not k.startswith('_')} for e in entries]
    json.dump(dict(entries=man, negctl=NEG, objs=sorted({e['obj'] for e in entries}), externs=idx.get('externs', {}), datasrc=dict(dir=os.path.basename(DIR), index_sha256=hashlib.sha256(open(os.path.join(DIR, 'index.json'), 'rb').read()).hexdigest())), open(splice.MANIFEST, 'w'), indent=0)
    json.dump([[e['va'], e['size']] for e in entries], open(os.path.join(GEN, 'skip_ranges.json'), 'w'))
    tot = collections.Counter()
    for e in entries: tot[e['section']] += e['size']
    log = dict(selected=len(entries), kept=len(entries), dropped={}, bytes_by_section=dict(tot), by_type=dict(collections.Counter(e['type'] for e in entries)), selection='datasrc', negctl=NEG,
               kinds=dict(collections.Counter(e['kind'] for e in entries)), kind_bytes=dict(sum((collections.Counter({e['kind']: e['size']}) for e in entries), collections.Counter())),
               objs=len({e['obj'] for e in entries}), reference_reads=0)
    json.dump(log, open(os.path.join(GEN, 'm3_gen.log.json'), 'w'), indent=1)
    print('datasrc globals: kept %d bytes %s' % (len(entries), dict(tot)))


if __name__ == '__main__': main()
