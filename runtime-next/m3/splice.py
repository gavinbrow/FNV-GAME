r"""M3 phase 1 splice library: bytes of generated global definitions, sliced out of the compiled m3_data.obj.
load(manifest=None, obj=None) -> list of dict(va, data(bytes), relocs[(offset, symname, addend)], entry)
Used by place.py (via m3secs), layout-v2\make_image.py and data-v3\verify.py (all only when FNV_M3=1)."""
import os, sys, json, re, bisect
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\Projects\Decompilation'
sys.path.insert(0, os.path.join(PROJ, 'fnv_decomp', 'tools'))
from compare import Coff
GEN = os.path.join(HERE, 'gen')
MANIFEST = os.path.join(GEN, 'm3_manifest.json')
OBJ = os.path.join(GEN, 'm3_data.obj')

ADDR_RE = re.compile(r'(?:^|_)(?:M3[FD]|FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC|D|C)_([0-9a-f]{8})$')
M32 = 0xffffffff
SYM_RE = re.compile(r'\?(?:DAT|M3)_([0-9a-f]{8})(?:@[A-Za-z0-9_]+)*@@3')      # mangled names of generated definitions, also inside namespaces (?DAT_<va>@fnv_xxxx@@3..)


def objpath(base, k):
    """object k of the generated globals: m3_data.obj (k=0), m3_data_<k>.obj (batch 7: one COFF section holds at most 65535 relocations)"""
    if not k: return base
    root, ext = os.path.splitext(base); return '%s_%d%s' % (root, k, ext)


def resolve(name, table=None):
    """symbol name used by the m3 object -> original VA. m3 definitions (manifest sym/name) first, then the address embedded in the name
    (extern "C" targets M3F_<va>/M3D_<va> -> '_M3F_<va>', or _FUN_/_DAT_/D_/C_ style names). None when unresolvable."""
    if table and name in table: return table[name]
    m = ADDR_RE.search(name)
    if m: return int(m.group(1), 16)
    m = SYM_RE.match(name)
    return int(m.group(1), 16) if m else None


def name_table(entries):
    t = {}
    for e in entries: t[e['sym']] = e['va']; t[e['name']] = e['va']
    return t


def slice_entry(c, e):
    """-> (bytes, relocs, section name, flags, storage) of the definition of symbol e['sym'] in Coff c (sliced per symbol: exactly e['size'] bytes).
    relocs = [(offset in the object, target symbol name, addend)]; every relocation must be DIR32 (kind 6)."""
    sy = c.named(e['sym']); sec = c.sections[sy['section']]
    o = sy['value']; n = e['size']
    data = bytes(sec['data'][o:o + n])
    rel = []
    ix = c.__dict__.setdefault('_ridx', {})
    if sy['section'] not in ix:      # relocations of the section sorted by offset (batch 7: tens of thousands per section)
        rs = sorted(sec['relocs'], key=lambda r: r[0]); ix[sy['section']] = ([r[0] for r in rs], rs)
    offs, rs = ix[sy['section']]
    for j in range(bisect.bisect_left(offs, o), bisect.bisect_left(offs, o + n)):
        off, ri, kind = rs[j]
        if kind != 6: raise ValueError('relocation kind %d at +%d is not DIR32' % (kind, off - o))
        add = int.from_bytes(sec['data'][off:off + 4], 'little', signed=True)
        rel.append((off - o, c.symbols[ri]['name'], add))
    return data, rel, sec['name'], sec['flags'], sy['storage']


