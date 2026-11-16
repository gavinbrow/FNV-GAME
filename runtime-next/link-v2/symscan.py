r"""link-v2 symscan.py: symbol census of everything that goes into the link (unit objects, contribution objects, data-v3 objects, libcmt/libcpmt).
Writes symscan.json: defined (name -> [(origin, comdat)]), undefined names with referencing origins, duplicates, categories. usage: python -I symscan.py"""
import collections
import json
import re
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import uncovered_v2 as U

RN = Path(r'C:\Projects\Decompilation\runtime-next')
HERE = RN / 'link-v2'
ADDR = re.compile(r'(?<![0-9A-Za-z])(?:FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC|g|C|D|X)_([0-9a-f]{8})(?![0-9A-Za-z])')
defs = collections.defaultdict(list)       # name -> [(origin, comdat)]
undef = collections.defaultdict(set)
origins = {}


def scan(path, origin):
    r = U.parse_obj(path.read_bytes())
    if not r: return
    secs, syms = r
    for si, (nm, value, sec, ty, sc) in syms.items():
        if sc == 2 or sc == 105:
            if sec > 0:
                s = secs[sec - 1]
                defs[nm].append((origin, bool(s['flags'] & 0x1000)))
            elif sec == 0 and value == 0: undef[nm].add(origin)
            elif sec == 0 and value > 0: defs[nm].append((origin, 'common'))
        elif sc == 3 and sec == -1: pass


n = 0
for p in sorted((RN / 'pinned-build' / 'obj_v3').glob('*.obj')): scan(p, 'u' + p.stem); n += 1
for p in sorted((HERE / 'obj_contrib').glob('*.obj')): scan(p, 'c' + p.stem); n += 1
for p in sorted((RN / 'data-v3' / 'out').glob('*.obj')): scan(p, 'd' + p.stem); n += 1
libdefs = collections.defaultdict(list)
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib') / ln):
        r = U.parse_obj(blob)
        if not r: continue
        secs, syms = r
        for si, (nm, value, sec, ty, sc) in syms.items():
            if sc == 2 and sec > 0: libdefs[nm].append(ln + ':' + mname)
print('objects', n)
ours = set(defs)
und = {k: v for k, v in undef.items() if k not in ours}
cat = collections.Counter(); per = collections.defaultdict(list)
for nm, o in und.items():
    if nm in libdefs: c = 'defined in libcmt/libcpmt'
    elif nm.startswith('__imp_'): c = 'import (__imp_)'
    elif nm.startswith(('__ehhandler$', '__unwindfunclet$', '__ehfuncinfo$', '__catch$', '__tryblocktable$', '__unwindtable$', '__sehtable$')): c = 'EH label'
    elif ADDR.search(nm): c = 'address-named'
    elif nm.startswith('$SG') or nm.startswith('??_C@'): c = 'string literal'
    elif nm.startswith('__real@'): c = 'float constant'
    else: c = 'other'
    cat[c] += 1; per[c].append(nm)
dup = {k: v for k, v in defs.items() if len(v) > 1 and not all(x[1] is True for x in v) and not all(x[1] == 'common' for x in v)}
dupc = {k: v for k, v in defs.items() if len(v) > 1 and all(x[1] is True for x in v)}
print('defined names', len(defs), 'undefined (unresolved by our objects)', len(und), dict(cat))
print('non-COMDAT duplicate definitions', len(dup), 'COMDAT duplicates (ok)', len(dupc))
json.dump(dict(undefined={k: sorted(v)[:5] for k, v in und.items()}, categories=dict(cat), per={k: v[:2000] for k, v in per.items()}, dup_noncomdat={k: v[:6] for k, v in dup.items()},
               dup_comdat_n=len(dupc)), open(HERE / 'symscan.json', 'w'))
for c, v in per.items(): print(c, len(v), v[:6])
