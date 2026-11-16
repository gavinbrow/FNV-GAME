r"""link-v2 mkimp.py: import libraries written directly as short-import archive members (no lib.exe /def).
For every `__imp_<dec>` name the link objects reference, mk_implibs' matching (IAT description + symaddr slot map) gives (dll, import name). One member per (dll, import name):
symbol = the import name, NAME import type (imported by exactly that string), plus `/ALTERNATENAME:__imp_<dec>=__imp_<name>` (and `<dec>=<name>` for the call thunk) when the referenced decoration differs.
Writes implibs2\<dll>.lib and opts_imp.txt. usage: python -I mkimp.py"""
import collections
import subprocess, tempfile, os
import json
import re
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RN = HERE.parent
sys.path.insert(0, str(HERE))
import coffrw

spec = json.load(open(RN / 'direct-v1' / 'iat_spec.json'))
byname = collections.defaultdict(set); slot = {}
for d in spec['dlls']:
    for k, e in enumerate(d['ents']):
        if e.get('name'):
            byname[e['name']].add(d['dll']); slot[0x400000 + d['iat'] + 4 * k] = (d['dll'], e['name'])
sa = json.load(open(HERE / 'symaddr.json')); gmap = collections.defaultdict(set)
for _u, _d in sa.items():
    for _n, _a in _d.items():
        if _n.startswith('__imp_'): gmap[_n].update(_a)
imps = set()
for dd in ('obj_rw', 'obj_contrib_rw'):
    for p in (HERE / dd).glob('*.obj'):
        for i, nm, v, sec, ty, sc, naux, o in coffrw.symbols(p.read_bytes()):
            if nm.startswith('__imp_') and sec == 0: imps.add(nm)
ORD = {'accept': ('WSOCK32.dll', 1), 'bind': ('WSOCK32.dll', 2), 'inet_ntoa': ('WSOCK32.dll', 11), 'listen': ('WSOCK32.dll', 13), 'ntohs': ('WSOCK32.dll', 15),
       'setsockopt': ('WSOCK32.dll', 21), 'gethostname': ('WSOCK32.dll', 57), 'WSAStartup': ('WSOCK32.dll', 115), 'XInputGetState': ('XINPUT1_3.dll', 2)}
ordof = {}
pairs = {'__imp__DirectSoundCreate8@12': ('DSOUND.dll', 'DirectSoundCreate8')}; miss = []
for nm in sorted(imps):
    dec = nm[6:]
    m = re.search(r'(?:IMP|FUN|DAT)_([0-9a-f]{6,8})(?:_import)?@', dec)
    if m and int(m.group(1), 16) in slot: pairs[nm] = slot[int(m.group(1), 16)]; continue
    ga = gmap.get(nm)
    if ga and len(ga) == 1 and next(iter(ga)) in slot: pairs[nm] = slot[next(iter(ga))]; continue
    if dec.startswith('_'): und = re.sub(r'@\d+$', '', dec[1:])
    elif dec.startswith('?') and re.match(r'\?(\w+)@', dec): und = re.match(r'\?(\w+)@', dec).group(1)
    else: und = dec
    for c in (und, und.replace('fnv_Import_', '').replace('fnv_', ''), dec, dec[1:]):
        if c in ORD: pairs[nm] = (ORD[c][0], c); ordof[c] = ORD[c][1]; break
        if c in byname: pairs[nm] = (sorted(byname[c])[0], c); break
    else: miss.append(nm)


def member(dll, name, ordinal=0):
    sym = name.encode('latin1') + b'\0'; dl = dll.encode('latin1') + b'\0'
    hdr = struct.pack('<HHHHIIHH', 0, 0xFFFF, 0, 0x14c, 0, len(sym) + len(dl), ordinal, 0 | ((0 if ordinal else 1) << 2))      # import type CODE, name type NAME
    return hdr + sym + dl


