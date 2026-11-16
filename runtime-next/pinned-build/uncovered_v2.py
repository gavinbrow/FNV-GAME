"""Task D: characterise the uncovered non-trivial runs of .text; test stock CRT libs (libcmt/libcpmt) against them.  Read-only."""
import sys, json, struct, re, collections
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', __import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages'))))
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
FN = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp'))
sys.path.insert(0, str(FN / 'tools'))
from compare import Pe
IMG = Path((__import__('os').environ.get('FNV_REF_IMAGE', r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')))
LIBDIR = Path((__import__('os').environ.get('FNV_MSVC9_ROOT', r'C:\Projects\Decompilation\FNV\tools\vc2008') + r'\VC\lib'))
pe = Pe(IMG); d = pe.data
rva, vs, rs, raw = pe.sections[0]
TEXT_VA = pe.base + rva; TEXT_RAW = raw; TEXT_N = rs
units = json.loads((FN / 'build/units.json').read_text())['units']
text = np.frombuffer(d, np.uint8)[raw:raw + rs]
cover = np.zeros(rs, np.uint8)
for u in units:
    for f in u['functions']:
        a = int(f['address'], 16) - TEXT_VA; cover[a:a + f['size']] = 1
    for t in u.get('eh_tails', []):
        a = int(t['address'], 16) - TEXT_VA; seg = cover[a:a + t['size']]; seg[seg == 0] = 2
nontriv = (cover == 0) & ~np.isin(text, (0xcc, 0x90, 0x00))
unc = (cover == 0).astype(np.int8)
dd = np.diff(np.concatenate(([0], unc, [0])))
runs = []
for s, e in zip(np.flatnonzero(dd == 1), np.flatnonzero(dd == -1)):
    nt = int(nontriv[s:e].sum())
    if nt: runs.append(dict(start=int(s), end=int(e), nt=nt))
print('runs', len(runs), 'nontrivial bytes', sum(r['nt'] for r in runs), 'uncovered total', int((cover == 0).sum()))

# ---- symbol map (all units' `symbols`) -> addresses in .text
symaddr = collections.defaultdict(set)
for u in units:
    for k, v in u.get('symbols', {}).items():
        a = int(v, 0)
        if TEXT_VA <= a < TEXT_VA + rs: symaddr[a].add(k)
addrs = sorted(symaddr)
import bisect
CRT_RE = re.compile(r'^_?_?(malloc|free|calloc|realloc|mem(cpy|set|move|cmp|chr)|str(len|cpy|cat|cmp|chr|ncpy|str)|_?CxxFrameHandler|_?_?security_|_?_?SEH|_?_?EH_|_?_?alloca|_?_?chkstk|_?_?ftol|_?_?allmul|_?_?aull|_?_?alldiv|_?_?CIpow|_?_?CI|printf|sprintf|fopen|fclose|fread|fwrite|_?_?initterm|_?_?cinit|_?_?amsg|_?_?lock|_?_?unlock|_?_?encode|_?_?decode|_?_?purecall|_?_?onexit|atexit|exit|_?_?crt|_?_?mtinit|_?_?getptd|_?_?XcptFilter|_?_?except|_?_?local_unwind|_?_?global_unwind|_?_?NLG|_?_?cfltcvt|_?_?fltout|_?_?mbs|_?_?wcs|_?_?strtol|_?_?atoi|__Cxx|__RTC|__RTDynamicCast|__RTtypeid|__unDName|_?_?heap|_?_?sbh|_?_?free_osfhnd|_?_?ioinit|_?_?setmode|_?_?close|_?_?write|_?_?read|_?_?lseek|_?_?output|_?_?input|_?_?fassign|_?_?fp|_?_?dtold|_?_?cftof|_?_?fptostr)', re.I)
HAV_RE = re.compile(r'hk|havok|bhk|zlib|inflate|deflate|bink|bik|gamebryo|^Ni[A-Z]|BS[A-Z]|speedtree|CSpeedTree|fmod|FMOD|xvid|ogg|vorbis|ZLIB')
def names_in(s, e):
    lo = bisect.bisect_left(addrs, TEXT_VA + s); hi = bisect.bisect_left(addrs, TEXT_VA + e)
    out = []
    for a in addrs[lo:hi]: out += [(a, n) for n in sorted(symaddr[a])]
    return out
def jt_fraction(s, e):
    # aligned dwords that point into .text (switch jump tables / function-pointer arrays)
    n = (e - s) // 4;
    if n == 0: return 0.0
    w = np.frombuffer(bytes(text[s:s + 4 * n]), '<u4')
    ok = (w >= TEXT_VA) & (w < TEXT_VA + rs)
    return float(ok.mean())
def prologue_ratio(s, e):
    b = bytes(text[s:e]); return len(re.findall(rb'\x55\x8b\xec|\x8b\xff\x55\x8b\xec', b))

# ---- CRT library functions
def read_ar(path):
    b = path.read_bytes(); assert b[:8] == b'!<arch>\n'
    pos = 8; members = []
    while pos + 60 <= len(b):
        name = b[pos:pos + 16].decode('latin1').strip(); size = int(b[pos + 48:pos + 58])
        members.append((name, b[pos + 60:pos + 60 + size])); pos += 60 + size + (size & 1)
    return members
def parse_obj(blob):
    if len(blob) < 20 or struct.unpack_from('<H', blob, 0)[0] != 0x14c: return None
    nsec, _, symptr, nsym = struct.unpack_from('<HIII', blob, 2)
    # symbol table + string table
    secs = []
    for i in range(nsec):
        o = 20 + 40 * i
        nm, vsz, va, rsz, rptr, relptr, _, nrel, _, fl = struct.unpack_from('<8sIIIIIIHHI', blob, o)
        data = blob[rptr:rptr + rsz] if rsz and not (fl & 0x80) else b''
        relocs = []
        for j in range(nrel):
            ro, si, ty = struct.unpack_from('<IIH', blob, relptr + 10 * j); relocs.append((ro, si, ty))
        secs.append(dict(name=nm.rstrip(b'\0').decode('latin1'), data=data, flags=fl, relocs=relocs))
    strtab = blob[symptr + 18 * nsym:]
    syms = {}; i = 0
    while i < nsym:
        o = symptr + 18 * i
        nm = blob[o:o + 8]
        if nm[:4] == b'\0\0\0\0': off = struct.unpack_from('<I', nm, 4)[0]; nm = strtab[off:strtab.index(b'\0', off)]
        else: nm = nm.rstrip(b'\0')
        value, sec, ty, sc, aux = struct.unpack_from('<IhHBB', blob, o + 8)
        syms[i] = (nm.decode('latin1'), value, sec, ty, sc)
        i += 1 + aux
    return secs, syms
def lib_functions(path):
    out = []
    for mname, blob in read_ar(path):
        r = parse_obj(blob)
        if not r: continue
        secs, syms = r
        # function symbol names per section
        names = collections.defaultdict(list)
        for si, (nm, value, sec, ty, sc) in syms.items():
            if sec > 0 and (ty & 0x20): names[sec - 1].append((value, nm))
        for k, s in enumerate(secs):
            if not (s['flags'] & 0x20) or not s['data'] or len(s['data']) < 24 or s['name'].startswith('.text$x'): continue
            m = bytearray(len(s['data'])); mask = bytearray(b'\x01' * len(s['data']))
            for ro, si, ty in s['relocs']:
                w = 2 if ty == 0x0a else 4
                for q in range(ro, min(ro + w, len(mask))): mask[q] = 0
            nm = sorted(names.get(k, [])); fname = nm[0][1] if nm else mname
            out.append(dict(lib=path.name, member=mname, name=fname, sec=s['name'], data=bytes(s['data']), mask=bytes(mask), nreloc=len(s['relocs'])))
    return out

if __name__ == '__main__':
    libs = []
    for n in ('libcmt.lib', 'libcpmt.lib'):
        if (LIBDIR / n).exists(): libs += lib_functions(LIBDIR / n)
    for n in ('binmode.obj', 'chkstk.obj', 'commode.obj', 'fp10.obj', 'invalidcontinue.obj'):
        p = LIBDIR / n
        if p.exists():
            r = parse_obj(p.read_bytes())
    print('lib code sections', len(libs), 'bytes', sum(len(f['data']) for f in libs))
    # index: 6-byte windows of the uncovered regions (cover==0) -> positions
    W = 6
    uncpos = np.flatnonzero(cover == 0)
    t = bytes(text)
    index = collections.defaultdict(list)
    for p in uncpos[:-W].tolist():
        index[t[p:p + W]].append(p)
    # located EH pieces of all compiled units (handler stubs, unwind funclets) -> bytes they occupy
    ehm = np.zeros(rs, np.uint8)
    for at, sz, ok, parent, unit, inrec in json.loads((HERE / 'logs' / 'pieces_all_v2.json').read_text()):
        a = at - TEXT_VA
        if 0 <= a and a + sz <= rs: ehm[a:a + sz] = 1
    ehnt = int((nontriv & (ehm == 1)).sum())
    print('uncovered nontrivial bytes inside located EH pieces (compiled units, any):', ehnt)
    results = []; claimed = np.zeros(rs, np.uint8)
    libs.sort(key=lambda f: -len(f['data']))
    for f in libs:
        data, mask = f['data'], f['mask']; L = len(data)
        # first fully-unmasked window of W bytes
        k = None
        for i in range(0, L - W + 1):
            if all(mask[i:i + W]): k = i; break
        if k is None: continue
        hits = []
        for p in index.get(data[k:k + W], []):
            st = p - k
            if st < 0 or st + L > rs: continue
            if (cover[st:st + L] != 0).any(): continue
            seg = t[st:st + L]
            if all(seg[i] == data[i] for i in range(L) if mask[i]):
                hits.append(st)
        for st in hits:
            if claimed[st:st + L].any(): continue
            claimed[st:st + L] = 1
            results.append(dict(va=TEXT_VA + st, size=L, lib=f['lib'], member=f['member'], name=f['name'], sec=f['sec'], nreloc=f['nreloc']))
    print('matched placements', len(results), 'bytes', sum(r['size'] for r in results))
    big = [r for r in results if r['size'] >= 16]
    print('matched >=16B', len(big), 'bytes', sum(r['size'] for r in big))
    # per-run report
    rr = []
    for r in runs:
        s, e = r['start'], r['end']
        nm = names_in(s, e)
        crtn = [n for a, n in nm if CRT_RE.search(n)]
        libm = [m for m in results if s <= m['va'] - TEXT_VA < e]
        libbytes = sum(m['size'] for m in libm)
        jt = jt_fraction(s, e); pr = prologue_ratio(s, e)
        eh_nt = int((nontriv[s:e] & (ehm[s:e] == 1)).sum())
        r.update(eh_nt=eh_nt, va='0x%08x' % (TEXT_VA + s), length=e - s, symbols_in_run=len(nm), sample_names=[n for a, n in nm][:6],
                 crt_names=len(crtn), lib_matched_bytes=libbytes, lib_matched_funcs=len(libm),
                 lib_top=[m['name'] for m in sorted(libm, key=lambda m: -m['size'])[:4]], jt=round(jt, 2), prologues=pr)
        # category
        if eh_nt >= 0.5 * r['nt']: c = 'EH-tail-pieces(handler stubs/unwind funclets)-not-in-recipe'
        elif libbytes >= 0.5 * r['nt']: c = 'matches-stock-CRT/STL-lib-functions'
        elif crtn and len(crtn) >= max(1, len(nm) // 2): c = 'named-CRT-by-symbol-map'
        elif nm and sum(1 for a, n in nm if HAV_RE.search(n)) >= max(1, len(nm) // 2): c = 'named-engine/library-by-symbol-map'
        elif jt >= 0.6 and r['length'] < 4096: c = 'jump-table/pointer-array-like'
        elif nm: c = 'named-other-by-symbol-map'
        elif pr >= 1 or r['nt'] / max(1, r['length']) > 0.7 and pr: c = 'unnamed-code(has prologues)'
        else: c = 'unnamed-other'
        r['category'] = c; rr.append(r)
    print('lib-matched bytes inside runs', sum(r['lib_matched_bytes'] for r in rr), 'EH nt total', sum(r['eh_nt'] for r in rr))
    cat = collections.defaultdict(lambda: [0, 0])
    for r in rr: cat[r['category']][0] += 1; cat[r['category']][1] += r['nt']
    print(json.dumps({k: v for k, v in cat.items()}, indent=1))
    rr.sort(key=lambda r: -r['nt'])
    for r in rr[:15]:
        print(r['va'], 'eh_nt', r['eh_nt'], 'len', r['length'], 'nt', r['nt'], r['category'], 'syms', r['symbols_in_run'], r['sample_names'][:3], 'lib', r['lib_matched_funcs'], r['lib_matched_bytes'], r['lib_top'][:3], 'jt', r['jt'], 'pro', r['prologues'])
    out = dict(runs=rr, categories={k: dict(runs=v[0], nontrivial_bytes=v[1]) for k, v in cat.items()},
               lib_matches=results[:5000], lib_summary=dict(placements=len(results), bytes=sum(r['size'] for r in results),
                                                           placements_ge16=len(big), bytes_ge16=sum(r['size'] for r in big),
                                                           by_lib=collections.Counter(r['lib'] for r in results)))
    (HERE / 'logs' / 'uncovered_v2.json').write_text(json.dumps(out, indent=1, default=dict))
