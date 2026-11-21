r"""M3 phase 1 splice library: bytes of generated global definitions, sliced out of the compiled m3_data.obj.
load(manifest=None, obj=None) -> list of dict(va, data(bytes), relocs[(offset, symname, addend)], entry)
Used by place.py (via m3secs), layout-v2\make_image.py and data-v3\verify.py (all only when FNV_M3=1)."""
import os, sys, json, re, bisect, struct
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
sys.path.insert(0, os.path.join(PROJ, 'fnv_decomp', 'tools'))
from compare import Coff
GEN = os.path.join(HERE, 'gen')
MANIFEST = os.path.join(GEN, 'm3_manifest.json')
OBJ = os.path.join(GEN, 'm3_data.obj')

ADDR_RE = re.compile(r'(?:^|_)(?:M3[FD]|FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC|D|C)_([0-9a-f]{8})$')
M32 = 0xffffffff
SYM_RE = re.compile(r'\?(?:DAT|M3)_([0-9a-f]{8})(?:@[A-Za-z0-9_]+)*@@3')      # mangled names of generated definitions, also inside namespaces (?DAT_<va>@fnv_xxxx@@3..)


class RangeClaims:
    """Reject overlapping overlay claims regardless of their byte contents."""
    def __init__(self):
        self.ranges = []

    def add(self, va, size):
        if size <= 0:
            raise ValueError('overlay range must be nonempty')
        end = va + size
        i = bisect.bisect_left(self.ranges, (va,))
        if (i and self.ranges[i - 1][1] > va) or (i < len(self.ranges) and self.ranges[i][0] < end):
            raise ValueError('overlapping overlay ranges at %x' % va)
        self.ranges.insert(i, (va, end))


def validate_records(records):
    claims = RangeClaims()
    for record in records:
        claims.add(record['va'], len(record['data']))


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
    # Coff materializes raw-less uninitialized sections as zero bytes. Those
    # represent memory allocation, not bytes the object can supply for splice.
    # Inspect the original section header rather than trusting the synthesized data.
    header = 20 + (sy['section'] - 1) * 40
    raw_size, raw_ptr = struct.unpack_from('<II', c.data, header + 16)
    if not raw_ptr or o < 0 or n < 0 or o + n > raw_size or raw_ptr + o + n > len(c.data):
        raise ValueError('symbol %s is not backed by object file bytes' % e['sym'])
    if e.get('align') == 16:
        encoded = (sec['flags'] >> 20) & 15
        if encoded < 5 or encoded > 14 or o % 16: raise ValueError('COFF symbol or section lacks 16-byte alignment')
    data = bytes(sec['data'][o:o + n])
    rel = []
    ix = c.__dict__.setdefault('_ridx', {})
    if sy['section'] not in ix:      # relocations of the section sorted by offset (batch 7: tens of thousands per section)
        rs = sorted(sec['relocs'], key=lambda r: r[0]); ix[sy['section']] = ([r[0] for r in rs], rs)
    offs, rs = ix[sy['section']]
    # Include preceding DIR32 sites so a cell straddling the symbol start is
    # not silently missed. Every included DIR32 cell must fit wholly inside it.
    for j in range(bisect.bisect_left(offs, max(0, o - 3)), bisect.bisect_left(offs, o + n)):
        off, ri, kind = rs[j]
        if off < o:
            if kind == 6 and off + 4 > o:
                raise ValueError('DIR32 relocation crosses start of symbol %s' % e['sym'])
            continue
        if kind != 6: raise ValueError('relocation kind %d at +%d is not DIR32' % (kind, off - o))
        if off + 4 > o + n:
            raise ValueError('DIR32 relocation crosses end of symbol %s' % e['sym'])
        if rel and off - o < rel[-1][0] + 4:
            raise ValueError('overlapping DIR32 relocations in symbol %s' % e['sym'])
        add = int.from_bytes(sec['data'][off:off + 4], 'little', signed=True)
        rel.append((off - o, c.symbols[ri]['name'], add))
    return data, rel, sec['name'], sec['flags'], sy['storage']


