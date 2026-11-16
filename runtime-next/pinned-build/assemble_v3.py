"""Pinned-address assembler.

Takes obj/NNNN.obj (from compile_units.py), the recipe (fnv_decomp/build/units.json) and the matcher's reference
image, and writes FalloutNV_pinned_v3.exe (+ FalloutNV_pinned_strict_v3.exe) and stats.json.  Re-uses fnv_decomp/tools/compare.py
(Coff / Pe / compare / same_literal) and build_and_match.py (recipe_names / eh_sections / image_ok) by import.
"""
import sys, os, re, json, struct, time, hashlib, inspect, collections, bisect
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))   # numpy lives in user site; -I hides it
HERE = Path(__file__).resolve().parent
FN = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp'))
sys.path.insert(0, str(FN / 'tools'))
import compare as CMP                      # noqa
from compare import Coff, Pe, compare, same_literal   # noqa
import build_and_match as BAM              # noqa

IMG = Path((__import__('os').environ.get('FNV_REF_IMAGE', r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')))
M32 = 0xffffffff
KINDS = {0x06: 'DIR32', 0x14: 'REL32', 0x07: 'DIR32NB', 0x0B: 'SECREL'}
ADDR_RE = re.compile(r'(?<![0-9A-Za-z])(?:FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC)_([0-9a-f]{8})(?![0-9A-Za-z])')
NOADDR_PREFIX = ('__ehhandler$', '__ehfuncinfo$', '__unwindtable$', '__unwindfunclet$', '__catchsym$', '__tryblocktable$',
                 '__tihandlers$', '__ip2state$', '__stateUnwindMap$', '__catch$', '__ehstate$', '__ehvec', '__xt_')

# ---------------------------------------------------------------- shared helpers
def rva2off(pe, rva):
    for start, vs, rs, raw in pe.sections:
        if start <= rva < start + rs:
            return raw + rva - start
    return None

def va2off(pe, va, size=1):
    rva = va - pe.base
    for start, vs, rs, raw in pe.sections:
        if start <= rva and rva + size <= start + rs:
            return raw + rva - start
    return None

def parse_imports(pe):
    d = pe.data
    peo = struct.unpack_from('<I', d, 0x3c)[0]
    rva, size = struct.unpack_from('<II', d, peo + 24 + 96 + 8)
    imp, slots = {}, []
    off = rva2off(pe, rva)
    while True:
        oft, _, _, name, ft = struct.unpack_from('<IIIII', d, off)
        if not name: break
        o = rva2off(pe, oft or ft); i = 0
        while True:
            th, = struct.unpack_from('<I', d, o + 4 * i)
            if not th: break
            slots.append(pe.base + ft + 4 * i)
            if not th & 0x80000000:
                fname = d[rva2off(pe, th) + 2:].split(b'\0', 1)[0].decode()
                imp.setdefault(fname, pe.base + ft + 4 * i)
            i += 1
        off += 20
    lo, hi = min(slots), max(slots)
    thunks = {}
    text = [(s, v, r, raw) for s, v, r, raw in pe.sections][0]
    start, vs, rs, raw = text
    blob = d[raw:raw + rs]
    for m in re.finditer(rb'\xff\x25(....)', blob, re.S):
        slot = struct.unpack('<I', m.group(1))[0]
        if lo <= slot <= hi:
            thunks.setdefault(slot, pe.base + start + m.start())
    return imp, thunks

def category(name):
    if name.startswith('__ehhandler$'): return 'ehhandler'
    if name.startswith('__ehfuncinfo$'): return 'ehfuncinfo'
    if name.startswith('__unwind'): return 'unwind'
    if name.startswith('$SG') or name.startswith('??_C@'): return 'string-literal'
    if name.startswith('__real@') or name.startswith('__xmm@'): return 'float-literal'
    if name.startswith('__imp_'): return 'import-iat'
    if name.startswith('??_7'): return 'vtable'
    if name.startswith('$L') or name.startswith('$LN'): return 'local-label'
    if name.startswith('.'): return 'section-symbol'
    if re.search(r'FUN_[0-9a-f]{8}', name): return 'FUN_named'
    if re.search(r'DAT_[0-9a-f]{8}', name): return 'DAT_named'
    return 'other:' + re.sub(r'[0-9a-fA-F]{8}', 'A', re.sub(r'\d+', 'N', name))[:28]

# ---------------------------------------------------------------- worker side
G = {}

def init(fnnames, symnames, imports, thunks):
    G['pe'] = Pe(IMG)
    G['fn'], G['sym'], G['imp'], G['thunks'] = fnnames, symnames, imports, thunks
    src = inspect.getsource(BAM.eh_sections)
    old = 'out.append([at, at + s1 - s0, ok, parent, sorted(guessed)])'
    assert old in src
    src = src.replace(old, 'out.append([at, at + s1 - s0, ok, parent, sorted(guessed), bytes(data[s0:s1]), index, s0])')
    old2 = 'return out, inferred, errors'
    assert old2 in src
    src = src.replace(old2, 'return out, inferred, errors, dict(data_bases), dict(anchors)')
    ns = dict(BAM.__dict__); exec(src, ns)
    G['eh'] = ns['eh_sections']
    G['bor'] = []

def import_target(name):
    imp, th = G['imp'], G['thunks']
    if name.startswith('__imp_'):
        n = name[6:]
        n = n[1:] if n.startswith('_') else n
        n = re.sub(r'@\d+$', '', n)
        return imp.get(n)
    if name.startswith('_') and re.search(r'@\d+$', name):
        n = re.sub(r'@\d+$', '', name[1:])
        if n in imp:
            return th.get(imp[n])
    return None

def resolve_field(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw):
    """-> (source, expected_abs or None).  Priorities: a function, b embedded address, c symbol map, d imports."""
    pe = G['pe']
    name = tsym['name']
    fnu = unit['_fnmap']
    t = None
    if name in fnu: return 'a', (fnu[name] + addend) & M32
    if name in G['fn'] and tsym['section'] <= 0: return 'a', (G['fn'][name] + addend) & M32
    if tsym['section'] > 0:
        point = tsym['value'] + addend
        for sec, val, addr, size in locals_:
            if sec == tsym['section'] and val <= point < val + size:
                return 'a', (addr + point - val) & M32
    s = unit.get('symbols', {})
    if name in s: return 'c', (int(s[name], 0) + addend) & M32
    if name in G['sym']: return 'c', (G['sym'][name] + addend) & M32
    if tsym['section'] == -1: return 'c', (tsym['value'] + addend) & M32
    if not name.startswith(NOADDR_PREFIX):
        m = ADDR_RE.search(name)
        if m:
            a = int(m.group(1), 16)
            # v2: an address inside a template non-type argument ('$1?DAT_xxxxxxxx@@3HA') is a parameter of the symbol, not its location
            if 0x400000 <= a < 0x400000 + 0x107b000 and not re.search(r'\$\d?\?$', name[:m.start()]):
                return 'b', (a + addend) & M32
    xv = unit.get('_xver', {})
    if tsym['section'] in xv:       # v2 (f): EH table (.xdata) whose placement was verified byte-for-byte against the image
        return 'f', (xv[tsym['section']] + tsym['value'] + addend) & M32
    a = import_target(name)
    if a is not None: return 'd', (a + addend) & M32
    return None, None

def fill_relocs(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope):
    """Resolve every relocation of section `sec` whose field starts in [lo,hi); buf holds bytes lo..hi at VA base_va."""
    pe = G['pe']
    for off, idx, kind in sec['relocs']:
        if not lo <= off < hi: continue
        rel = off - lo
        tsym = coff.symbols[idx]
        kn = KINDS.get(kind, 'K%d' % kind)
        field_va = base_va + rel
        if rel + 4 > hi - lo or kind not in KINDS:
            stats[(scope, 'e', 'borrow-' + ('crosses-end' if rel + 4 > hi - lo else 'kind-' + kn))] += 1
            continue
        try:
            orig_raw = pe.read(field_va, 4)
        except ValueError:
            stats[(scope, 'e', 'borrow-unreadable')] += 1
            continue
        o32, = struct.unpack('<I', orig_raw)
        if kind == 0x14:
            addend, = struct.unpack_from('<i', buf, rel)
            observed = (field_va + 4 + struct.unpack('<i', orig_raw)[0]) & M32
        else:
            addend, = struct.unpack_from('<I', buf, rel)
            observed = (o32 + pe.base) & M32 if kind == 0x07 else o32
        src, expected = resolve_field(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        if expected is not None and kind == 0x0B:
            try:
                field = pe.secrel(expected) & M32
                expected, observed = field, o32      # compare the section-relative offsets themselves
            except ValueError: src, expected = None, None
        if expected is None:
            # (e) last resort: borrow the original field
            buf[rel:rel + 4] = orig_raw
            stats[(scope, 'e', 'borrow:' + category(tsym['name']))] += 1
            G['bor'].append((scope, tsym['name'], observed, kn, tsym['section'], category(tsym['name'])))
            continue
        if kind == 0x14: field = (expected - (field_va + 4)) & M32
        elif kind == 0x07: field = (expected - pe.base) & M32
        elif kind == 0x06: field = expected
        if expected == observed:
            buf[rel:rel + 4] = struct.pack('<I', field)
            stats[(scope, src, 'agree')] += 1
        else:
            buf[rel:rel + 4] = orig_raw          # keep the image runnable; still counted
            stats[(scope, src, 'disagree')] += 1
            if src == 'b':      # counterfactual: would the project's symbol map (c) have been right?
                alt = unit.get('symbols', {}).get(tsym['name'])
                alt = int(alt, 0) if alt is not None else G['sym'].get(tsym['name'])
                tag = 'c_absent' if alt is None else ('c_would_agree' if ((alt + addend) & M32) == observed else 'c_would_disagree')
                stats[(scope, 'b-disagreements-by-alternative', tag)] += 1
            lit = same_literal(coff, pe, tsym, expected, observed)
            delta = (observed - expected) & M32
            if delta > 0x80000000: delta -= 1 << 32
            icf = False
            if src == 'a' and kind in (0x06, 0x14):
                try: icf = pe.read(expected, 32) == pe.read(observed, 32) and expected != observed
                except ValueError: pass
            dc = 'same-literal-bytes-other-pool-copy' if lit else ('first32-bytes-identical-to-observed-target(ICF-like)' if icf else ('delta=%+d' % delta if abs(delta) <= 16 else 'different-target'))
            key = '%s|%s|%s|%s|%s' % (scope, src, kn, category(tsym['name']), dc)
            pats[key][0] += 1
            if pats[key][1] is None:
                pats[key][1] = '%s: computed 0x%08x original 0x%08x' % (tsym['name'][:70], expected, observed)

def process(task):
    idx, unit = task
    pe = G['pe']
    out = dict(idx=idx, fn=[], tails=[], stats=collections.Counter(), pats=collections.defaultdict(lambda: [0, None]), error=None, xdata=None)
    G['bor'] = []
    obj = HERE / 'obj_v3' / ('%04d.obj' % idx)
    try:
        coff = Coff(obj)
    except Exception as e:
        out['error'] = 'coff:' + str(e)[:200]; return out
    unit['_fnmap'] = {}
    locals_ = []
    for f in unit['functions']:
        a = int(f['address'], 16)
        for nm in [f['symbol']] + f.get('fold_aliases', []):
            unit['_fnmap'][nm] = a
            try:
                s = coff.named(nm); locals_.append((s['section'], s['value'], a, f['size']))
            except ValueError:
                pass
    rows = None
    try:
        rows = compare(coff, pe, dict(symbols=unit.get('symbols', {}), functions=unit['functions'],
                                      literal_symbols=unit.get('literal_symbols', [])), None)
        verdict = {r['address']: r['verdict'] for r in rows}
    except Exception as e:
        verdict = {}; out['compare_error'] = str(e)[:200]
    for f in unit['functions']:
        addr, size = int(f['address'], 16), f['size']
        rec = dict(address=addr, size=size, symbol=f['symbol'], verdict=verdict.get('0x%08x' % addr), data=None, reason=None)
        out['fn'].append(rec)
        try:
            s = coff.named(f['symbol'])
        except ValueError as e:
            rec['reason'] = 'symbol-missing-in-obj'; continue
        sec = coff.sections[s['section']]; start = s['value']
        nxt = [x['value'] for x in coff.symbols.values() if x['section'] == s['section'] and x['type'] & 0x20
               and x['value'] > start and not x['name'].startswith('__catch$')]
        end = min(nxt) if nxt else len(sec['data'])
        if end - start < size:
            rec['reason'] = 'compiled-extent-shorter-than-recipe (%d < %d)' % (end - start, size); continue
        if any(b not in (0xcc, 0x90) for b in sec['data'][start + size:end]):
            rec['reason'] = 'compiled-extent-longer-than-recipe (non-padding tail)'; continue
        buf = bytearray(sec['data'][start:start + size])
        fill_relocs(coff, unit, locals_, sec, start, start + size, addr, buf, out['stats'], out['pats'], 'fn')
        rec['data'] = bytes(buf)
    if unit.get('eh_tails'):
        if rows is None:
            out['tails_error'] = 'compare-error: ' + out.get('compare_error', '')
        else:
            try:
                pieces, inferred, errors, data_bases, anchors = G['eh'](coff, pe, unit, rows, G['sym'])
                out['tail_errors'] = errors[:3]
                xver, xbad = {}, 0
                for xi, xb in data_bases.items():
                    xs = coff.sections[xi]
                    if not xs['name'].startswith('.xdata'): continue
                    m = bytearray(xs['data']); ref = None
                    try: ref = bytearray(pe.read(xb, len(m)))
                    except ValueError: pass
                    if ref is not None:
                        for ro, _, rk in xs['relocs']:
                            m[ro:ro + 4] = b'\x00\x00\x00\x00'; ref[ro:ro + 4] = b'\x00\x00\x00\x00'
                    if ref is not None and ref == m: xver[xi] = xb
                    else: xbad += 1
                unit['_xver'] = xver
                out['xdata'] = dict(sections=len([1 for xi in data_bases if coff.sections[xi]['name'].startswith('.xdata')]),
                                    verified=len(xver), unverified=xbad)
                for p in pieces:
                    if len(p) < 8:
                        out['tails'].append(dict(address=p[0], size=p[1] - p[0], parent=p[3], data=None, ok=False)); continue
                    at, end, ok, parent, guessed, pdata, index, s0 = p
                    buf = bytearray(pdata)
                    fill_relocs(coff, unit, locals_, coff.sections[index], s0, s0 + len(pdata), at, buf,
                                out['stats'], out['pats'], 'tail' if ok else 'tail_notok')
                    out['tails'].append(dict(address=at, size=end - at, parent=parent, data=bytes(buf), ok=ok, unit=idx))
            except Exception as e:
                out['tails_error'] = str(e)[:200]
    out['borrows'] = list(G['bor'])
    out['stats'] = dict(out['stats']); out['pats'] = {k: v for k, v in out['pats'].items()}
    return out

# ---------------------------------------------------------------- main side
def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    import numpy as np
    T0 = time.time()
    units = json.loads((FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (HERE / 'logs' / 'compile_v3.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = Pe(IMG)
    orig = pe.data
    ok_img, hits, tot = BAM.image_ok(pe)
    fnnames, seen = {}, collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []):
                seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = BAM.recipe_names(units)
    imports, thunks = parse_imports(pe)
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    nproc = max(1, (os.cpu_count() or 4) - 2)
    results = {}
    with ProcessPoolExecutor(nproc, initializer=init, initargs=(fnnames, symnames, imports, thunks)) as ex:
        for n, r in enumerate(ex.map(process, tasks, chunksize=8), 1):
            results[r['idx']] = r
            if n % 500 == 0: print('processed', n, 'of', len(tasks), round(time.time() - T0), 's', flush=True)
    t_proc = time.time() - T0

    # ---- ranges
    N = len(orig)
    cover = np.zeros(N, np.uint8)            # 1 = recipe function, 2 = recipe EH tail
    flist = []                                # (addr,size,symbol,unit)
    for i, u in enumerate(units):
        for f in u['functions']:
            a, s = int(f['address'], 16), f['size']
            flist.append((a, s, f['symbol'], i))
    tlist = []
    for i, u in enumerate(units):
        for t in u.get('eh_tails', []):
            tlist.append((int(t['address'], 16), t['size'], t.get('parent'), i))
    for a, s, _, _ in flist:
        o = va2off(pe, a, s); cover[o:o + s] = 1
    for a, s, _, _ in tlist:
        o = va2off(pe, a, s)
        seg = cover[o:o + s]; seg[seg == 0] = 2
    img = bytearray(orig)
    for a, s, _, _ in flist + tlist:
        o = va2off(pe, a, s); img[o:o + s] = b'\xcc' * s
    written = np.zeros(N, np.uint8)           # 1 compiled function bytes, 2 compiled tail bytes
    reasons = collections.Counter(); placed = 0; placed_bytes = 0; fn_status = {}
    dup_diff = 0
    by_unit_fns = collections.defaultdict(list)
    matcher = collections.Counter()
    for i, u in enumerate(units):
        c = comp[i]
        for f in u['functions']:
            a = int(f['address'], 16)
        if c['status'] != 'ok':
            for f in u['functions']:
                reasons['unit-not-compiled:' + c['status'] + ':' + u['compiler']] += 1
            continue
        r = results[i]
        if r['error']:
            for f in u['functions']: reasons['unit-process-error:' + r['error'][:40]] += 1
            continue
        for rec in r['fn']:
            matcher[rec['verdict']] += 1
            if rec['data'] is None:
                reasons[rec['reason'].split(' (')[0]] += 1; continue
            o = va2off(pe, rec['address'], rec['size'])
            if written[o:o + rec['size']].any():
                reasons['duplicate-address-already-placed'] += 1; continue
            img[o:o + rec['size']] = rec['data']; written[o:o + rec['size']] = 1
            placed += 1; placed_bytes += rec['size']; by_unit_fns[i].append(rec)
    tail_placed = tail_bytes = tail_clipped = tail_pieces = tail_unplaced = 0
    tail_ok = 0
    # v2 placement: pieces whose bytes verified (ok) go first; pieces that do not verify (genuine source/layout
    # mismatch) are held back so they cannot clobber verified neighbours, and are only written into the STRICT image.
    allp = [t for i, r in results.items() for t in r['tails']]
    tail_pieces = len(allp)
    notok_pieces = [t for t in allp if t['data'] is not None and not t['ok']]
    shared_addr = collections.defaultdict(set); shared_conflict = 0; shared_same = 0
    unplaced_reasons = collections.Counter()
    for t in allp:
        if t['data'] is None:
            tail_unplaced += 1; unplaced_reasons['no-data(outside image/compare-error)'] += 1; continue
        if not t['ok']:
            continue
        o = va2off(pe, t['address'], max(1, len(t['data'])))
        if o is None:
            tail_unplaced += 1; unplaced_reasons['unmapped'] += 1; continue
        L = len(t['data'])
        ok_mask = (cover[o:o + L] == 2) & (written[o:o + L] == 0)
        arr = np.frombuffer(t['data'], np.uint8)
        # already-written bytes (same address, folded by the original linker): do the two copies agree?
        ov = (written[o:o + L] != 0)
        if ov.any():
            if (np.frombuffer(bytes(img[o:o + L]), np.uint8)[ov] == arr[ov]).all(): shared_same += 1
            else: shared_conflict += 1
        if not ok_mask.any():
            tail_unplaced += 1
            unplaced_reasons['ok-piece-not-in-recipe-tail' if not (cover[o:o + L] == 2).any() else 'ok-piece-already-placed(same address)'] += 1
            continue
        tail_clipped += int(L - ok_mask.sum())
        cur = np.frombuffer(bytes(img[o:o + L]), np.uint8).copy()
        cur[ok_mask] = arr[ok_mask]
        img[o:o + L] = cur.tobytes()
        written[o:o + L][ok_mask] = 2
        tail_placed += 1; tail_bytes += int(ok_mask.sum()); tail_ok += 1
    notok_in_recipe = 0; notok_bytes_in_recipe = 0
    strict_img = bytearray(img); strict_written = written.copy()
    for t in notok_pieces:
        o = va2off(pe, t['address'], max(1, len(t['data'])))
        if o is None: continue
        L = len(t['data'])
        m = (cover[o:o + L] == 2) & (strict_written[o:o + L] == 0)
        if m.any():
            notok_in_recipe += 1; notok_bytes_in_recipe += int(m.sum())
            arr = np.frombuffer(t['data'], np.uint8)
            cur = np.frombuffer(bytes(strict_img[o:o + L]), np.uint8).copy(); cur[m] = arr[m]
            strict_img[o:o + L] = cur.tobytes(); strict_written[o:o + L][m] = 3
    # ---- strict image = what we have; runnable image restores covered-but-never-written bytes from the original
    strict = bytes(strict_img)
    full = bytearray(img)
    o_arr = np.frombuffer(orig, np.uint8)
    f_arr = np.frombuffer(bytes(full), np.uint8).copy()
    restore = (cover > 0) & (written == 0)
    f_arr[restore] = o_arr[restore]
    full = f_arr.tobytes()
    (HERE / 'FalloutNV_pinned_v3.exe').write_bytes(full)
    (HERE / 'FalloutNV_pinned_strict_v3.exe').write_bytes(strict)
    t_asm = time.time() - T0

    # ---- diff
    secs = [('headers', 0, pe.sections[0][3])] + [(n, raw, raw + rs) for n, (rva, vs, rs, raw) in zip(pe.names, pe.sections)]
    secs.append(('overlay/after-last-section', max(r[3] + r[2] for r in pe.sections), N))
    def off2va(o):
        for (rva, vs, rs, raw), n in zip(pe.sections, pe.names):
            if raw <= o < raw + rs: return pe.base + rva + o - raw
        return None
    fstarts = sorted((a, s, sym) for a, s, sym, _ in flist); fa = [x[0] for x in fstarts]
    tstarts = sorted((a, s, sym) for a, s, sym, _ in tlist); ta = [x[0] for x in tstarts]
    def owner(va):
        if va is None: return None
        k = bisect.bisect_right(fa, va) - 1
        if k >= 0 and fa[k] <= va < fa[k] + fstarts[k][1]: return 'fn 0x%08x %s' % (fa[k], fstarts[k][2][:50])
        k = bisect.bisect_right(ta, va) - 1
        if k >= 0 and ta[k] <= va < ta[k] + tstarts[k][1]: return 'eh-tail 0x%08x' % ta[k]
        return 'uncovered'
    def diffreport(blob, label):
        b = np.frombuffer(blob, np.uint8)
        d = np.flatnonzero(b != o_arr)
        rep = dict(total_differing_bytes=int(len(d)), per_section={}, first_ranges=[])
        for n, lo, hi in secs:
            rep['per_section'][n] = int(((d >= lo) & (d < hi)).sum())
        if len(d):
            br = np.flatnonzero(np.diff(d) > 1)
            starts = np.concatenate(([d[0]], d[br + 1])); ends = np.concatenate((d[br], [d[-1]])) + 1
            rep['range_count'] = int(len(starts))
            for s, e in list(zip(starts, ends))[:20]:
                va = off2va(int(s))
                rep['first_ranges'].append(dict(file_offset='0x%x' % s, va=None if va is None else '0x%08x' % va,
                                                length=int(e - s), in_=owner(va)))
        return rep
    diff_full = diffreport(full, 'full'); diff_strict = diffreport(strict, 'strict')
    # identical functions in the runnable image
    ident = sum(1 for a, s, _, _ in flist if full[va2off(pe, a, s):va2off(pe, a, s) + s] == orig[va2off(pe, a, s):va2off(pe, a, s) + s])
    ident_placed = 0; ident_matcher_match = 0; placed_not_ident = []
    for i, recs in by_unit_fns.items():
        for rec in recs:
            o = va2off(pe, rec['address'], rec['size'])
            same = bytes(full[o:o + rec['size']]) == orig[o:o + rec['size']]
            ident_placed += same
            if not same and len(placed_not_ident) < 20:
                placed_not_ident.append('0x%08x %s matcher=%s' % (rec['address'], rec['symbol'][:50], rec['verdict']))
    # ---- relocation stats
    rel = collections.Counter(); pats = {}
    for r in results.values():
        for k, v in r['stats'].items(): rel[k] += v
        for k, v in r['pats'].items():
            if k not in pats: pats[k] = [0, v[1]]
            pats[k][0] += v[0]
    relout = {}
    for (scope, src, what), v in sorted(rel.items()):
        relout.setdefault(scope, {}).setdefault(src, {})[what] = v
    toppats = sorted(pats.items(), key=lambda kv: -kv[1][0])[:20]
    # ---- coverage (phase 0)
    execs = [(n, raw, raw + rs, fl) for n, (rva, vs, rs, raw) in zip(pe.names, pe.sections)
             for fl in [struct.unpack_from('<I', pe.data, struct.unpack_from('<I', pe.data, 0x3c)[0] + 24 + struct.unpack_from('<H', pe.data, struct.unpack_from('<I', pe.data, 0x3c)[0] + 20)[0] + pe.names.index(n) * 40 + 36)[0]]
             if fl & 0x20000000]
    covout = {}
    for n, lo, hi, fl in execs:
        seg = np.frombuffer(orig, np.uint8)[lo:hi]; cv = cover[lo:hi]
        unc = seg[cv == 0]
        cnt = {hex(v): int((unc == v).sum()) for v in (0xcc, 0x90, 0x00)}
        nontriv = (cv == 0) & ~np.isin(np.frombuffer(orig, np.uint8)[lo:hi], (0xcc, 0x90, 0x00))
        # runs of uncovered bytes that contain any non-trivial byte
        unc_mask = (cv == 0).astype(np.int8)
        runs = []
        if unc_mask.any():
            dd = np.diff(np.concatenate(([0], unc_mask, [0])))
            rs_, re_ = np.flatnonzero(dd == 1), np.flatnonzero(dd == -1)
            for s, e in zip(rs_, re_):
                nt = int(nontriv[s:e].sum())
                if nt: runs.append((nt, int(e - s), int(s)))
        runs.sort(reverse=True)
        covout[n] = dict(raw_bytes=int(hi - lo), covered_by_function=int((cv == 1).sum()), covered_by_eh_tail=int((cv == 2).sum()),
                         uncovered=int((cv == 0).sum()), uncovered_by_value=cnt, uncovered_nontrivial=int(nontriv.sum()),
                         uncovered_runs_with_nontrivial=len(runs),
                         largest_nontrivial_runs=[dict(nontrivial=a, run_len=b, va='0x%08x' % (off2va(lo + c) or 0)) for a, b, c in runs[:10]])
    # ---- cross-check of borrowed external targets: does every site of one name see the same address?
    byname = collections.defaultdict(lambda: collections.defaultdict(set)); sites = collections.Counter()
    for i, r in results.items():
        for scope, name, observed, kn, sec_, cat in r.get('borrows', []):
            byname[name][observed].add(i); sites[(scope, name)] += 1
    bor_summary = collections.Counter(); bor_examples = {}
    for i, r in results.items():
        for scope, name, observed, kn, sec_, cat in r.get('borrows', []):
            addrs = byname[name]
            nunits = len(set().union(*addrs.values()))
            if sec_ > 0: k = 'local-data-section-symbol'
            elif len(addrs) > 1: k = 'conflicting-addresses-across-sites'
            elif nunits >= 2: k = 'consistent-across-%s-units(cross-validated)' % ('2+')
            else: k = 'single-unit-only'
            key = '%s|%s|%s' % (scope, cat if cat in ('ehfuncinfo', 'FUN_named', 'DAT_named') else 'other', k)
            bor_summary[key] += 1
            bor_examples.setdefault(key, '%s -> 0x%08x' % (name[:80], observed))
    bor_summary = dict(sorted(bor_summary.items())); bor_ex = bor_examples
    # ---- stats
    cs = collections.Counter(c['status'] for c in comp.values())
    cbyc = collections.Counter((u['compiler'], comp[i]['status']) for i, u in enumerate(units))
    fails = [dict(source=c['source'], status=c['status'], compiler=c['compiler'], error=c['error'][:200]) for c in comp.values() if c['status'] != 'ok']
    wall = float((HERE / 'logs' / 'compile_wall_v3.txt').read_text())
    uniq_addr = len({a for a, _, _, _ in flist})
    stats = dict(
        reference_image=dict(path=str(IMG), size=N, sha256=sha(orig), image_check_ok=ok_img, probes_matched='%d/%d' % (hits, tot)),
        units=dict(total=len(units), compiled=cs['ok'], failed=len(units) - cs['ok'], by_status=dict(cs),
                   by_compiler_status={'%s/%s' % k: v for k, v in cbyc.items()}, failures_first20=fails[:20]),
        functions=dict(entries_in_recipe=len(flist), unique_addresses=uniq_addr, placed=placed, skipped=len(flist) - placed,
                       skipped_reasons=dict(reasons), compiler_bytes_placed=placed_bytes,
                       placed_identical_to_original=ident_placed, placed_not_identical_examples=placed_not_ident,
                       all_recipe_functions_identical_in_runnable_image=ident,
                       matcher_verdict_among_compiled=dict((str(k), v) for k, v in matcher.items())),
        eh_tails=dict(recipe_tails=len(tlist), recipe_tail_bytes=sum(s for _, s, _, _ in tlist), located_pieces=tail_pieces,
                      pieces_placed=tail_placed, pieces_unplaced=tail_unplaced, unplaced_reasons=dict(unplaced_reasons), bytes_placed=tail_bytes,
                      bytes_clipped_outside_recipe_tails=tail_clipped, pieces_whose_matcher_check_ok=tail_ok,
                      pieces_not_ok=len(notok_pieces), notok_pieces_overlapping_recipe_tails=notok_in_recipe,
                      notok_bytes_written_to_strict_only=notok_bytes_in_recipe,
                      ok_pieces_sharing_bytes_with_earlier_piece_same_content=shared_same, ok_pieces_sharing_bytes_with_conflicting_content=shared_conflict,
                      xdata=dict(sections=sum((r['xdata'] or {}).get('sections', 0) for r in results.values()),
                                 verified=sum((r['xdata'] or {}).get('verified', 0) for r in results.values()),
                                 unverified=sum((r['xdata'] or {}).get('unverified', 0) for r in results.values()))),
        borrow_crosscheck=bor_summary,
        relocations=relout, top20_disagreement_patterns=[dict(count=v[0], pattern=k, example=v[1]) for k, v in toppats],
        coverage=covout, borrow_examples=bor_ex,
        diff_runnable_image=diff_full, diff_strict_image=diff_strict,
        hashes=dict(original=sha(orig), runnable=sha(full), strict=sha(strict), runnable_equals_original=full == orig),
        timing=dict(compile_wall_s=round(wall, 1), assemble_processing_s=round(t_proc, 1), assemble_total_s=round(t_asm, 1)),
        workers=dict(compile_threads=30, assemble_processes=nproc),
    )
    (HERE / 'stats_v3.json').write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: stats[k] for k in ('units', 'functions', 'eh_tails', 'hashes', 'timing')}, indent=1)[:4000])

if __name__ == '__main__':
    main()

