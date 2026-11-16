"""assemble_v4: true-strict .text assembler. Writes only under build-v4.
Pass 1 (pool): re-run assemble_v3.process over obj_v3 for every compiled unit (functions + EH scan on all units), logging every relocation field.
Pass 2: place recipe functions, EH pieces (exact-bytes acceptance), CRT pieces (extra_pieces.json matching, re-run with logging).
Outputs: strict/filled images, progress.json, relocs_v4.tsv.gz, rebase test."""
import sys, os, json, struct, collections, time, gzip, bisect, hashlib
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
HERE = Path(__file__).resolve().parent
PB = Path(r'C:\Projects\Decompilation\runtime-next\pinned-build')
CV = Path(r'C:\Projects\Decompilation\runtime-next\coverage-v3')
sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV))
import numpy as np
import assemble_v3 as A
M32 = 0xffffffff
NEWBASE = 0x10000000

# ------------------------------------------------------------ worker
_log = []
def init4(*a):
    A.init(*a)
    orig_rf, orig_fr = A.resolve_field, A.fill_relocs
    def rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw):
        src, exp = orig_rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        _log.append([field_va, kind, src, exp, tsym['name'][:80], addend])
        return src, exp
    def fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope):
        n0 = len(_log)
        orig_fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope)
        pe = A.G['pe']; seen = set()
        for e in _log[n0:]:
            va, kind, src, exp = e[:4]; seen.add(va)
            st = 'borrow'
            try: raw = pe.read(va, 4)
            except ValueError: raw = None
            if raw is not None and exp is not None and kind in (6, 7, 0x14):
                o32, = struct.unpack('<I', raw)
                obs = (va + 4 + struct.unpack('<i', raw)[0]) & M32 if kind == 0x14 else ((o32 + pe.base) & M32 if kind == 7 else o32)
                st = 'agree' if (exp & M32) == obs else 'disagree'
            e += [st, scope]
        for off, idx, kind in sec['relocs']:
            if lo <= off < hi and base_va + off - lo not in seen:
                _log.append([base_va + off - lo, kind, 'skip', None, coff.symbols[idx]['name'][:80], 0, 'borrow', scope])
    A.resolve_field, A.fill_relocs = rf, fr

def proc4(task):
    _log.clear()
    if not task[1].get('eh_tails'):
        task[1]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    out = A.process(task)
    out['rl'] = [tuple(e) for e in _log]
    for k in ('stats', 'pats', 'borrows'): out.pop(k, None)
    return out

