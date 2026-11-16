"""verify_v7 (verify_contrib with v5 relocation resolution + EH funclet/tail extraction): compile every accepted local-target contribution exactly as FNV/scripts/local_targets.py check() does,
verify independently against reference bytes (relocation fields resolved like the build; unresolved/disagreeing fields borrowed),
write contrib_status.csv, contrib_pieces.json (verified pieces incl. relocation site logs) and contrib.jsonl (one line per target).
Read-only on FNV; writes only under build-v7. usage: python -I verify_contrib.py [jobs]"""
import sys, os, json, csv, subprocess, hashlib, shutil, struct, collections, bisect
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')))
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
RN = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(RN / 'pinned-build')); sys.path.insert(0, str(RN / 'coverage-v3'))
sys.path.insert(0, (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\FNV\scripts'))
import assemble_v7 as V
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
        tid, t0 = by_addr[addr]
        t = dict(t0); t['compiler'] = a.get('compiler') or t0['compiler']          # accepted record overrides catalog (as the checker's submit stored them)
        t['flags'] = list(a['flags']) if a.get('flags') else (t0['flags'] if t['compiler'] == t0['compiler'] else LT._flags_for(t['compiler'], t0))
        t['entry'] = (a.get('entry') or '').strip(); t['catalog_flags'] = list(t0['flags'])
        cat[tid] = t
        src = LT.CONTRIB / ('FUN_%s.cpp' % addr[2:])
        r = dict(target_id=tid, address=addr, size=t['size'], kind=t['kind'], compiler=t['compiler'], flags_override=int(bool(a.get('flags'))), entry=t['entry'], status='fail', reason='',
                 sha_matches_accepted='', reloc_agree=0, reloc_borrowed=0, checker_verdict='')
        rows[addr] = r
        if not src.exists():
            r['reason'] = 'source-missing'; continue
        raw = src.read_bytes()
        r['sha_matches_accepted'] = int(hashlib.sha256(raw).hexdigest() == a.get('sha256'))
        if not r['sha_matches_accepted']:   # the checker hashed/compiled candidate.cpp with CRLF line ends; the contribution file was written LF
            crlf = raw.replace(bytes([13, 10]), bytes([10])).replace(bytes([10]), bytes([13, 10]))
            if hashlib.sha256(crlf).hexdigest() == a.get('sha256'):
                (HERE / 'src').mkdir(exist_ok=True); src = HERE / 'src' / (tid + '.cpp'); src.write_bytes(crlf); r['sha_matches_accepted'] = 2
        jobs.append((tid, t, src))
    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 12) as ex:
        cres = {tid: (ok, err) for tid, ok, err in ex.map(compile_one, jobs)}
    shutil.rmtree(TMP, ignore_errors=True); shutil.rmtree(HERE / 'src', ignore_errors=True)
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
    pieces = []; eh = []
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
            if t['kind'] == 'text_data':   # w1: same gate as local_targets.check(): const data in a .text* section may be the entry
                funcs += [s for s in coff.symbols.values() if s['section'] > 0 and not s['type'] & 0x20 and s['storage'] in (2, 3) and coff.sections[s['section']]['name'].startswith('.text') and want.lower() in s['name'].lower()]
            inits = [s for s in funcs if s['name'].startswith(('??__E', '??__F'))]
            ent_req = t['entry']
            if ent_req: cands = [s for s in funcs if s['name'] == ent_req] or [s for s in funcs if ent_req.lower() in s['name'].lower()]
            else:
                cands = [s for s in funcs if want.lower() in s['name'].lower()] or [s for s in funcs if s['name'] in t.get('symbols_hint', [])]
                ambiguous = len(cands) > 1 and not all(s in inits for s in cands)
                if not ambiguous:
                    if cands and cands[0] not in inits: cands = cands + [s for s in inits if s not in cands]   # w1: ??__E/??__F initializers stay candidates next to a dummy FUN_ definition
                    elif (len(cands) != 1 and t['kind'] == 'static_init') or (not cands and inits): cands = inits
            if not cands or (not ent_req and ambiguous):
                r['reason'] = 'no_entry_function'; continue
            size = t['size']
            mapping = dict(LT._symbols())
            for s in coff.symbols.values():
                if s['section'] == 0 and s['storage'] == 2 and s['name'] not in mapping:
                    m = LT.ADDR_RE.search(s['name'])
                    if m: mapping[s['name']] = int(m.group(1), 16)
            scored = []
            for ce in cands:
                try: scored.append((LT._compare_entry(cm, cpe, coff, t, av, ce['name'], mapping), ce['name']))
                except ValueError as e: scored.append((dict(error=str(e)), ce['name']))
            good = [x for x in scored if 'row' in x[0]]
            if not good: r['reason'] = 'checker_error'; r['detail'] = scored[0][0].get('error', '')[:100]; continue
            good.sort(key=lambda x: (not x[0]['match'], x[0]['score']))
            ent, sym = good[0]
            r['checker_verdict'] = 'match' if ent['match'] else ('body-match-eh-differs' if ent['row']['verdict'] == 'match' else ent['row']['verdict'])
            man = dict(symbols={k: v for k, v in mapping.items() if k in coff.by_name}, functions=[dict(address=av, symbol=sym, size=size)])
            man['symbols'].update(LT._eh_bindings(coff, cpe, av, size, sym))
            s = coff.named(sym); sec = coff.sections[s['section']]; start = s['value']
            nxt = [x['value'] for x in coff.symbols.values() if x['section'] == s['section'] and x['type'] & 0x20 and x['value'] > start and not x['name'].startswith('__catch$')]
            end = min(nxt) if nxt else len(sec['data'])
            if end - start < size:
                r['reason'] = 'extent_short'; continue
            if any(b not in (0xcc, 0x90) for b in sec['data'][start + size:end]):
                r['reason'] = 'extent_long'; continue
            locals_ = [(s['section'], start, av, size)]
            # ---- exception-handler pieces (handler stub + unwind funclets, .text$x) located and compared like build_and_match.eh_sections
            eh_here = []; ehbind = {}
            try:
                ufn = dict(address='0x%08x' % av, symbol=sym, size=size)
                unit2 = dict(_fnmap={sym: av}, symbols={k: hex(v) for k, v in man['symbols'].items()}, functions=[ufn], eh_tails=[1])
                rows_ = [dict(address=ufn['address'], verdict=ent['row']['verdict'])]
                epieces, _inf, _errs, data_bases, _anch = A.G['eh'](coff, pe, unit2, rows_, symnames)
                xver = {}
                for xi, xb in data_bases.items():
                    xs = coff.sections[xi]
                    if not xs['name'].startswith('.xdata'): continue
                    m = bytearray(xs['data'])
                    try: rf_ = bytearray(pe.read(xb, len(m)))
                    except ValueError: rf_ = None
                    if rf_ is not None:
                        for ro, _, rk in xs['relocs']: m[ro:ro + 4] = bytes(4); rf_[ro:ro + 4] = bytes(4)
                        if rf_ == m: xver[xi] = xb
                unit2['_xver'] = xver
                nok = nbad = 0; okranges = []
                for p_ in epieces:
                    if len(p_) < 8: nbad += 1; continue
                    at, end, ok, parent, guessed, pdata, index, s0 = p_
                    if not ok: nbad += 1; continue
                    b2 = bytearray(pdata); V._log.clear(); V._tsec.clear()
                    A.fill_relocs(coff, unit2, locals_, coff.sections[index], s0, s0 + len(pdata), at, b2, collections.Counter(), collections.defaultdict(lambda: [0, None]), 'tail')
                    eh_here.append(dict(address=at, size=len(pdata), target_id=tid, ok=True, data=bytes(b2).hex(), sites=[list(e) for e in V._log], tsec=dict(V._tsec))); nok += 1
                    okranges.append((at, at + len(pdata)))
                r['eh_ok'] = nok; r['eh_notok'] = nbad
                # the body's __ehhandler$ relocation resolves to OUR placed stub when its piece verified (placement itself is where the checker verified it)
                for nm_, ad_ in LT._eh_bindings(coff, cpe, av, size, sym).items():
                    if any(lo_ <= ad_ < hi_ for lo_, hi_ in okranges): ehbind[nm_] = ad_
            except Exception as e:
                eh_here = []; r['eh_error'] = str(e)[:100]
            unit = dict(_fnmap={sym: av}, symbols=symmap, functions=[])
            buf = bytearray(sec['data'][start:start + size])
            V._log.clear(); V._tsec.clear(); V.EHBIND.clear(); V.EHBIND.update(ehbind)
            st = collections.Counter(); pats = collections.defaultdict(lambda: [0, None])
            A.fill_relocs(coff, unit, locals_, sec, start, start + size, av, buf, st, pats, 'contrib')
            sites = [list(e) for e in V._log]; tsec = dict(V._tsec); V.EHBIND.clear()
            ref = pe.read(av, size)
            if bytes(buf) != ref:
                r['reason'] = 'bytes_differ'; r['detail'] = 'first diff at +%d' % next(i for i in range(size) if buf[i] != ref[i]); continue
            ag = sum(1 for e in sites if e[6] == 'agree'); r['reloc_agree'] = ag; r['reloc_borrowed'] = len(sites) - ag
            if overlaps_recipe(av, av + size):
                r['reason'] = 'overlaps_recipe'; continue
            r['status'] = 'pass'
            pieces.append(dict(address=av, size=size, target_id=tid, data=bytes(buf).hex(), sites=sites, tsec=tsec))
            eh.extend(eh_here)
        except Exception as e:
            r['reason'] = 'verify_error'; r['detail'] = str(e)[:150]
    fields = ['eh_ok', 'eh_notok', 'eh_error', 'target_id', 'address', 'size', 'kind', 'compiler', 'status', 'reason', 'detail', 'sha_matches_accepted', 'checker_verdict', 'reloc_agree', 'reloc_borrowed']
    with open(HERE / 'contrib_status.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fields, extrasaction='ignore'); w.writeheader()
        for r in rows.values(): w.writerow(r)
    with open(HERE / 'contrib.jsonl', 'w') as f:
        for r in rows.values(): f.write(json.dumps(r) + '\n')
    (HERE / 'contrib_pieces.json').write_text(json.dumps(dict(pieces=pieces, eh=eh)))
    c = collections.Counter(r['status'] if r['status'] == 'pass' else r['reason'] for r in rows.values())
    print('eh pieces', len(eh), 'bytes', sum(t['size'] for t in eh)); print('accepted', len(rows), dict(c), 'pass bytes', sum(p['size'] for p in pieces))
    print('checker verdict among pass:', dict(collections.Counter(r['checker_verdict'] for r in rows.values() if r['status'] == 'pass')),
          'sha mismatch:', sum(1 for r in rows.values() if r.get('sha_matches_accepted') == 0))


if __name__ == '__main__':
    main()
