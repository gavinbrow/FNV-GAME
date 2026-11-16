import json,re,collections,bisect
u=json.load(open(r'C:\Projects\Decompilation\fnv_decomp\build\units.json'))['units']
ranges=sorted((int(f['address'],16),int(f['address'],16)+f['size'],i) for i,x in enumerate(u) for f in x['functions'])
ks=[r[0] for r in ranges]
d=json.load(open('../build-v7/rebase_remaining_v7.json'))['we-shift-a-field-the-original-does-not-relocate']
need=collections.defaultdict(set)
for e in d:
    f=int(e['field'],16);r=ranges[bisect.bisect_right(ks,f)-1]
    sym=e['symbol']
    m=re.match(r'\??_?(DAT_[0-9a-f]+|FUN_00a00000|g_[0-9a-f]+_arg1)',sym)
    need[u[r[2]]['source']].add(m.group(1) if m else sym)
S='C:/Projects/Decompilation/fnv_decomp/'
for src,syms in sorted(need.items()):
    t=open(S+src,encoding='latin1').read().split('\n')
    for s in syms:
        for i,l in enumerate(t):
            if re.search(r'\b'+re.escape(s)+r'\b',l): print(src.split('/')[-1],i+1,l.strip()[:140])
