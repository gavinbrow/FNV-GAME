"""crt5: CRT/STL library-piece matcher with (1) small-function matching (unique location only), (2) data-section matching for
symbols the code pieces need, (3) per-member section placement so statics living in other sections of the same member resolve.
Everything is resolved from the library objects (libcmt/libcpmt) plus byte matching against the image; no field value is copied
from the reference (a site that does not equal the reference value is kept 'disagree' = borrowed, as in v4)."""
import os, json, struct, collections, re
import numpy as np
M32 = 0xffffffff
OVL_ = None   # set by assemble_v7 (shared dict with by_field {int va: target} / global_name)

def mkmask(s):
    mask = bytearray(b'\x01' * len(s['data']))
    for ro, si, ty in s['relocs']:
        for q in range(ro, min(ro + (2 if ty == 0x0a else 4), len(mask))): mask[q] = 0
    return bytes(mask)

def run_crt5(BE, units, pe, cover_text, TEXT_VA, rs, text, libdir, extra_cover, pe_data_sections, small_min=8):
    import uncovered_v2 as U
    Av2 = BE.A
    cover = cover_text.copy(); cover[extra_cover > 0] = 3
    t = bytes(text)
    index6 = collections.defaultdict(list); index4 = collections.defaultdict(list)
    zp = np.flatnonzero(cover == 0)
    for p in zp[:-6].tolist(): index6[t[p:p + 6]].append(p)
    for p in zp[:-4].tolist(): index4[t[p:p + 4]].append(p)
    MEM = {}; cands = []; LIBDEF = collections.defaultdict(list)
    for lname in ('libcmt.lib', 'libcpmt.lib'):
        for mi, (mname, blob) in enumerate(BE.read_ar(libdir / lname)):
            r = U.parse_obj(blob)
            if not r: continue
            secs, syms = r
            MEM[(lname, mi)] = (mname, secs, syms)
            names = collections.defaultdict(list)
            for si, (nm, value, sec, ty, sc) in syms.items():
                if sec > 0 and sc == 2:
                    names[sec - 1].append((value, nm)); LIBDEF[nm].append((lname, mi, sec - 1, value))
            for k, s in enumerate(secs):
                if not (s['flags'] & 0x20) or len(s['data']) < small_min or s['name'].startswith('.text$x'): continue
                nm = sorted(names.get(k, []))
                cands.append(dict(key=(lname, mi, k), lib=lname, member=mname, secidx=k, sec=s['name'], sym=nm[0][1] if nm else None,
                                  names=nm, data=bytes(s['data']), mask=mkmask(s), relocs=s['relocs'], syms=syms))
    cands.sort(key=lambda f: -len(f['data']))
    claimed = np.zeros(rs, np.uint8); matches = []; small = []
    for f in cands:
        data, mask = f['data'], f['mask']; L = len(data)
        big = L >= 24; W = 6 if big else 4
        k = next((i for i in range(L - W + 1) if all(mask[i:i + W])), None)
        if k is None: continue
        hits = []
        for p in (index6 if big else index4).get(data[k:k + W], []):
            st = p - k
            if st < 0 or st + L > rs or (cover[st:st + L] != 0).any() or claimed[st:st + L].any(): continue
            seg = t[st:st + L]
            if all(seg[i] == data[i] for i in range(L) if mask[i]): hits.append(st)
        if big:
            for st in hits:
                if not claimed[st:st + L].any(): claimed[st:st + L] = 1; matches.append((st, f))
        elif len(hits) == 1:
            st = hits[0]; claimed[st:st + L] = 1; matches.append((st, f)); small.append((st, f))
    place = collections.defaultdict(set)      # (lib, midx, secidx) -> {VA}
    for st, f in matches: place[f['key']].add(TEXT_VA + st)

    fnn = {}
    seen = collections.defaultdict(set)
    for u in units:
        for fx in u['functions']:
            for n in [fx['symbol']] + fx.get('fold_aliases', []): seen[n].add(int(fx['address'], 16))
    fnn = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = Av2.BAM.recipe_names(units)
    imports, thunks = Av2.parse_imports(pe)
    Av2.G['imp'], Av2.G['thunks'] = imports, thunks

    def defaddr_now():
        defs = collections.defaultdict(set)
        for (lname, mi, k), vas in place.items():
            mname, secs, syms = MEM[(lname, mi)]
            for si, (nm, value, sec, ty, sc) in syms.items():
                if sec - 1 == k and sc == 2:
                    for va in vas: defs[nm].add(va + value)
        return {n: next(iter(v)) for n, v in defs.items() if len(v) == 1}

    def resolve(matches_, defaddr, collect_need=None):
        out = []; rejected = []
        for st, f in sorted(matches_, key=lambda m: m[0]):
            va = TEXT_VA + st; L = len(f['data']); buf = bytearray(f['data']); sites = []
            lname, mi, k_ = f['key']
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
                if sec > 0 and sc == 3 and sec - 1 == k_: exp, src = va + value + addend, 'self'
                elif sec > 0 and len(place.get((lname, mi, sec - 1), ())) == 1:
                    exp, src = next(iter(place[(lname, mi, sec - 1)])) + value + addend, 'member-section'
                elif nm in defaddr: exp, src = defaddr[nm] + addend, 'lib-matched'
                elif sec > 0 and sc == 3: pass
                elif nm in fnn: exp, src = fnn[nm] + addend, 'recipe-fn'
                elif nm in symnames: exp, src = symnames[nm] + addend, 'symbol-map'
                else:
                    m = Av2.ADDR_RE.search(nm)
                    if m and not nm.startswith(Av2.NOADDR_PREFIX): exp, src = int(m.group(1), 16) + addend, 'addr-in-name'
                    elif nm == '___ImageBase': exp, src = pe.base + addend, 'linker-imagebase'
                    else:
                        a_ = Av2.import_target(nm)
                        if a_ is not None: exp, src = a_ + addend, 'import'
                if OVL_ is not None and collect_need is None and (exp is None or exp & M32 != observed) and ty in (6, 0x14):   # final pass only: phase 1 must still see these as unresolved so the data sections get placed   # w-B binding overlay (reloc-v7/NOTES.md)
                    _ox = OVL_['by_field'].get(fva)
                    if _ox is not None: exp, src = _ox, 'overlay-field'
                    elif nm[:80] in OVL_['global_name'] and not nm.startswith('??_C@'): exp, src = OVL_['global_name'][nm[:80]] + addend, 'overlay-global'
                if exp is None:
                    if collect_need is not None: collect_need.append((lname, mi, sec, sc, nm))
                    buf[ro:ro + 4] = orig; sites.append((fva, ty, 'unresolved', None, nm[:80], addend, 'borrow', 'crt')); continue
                exp &= M32
                fld = (exp - (fva + 4)) & M32 if ty == 0x14 else (exp if ty == 0x06 else (exp - pe.base) & M32)
                if exp == observed: buf[ro:ro + 4] = struct.pack('<I', fld); st_ = 'agree'
                else: buf[ro:ro + 4] = orig; st_ = 'disagree'
                sites.append((fva, ty, src, exp, nm[:80], addend, st_, 'crt'))
            if bytes(buf) != pe.read(va, L): rejected.append((va, L)); continue
            out.append(dict(address=va, size=L, data=bytes(buf), sites=sites, lib=f['lib'], member=f['member'], symbol=f['sym'], small=any(f is g for _, g in small)))
        return out, rejected

    # ---- phase 1: find what is still unresolved, then try to place the data sections that define those names/statics
    need = []
    resolve(matches, defaddr_now(), need)
    want = set()
    for lname, mi, sec, sc, nm in need:
        if sec > 0: want.add((lname, mi, sec - 1))
        else:
            d = LIBDEF.get(nm, [])
            if len(d) == 1: want.add((d[0][0], d[0][1], d[0][2]))
    dsecs = []
    for key in sorted(want):
        if key in place: continue
        lname, mi, k = key
        s = MEM[(lname, mi)][1][k]
        if s['flags'] & 0x20 or s['flags'] & 0x80 or not s['flags'] & 0x40 or len(s['data']) < 8: continue
        dsecs.append((key, s))
    dstat = collections.Counter(wanted=len(want), data_candidates=len(dsecs))
    for key, s in dsecs:
        data = s['data']; mask = mkmask(s); L = len(data)
        k = next((i for i in range(L - 7) if all(mask[i:i + 8]) and any(data[i:i + 8])), None)
        if k is None: dstat['no-distinct-window'] += 1; continue
        keyb = data[k:k + 8]; hits = set()
        for vbase, blob in pe_data_sections:
            p = blob.find(keyb)
            while p >= 0:
                st = p - k
                if st >= 0 and st + L <= len(blob) and all(blob[st + i] == data[i] for i in range(L) if mask[i]): hits.add(vbase + st)
                p = blob.find(keyb, p + 1)
        if len(hits) == 1: place[key].add(next(iter(hits))); dstat['placed'] += 1
        elif not hits: dstat['no-hit'] += 1
        else: dstat['ambiguous(%d)' % min(len(hits), 9)] += 1
    _da = defaddr_now()
    if os.environ.get('FNV_DUMP_SYMADDR') == '1': json.dump(_da, open((__import__('os').environ.get('FNV_PROJ_ROOT', 'C:\\path\\to\\Decompilation').replace('\\', '/') + '/runtime-next/link-v2/crt_defaddr.json'), 'w'))
    if os.environ.get('FNV_DUMP_SYMADDR') == '1': json.dump([[k[0], MEM[(k[0], k[1])][0], k[2], sorted(v)] for k, v in place.items() if v], open(os.environ.get('FNV_PROJ_ROOT', 'C:/path/to/Decompilation').replace(chr(92), '/') + '/runtime-next/link-v2/crt_place.json', 'w'))
    out, rejected = resolve(matches, _da)
    stat = dict(code_matches=len(matches), small_matches=len(small), small_bytes=sum(len(f['data']) for _, f in small), data=dict(dstat),
                data_sections_placed=sum(1 for k in place if k not in {m[1]['key'] for m in matches}))
    return out, rejected, len(matches), stat
