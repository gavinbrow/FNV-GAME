"""Markdown tables of the baseline borrowed fields (breakdown_fields.json from breakdown.py, taken from the build-v7 run before any change of worker B)
and of what is left in the current build-v7/borrowed_v7.tsv.gz. Writes breakdown_baseline.md and prints the remaining list."""
import collections
import gzip
import json

R = 'C:/Projects/Decompilation/runtime-next/'
o = json.load(open(R + 'reloc-v7/breakdown_fields.json'))
out = []


def table(title, counter, n=25, total=None):
    out.append('\n### ' + title + '\n')
    out.append('| group | fields | bytes |')
    out.append('|---|---:|---:|')
    for k, v in counter.most_common(n):
        out.append('| %s | %d | %d |' % (str(k).replace('|', '/'), v, 4 * v))
    if total:
        out.append('| total | %d | %d |' % (total, 4 * total))


def grp(o_):
    if o_['origin'] == 'crt':
        return 'CRT/STL library code'
    if o_['origin'] == 'contrib':
        return 'accepted web contribution (function body)'
    if o_['origin'] == 'contrib-eh':
        return 'accepted web contribution (EH piece)'
    if o_['origin'] == 'fn' and o_['source'] == 'a':
        return 'recipe function: call resolves to a different function (source bug)'
    if o_['origin'] == 'fn':
        return 'recipe function: float/string pool copy or literal'
    if o_['source'] == 'icf-fold':
        return 'EH funclet: call to identical-body copy, ICF picked another copy'
    if o_['source'] == 'c':
        return 'EH funclet: name bound by symbol map to another copy'
    return 'EH funclet: callee name defined nowhere in our sources'


table('Baseline: by cause', collections.Counter(grp(x) for x in o), 20, len(o))
table('Baseline: by origin / status', collections.Counter((x['origin'], x['status'], x['source']) for x in o), 20)
own = collections.Counter()
for x in o:
    own[x['src'] if x['origin'] in ('fn', 'tail') else '(' + x['origin'] + ')'] += 1
table('Baseline: by owner (source file of the placing unit; CRT and contributions have no source file)', own, 40)
nm = collections.Counter(x['name'][:70] for x in o if x['origin'] in ('tail', 'contrib-eh'))
table('Baseline: EH-funclet callee names (top 25)', nm, 25)
cr = collections.Counter(x['name'][:50] for x in o if x['origin'] == 'crt')
table('Baseline: CRT symbols (top 25)', cr, 25)
open(R + 'reloc-v7/breakdown_baseline.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out)[:3000])
print('---- remaining')
for l in gzip.open(R + 'build-v7/borrowed_v7.tsv.gz', 'rt'):
    print(l.rstrip('\n')[:200])
