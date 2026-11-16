"""Where are the overlay's CRT global names defined? libcmt.lib / libcpmt.lib members (our CRT objects): kind of the defining section and whether the section carries bytes
that could place it. Writes reloc-v7/libdef_report.json. usage: python -I libdef.py"""
import collections
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
import uncovered_v2 as U
from pathlib import Path

LIB = Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\lib')
R = r'C:\Projects\Decompilation\runtime-next\reloc-v7'
ov = json.load(open(R + r'\binding_overlay.json'))
names = set(ov['global_name'])
defs = collections.defaultdict(list)       # name -> [(lib, member, kind, secname, size, nbytes)]
for ln in ('libcmt.lib', 'libcpmt.lib'):
    for mname, blob in U.read_ar(LIB / ln):
        r = U.parse_obj(blob)
        if not r: continue
        secs, syms = r
        for si, (nm, value, sec, ty, sc) in syms.items():
            if nm not in names: continue
            if sec > 0 and sc in (2, 3):
                s = secs[sec - 1]; fl = s['flags']
                kind = 'code' if fl & 0x20 else ('bss' if fl & 0x80 else ('data(bytes)' if s['data'] else 'empty'))
                if kind == 'data(bytes)' and fl & 0x80000000 == 0 and not fl & 0x80 and (fl & 0x40) and not (fl & 0x80000000): kind = 'data(bytes)'
                defs[nm].append((ln, mname, kind, s['name'], len(s['data'])))
            elif sec == 0 and value > 0 and sc == 2:
                defs[nm].append((ln, mname, 'common', '', value))
cnt = collections.Counter(); per = {}
for n in sorted(names):
    d = defs.get(n)
    if not d: cnt['not defined in libcmt/libcpmt (our source / import / thunk / label)'] += 1; per[n] = 'none'; continue
    kinds = {x[2] for x in d}; members = {(x[0], x[1]) for x in d}
    k = '+'.join(sorted(kinds)) + (' (%d members)' % len(members) if len(members) > 1 else '')
    cnt[k] += 1; per[n] = k
members_needed = {(x[0], x[1]) for n in names for x in defs.get(n, [])}
rep = dict(overlay_global_names=len(names), by_definition=dict(cnt), distinct_defining_members=len(members_needed), per_name=per)
json.dump(rep, open(R + r'\libdef_report.json', 'w'), indent=0)
print(json.dumps({k: v for k, v in rep.items() if k != 'per_name'}, indent=1))
