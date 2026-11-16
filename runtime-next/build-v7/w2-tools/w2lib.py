"""w2 library: single-unit compile + unit-level evaluation using assemble_v7 accounting (no writes outside w2)."""
import sys, os, json, collections, re, subprocess, struct
sys.dont_write_bytecode = True
os.environ['W2OBJ'] = '0'
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
W2 = Path(__file__).resolve().parent
PB = Path(r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, str(PB)); sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3'); sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\build-v7')
import numpy as np
import assemble_v3 as A
import compile_units_v3 as CU
import ehdiag as D
import sgmap_w2 as SG
SIDE = {}
FN = A.FN
BAK = PB / 'obj_v3.bak-20261115'
OVR = {}      # obj basename -> path
import ehdiag as _D0
_Coff = _D0._Coff
def _Cov(path, *a, **k):
    p = Path(path)
    if p.name in OVR: p = Path(OVR[p.name])
    elif (BAK / p.name).exists(): p = BAK / p.name
    return _Coff(p, *a, **k)
A.Coff = _Cov
M32 = 0xffffffff
SG_ON = True
LOG = []
LASTDATA = {}
def init_logging():
    orig_rf, orig_fr = A.resolve_field, A.fill_relocs
    def rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw):
        src, exp = orig_rf(coff, unit, locals_, kind, tsym, addend, field_va, orig_raw)
        LOG.append([field_va, kind, src, exp, tsym['name'][:80], addend]); return src, exp
    def fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope):
        n0 = len(LOG); orig_fr(coff, unit, locals_, sec, lo, hi, base_va, buf, stats, pats, scope)
        pe = A.G['pe']; seen = set()
        for e in LOG[n0:]:
            va, kind, src, exp = e[:4]; seen.add(va); st = 'borrow'
            try: raw = pe.read(va, 4)
            except ValueError: raw = None
            if raw is not None and exp is not None and kind == 0x0B:
                try: st = 'agree' if (pe.secrel(exp) & M32) == struct.unpack('<I', raw)[0] else 'disagree'
                except ValueError: st = 'borrow'
            elif raw is not None and exp is not None and kind in (6, 7, 0x14):
                o32, = struct.unpack('<I', raw)
                obs = (va + 4 + struct.unpack('<i', raw)[0]) & M32 if kind == 0x14 else ((o32 + pe.base) & M32 if kind == 7 else o32)
                st = 'agree' if (exp & M32) == obs else 'disagree'
            e += [st, scope]
        for off, idx, kind in sec['relocs']:
            if lo <= off < hi and base_va + off - lo not in seen: LOG.append([base_va + off - lo, kind, 'skip', None, '', 0, 'borrow', scope])
    A.resolve_field, A.fill_relocs = rf, fr
U = None; PE = None; TOOLS = None
def setup():
    global U, PE, TOOLS
    U = D.setup(); PE = A.G['pe']; init_logging()
    TOOLS = CU.find_toolchains()
    return U
def compile_src(idx, src_rel, outobj, extra=()):
    """returns (ok, stdout)"""
    u = U[idx]; info = TOOLS[u['compiler']]
    vc = Path(info['vc']); env = CU.make_env(vc, Path(info['sdk']) if info['sdk'] != 'None' else None)
    r = subprocess.run([str(vc / 'bin' / 'cl.exe'), '/c', '/nologo'] + u['flags'] + list(extra) + ['/I' + str(FN / 'include'), str(FN / src_rel), '/Fo' + str(outobj)],
                       cwd=FN, env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    return r.returncode == 0 and Path(outobj).exists(), r.stdout + r.stderr
def evalunit(idx, objpath=None):
    """-> {addr: (kind, size, good_bytes)} for functions and EH pieces of the unit. good = bytes equal reference minus borrowed (non-agree) fields."""
    name = '%04d.obj' % idx
    if objpath: OVR[name] = str(objpath)
    else: OVR.pop(name, None)
    LOG.clear()
    u = U[idx]
    if SG_ON and objpath:
        side = SIDE.get(idx)
        if side is None:
            side = SIDE[idx] = SG.make_sidecar(_Coff(BAK / name if (BAK / name).exists() else PB / 'obj_v3' / name), u.get('symbols', {}), A.G['sym'])
        u = dict(u, symbols=SG.remap(_Coff(objpath), u.get('symbols', {}), side))
    if not u.get('eh_tails'): u['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    r = A.process((idx, u)); OVR.pop(name, None)
    if r.get('error'): return None
    rl = sorted(LOG, key=lambda e: e[0]); keys = [e[0] for e in rl]
    import bisect
    def good(addr, data, scope_ok):
        L = len(data)
        try: ref = PE.read(addr, L)
        except ValueError: return 0
        if data != ref: return 0
        lo = bisect.bisect_left(keys, addr - 3); hi = bisect.bisect_left(keys, addr + L)
        bor = np.zeros(L, bool)
        for e in rl[lo:hi]:
            if e[7] not in scope_ok: continue
            rel = e[0] - addr
            if e[6] != 'agree' and rel >= 0 and rel < L: bor[rel:rel + 4] = True
        return L - int(bor.sum())
    out = {}
    PAR = {}
    for rec in r['fn']:
        if rec['data'] is not None: out[rec['address']] = ('fn', rec['size'], good(rec['address'], rec['data'], ('fn',)), rec['verdict'])
        else: out[rec['address']] = ('fn', rec['size'], 0, rec['reason'])
    global LASTDATA
    LASTDATA = {t['address']: t['data'] for t in r['tails'] if t['data'] is not None}
    for t in r['tails']:
        if t['data'] is None: continue
        out[t['address']] = ('tail', len(t['data']), good(t['address'], t['data'], ('tail', 'tail_notok')), t['ok'], t['parent'])
    return out
def score(ev): return sum(v[2] for v in ev.values()) if ev else -1
def regress(base, new):
    """addresses where good bytes dropped"""
    return {a: (base[a][2], new.get(a, (0, 0, 0))[2]) for a in base if base[a][2] > new.get(a, (0, 0, 0))[2]}
