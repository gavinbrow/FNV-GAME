"""verify_contrib: compile every accepted local-target contribution exactly as FNV/scripts/local_targets.py check() does,
verify independently against reference bytes (relocation fields resolved like the build; unresolved/disagreeing fields borrowed),
write contrib_status.csv, contrib_pieces.json (verified pieces incl. relocation site logs) and contrib.jsonl (one line per target).
Read-only on FNV; writes only under contrib-v5. usage: python -I verify_contrib.py [jobs]"""
import sys, os, json, csv, subprocess, hashlib, shutil, struct, collections, bisect
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
RN = HERE.parent
sys.path.insert(0, str(RN / 'build-v4')); sys.path.insert(0, str(RN / 'pinned-build')); sys.path.insert(0, str(RN / 'coverage-v3'))
sys.path.insert(0, r'C:\Projects\Decompilation\FNV\scripts')
import assemble_v4 as V
import assemble_v3 as A
import local_targets as LT
OBJ = HERE / 'obj'; TMP = HERE / 'tmp'
M32 = 0xffffffff


def compile_one(a):
    tid, t, src = a
    obj = OBJ / (tid + '.obj'); w = TMP / tid; w.mkdir(parents=True, exist_ok=True)
    try:
        cl, env = LT._env_for(t['compiler']); env['TMP'] = env['TEMP'] = str(w)
        if obj.exists(): obj.unlink()
        r = subprocess.run([str(cl), '/c', '/nologo'] + t['flags'] + ['/I' + str(LT.FN / 'include'), str(src), '/Fo' + str(obj)],
                           cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=300)
        ok = r.returncode == 0 and obj.exists()
        err = '' if ok else '; '.join(l.strip() for l in (r.stdout + r.stderr).splitlines() if ' error ' in l)[:200]
        return tid, ok, err
    except Exception as e:
        return tid, False, 'tool:' + str(e)[:150]
    finally:
        shutil.rmtree(w, ignore_errors=True)


