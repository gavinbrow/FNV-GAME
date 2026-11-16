"""Cross-check iat_spec.json against (a) __imp_ references in our objects (pinned-build/obj_v3) and (b) SDK import libs."""
import json, re
from libimps import scan
import scan_imps, glob
spec = json.load(open('iat_spec.json'))
byname = {}; slots = {}
for d in spec['dlls']:
    for k, e in enumerate(d['ents']):
        va = d['iat'] + 4 * k + 0x400000   # slot VA in order of the (alphabetical-by-IAT) layout
        if 'name' in e: byname[e['name']] = (d['dll'], va)
objs = set()
for f in glob.glob('../pinned-build/obj_v3/*.obj'): objs |= scan_imps.imps(f)
found = set(); islots = set()
for s in objs:
    m = re.match(r'__imp_\?IMP_([0-9a-f]+)@', s)
    if m: islots.add(int(m.group(1), 16)); continue
    m = re.match(r'__imp_\?(\w+?)@', s) or re.match(r'__imp__?(\w+?)(@\d+)?$', s)
    if m and m.group(1) in byname: found.add(byname[m.group(1)][1])
total = sum(len(d['ents']) for d in spec['dlls'])
print('slots in spec', total, '; referenced by name from our objs', len(found), '; by IMP_ address', len(islots))
lib = scan(); idx = {}
for (dll, sym) in lib:
    idx.setdefault(dll, set()).update({sym, re.sub(r'@\d+$', '', sym[1:] if sym.startswith('_') else sym)})
ok = [n for n, (dll, _) in byname.items() if n in idx.get(dll.lower(), ())]
print('named imports', len(byname), '; found under same DLL in SDK libs', len(ok))
