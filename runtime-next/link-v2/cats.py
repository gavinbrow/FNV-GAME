import re,collections,sys
log=open(sys.argv[1] if len(sys.argv)>1 else 'link1.log',encoding='latin1').read().splitlines()
rows=[]
for l in log:
    m=re.search(r'^(\S+) : error LNK(2001|2019): unresolved external symbol (.*?)(?: referenced in function (.*))?$',l)
    if not m: continue
    t=m.group(3); mm=re.search(r'\(([^()\s]+)\)\s*$',t); name=mm.group(1) if mm else t.split()[0]
    rows.append((m.group(1),m.group(2),name,m.group(4) or ''))
def src(o): return 'data-v3' if o.startswith(('rdata','data_','tls','const')) else 'unit/contrib'
def cat(n):
    if n.startswith('C_'): return 'C_<va>'
    if n.startswith('D_'): return 'D_<va>'
    if n.startswith('__imp_'): return 'import'
    if n.startswith('??_G') or n.startswith('??_E'): return 'deleting dtor ??_G/??_E'
    if n.startswith('??1'): return 'dtor'
    if n.startswith('??0'): return 'ctor'
    if re.search(r'(FUN|DAT|PTR|SUB)_[0-9a-f]{8}',n): return 'address-named'
    return 'other'
d=collections.defaultdict(set); u=collections.Counter()
for o,k,n,f in rows: d[(src(o),k,cat(n))].add(n); u[(src(o),k,cat(n))]+=1
for k,v in sorted(d.items(),key=lambda x:-len(x[1])): print(len(v),u[k],k)