def main():
    OBJ.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
    state = json.loads(LT.STATE.read_text(encoding='utf-8')); acc = state.get('accepted', {})
    cat = LT.catalog(); by_addr = {t['address']: (k, t) for k, t in cat.items()}
    rows = {}; jobs = []
    for addr, a in sorted(acc.items()):
        if addr not in by_addr:
            rows[addr] = dict(address=addr, status='fail', reason='not-in-catalog'); continue
        tid, t = by_addr[addr]
        src = LT.CONTRIB / ('FUN_%s.cpp' % addr[2:])
        r = dict(target_id=tid, address=addr, size=t['size'], kind=t['kind'], compiler=t['compiler'], status='fail', reason='',
                 sha_matches_accepted='', reloc_agree=0, reloc_borrowed=0, checker_verdict='')
        rows[addr] = r
        if not src.exists():
            r['reason'] = 'source-missing'; continue
        r['sha_matches_accepted'] = int(hashlib.sha256(src.read_bytes()).hexdigest() == a.get('sha256'))
        jobs.append((tid, t, src))
    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 12) as ex:
        cres = {tid: (ok, err) for tid, ok, err in ex.map(compile_one, jobs)}
    shutil.rmtree(TMP, ignore_errors=True)
    print('compiled', sum(1 for v in cres.values() if v[0]), 'of', len(jobs), flush=True)

    # ---- verification (same relocation resolution as the build)
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    pe = A.Pe(A.IMG); imports, thunks = A.parse_imports(pe)
    V.init4(fnnames, symnames, imports, thunks)
    cm = LT._compare_module(); cpe = LT._pe()
    rec_ranges = sorted((int(f['address'], 16), int(f['address'], 16) + f['size']) for u in units for f in u['functions'])
    starts = [r[0] for r in rec_ranges]

    def overlaps_recipe(a, b):
        i = bisect.bisect_left(starts, b)
        return any(rec_ranges[j][1] > a for j in range(max(0, i - 3), i))
    symmap = LT._read(LT.SYMBOLS, {})
    pieces = []
    for addr, r in rows.items():
        if r['status'] != 'fail' or r['reason']: continue
        tid = r['target_id']; t = cat[tid]
        ok, err = cres[tid]
        if not ok:
            r['reason'] = 'compile_error'; r['detail'] = err; continue
        try:
            coff = cm.Coff(OBJ / (tid + '.obj'))
            av = int(addr, 16); want = 'FUN_%08x' % av
            funcs = [s for s in coff.symbols.values() if s['section'] > 0 and s['type'] & 0x20 and not s['name'].startswith(('__catch$', '__unwind', '__ehhandler'))]
            entry = [s for s in funcs if want.lower() in s['name'].lower()] or [s for s in funcs if s['name'] in t.get('symbols_hint', [])]
            if len(entry) != 1 and t['kind'] == 'static_init':
                entry = [s for s in funcs if s['name'].startswith(('??__E', '??__F'))]
            if len(entry) != 1:
                r['reason'] = 'no_entry_function'; continue
            sym = entry[0]['name']; size = t['size']
            mapping = {k: int(v, 0) for k, v in symmap.items()}
            for s in coff.symbols.values():
                if s['section'] == 0 and s['storage'] == 2 and s['name'] not in mapping:
                    m = LT.ADDR_RE.search(s['name'])
                    if m: mapping[s['name']] = int(m.group(1), 16)
            man = dict(symbols={k: v for k, v in mapping.items() if k in coff.by_name}, functions=[dict(address=av, symbol=sym, size=size)])
            try: r['checker_verdict'] = cm.compare(coff, cpe, man)[0]['verdict']
            except Exception: r['checker_verdict'] = 'error'
            s = coff.named(sym); sec = coff.sections[s['section']]; start = s['value']
            nxt = [x['value'] for x in coff.symbols.values() if x['section'] == s['section'] and x['type'] & 0x20 and x['value'] > start and not x['name'].startswith('__catch$')]
            end = min(nxt) if nxt else len(sec['data'])
            if end - start < size:
                r['reason'] = 'extent_short'; continue
            if any(b not in (0xcc, 0x90) for b in sec['data'][start + size:end]):
                r['reason'] = 'extent_long'; continue
            unit = dict(_fnmap={sym: av}, symbols=symmap, functions=[])
            locals_ = [(s['section'], start, av, size)]
            buf = bytearray(sec['data'][start:start + size])
            V._log.clear()
            st = collections.Counter(); pats = collections.defaultdict(lambda: [0, None])
            A.fill_relocs(coff, unit, locals_, sec, start, start + size, av, buf, st, pats, 'contrib')
            sites = [list(e) for e in V._log]
            ref = pe.read(av, size)
            if bytes(buf) != ref:
                r['reason'] = 'bytes_differ'; r['detail'] = 'first diff at +%d' % next(i for i in range(size) if buf[i] != ref[i]); continue
            ag = sum(1 for e in sites if e[6] == 'agree'); r['reloc_agree'] = ag; r['reloc_borrowed'] = len(sites) - ag
            if overlaps_recipe(av, av + size):
                r['reason'] = 'overlaps_recipe'; continue
            r['status'] = 'pass'
            pieces.append(dict(address=av, size=size, target_id=tid, data=bytes(buf).hex(), sites=sites))
        except Exception as e:
            r['reason'] = 'verify_error'; r['detail'] = str(e)[:150]
    fields = ['target_id', 'address', 'size', 'kind', 'compiler', 'status', 'reason', 'detail', 'sha_matches_accepted', 'checker_verdict', 'reloc_agree', 'reloc_borrowed']
    with open(HERE / 'contrib_status.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fields, extrasaction='ignore'); w.writeheader()
        for r in rows.values(): w.writerow(r)
    with open(HERE / 'contrib.jsonl', 'w') as f:
        for r in rows.values(): f.write(json.dumps(r) + '\n')
    (HERE / 'contrib_pieces.json').write_text(json.dumps(dict(pieces=pieces)))
    c = collections.Counter(r['status'] if r['status'] == 'pass' else r['reason'] for r in rows.values())
    print('accepted', len(rows), dict(c), 'pass bytes', sum(p['size'] for p in pieces))
    print('checker verdict among pass:', dict(collections.Counter(r['checker_verdict'] for r in rows.values() if r['status'] == 'pass')),
          'sha mismatch:', sum(1 for r in rows.values() if r.get('sha_matches_accepted') == 0))


if __name__ == '__main__':
    main()
