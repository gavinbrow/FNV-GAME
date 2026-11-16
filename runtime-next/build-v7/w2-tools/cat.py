import glob,re,collections,pickle,sys
rows=pickle.load(open(sys.argv[1]+'_rows.pkl','rb'))
byu=collections.defaultdict(int)
for r in rows:
    if r['sig'].startswith('mov eax, dword ptr [ebp - N]  <>  push N'): byu[(r['i'],int(r['parent'],16) if isinstance(r['parent'],str) else r['parent'])]+=r['m']
cat=collections.Counter(); ex={}
seen=set()
for f in glob.glob('auto/*.log'):
    i=int(f[5:9])
    for l in open(f):
        m=re.match(r"\s+\('(0x[0-9a-f]+)', '([^']+)'(.*)",l)
        if not m: continue
        p=int(m.group(1),16); b=byu.get((i,p))
        if not b or (i,p) in seen: continue
        seen.add((i,p))
        k=m.group(2)
        if k=='no candidate class':
            need=eval(re.search(r'\[(\d+(?:, \d+)*)\]',m.group(3)).group(0)); det=eval(re.search(r'(\[\(.*\])\)',m.group(3)).group(1)) if '[(' in m.group(3) else []
            if not det: k+=':no news'
            elif all(not d[2] for d in det): k+=':class not in file'
            elif all(d[3] for d in det): k+=':edited'
            elif all(d[1] and not (set(d[1])&set(need)) for d in det if d[2]): k+=':size mismatch'
            else: k+=':has decl/other'
        cat[k]+=b; ex.setdefault(k,[]).append((i,hex(p),b,m.group(3)[:170]))
print(cat, sum(cat.values()), sum(byu.values()))
for k in ex: print(k); [print('  ',x) for x in ex[k][:int(sys.argv[2]) if len(sys.argv)>2 else 4]]
