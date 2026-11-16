"""List unit indices affected by the source edits of this worker (files with a .bak-20261116-wB backup): units whose source is an edited .cpp, plus units whose
source text includes an edited header by name (one level; the headers here are included directly by the .cpp). Writes the list to argv[1]."""
import glob
import json
import sys

S = 'C:/Projects/Decompilation/fnv_decomp/src/'
u = json.load(open('C:/Projects/Decompilation/fnv_decomp/build/units.json'))['units']
edited = set()
for b in glob.glob(S + '**/*.bak-20261116-wB', recursive=True):
    edited.add(b.replace('\\', '/')[len(S):-len('.bak-20261116-wB')])
cpp = {e for e in edited if e.endswith('.cpp')}
hdr = {e for e in edited if e.endswith('.h')}
ids = set(i for i, x in enumerate(u) if x['source'][4:] in cpp)
for i, x in enumerate(u):
    try:
        t = open(S + x['source'][4:], 'rb').read().decode('latin1')
    except OSError:
        continue
    for h in hdr:
        if '"' + h.rsplit('/', 1)[-1] + '"' in t:
            ids.add(i)
print(len(cpp), 'cpp edited;', sorted(hdr), '->', len(ids), 'units')
json.dump(sorted(ids), open(sys.argv[1], 'w'))
