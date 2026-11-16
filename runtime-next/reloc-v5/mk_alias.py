# proposal only (reference-assisted): for destructor/operator-delete symbols referenced only from EH funclets, the original target address
# and whether it is the start of a recipe function. NOT applied by assemble_v5.
import sys; sys.path.insert(0, "C:/Projects/Decompilation/runtime-next/reloc-v5")
from common import *
import gzip
rows=[]
with gzip.open('borrowed_v5.tsv.gz','rt') as f:
    next(f)
    for l in f: rows.append(l.rstrip('\n').split('\t'))
addr2n=collections.defaultdict(list)
for u in UNITS:
    for f in u['functions']: addr2n[int(f['address'],16)].append(f['symbol'])
by=collections.defaultdict(list)
for r in rows:
    if r[4]!='tail' or r[2]!='None' or r[1]!='20': continue
    va=int(r[0],16); obs=(va+4+struct.unpack('<i',rd(va))[0])&0xffffffff
    by[r[6]].append(obs)
out={}; st=collections.Counter()
for nm,v in by.items():
    c=collections.Counter(v); T,n=c.most_common(1)[0]
    kind='unique-target' if len(c)==1 else 'multiple-targets'
    isf=T in addr2n
    st[(kind,'target is recipe fn start' if isf else 'target not a recipe fn start')]+=1
    out[nm]=dict(sites=len(v),targets={hex(k):x for k,x in c.items()},recipe_names_at_top_target=addr2n.get(T,[])[:2])
json.dump(out,open('tail_alias_candidates.json','w'),indent=0)
print(len(rows),len(out),dict(st), sum(len(v) for v in by.values()))
