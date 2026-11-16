import sys, json, pickle, collections, re
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import numpy as np
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_32)
name = sys.argv[1] if len(sys.argv) > 1 else 'progress_w2'
P = pickle.load(open(name + '.pkl', 'rb')); G = pickle.load(open('../gaps/dump.pkl', 'rb'))
TV = G['TEXT_VA']; ref = G['ref']
units = json.load(open('C:/Projects/Decompilation/fnv_decomp/build/units.json'))['units']
cB = np.zeros(len(ref), bool); cB[P['cB']] = True
def dis(b, at): return [(i.mnemonic, i.op_str) for i in md.disasm(b, at)]
def norm(m, o): return m + ' ' + re.sub(r'0x[0-9a-f]+', 'N', o)
rows = []; seen = set()
for at, i, hx, parent, notok in sorted(P['RJ']):
    if (at, i) in seen: continue
    seen.add((at, i))
    d = bytes.fromhex(hx); L = len(d); o = at - TV
    m = int(cB[o:o + L].sum())
    if not m: continue
    r = bytes(ref[o:o + L])
    a, b = dis(d, at), dis(r, at)
    k = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
    sig = (norm(*a[k]) if k < len(a) else 'END') + '  <>  ' + (norm(*b[k]) if k < len(b) else 'END')
    rows.append(dict(at=at, i=i, L=L, m=m, sig=sig, parent=parent, ours=a, ref=b, src=units[i]['source']))
print(len(rows), sum(r['m'] for r in rows))
c = collections.Counter(); ex = {}
for r in rows: c[r['sig']] += r['m']; ex.setdefault(r['sig'], []).append(r)
for s, m in c.most_common(40): print(m, len(ex[s]), s)
pickle.dump(rows, open(name + '_rows.pkl', 'wb'))
