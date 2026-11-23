r"""M3 batch 9 stage 3, part A: extra library candidates (whole sections that are plain, byte-identical to the reference, placed by data-v1, and were left out of phase2\library_candidates.json
because several library members claim the same address or overlap).  python -I b9_libext.py <dv1_placed.pkl> [--out phase2\library_candidates_b9s3.json]
Same schema as library_candidates.json (validated at build time by phase2\library_overlay.select_library, pinned by digest); where several candidates share an address the lowest unit id wins,
overlapping candidates are dropped greedily (largest first).  Claims = default coverage (inventory\b9_default_cov.json) + stage 1 objects (batch9_selection.json batch 9) + rewritten ranges.
Needs FNV_REF_IMAGE (the stand-in image is fine)."""
import os, sys, json, hashlib, bisect, collections, pickle
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'; RN = os.path.join(PROJ, 'runtime-next')
pkl = sys.argv[1]; OUT = os.path.join(HERE, 'phase2', 'library_candidates_b9s3.json')
if '--out' in sys.argv: OUT = os.path.join(HERE, sys.argv[sys.argv.index('--out') + 1])
sys.path.insert(0, os.path.join(RN, 'data-v1')); sys.path.insert(0, os.path.join(RN, 'data-v3')); sys.path.insert(0, os.path.join(RN, 'data-v2'))
import place as PL, libsecs
from common import SEC, sec_of, orig_reloc_sites, read_ref
st = pickle.load(open(pkl, 'rb'))
J = os.path.join
cov = json.load(open(J(HERE, 'inventory', 'b9_default_cov.json')))
s1 = [e for e in json.load(open(J(HERE, 'batch9_selection.json')))['entries'] if e.get('batch') == 9]
REW = ((0xfdf000, 0xfdf4a4), (0x118062c, 0x118204c), (0x110147c, 0x1101494))
claims = sorted([tuple(x) for x in cov['m3'] + cov['dv1']] + list(REW))
cl_lo = [a for a, b in claims]
def claimed(a, b):
    i = bisect.bisect_right(cl_lo, a) - 1
    for j in range(max(0, i - 1), min(len(claims), i + 3)):
        if claims[j][0] < b and a < claims[j][1]: return True
    return False
sj = json.load(open(J(RN, 'data-v3', 'symbolic.json'))); fields = sorted({SEC[r[0]]['va'] + r[1] for r in sj['fields']} | orig_reloc_sites())
def field_in(a, b):
    i = bisect.bisect_left(fields, a - 3); return i < len(fields) and fields[i] < b
chunks = [(c['va'], c['va'] + c['size'], c['section'], c['file']) for c in json.load(open(J(RN, 'data-v3', 'out', 'manifest.json'))) if c['section'] in ('.data', '.rdata')]
triage = json.load(open(J(HERE, 'phase2', 'library_triage.json'))); members = {x['unit']: x for x in triage['member_coverage_nonadditive']}
dig = lambda b: hashlib.sha256(b).hexdigest()
objh = {}; uid = 100000
for lib in ('libcmt.lib', 'libcpmt.lib'):
    for _, blob in libsecs.U.read_ar(libsecs.LIB / lib): uid += 1; objh[uid] = dig(blob)
units = libsecs.lib_units()
ALLOWED = ('rdata-other-unit', 'data-unit', 'rdata-other', 'data', 'float-const', 'string')
inv_key = collections.defaultdict(list)
for (u, k), key in st.KEYOF.items(): inv_key[key].append((u, k))
found = []; rej = collections.Counter()
for key, (A, tier) in st.placed.items():
    s = st.SEC[key]; L = len(s['data'])
    if not any(u >= 100000 for u in s['units']) or any(u < 100000 for u in s['units']): continue
    if s['kind'] not in ALLOWED or L == 0 or tier == 'M' or not any(s['data']) or s['relocs']: rej['kind/reloc/zero'] += L; continue
    if sec_of(A) not in ('.data', '.rdata'): continue
    if claimed(A, A + L): rej['claimed'] += L; continue
    if not inv_key.get(key): rej['no-KEYOF'] += L; continue
    for (u, k) in inv_key.get(key, []):
        if u < 100000: continue
        if claimed(A, A + L): rej['claimed'] += 1; continue
        if field_in(A, A + L): rej['field'] += 1; continue
        ch = [(f, sec) for x, y, sec, f in chunks if x <= A and A + L <= y]
        if len(ch) != 1: rej['chunk'] += 1; continue
        if read_ref(A, L) != bytes(s['data']): rej['differs'] += 1; continue
        o = [x for x in units.get(u, {}).get('secs', []) if x['k'] == k]
        if len(o) != 1 or o[0]['relocs'] or o[0]['data'] != s['data'] or o[0]['defs'] != s['defs'] or o[0]['flags'] != s['flags'] or o[0]['name'] != s['name']: rej['source-section'] += 1; continue
        if (u, A) not in {(uu, A) for uu in s['units'] if uu >= 100000}: rej['units'] += 1; continue
        bits = (s['flags'] >> 20) & 15; al = 1 << (bits - 1) if bits else 1
        if A % al: rej['alignment'] += 1; continue
        offs = {d[0]: d[1] for d in s['defs']}
        if not offs: rej['no-symbol'] += 1; continue
        m = members[u]
        found.append({'va': A, 'size': L, 'section': ch[0][1], 'chunk': ch[0][0], 'kind': s['kind'], 'tier': tier, 'unit': u, 'library': m['library'], 'archive_sha256': triage['library_sha256'][m['library']],
                      'member': m['member'], 'object_sha256': objh[u], 'unit_section_index': k, 'section_flags': s['flags'], 'alignment': al, 'symbol_offsets': offs, 'section_name': s['name'],
                      'compiler_bytes_sha256': dig(bytes(s['data'])), 'evidence': 'batch9 stage 3: whole library section, plain, byte-identical to the reference, placed by data-v1; one of several members at this address: lowest unit id',
                      'limitations': 'library placement opt-in; source ownership still requires review'})
by = {}
for x in sorted(found, key=lambda x: (x['va'], x['size'], x['unit'])):
    by.setdefault((x['va'], x['size']), x)
cand = sorted(by.values(), key=lambda x: (-x['size'], x['va'])); keep = []
for x in cand:
    if not any(y['va'] < x['va'] + x['size'] and x['va'] < y['va'] + y['size'] for y in keep): keep.append(x)
keep.sort(key=lambda x: x['va'])
base = json.load(open(J(HERE, 'phase2', 'library_candidates.json')))['candidates']; allc = sorted(base + keep, key=lambda x: x['va'])
doc = {'scope': 'phase2 library_candidates.json (%d) + batch 9 stage 3 additions (%d): whole library sections left out of the first list (several members at one address); lowest unit id' % (len(base), len(keep)), 'candidate_count': len(allc), 'candidate_bytes': sum(x['size'] for x in allc), 'candidates': allc}
json.dump(doc, open(OUT, 'w'), indent=1)
print('found', len(found), 'unique identity', len(by), 'added', len(keep), sum(x['size'] for x in keep), 'bytes; total', len(allc), doc['candidate_bytes'], 'rejects', dict(rej))