def load(manifest=None, obj=None):
    """-> [dict(va, data, relocs[(offset, symname, addend)], reloc_va[target VA per reloc], entry)]; pointer fields are checked against the manifest
    (offsets == entry['fields'] offsets, target VA == entry['ptr']['target'], bytes at the field == addend)."""
    man = json.load(open(manifest or MANIFEST))
    base = obj or OBJ; cs = {k: Coff(objpath(base, k)) for k in man.get('objs', [0])}; out = []; tab = name_table(man['entries'])
    for e in man['entries']:
        data, rel, sname, fl, st = slice_entry(cs[e.get('obj', 0)], e)
        assert sname == e['section'] and len(data) == e['size'], (e['sym'], sname, len(data))
        want = [f[0] for f in e.get('fields', [])]
        assert [r[0] for r in rel] == want, ('pointer field offsets differ from the manifest', e['sym'], rel, want)
        rv = []
        for off, nm, add in rel:
            t = resolve(nm, tab); assert t is not None, ('unresolvable relocation target', e['sym'], nm)
            rv.append(t)
        out.append(dict(va=e['va'], data=data, relocs=rel, reloc_va=rv, entry=e))
    return out


DV1 = os.path.join(GEN, 'dv1_pieces.json')


def load_dv1(path=None):
    """Batch 5 (opt-in FNV_M3_DV1=1): data-v1 placed pieces of OUR unit objects (m3\dv1_splice.py selection). -> same record format as load():
    dict(va, data, relocs[(offset, symname, addend)], reloc_va[target VA], entry=dict(section, kind, tier, unit)). The pointer fields are DIR32 relocations of the
    compiled objects whose target our resolution produced (== the reference value, checked by dv1_splice.py and again by verify.py / make_image.py); they are re-linked
    as synthetic symbol 'M5T_<target va>' (alladdr -> that VA) with addend 0, so the common rewrite loop emits Lone(target) and the original .reloc site."""
    out = []
    for p in json.load(open(path or DV1))['pieces']:
        rel = []; rv = []
        for off, tgt, add in p['relocs']:
            rel.append((off, 'M5T_%08x' % tgt, 0)); rv.append(tgt)
        out.append(dict(va=p['va'], data=bytes.fromhex(p['data']), relocs=rel, reloc_va=rv, entry=dict(section=p['section'], kind=p['kind'], tier=p['tier'], unit=p['unit'], size=p['size'], ext=bool(p.get('ext')))))
    neg = os.environ.get('FNV_M3_NEGCTL')
    if neg == 'b5v':          # negative control: one byte of the first piece with a non-relocated, non-zero first byte changes
        for r in out:
            if r['data'] and r['data'][0] and not any(o < 1 for o, _n, _a in r['relocs']): r['data'] = bytes([r['data'][0] ^ 1]) + r['data'][1:]; r['entry']['negctl'] = 'b5v'; break
    elif neg == 'b5p':        # negative control: the first relocation of the first piece with relocations is retargeted to a different valid target
        rs = [r for r in out if r['relocs']]
        for r in rs:
            alt = next((t for q in rs for t in q['reloc_va'] if t != r['reloc_va'][0]), None)
            if alt is not None: o, _n, a = r['relocs'][0]; r['relocs'][0] = (o, 'M5T_%08x' % alt, a); r['reloc_va'][0] = alt; r['entry']['negctl'] = 'b5p'; break
    elif neg in ('b6v', 'b6p'):   # batch 6 negative controls, in a piece that exists only through the EXT resolution (ext flag set by dv1_splice.py)
        ex = [r for r in out if r['entry'].get('ext')]
        assert ex, 'FNV_M3_NEGCTL=%s needs EXT pieces (FNV_M3_DV1_EXT=1)' % neg
        if neg == 'b6v':          # one non-relocated non-zero byte of the first EXT piece that has one
            for r in ex:
                rel = {o + i for o, _n, _a in r['relocs'] for i in range(4)}
                j = next((i for i, b in enumerate(r['data']) if b and i not in rel), None)
                if j is not None: d = bytearray(r['data']); d[j] ^= 1; r['data'] = bytes(d); r['entry']['negctl'] = 'b6v'; break
        else:                     # the first relocation of the first EXT piece with relocations is retargeted
            alls = [t for q in out for t in q['reloc_va']]
            for r in ex:
                if r['relocs']:
                    alt = next(t for t in alls if t != r['reloc_va'][0]); o, _n, a = r['relocs'][0]; r['relocs'][0] = (o, 'M5T_%08x' % alt, a); r['reloc_va'][0] = alt; r['entry']['negctl'] = 'b6p'; break
    return out
