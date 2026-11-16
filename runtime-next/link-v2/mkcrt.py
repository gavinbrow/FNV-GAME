"""link-v2 mkcrt.py: libcmt/libcpmt members whose code/data crt5 matched at original addresses (crt_place.json) are extracted from the library and linked as objects with extra
alias symbols C_<va>/D_<va> at every symbol offset of the matched sections (statics included); all original external names stay, so the library copy is never pulled in a second time.
Writes crt_obj\*.obj. usage: python -I mkcrt.py"""
import collections, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / 'pinned-build'))
sys.path.insert(0, str(HERE.parent / 'coverage-v3'))
import coffrw, uncovered_v2 as U
import build_extra as BE
place = json.load(open(HERE / 'crt_place.json'))
LIB = Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib')
dl = set(json.load(open(HERE / 'data_out' / 'data_labels.json'))['data_labels'])
defd = set()
for d_ in ('obj_rw', 'obj_contrib_rw'):
    for p_ in (HERE / d_).glob('*.obj'):
        for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(p_.read_bytes()):
            if sec > 0 and sc == 2 and nm.startswith('C_'): defd.add(nm)
gseen = set()
by = collections.defaultdict(dict)       # (lib, member) -> {k: [vas]}
for lib, mname, k, vas in place: by[(lib, mname)].setdefault(k, []).extend(vas)
out = HERE / 'crt_obj'; out.mkdir(exist_ok=True)
members = {}
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in BE.read_ar(LIB / ln): members.setdefault((ln, mname), blob)
sys.path.insert(0, str(HERE.parent / 'data-v3'))
from common import ref, SEC, TLO
T = ref[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
def find_text(data, relocs):
    mask = bytearray(b'' * len(data))
    for o, si, ty in relocs:
        for q in range(o, min(o + (2 if ty == 0x0a else 4), len(data))): mask[q] = 0
    runs = []; i = 0
    while i < len(data):
        if mask[i]:
            j = i
            while j < len(data) and mask[j]: j += 1
            runs.append((i, j)); i = j
        else: i += 1
    if not runs: return None
    a, b = max(runs, key=lambda r: r[1] - r[0])
    if b - a < 6: return None
    key = data[a:b][:12]; hits = []; p = T.find(key)
    while p >= 0 and len(hits) < 4:
        st = p - a
        if st >= 0 and st + len(data) <= len(T) and all(T[st + i] == data[i] for i in range(len(data)) if mask[i]): hits.append(st)
        p = T.find(key, p + 1)
    return TLO + hits[0] if len(hits) == 1 else None
stat = collections.Counter()
for n, ((lib, mname), secs) in enumerate(sorted(by.items())):
    blob = members.get((lib, mname))
    if blob is None: stat['member not found'] += 1; continue
    s_ = coffrw.sections(blob); adds = []; seen = set()
    import uncovered_v2 as _U
    parsed = _U.parse_obj(blob)
    if parsed:
        for k, sd in enumerate(parsed[0]):
            if sd['name'].startswith('.text$x') and (sd['flags'] & 0x20) and k not in secs and sd['data']:
                va = find_text(sd['data'], sd['relocs'])
                if va: secs[k] = [va]; stat['.text$x sections located'] += 1
                else: stat['.text$x sections not located'] += 1
    for i, nm, value, sec, ty, sc, naux, o in coffrw.symbols(blob):
        # section numbers in crt_place are 0-based indexes (crt5 'k'): COFF section = k + 1
        if sec > 0 and (sec - 1) in secs and len(set(secs[sec - 1])) == 1 and not nm.startswith('.') and sc in (2, 3):
            va = secs[sec - 1][0] + value
            code = bool(s_[sec - 1]['flags'] & 0x20)
            name = '%s_%08x' % ('C' if code else 'D', va)
            if name in seen or name in gseen or name in dl or name in defd: continue
            seen.add(name); gseen.add(name); adds.append((name, sec, value, 0x20 if code else 0))
    if adds:
        (out / ('%03d_%s.obj' % (n, Path(mname.replace(chr(92), '/')).name[:40]))).write_bytes(coffrw.add_symbols(blob, adds)); stat['members'] += 1; stat['alias symbols'] += len(adds)
print(dict(stat))