def load(manifest=None, obj=None):
    """-> [dict(va, data, relocs[(offset, symname, addend)], reloc_va[target VA per reloc], entry)]; pointer fields are checked against the manifest
    (offsets == entry['fields'] offsets, target VA == entry['ptr']['target'], bytes at the field == addend)."""
    with open(manifest or MANIFEST) as fh:
        man = json.load(fh)
    # Zero-filled objects cannot expose overlap via the overlay's non-zero test.
    # Reject overlapping claimed address ranges independently of their contents.
    for e in man['entries']:
        alignment = e.get('align') or e['size']
        if type(alignment) is not int or alignment not in (1, 2, 4, 8, 16) or e['va'] % alignment:
            raise ValueError('invalid M3 destination alignment for %s' % e['sym'])
    ranges = sorted((e['va'], e['va'] + e['size'], e['sym']) for e in man['entries'])
    for a, b in zip(ranges, ranges[1:]):
        if b[0] < a[1]:
            raise ValueError('overlapping M3 ranges: %s and %s' % (a[2], b[2]))
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
    control_meta = {}
    neg = os.environ.get('FNV_M3_NEGCTL')
    for p in json.load(open(path or DV1))['pieces']:
        rel = []; rv = []
        for off, tgt, add in p['relocs']:
            rel.append((off, 'M5T_%08x' % tgt, 0)); rv.append(tgt)
        entry = dict(section=p['section'], kind=p['kind'], tier=p['tier'], unit=p['unit'], size=p['size'], ext=bool(p.get('ext')))
        if p.get('library_opt_in') is True: entry['library_opt_in'] = True
        if neg in ('p2rv', 'p2rp', 'p2tv', 'p2tp', 'p2nv', 'p2np', 'p2bv', 'p2bp', 'p2cv', 'p2cp'): control_meta.setdefault(p['va'], []).append((p.get('names'), p.get('nunits')))
        out.append(dict(va=p['va'], data=bytes.fromhex(p['data']), relocs=rel, reloc_va=rv, entry=entry))
    neg = os.environ.get('FNV_M3_NEGCTL')
    if neg in ('p2rv', 'p2rp'):
        va, size, kind = (0x1196e20, 26, 'rtti0') if neg == 'p2rv' else (0x110fbe8, 20, 'rtti4')
        pieces = [r for r in out if r['va'] == va]
        if len(pieces) != 1: raise ValueError('PSA control requires exactly one native piece')
        r = pieces[0]; e = r['entry']
        if e['unit'] != 620 or e['kind'] != kind or e['section'] != ('.data' if neg == 'p2rv' else '.rdata') or e['size'] != size or control_meta.get(va) != [((['??_R0?AVTESModelPSA@@@8'] if neg == 'p2rv' else ['??_R4TESModelPSA@@6B@']), 1)] or len(r['data']) != size: raise ValueError('PSA control native piece identity mismatch')
        if neg == 'p2rv':
            if r['data'] != b'\0'*8 + b'.?AVTESModelPSA@@\0' or r['relocs'] != [(0, 'M5T_010f1ee0', 0)] or r['reloc_va'] != [0x10f1ee0]: raise ValueError('PSA TD field mismatch')
            data = bytearray(r['data']); data[8] ^= 1; r['data'] = bytes(data)
            print('NEGATIVE CONTROL (p2 PSA value): VA 01196e20 offset 8 changed from 2e to 2f')
        else:
            alts = [q for q in out if q['va'] == 0x11831e8 and q['entry']['kind'] == 'rtti0']
            ix = [i for i, (off, name, add) in enumerate(r['relocs']) if off == 12 and name == 'M5T_01196e20' and add == 0]
            if len(alts) != 1 or alts[0]['entry']['unit'] != 250 or alts[0]['entry']['size'] != 23 or alts[0]['entry']['section'] != '.data' or control_meta.get(0x11831e8) != [(['??_R0?AVTESModel@@@8'], 36)] or alts[0]['data'] != b'\0'*8 + b'.?AVTESModel@@\0' or alts[0]['relocs'] != [(0, 'M5T_010f1ee0', 0)] or alts[0]['reloc_va'] != [0x10f1ee0] or r['data'] != b'\0'*20 or len(ix) != 1 or r['relocs'] != [(12, 'M5T_01196e20', 0), (16, 'M5T_0110fbfc', 0)] or r['reloc_va'] != [0x1196e20, 0x110fbfc]: raise ValueError('PSA COL relocation or alternate mismatch')
            j = ix[0]; r['relocs'][j] = (12, 'M5T_011831e8', 0); r['reloc_va'][j] = 0x11831e8
            print('NEGATIVE CONTROL (p2 PSA pointer): VA 0110fbe8 offset 12 changed from 01196e20 to 011831e8')
        e['negctl'] = neg
    elif neg in ('p2tv', 'p2tp'):
        va = 0x011b8140
        candidates = [r for r in out if r['va'] == va]
        if len(candidates) != 1: raise ValueError('typeid control requires exactly one native piece')
        r = candidates[0]; e = r['entry']
        if e['unit'] != 2996 or e['kind'] != 'rtti0' or e['tier'] != 'B' or e['section'] != '.data' or e['size'] != 47 or e['ext'] or control_meta.get(va) != [(['??_R0?AVhkpConstraintChainInstanceAction@@@8'], 1)]: raise ValueError('typeid control native piece identity mismatch')
        if r['data'] != b'\0'*8 + b'.?AVhkpConstraintChainInstanceAction@@\0' or r['relocs'] != [(0, 'M5T_010f1ee0', 0)] or r['reloc_va'] != [0x010f1ee0]: raise ValueError('typeid control field mismatch')
        if neg == 'p2tv':
            data = bytearray(r['data']); data[8] ^= 1; r['data'] = bytes(data)
            print('NEGATIVE CONTROL (p2 typeid value): VA 011b8140 offset 8 changed from 2e to 2f')
        else:
            r['relocs'][0] = (0, 'M5T_010f1ee4', 0); r['reloc_va'][0] = 0x010f1ee4
            print('NEGATIVE CONTROL (p2 typeid pointer): VA 011b8140 offset 0 changed from 010f1ee0 to 010f1ee4')
        e['negctl'] = neg
    elif neg in ('p2cv', 'p2cp'):
        va = 0x01183f7c
        candidates = [r for r in out if r['va'] == va]
        if len(candidates) != 1: raise ValueError('bulk control requires exactly one native descriptor')
        r = candidates[0]; e = r['entry']
        if e['unit'] != 3019 or e['kind'] != 'rtti0' or e['tier'] not in ('B', 'H') or e['section'] != '.data' or e['size'] != 28 or e['ext'] or control_meta.get(va) != [(['??_R0?AVBaseExtraList@@@8'], 1)]: raise ValueError('bulk descriptor identity mismatch')
        if r['data'] != b'\0'*8 + b'.?AVBaseExtraList@@\0' or r['relocs'] != [(0, 'M5T_010f1ee0', 0)] or r['reloc_va'] != [0x010f1ee0]: raise ValueError('bulk descriptor field mismatch')
        if neg == 'p2cv':
            data = bytearray(r['data']); data[8] ^= 1; r['data'] = bytes(data)
            print('NEGATIVE CONTROL (p2 bulk value): VA 01183f7c offset 8 changed from 2e to 2f')
        else:
            r['relocs'][0] = (0, 'M5T_010f1ee4', 0); r['reloc_va'][0] = 0x010f1ee4
            print('NEGATIVE CONTROL (p2 bulk pointer): VA 01183f7c offset 0 changed from 010f1ee0 to 010f1ee4')
        e['negctl'] = neg
    elif neg in ('p2bv', 'p2bp'):
        va = 0x011ac95c
        candidates = [r for r in out if r['va'] == va]
        if len(candidates) != 1: raise ValueError('BSAudio control requires exactly one native descriptor')
        r = candidates[0]; e = r['entry']
        if e['unit'] != 3018 or e['kind'] != 'rtti0' or e['tier'] not in ('B', 'H') or e['section'] != '.data' or e['size'] != 22 or e['ext'] or control_meta.get(va) != [(['??_R0?AVBSAudio@@@8'], 1)]: raise ValueError('BSAudio descriptor identity mismatch')
        if r['data'] != b'\0'*8 + b'.?AVBSAudio@@\0' or r['relocs'] != [(0, 'M5T_010f1ee0', 0)] or r['reloc_va'] != [0x010f1ee0]: raise ValueError('BSAudio descriptor field mismatch')
        if neg == 'p2bv':
            data = bytearray(r['data']); data[8] ^= 1; r['data'] = bytes(data)
            print('NEGATIVE CONTROL (p2 BSAudio value): VA 011ac95c offset 8 changed from 2e to 2f')
        else:
            r['relocs'][0] = (0, 'M5T_010f1ee4', 0); r['reloc_va'][0] = 0x010f1ee4
            print('NEGATIVE CONTROL (p2 BSAudio pointer): VA 011ac95c offset 0 changed from 010f1ee0 to 010f1ee4')
        e['negctl'] = neg
    elif neg in ('p2nv', 'p2np'):
        va = 0x01185d30
        candidates = [r for r in out if r['va'] == va]
        if len(candidates) != 1: raise ValueError('native literal control requires exactly one piece')
        r = candidates[0]; e = r['entry']
        if e['unit'] != 75 or e['kind'] != 'rtti0' or e['tier'] != 'B' or e['section'] != '.data' or e['size'] != 64 or e['ext'] or control_meta.get(va) != [(['??_R0?AV?$LockFreeQueue@V?$NiPointer@VQueuedReference@@@@@@@8'], 1)]: raise ValueError('native literal control identity mismatch')
        if r['data'] != bytes.fromhex('00000000000000002e3f41563f244c6f636b46726565517565756540563f244e69506f696e74657240565175657565645265666572656e636540404040404000') or r['relocs'] != [(0, 'M5T_010f1ee0', 0)] or r['reloc_va'] != [0x010f1ee0]: raise ValueError('native literal control bytes or relocation mismatch')
        if neg == 'p2nv':
            data = bytearray(r['data']); data[8] ^= 1; r['data'] = bytes(data)
            print('NEGATIVE CONTROL (p2 native literal value): VA 01185d30 offset 8 changed from 2e to 2f')
        else:
            r['relocs'][0] = (0, 'M5T_010f1ee4', 0); r['reloc_va'][0] = 0x010f1ee4
            print('NEGATIVE CONTROL (p2 native literal pointer): VA 01185d30 offset 0 changed from 010f1ee0 to 010f1ee4')
        e['negctl'] = neg
    elif neg == 'p2lv':
        candidates = [r for r in out if r['entry'].get('library_opt_in') is True and r['data'] and not r['relocs']]
        if not candidates: raise ValueError('p2lv requires a marked non-relocating library piece')
        r = candidates[0]; old = r['data'][0]; changed = old ^ 1
        r['data'] = bytes([changed]) + r['data'][1:]; r['entry']['negctl'] = 'p2lv'
        print('NEGATIVE CONTROL (p2 library value): VA %08x offset 0 changed from %02x to %02x' % (r['va'], old, changed))
    elif neg == 'b5v':          # negative control: one byte of the first piece with a non-relocated, non-zero first byte changes
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
