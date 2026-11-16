"""link-v2 dedupe.py: one defining object per data global. A non-COMDAT data section whose defined external symbols are all also defined by a lower-numbered object is dropped
there (its symbols become undefined and bind to the owner's definition). usage: python -I dedupe.py [dir...]"""
import sys, collections, struct
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import coffrw
dirs = [HERE / d for d in (sys.argv[1:] or ['obj_rw', 'obj_contrib_rw'])]
files = sorted([p for d in dirs for p in d.glob('*.obj')], key=lambda p: (p.stem.isdigit() and len(p.stem) < 8 and 0 or 1, p.stem))
defs = collections.defaultdict(list)
info = {}
for p in files:
    b = p.read_bytes(); secs = coffrw.sections(b); ci = coffrw.comdat_info(b)
    d = {}
    for i, nm, v, sec, ty, sc, naux, o in coffrw.symbols(b):
        if sc == 2 and sec > 0 and not (secs[sec - 1]['flags'] & 0x20) and sec not in ci:
            d.setdefault(sec, []).append(nm); defs[nm].append(p)
    info[p] = d
dups = {n for n, l in defs.items() if len(l) > 1}
stat = collections.Counter()
for p in files:
    d = info[p]; drop = set()
    for sec, names in d.items():
        if all(n in dups and defs[n][0] != p for n in names): drop.add(sec)
        elif any(n in dups and defs[n][0] != p for n in names): stat['mixed section kept (duplicate remains)'] += 1
    if drop:
        b = p.read_bytes(); p.write_bytes(coffrw.rebuild(b, drop, {})); stat['sections dropped'] += len(drop)
    # mixed sections: the duplicated global becomes an undefined reference to the owner's definition (its bytes stay as dead padding)
    b = p.read_bytes(); buf = bytearray(b); ch = 0
    for i, nm, v, sec, ty, sc, naux, o in coffrw.symbols(b):
        if sc == 2 and sec > 0 and nm in dups and defs[nm][0] != p:
            import struct as _s; _s.pack_into('<I', buf, o + 8, 0); _s.pack_into('<h', buf, o + 12, 0); ch += 1
    if ch: p.write_bytes(bytes(buf)); stat['mixed-section duplicates made undefined'] += ch
print(len(dups), 'duplicated data globals;', dict(stat))
