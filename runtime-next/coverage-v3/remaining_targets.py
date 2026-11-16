"""Compute the functions still to decompile: .text bytes the v4 build does not produce (strict image vs reference), no recipe entry.
Read-only. Writes remaining_targets.json (addresses, sizes, categories, names; no bytes). Needs rest2_mask.npy from holes_probe.py."""
import sys, json, re, bisect, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
sys.path.insert(0, r'C:\Projects\Decompilation\fnv_decomp\tools')
from compare import Pe
H = r'C:\Projects\Decompilation\runtime-next\coverage-v3'
ref = Pe(r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe')
rva, vs, rs, raw = ref.sections[0]; TV = ref.base + rva
R = np.frombuffer(ref.data, np.uint8)[raw:raw + rs]
M = np.load(H + r'\rest2_mask.npy')
units = json.load(open(r'C:\Projects\Decompilation\fnv_decomp\build\units.json'))['units']
cov = np.zeros(rs, np.uint8)
fnstarts = {}
for u in units:
    for f in u['functions']:
        a = int(f['address'], 16); cov[a - TV:a - TV + f['size']] = 1; fnstarts[a] = f['symbol']
    for t in u.get('eh_tails', []):
        a = int(t['address'], 16) - TV; seg = cov[a:a + t['size']]; seg[seg == 0] = 2
for p in json.load(open(H + r'\extra_pieces.json'))['pieces']:
    a = p['address'] - TV; seg = cov[a:a + p['size']]; seg[seg == 0] = 3 if p['kind'] == 'eh' else 4
M = M & (cov == 0)
print('missing bytes', int(M.sum()))
symaddr = collections.defaultdict(set)
for u in units:
    for k, v in u.get('symbols', {}).items():
        a = int(v, 0)
        if TV <= a < TV + rs: symaddr[a].add(k)
Rb = R.tobytes()
pushref = collections.defaultdict(list)
pushall = collections.defaultdict(list)
for p in np.flatnonzero(R[:-4] == 0x68).tolist():
    v = int.from_bytes(Rb[p + 1:p + 5], 'little')
    if TV <= v < TV + rs:
        pushall[v].append(p + TV)
        if M[v - TV]: pushref[v].append(p + TV)
idx = np.flatnonzero(M); br = np.flatnonzero(np.diff(idx) > 1)
st = np.concatenate(([idx[0]], idx[br + 1])); en = np.concatenate((idx[br], [idx[-1]])) + 1
runs = list(zip(st.tolist(), en.tolist()))
def endsret(b):
    return len(b) > 0 and (b[-1] == 0xc3 or (len(b) >= 3 and b[-3] == 0xc2) or (len(b) >= 5 and b[-5] == 0xe9) or (len(b) >= 6 and b[-6:-4] == b'\xff\x25') or (len(b) >= 2 and b[-2] == 0xeb))
PRO = (b'\x55\x8b\xec', b'\x8b\xff\x55', b'\x83\xec', b'\x56\x57', b'\x6a\xff', b'\xb9', b'\x53', b'\x51', b'\x56', b'\x57', b'\x8b\x44\x24', b'\x8b\x4c\x24', b'\x33\xc0', b'\xa1', b'\x8b\x0d', b'\xb8', b'\xe9', b'\x68')
STRICT = (b'\x55\x8b\xec', b'\x8b\xff\x55\x8b\xec')
def startsok(b): return any(b.startswith(x) for x in PRO)
def strict(b): return any(b.startswith(x) for x in STRICT)
merged = []
for s, e in runs:
    if merged:
        ps, pe_ = merged[-1]
        if s - pe_ <= 3 and set(Rb[pe_:s]) <= {0xcc} and not endsret(Rb[ps:pe_]) and not startsok(Rb[s:s + 4]):
            merged[-1] = (ps, e); continue
    merged.append((s, e))
print('runs', len(runs), 'merged', len(merged))
dw = []
for (r_, v_, rsz, rw), nm in zip(ref.sections, ref.names):
    if nm == '.text': continue
    n = rsz // 4
    dw.append((ref.base + r_, np.frombuffer(ref.data[rw:rw + n * 4], '<u4')))
ehf = []
for base, arr in dw:
    for i in np.flatnonzero((arr >= 0x19930520) & (arr <= 0x19930522)).tolist():
        if i + 2 < len(arr):
            mx = int(arr[i + 1]); pu = int(arr[i + 2])
            if 0 < mx < 4096 and ref.base <= pu < ref.base + 0x2000000: ehf.append((pu, pu + 8 * mx, base + 4 * i))
ehf.sort(); ehf_starts = [x[0] for x in ehf]
def rd(va):
    return int.from_bytes(ref.read(va, 4), 'little')
extra_entries = {}   # address -> kind
for lo, hi, fi in ehf:
    for q in range(lo, hi, 8):
        act = rd(q + 4)
        if TV <= act < TV + rs and M[act - TV]: extra_entries[act] = ('funclet', fi)
    mxs = rd(fi + 12); ptb = rd(fi + 16)
    if 0 < mxs < 512 and ref.base <= ptb < ref.base + 0x2000000:
        for t in range(mxs):
            try:
                nc = rd(ptb + 20 * t + 12); ph = rd(ptb + 20 * t + 16)
                for h in range(min(nc, 64)):
                    ha = rd(ph + 20 * h + 12)
                    if TV <= ha < TV + rs and M[ha - TV]: extra_entries[ha] = ('catch', fi)
            except ValueError: pass
print('unwind/catch entries in missing space', len(extra_entries))
segs = []
allsym = sorted(a - TV for a in symaddr)
allpush = sorted(a - TV for a in pushref)
allextra = sorted(a - TV for a in extra_entries)
def inrange(lst, s, e):
    return lst[bisect.bisect_right(lst, s):bisect.bisect_left(lst, e)]
for s, e in merged:
    ents = [s]
    for c in set(inrange(allsym, s, e)) | set(inrange(allpush, s, e)):
        if endsret(Rb[max(s, c - 6):c]): ents.append(c)
    for c in inrange(allextra, s, e): ents.append(c)
    for m in re.finditer(rb'\xc3|\xc2..', Rb[s:e], re.S):
        c = s + m.end()
        if c < e and strict(Rb[c:c + 5]): ents.append(c)
    ents = sorted(set(ents))
    for i, a in enumerate(ents):
        segs.append((a, ents[i + 1] if i + 1 < len(ents) else e))
print('segments', len(segs))
segaddr = [TV + a for a, _ in segs]
sv = np.array(sorted(segaddr), dtype=np.uint32)
refs = collections.defaultdict(list)
for base, arr in dw:
    for i in np.flatnonzero(np.isin(arr, sv)).tolist(): refs[int(arr[i])].append(base + 4 * i)

stubs = {}
pk = sorted(pushall)
for p in np.flatnonzero(R[:-9] == 0xb8).tolist():
    if Rb[p + 5] in (0xe9, 0xff):
        i = bisect.bisect_right(pk, TV + p) - 1
        start = pk[i] if i >= 0 and TV + p - pk[i] <= 48 else TV + p
        stubs.setdefault(int.from_bytes(Rb[p + 1:p + 5], 'little'), []).append(start)
fa = sorted(fnstarts)
segstarts = sorted(segaddr)
def owner(addr):
    i = bisect.bisect_right(fa, addr) - 1
    j = bisect.bisect_right(segstarts, addr) - 1
    a = fa[i] if i >= 0 else 0; b = segstarts[j] if j >= 0 else 0
    return max(a, b)
out = []
for a, z in segs:
    va = TV + a; size = z - a; b = Rb[a:z]
    while size > 1 and b[size - 1] == 0xcc: size -= 1
    b = b[:size]
    names = sorted(symaddr.get(va, []))
    cat = 'A_real'; why = []; parent = None
    if set(b) <= {0, 0x90, 0xcc}: cat = 'D_ambiguous'; why.append('zero/nop only')
    else:
        w = np.frombuffer(b[:size // 4 * 4], '<u4') if size >= 4 else np.array([], np.uint32)
        if len(w) and float(((w >= TV) & (w < TV + rs)).mean()) > 0.5 and not startsok(b[:4]): cat = 'D_ambiguous'; why.append('mostly .text pointers (table)')
    if cat == 'A_real':
        eh = None
        if any(n.startswith(('__ehhandler$', '__unwindfunclet$', '__catch$')) for n in names): eh = 'symbol'
        if va in pushref and size <= 64 and not strict(b[:5]):
            eh = 'handler-stub'; parent = owner(pushref[va][0])
        elif va in extra_entries and not strict(b[:5]):
            kind, fi = extra_entries[va]
            for stubaddr in stubs.get(fi, []):
                if stubaddr in pushall: parent = owner(pushall[stubaddr][0]); break
            eh = kind
        elif va in refs and size <= 2000 and not strict(b[:5]):
            for q in refs[va]:
                j = bisect.bisect_right(ehf_starts, q) - 1
                if j >= 0 and ehf[j][0] <= q < ehf[j][1]:
                    f = ehf[j][2]
                    for stubaddr in stubs.get(f, []):
                        if stubaddr in pushall: parent = owner(pushall[stubaddr][0]); break
                    eh = 'unwind-funclet'; break
        if eh: cat = 'C_eh'; why.append(eh)
        elif any(n.startswith(('??__E', '??__F', '?__E', '?__F')) for n in names): cat = 'B_static_init'; why.append('symbol')
        elif va >= 0x00fd9000 and size <= 600 and endsret(b): cat = 'B_static_init'; why.append('region .text$y*')
        if cat == 'A_real' and size < 3: cat = 'D_ambiguous'; why.append('tiny')
    if cat == 'C_eh' and not (parent and parent in fnstarts): cat = 'A_real'; why.append('eh-tail-of-undecompiled-or-unresolved-parent')
    out.append(dict(address='0x%08x' % va, size=size, missing=int(M[a:a + size].sum()), category=cat, why=why, names=names[:3], parent=('0x%08x' % parent if parent else None), parent_name=(fnstarts.get(parent) if parent else None)))
cnt = collections.Counter(); byt = collections.Counter()
for o in out: cnt[o['category']] += 1; byt[o['category']] += o['size']
print(dict(cnt), dict(byt), 'total', sum(byt.values()))
par = collections.Counter(o['parent'] for o in out if o['category'] == 'C_eh')
print('eh with parent', sum(v for k, v in par.items() if k), 'no parent', par.get(None, 0), 'distinct parents', len([k for k in par if k]))
json.dump(dict(note='functions still to decompile, from strict image vs reference', total_bytes=sum(byt.values()), counts=dict(cnt), bytes=dict(byt), functions=out), open(H + r'\remaining_targets.json', 'w'))
for o in sorted(out, key=lambda o: -o['size'])[:12]: print(o['address'], o['size'], o['category'], o['names'][:1], o['why'])