def descr_members(dll):
    # descriptor / null descriptor / null thunk objects: taken from a lib.exe-built stub library (one dummy export)
    import build_extra as BE
    d = Path(tempfile.mkdtemp(prefix='impd_', dir=str(HERE / 'implibs2_tmp')))
    (d / 'x.def').write_text('LIBRARY %s' % dll + chr(10) + 'EXPORTS' + chr(10) + '  dummy_x' + chr(10))
    env = dict(os.environ); vc = 'C:/Projects/Decompilation/FNV/tools/vc2008'
    env['PATH'] = vc + '/VC/bin;' + vc + '/Common7/IDE;' + env['PATH']
    subprocess.run([vc + '/VC/bin/lib.exe', '/nologo', '/MACHINE:X86', '/DEF:' + str(d / 'x.def'), '/OUT:' + str(d / 'x.lib')], env=env, capture_output=True)
    res = []
    for mn, blob in BE.read_ar(d / 'x.lib'):
        if mn.strip('/ ') == '' or blob[:4] == bytes([0, 0, 0xFF, 0xFF]) or blob[:2] != bytes([0x4c, 1]): continue
        ss = [nm for i, nm, v, sec, ty, sc, naux, o in coffrw.symbols(blob) if sec > 0 and sc == 2]
        res.append((ss, blob))
    return res


def archive(dll, names):
    mems = descr_members(dll)                    # (symbols, data)
    for n in sorted(names): mems.append(([('__imp_' + n), n], member(dll, n, ordof.get(n, 0))))
    # layout: '!<arch>\n' + first linker member + members
    syms = [s for m in mems for s in m[0]]
    strtab = b''.join(s.encode('latin1') + b'\0' for s in syms)
    first_size = 4 + 4 * len(syms) + len(strtab)
    first_pad = first_size & 1
    off = 8 + 60 + first_size + first_pad
    offs = []
    for ss, data in mems:
        offs += [off] * len(ss)
        off += 60 + len(data) + (len(data) & 1)
    first = struct.pack('>I', len(syms)) + b''.join(struct.pack('>I', o) for o in offs) + strtab
    def hdr(name, size): return (name.ljust(16)[:16] + '0'.ljust(12) + '0'.ljust(6) + '0'.ljust(6) + '0'.ljust(8) + str(size).ljust(10) + '`\n').encode('latin1')
    out = bytearray(b'!<arch>\n') + hdr('/', len(first)) + first + (b'\n' * first_pad)
    for ss, data in mems:
        out += hdr(dll[:15] + '/', len(data)) + data + (b'\n' * (len(data) & 1))
    return bytes(out)


out = HERE / 'implibs2'; out.mkdir(exist_ok=True); (HERE / 'implibs2_tmp').mkdir(exist_ok=True); sys.path.insert(0, str(RN / 'coverage-v3'))
bydll = collections.defaultdict(set); alt = []
for nm, (dll, c) in pairs.items():
    bydll[dll].add(c)
    dec = nm[6:]
    if dec != c: alt.append('/ALTERNATENAME:%s=__imp_%s' % (nm, c)); alt.append('/ALTERNATENAME:%s=%s' % (dec, c))
sys.path.insert(0, str(RN / 'data-v3'))
from common import ref as _ref, SEC as _SEC, TLO as _TLO
_T = _ref[_SEC['.text']['off']:_SEC['.text']['off'] + _SEC['.text']['raw']]
nthunk = 0
for va in json.load(open(HERE / 'code_targets.json')):
    o = va - _TLO
    if 0 <= o < len(_T) - 6 and _T[o:o + 2] == bytes([0xff, 0x25]):
        tgt = struct.unpack_from('<I', _T, o + 2)[0]
        if tgt in slot:
            dll_, c_ = slot[tgt]; bydll[dll_].add(c_); alt.append('/ALTERNATENAME:C_%08x=%s' % (va, c_)); nthunk += 1
print('import call thunks bound', nthunk)
for dll, names in bydll.items(): (out / (dll.rsplit('.', 1)[0] + '.lib')).write_bytes(archive(dll, names))
(HERE / 'opts_imp.txt').write_text('\n'.join(alt) + '\n')
print('import names', len(imps), 'matched', len(pairs), 'dlls', {k: len(v) for k, v in bydll.items()}, 'unmatched', len(miss), miss[:12])