# ------------------------------------------------------------ CRT (copy of build_extra.run_crt with per-site logging)
def run_crt4(BE, units, pe, cover_text, TEXT_VA, rs, text, libdir, extra_cover):
    import uncovered_v2 as U
    Av2 = BE.A
    cover = cover_text.copy(); cover[extra_cover > 0] = 3
    W = 6; t = bytes(text)
    index = collections.defaultdict(list)
    for p in np.flatnonzero(cover == 0)[:-W].tolist(): index[t[p:p + W]].append(p)
    cands = []
    for lname in ('libcmt.lib', 'libcpmt.lib'):
        for mname, blob in BE.read_ar(libdir / lname):
            r = U.parse_obj(blob)
            if not r: continue
            secs, syms = r
            names = collections.defaultdict(list)
            for si, (nm, value, sec, ty, sc) in syms.items():
                if sec > 0 and sc == 2: names[sec - 1].append((value, nm))
            for k, s in enumerate(secs):
                if not (s['flags'] & 0x20) or len(s['data']) < 24 or s['name'].startswith('.text$x'): continue
                mask = bytearray(b'\x01' * len(s['data']))
                for ro, si, ty in s['relocs']:
                    for q in range(ro, min(ro + (2 if ty == 0x0a else 4), len(mask))): mask[q] = 0
                nm = sorted(names.get(k, []))
                cands.append(dict(lib=lname, member=mname, secidx=k, sec=s['name'], sym=nm[0][1] if nm else None, names=nm,
                                  data=bytes(s['data']), mask=bytes(mask), relocs=s['relocs'], syms=syms))
    cands.sort(key=lambda f: -len(f['data']))
    claimed = np.zeros(rs, np.uint8); matches = []
    for f in cands:
        data, mask = f['data'], f['mask']; L = len(data)
        k = next((i for i in range(L - W + 1) if all(mask[i:i + W])), None)
        if k is None: continue
        for p in index.get(data[k:k + W], []):
            st = p - k
            if st < 0 or st + L > rs or (cover[st:st + L] != 0).any() or claimed[st:st + L].any(): continue
            seg = t[st:st + L]
            if all(seg[i] == data[i] for i in range(L) if mask[i]):
                claimed[st:st + L] = 1; matches.append((st, f))
    defs = collections.defaultdict(set)
    for st, f in matches:
        for value, nm in f['names']: defs[nm].add(TEXT_VA + st + value)
    defaddr = {n: next(iter(v)) for n, v in defs.items() if len(v) == 1}
    seen = collections.defaultdict(set)
    for u in units:
        for fx in u['functions']:
            for n in [fx['symbol']] + fx.get('fold_aliases', []): seen[n].add(int(fx['address'], 16))
    fnn = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = Av2.BAM.recipe_names(units)
    imports, thunks = Av2.parse_imports(pe)
    Av2.G['imp'], Av2.G['thunks'] = imports, thunks
    out = []; rejected = []
    for st, f in sorted(matches, key=lambda m: m[0]):
        va = TEXT_VA + st; L = len(f['data']); buf = bytearray(f['data']); sites = []
        for ro, si, ty in f['relocs']:
            nm, value, sec, sty, sc = f['syms'][si]
            if ty not in (0x06, 0x14, 0x07) or ro + 4 > L:
                n = max(0, min(4, L - ro)); buf[ro:ro + n] = pe.read(va + ro, n)
                sites.append((va + ro, ty, 'skip', None, nm[:80], 0, 'borrow', 'crt')); continue
            fva = va + ro; orig = pe.read(fva, 4); o32, = struct.unpack('<I', orig)
            if ty == 0x14:
                addend, = struct.unpack_from('<i', buf, ro); observed = (fva + 4 + struct.unpack('<i', orig)[0]) & M32
            else:
                addend, = struct.unpack_from('<I', buf, ro); observed = o32
                if ty == 0x07: observed = (o32 + pe.base) & M32
            exp = None; src = None
            if sec > 0 and sc == 3 and sec - 1 == f['secidx']: exp, src = va + value + addend, 'self'
            elif sec > 0 and sc == 3: pass
            elif nm in defaddr: exp, src = defaddr[nm] + addend, 'lib-matched'
            elif nm in fnn: exp, src = fnn[nm] + addend, 'recipe-fn'
            elif nm in symnames: exp, src = symnames[nm] + addend, 'symbol-map'
            else:
                m = Av2.ADDR_RE.search(nm)
                if m and not nm.startswith(Av2.NOADDR_PREFIX): exp, src = int(m.group(1), 16) + addend, 'addr-in-name'
                else:
                    a_ = Av2.import_target(nm)
                    if a_ is not None: exp, src = a_ + addend, 'import'
            if exp is None:
                buf[ro:ro + 4] = orig; sites.append((fva, ty, 'unresolved', None, nm[:80], addend, 'borrow', 'crt')); continue
            exp &= M32
            fld = (exp - (fva + 4)) & M32 if ty == 0x14 else (exp if ty == 0x06 else (exp - pe.base) & M32)
            if exp == observed: buf[ro:ro + 4] = struct.pack('<I', fld); st_ = 'agree'
            else: buf[ro:ro + 4] = orig; st_ = 'disagree'
            sites.append((fva, ty, src, exp, nm[:80], addend, st_, 'crt'))
        if bytes(buf) != pe.read(va, L): rejected.append((va, L)); continue
        out.append(dict(address=va, size=L, data=bytes(buf), sites=sites, lib=f['lib'], member=f['member'], symbol=f['sym']))
    return out, rejected, len(matches)

