# independent-ish cross-check of call/address targets: does the target the build chose correspond to a function our own sources define
# under that very symbol, and is that function's body unique in the image?
import sys; sys.path.insert(0, "C:/Projects/Decompilation/runtime-next/reloc-v5")
from common import *
import gzip, hashlib
rows=[]
with gzip.open('relocs_v5.tsv.gz','rt') as f:
    next(f)
    for l in f: rows.append(l.rstrip('\n').split('\t'))
placed=json.load(gzip.open('placed_functions_v5.json.gz','rt'))
pl={a:(L,sym) for a,L,sym in placed}
defs=collections.defaultdict(set)      # symbol (incl fold aliases) -> addresses where recipe defines it
at=collections.defaultdict(set)
for u in UNITS:
    for f in u['functions']:
        a=int(f['address'],16)
        for n in [f['symbol']]+f.get('fold_aliases',[]): defs[n].add(a); at[a].add(n)
h=collections.defaultdict(list)
for a,(L,sym) in pl.items(): h[hashlib.md5(rd(a,L)).digest()].append(a)
dupbody={a for v in h.values() if len(v)>1 for a in v}
c=collections.Counter(); ex={}
for r in rows:
    if r[3]!='agree' or r[1] not in ('REL32','DIR32'): continue
    if r[2] not in ('a','c','f','a-fixup'): continue
    T=int(r[5],16); nm=r[6]
    if T not in pl: 
        k='target is not the start of a function placed from our source (data, thunk, CRT, undecompiled, middle of code)'
        k2='n/a'
    else:
        L,sym=pl[T]
        if nm in at[T]: k='CONFIRMED: target is the function our source defines under this very symbol'
        elif nm in defs: k='CONFLICT: symbol is defined by our source elsewhere (%s) but resolves here' % ('same bytes' if all(rd(a,pl[a][0] if a in pl else 1)==rd(T,pl[a][0] if a in pl else 1) for a in defs[nm] if a in pl) else 'different bytes')
        else:
            def sig(n): return n.split('@@',1)[1] if n.startswith('?') and '@@' in n else None
            sg=sig(nm); same=any(sg is not None and sig(x)==sg for x in at[T])
            k='ALIAS: target is a function from our source under a different symbol name; ' + ('signature part of the mangled names agrees' if same else ('signature differs or not C++-mangled'))
        k2='body-unique' if (T not in dupbody and L>=16) else ('body-duplicated-elsewhere' if T in dupbody else 'body<16B')
    c[(k,k2)]+=1; ex.setdefault((k,k2),[]).append((r[0],nm[:50],r[5]))
tot=sum(c.values())
print('call/address sites checked',tot)
for k,v in sorted(c.items(),key=lambda x:-x[1]): print(v,k,ex[k][:2])
json.dump({'%s | %s'%k:v for k,v in c.items()},open('xcheck_v5.json','w'),indent=1)
