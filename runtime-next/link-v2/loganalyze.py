import re,collections,sys,json
log=open(sys.argv[1] if len(sys.argv)>1 else 'link1.log',encoding='latin1').read().splitlines()
un=collections.defaultdict(set); dup=collections.defaultdict(set)
for l in log:
    m=re.search(r'LNK(2001|2019): unresolved external symbol (.*?)(?: referenced in function| in function|$)',l)
    if m:
        t=m.group(2); mm=re.search(r'\((\S+)\)\s*$',t.strip()); name=mm.group(1) if mm else t.strip().split()[0]
        un[name].add(l.split(':')[0]); continue
    m=re.search(r'LNK2005: (.*) already defined in (\S+)',l)
    if m:
        t=m.group(1); mm=re.search(r'\((\S+)\)\s*$',t.strip()); name=mm.group(1) if mm else t.split()[0]
        dup[name].add(l.split(':')[0])
cat=collections.Counter(); ex={}
for n in un:
    if n.startswith('C_'): k='C_<va> (code address, no definition)'
    elif n.startswith('D_'): k='D_<va> (data label missing)'
    elif n.startswith('__imp_'): k='import'
    elif re.search(r'(FUN|DAT|PTR|SUB)_[0-9a-f]{8}',n): k='address-named, not rewritten'
    else: k='other name'
    cat[k]+=1; ex.setdefault(k,[]).append(n)
print('unresolved distinct',len(un),dict(cat)); 
for k,v in ex.items(): print(k,v[:5])
print('duplicate names',len(dup)); print(list(dup)[:5])
json.dump(dict(unresolved={k:sorted(v)[:3] for k,v in un.items()},dups={k:sorted(v)[:3] for k,v in dup.items()}),open('link_errors.json','w'))