# ------------------------------------------------------------ main
def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    T0 = time.time()
    import build_extra as BE
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (PB / 'logs' / 'compile_v3.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG); orig = pe.data
    rva0, vs0, rs, raw0 = pe.sections[0]; TEXT_VA = pe.base + rva0
    assert rs == 12441088
    ref = np.frombuffer(orig, np.uint8)[raw0:raw0 + rs]
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    results = {}
    with ProcessPoolExecutor(max(1, os.cpu_count() - 2), initializer=init4, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for r in ex.map(proc4, tasks, chunksize=8): results[r['idx']] = r
    print('pass1 done', round(time.time() - T0), 's', flush=True)

    # recipe coverage over ALL units
    cover = np.zeros(rs, np.uint8); unc = np.zeros(rs, np.uint8)   # unc: range of uncompiled unit
    for i, u in enumerate(units):
        ok = comp[i]['status'] == 'ok'
        for f in u['functions']:
            a = int(f['address'], 16) - TEXT_VA; cover[a:a + f['size']] = 1
            if not ok: unc[a:a + f['size']] = 1
    for i, u in enumerate(units):
        ok = comp[i]['status'] == 'ok'
        for t in u.get('eh_tails', []):
            a = int(t['address'], 16) - TEXT_VA; seg = cover[a:a + t['size']]; seg[seg == 0] = 2
            if not ok: unc[a:a + t['size']] = 1
    S = np.full(rs, 0xcc, np.uint8)           # strict
    Wm = np.zeros(rs, np.uint8)               # 1 fn, 2 recipe tail, 3 eh extra, 4 crt
    B = np.zeros(rs, np.uint8)                # borrowed field bytes (set to 0xCC in strict)
    rej = np.zeros(rs, np.uint8)              # ranges of located-but-rejected pieces
    sites = []                                # (va, kind, src, exp, name, addend, status, origin, unit)
    reasons = collections.Counter()

    def place(o, data, P, ents, origin, cls, unit):
        L = len(data); arr = np.frombuffer(data, np.uint8)
        S[o:o + L][P] = arr[P]; Wm[o:o + L][P] = cls
        at = TEXT_VA + o
        for e in ents:
            rel = e[0] - at
            if rel < 0 or rel >= L or not P[rel]: continue
            full = rel + 4 <= L and P[rel:rel + 4].all()
            st = e[6] if full else 'borrow'
            if st != 'agree':
                n = min(4, L - rel); m = P[rel:rel + n]
                S[o + rel:o + rel + n][m] = 0xcc; B[o + rel:o + rel + n][m] = 1
            sites.append((e[0], e[1], e[2], e[3], e[4], e[5], st, origin, unit))

    # ---- recipe functions (unit order, first placement wins as in v3)
    nfn_placed = 0
    for i, u in enumerate(units):
        r = results.get(i)
        if r is None: continue
        rl = sorted((e for e in r['rl'] if e[7] == 'fn'), key=lambda e: e[0]); keys = [e[0] for e in rl]
        for rec in r['fn']:
            if rec['data'] is None: reasons['fn-' + (rec['reason'] or '?').split(' (')[0]] += 1; continue
            o = rec['address'] - TEXT_VA; L = rec['size']
            if Wm[o:o + L].any(): reasons['fn-duplicate-address'] += 1; continue
            if rec['data'] != bytes(ref[o:o + L]): reasons['fn-bytes-differ-from-reference'] += 1; rej[o:o + L] = 1; continue
            lo = bisect.bisect_left(keys, rec['address']); hi = bisect.bisect_left(keys, rec['address'] + L)
            place(o, rec['data'], np.ones(L, bool), rl[lo:hi], 'fn', 1, i); nfn_placed += 1
    fn_bytes = int((Wm == 1).sum())
    # ---- EH pieces from obj_v3 scan: all ok pieces, exact-bytes acceptance
    pieces = []
    for i, r in results.items():
        for t in r['tails']:
            if t['data'] is None: continue
            pieces.append((t['address'], not t['ok'], i, t))
    pieces.sort(key=lambda p: (p[0], p[1], p[2]))
    eh_stat = collections.Counter(); rlcache = {}
    for at, notok, i, t in pieces:
        eh_stat['located'] += 1
        o = at - TEXT_VA; data = t['data']; L = len(data)
        if not (0 <= o and o + L <= rs): eh_stat['outside-text'] += 1; continue
        if notok:
            eh_stat['not-ok(matcher)'] += 1; seg = rej[o:o + L]; seg[Wm[o:o + L] == 0] = 1; continue
        P = (Wm[o:o + L] == 0) & (cover[o:o + L] != 1)
        if not P.any(): eh_stat['nothing-new(already placed/inside function range)'] += 1; continue
        arr = np.frombuffer(data, np.uint8)
        if not (arr[P] == ref[o:o + L][P]).all(): eh_stat['bytes-differ-from-reference'] += 1; rej[o:o + L][Wm[o:o + L] == 0] = 1; continue
        if i not in rlcache:
            ee = sorted((e for e in results[i]['rl'] if e[7] == 'tail'), key=lambda e: e[0]); rlcache[i] = (ee, [e[0] for e in ee])
        ee, kk = rlcache[i]
        ents = ee[bisect.bisect_left(kk, at):bisect.bisect_left(kk, at + L)]
        recipe = bool((cover[o:o + L][P] == 2).any())
        place(o, data, P, ents, 'tail', 2 if recipe else 3, i)
        eh_stat['accepted-in-recipe-tail' if recipe else 'accepted-outside-recipe(new)'] += 1
    # ---- old-obj EH pieces (not placed; measure only)
    ep = json.loads((CV / 'extra_pieces.json').read_text())
    old_eh = [p for p in ep['pieces'] if p['kind'] == 'eh']
    old_only = 0
    for p in old_eh:
        o = p['address'] - TEXT_VA
        old_only += int((Wm[o:o + p['size']] == 0).sum())
    ehm = np.zeros(rs, np.uint8)
    for p in old_eh: o = p['address'] - TEXT_VA; ehm[o:o + p['size']] = 1
    print('eh done', round(time.time() - T0), 's', flush=True)
    # ---- CRT
    crt, crt_rej, nmatch = run_crt4(BE, units, pe, cover, TEXT_VA, rs, ref, Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib'), ehm)
    crt_stat = collections.Counter(matched=nmatch, accepted_by_rerun=len(crt), json_crt=sum(1 for p in ep['pieces'] if p['kind'] == 'crt'))
    jc = {p['address']: p['data'] for p in ep['pieces'] if p['kind'] == 'crt'}
    crt_stat['rerun_equals_json'] = sum(1 for c in crt if jc.get(c['address']) == c['data'].hex())
    for c in crt:
        o = c['address'] - TEXT_VA; L = c['size']
        P = (Wm[o:o + L] == 0) & (cover[o:o + L] != 1)
        if not P.any(): crt_stat['nothing-new'] += 1; continue
        arr = np.frombuffer(c['data'], np.uint8)
        if not (arr[P] == ref[o:o + L][P]).all(): crt_stat['bytes-differ'] += 1; continue
        place(o, c['data'], P, [s for s in c['sites']], 'crt', 4, -1); crt_stat['placed'] += 1
    print('crt done', round(time.time() - T0), 's', flush=True)

    # ---- images
    secs = [(rva, vs, rsz, raw) for rva, vs, rsz, raw in pe.sections]
    strict = bytearray(orig); strict[raw0:raw0 + rs] = S.tobytes()
    M = Wm > 0
    filled = bytearray(orig)           # holes from reference; produced bytes from our image (non-borrowed)
    fa = np.frombuffer(filled, np.uint8)
    keep = M & (B == 0)
    fa[raw0:raw0 + rs][keep] = S[keep]
    (HERE / 'FalloutNV_v4_strict.exe').write_bytes(bytes(strict))
    (HERE / 'FalloutNV_v4_filled.exe').write_bytes(bytes(filled))
    filled_eq = bytes(filled) == bytes(orig)
    diffr = []
    if not filled_eq:
        d = np.flatnonzero(np.frombuffer(bytes(filled), np.uint8) != np.frombuffer(orig, np.uint8))
        br = np.flatnonzero(np.diff(d) > 1); st = np.concatenate(([d[0]], d[br + 1])); en = np.concatenate((d[br], [d[-1]])) + 1
        diffr = [(hex(int(a)), int(b - a)) for a, b in zip(st, en)][:50]

    # ---- progress
    padv = np.isin(ref, (0xcc, 0x00))
    ours = M & (B == 0) & ~padv
    padding = padv & (S == ref) & (B == 0)
    pad_produced = int((padding & M).sum()); pad_holes_cc = int((padding & ~M).sum())
    bor_bytes = int(B.sum())
    missing = ~ours & ~padding                 # includes borrowed field bytes
    miss_b = missing & (B == 1)
    rest = missing & (B == 0)
    cA = rest & (unc == 1)
    cB = rest & ~cA & ((rej == 1) | ((cover > 0)))
    cC = rest & ~cA & ~cB & (cover == 0) & (ref != 0x90)
    cD = rest & ~cA & ~cB & ~cC
    total = rs
    prog = dict(
        headline_pct_text_from_our_compile_or_library=round(100 * int(ours.sum()) / total, 3),
        headline_definition='.text bytes written by obj_v3 compile / SP1 CRT-lib output, non-padding (ref not 0xCC/0x00), excluding 4-byte relocation fields borrowed from the reference, divided by 12,441,088',
        raw_text_bytes=total, ours_bytes=int(ours.sum()),
        ours_by_origin={k: int((ours & (Wm == c)).sum()) for k, c in (('recipe_functions', 1), ('recipe_eh_tails', 2), ('eh_pieces_outside_recipe', 3), ('crt_lib_functions', 4))},
        padding_bytes_total=int(padding.sum()), padding_inside_produced_pieces=pad_produced, padding_holes_left_0xCC_matching_reference=pad_holes_cc,
        borrowed_relocation_field_bytes=bor_bytes, pct_if_borrowed_field_bytes_counted_as_ours=round(100 * (int(ours.sum()) + bor_bytes) / total, 3),
        missing_bytes_total=int(missing.sum()), missing_excluding_borrowed_fields=int(rest.sum()),
        missing_a_uncompiled_units_275=int(cA.sum()),
        missing_b_unverified_or_failed_pieces=int(cB.sum()),
        missing_b_detail=dict(in_recipe_range_of_compiled_unit_unplaced=int((cB & (cover > 0)).sum()), in_rejected_piece_outside_recipe=int((cB & (cover == 0)).sum())),
        missing_c_undecompiled_no_recipe_entry=int(cC.sum()),
        missing_d_everything_else=int(cD.sum()), missing_d_note='no recipe entry and reference byte is 0x90 (nop padding) or otherwise unclassified',
        missing_that_are_ref_0x00=int((rest & (ref == 0)).sum()),
        missing_with_ref_0x90=int((rest & (ref == 0x90)).sum()),
        uncompiled_units=sum(1 for c in comp.values() if c['status'] != 'ok'),
        pieces=dict(functions_placed=nfn_placed, function_bytes=fn_bytes, fn_reject_reasons=dict(reasons), eh=dict(eh_stat), crt=dict(crt_stat),
                    old_obj_eh_pieces_bytes_not_in_v4=old_only),
        filled_equals_reference=filled_eq, filled_diff_ranges=diffr,
        sha256=dict(strict=sha(bytes(strict)), filled=sha(bytes(filled)), reference=sha(orig)),
        strict_nonCC_text_bytes=int((S != 0xcc).sum()), strict_nonCC_not_produced=int(((S != 0xcc) & ~M).sum()),
    )
    # ---- relocation stats + tsv
    ssum = collections.Counter(); borrowed = 0; uniq = {}
    for s in sites: uniq[s[0]] = s
    for s in uniq.values():
        ssum[(s[7], 'k%x' % s[1], s[2], s[6])] += 1
        if s[6] != 'agree': borrowed += 1
    prog['relocation_fields'] = dict(total_in_placed_code=len(uniq), borrowed_from_reference=borrowed,
        resolved_agree=len(uniq) - borrowed, by_status=dict(collections.Counter(s[6] for s in uniq.values())),
        by_source=dict(collections.Counter(s[2] for s in uniq.values())))
    with gzip.open(HERE / 'relocs_v4.tsv.gz', 'wt') as f:
        f.write('field_va\tkind\tsource\tstatus\torigin\texpected\ttarget_name\n')
        for s in sorted(uniq.values()):
            f.write('%08x\t%s\t%s\t%s\t%s\t%s\t%s\n' % (s[0], {6: 'DIR32', 7: 'DIR32NB', 0x14: 'REL32'}.get(s[1], str(s[1])), s[2], s[6], s[7], '' if s[3] is None else '%08x' % s[3], s[4]))

    # ---- rebase test
    delta = NEWBASE - pe.base
    peo = struct.unpack_from('<I', orig, 0x3c)[0]
    rrva, rsz = struct.unpack_from('<II', orig, peo + 24 + 96 + 5 * 8)
    roff = A.rva2off(pe, rrva); p = roff; tbl = set()
    while p < roff + rsz:
        pg, bs = struct.unpack_from('<II', orig, p)
        if bs == 0: break
        for k in range((bs - 8) // 2):
            w, = struct.unpack_from('<H', orig, p + 8 + 2 * k)
            if w >> 12 == 3: tbl.add(pg + (w & 0xfff))
        p += bs
    def rebase_blob(b):
        b = bytearray(b)
        for r_ in tbl:
            o = A.rva2off(pe, r_)
            v, = struct.unpack_from('<I', b, o); struct.pack_into('<I', b, o, (v + delta) & M32)
        struct.pack_into('<I', b, peo + 52, NEWBASE)
        return b
    refreb = rebase_blob(orig)
    (HERE / 'FalloutNV_ref_rebased_10000000.exe').write_bytes(bytes(refreb))
    Sr = S.copy(); imgsz = struct.unpack_from('<I', orig, peo + 24 + 56)[0]
    nonimg = 0; agree6 = 0
    for s in uniq.values():
        if s[1] == 6 and s[6] == 'agree':
            agree6 += 1
            ex = s[3]; o = s[0] - TEXT_VA
            tgt = (ex + delta) & M32 if pe.base <= ex < pe.base + imgsz else ex
            if not (pe.base <= ex < pe.base + imgsz): nonimg += 1
            Sr[o:o + 4] = np.frombuffer(struct.pack('<I', tgt), np.uint8)
    # build ours-at-new-base filled image: start from rebased reference; overwrite produced non-borrowed .text bytes with our values
    ours_reb = bytearray(refreb)
    oa = np.frombuffer(ours_reb, np.uint8)
    oa[raw0:raw0 + rs][keep] = Sr[keep]
    (HERE / 'FalloutNV_v4_filled_base10000000.exe').write_bytes(bytes(ours_reb))
    # strict at new base: header ImageBase updated, non-.text sections from rebased reference (data tables), .text from ours
    sr = bytearray(refreb); sa = np.frombuffer(sr, np.uint8); sa[raw0:raw0 + rs] = Sr
    # borrowed fields in strict stay 0xCC
    (HERE / 'FalloutNV_v4_strict_base10000000.exe').write_bytes(bytes(sr))
    tr = np.frombuffer(bytes(refreb), np.uint8)[raw0:raw0 + rs]
    to = np.frombuffer(bytes(ours_reb), np.uint8)[raw0:raw0 + rs]
    dmask = tr != to
    dd = np.flatnonzero(dmask)
    # classify sites
    tbl_text = sorted(r_ for r_ in tbl if rva0 <= r_ < rva0 + rs)
    d6 = [s for s in uniq.values() if s[1] == 6]
    d6_agree = [s for s in d6 if s[6] == 'agree']; d6_bor = [s for s in d6 if s[6] != 'agree']
    notin = lambda lst: [s for s in lst if (s[0] - pe.base) not in tbl]
    byfield = {s[0]: s for s in uniq.values()}
    tp = np.zeros(rs, np.uint8)
    t_in_ours = t_ours_dir32 = t_borrowed = t_other_kind = t_unknown = t_partial = 0
    unk_examples = []
    for r_ in tbl_text:
        o = r_ - rva0
        if o + 4 > rs: continue
        m4 = M[o:o + 4]
        if not m4.any(): continue
        t_in_ours += 1
        if not m4.all(): t_partial += 1; continue
        s = byfield.get(pe.base + r_)
        if s is not None and s[1] == 6:
            if s[6] == 'agree': t_ours_dir32 += 1
            else: t_borrowed += 1
        elif s is not None: t_other_kind += 1
        else:
            t_unknown += 1
            if len(unk_examples) < 8: unk_examples.append('0x%08x' % (pe.base + r_))
    rb = dict(
        delta=hex(delta), reloc_table_highlow_sites=len(tbl), reloc_sites_in_text=len(tbl_text),
        text_bytes_differing_ours_vs_rebased_reference=int(len(dd)),
        text_bytes_compared=rs, differing_all_inside_produced_bytes=bool(M[dd].all()) if len(dd) else True,
        our_dir32_sites_total=len(d6), our_dir32_resolved_by_us=len(d6_agree), our_dir32_borrowed_rebased_by_delta=len(d6_bor),
        borrowed_dir32_sites_in_reloc_table=len(d6_bor) - len(notin(d6_bor)), borrowed_dir32_sites_not_in_reloc_table=len(notin(d6_bor)),
        dir32_resolved_by_us_NOT_in_reloc_table=len(notin(d6_agree)),
        dir32_resolved_by_us_target_outside_image=nonimg,
        reloc_sites_in_our_placed_code=t_in_ours, of_which_we_produced_DIR32=t_ours_dir32, of_which_borrowed_field=t_borrowed,
        of_which_we_logged_non_DIR32_kind=t_other_kind, of_which_no_relocation_at_all_in_our_output=t_unknown, of_which_partially_placed=t_partial,
        no_reloc_examples=unk_examples,
        borrowed_fields_all_kinds=borrowed,
    )
    prog['rebase_test'] = rb
    prog['seconds'] = round(time.time() - T0)
    (HERE / 'progress.json').write_text(json.dumps(prog, indent=1))
    print(json.dumps(prog, indent=1)[:6000])

if __name__ == '__main__':
    main()
