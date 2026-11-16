"""Select the next rename batch from batch_cands.json (pilot_pick2.py): drop classes already renamed, duplicate targets, targets that already occur as a class name in any
recipe symbol (units.json), and sources shared by more than 3 units. usage: python -I batch_select.py out.json [max]"""
import collections
import glob
import json
import re
import sys

R = 'C:/Projects/Decompilation/runtime-next/data-v2/'
txt = open('C:/Projects/Decompilation/fnv_decomp/build/units.json', encoding='latin1').read()
doc = json.loads(txt)
units = doc['units']
classes = set(re.findall(r'(?<=[?@])([A-Za-z_][A-Za-z0-9_]*)@', txt))
g = json.load(open(R + 'batch_cands.json'))
done = set()
for f in glob.glob(R + 'renamed_*.json'):
    for d in json.load(open(f)):
        done.add(d[0]); done.add(d[1])
src2u = collections.defaultdict(list)
for i, x in enumerate(units):
    src2u[x['source']].append(i)
n = collections.Counter(x['new'] for x in g)
o = collections.Counter(x['old'] for x in g)
sel = []
for x in g:
    if x['old'] in done or x['new'] in done or n[x['new']] != 1 or o[x['old']] != 1 or x['new'] in classes:
        continue
    x['units'] = src2u.get('src/' + x['file'], [])
    if x['units'] and len(x['units']) <= 3:
        sel.append(x)
json.dump(sel[:int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6], open(sys.argv[1], 'w'))
print(len(g), 'candidates ->', len(sel), 'selected')
