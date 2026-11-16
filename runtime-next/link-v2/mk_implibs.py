import json,re,sys,collections
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; RN=HERE.parent
sys.path.insert(0,str(HERE)); sys.path.insert(0,str(RN/'pinned-build'))
import coffrw
spec=json.load(open(RN/'direct-v1'/'iat_spec.json'))
byname=collections.defaultdict(set); slot={}
for d in spec['dlls']:
    for k,e in enumerate(d['ents']):
        if e.get('name'): byname[e['name']].add(d['dll']); slot[0x400000+d['iat']+4*k]=(d['dll'],e['name'])
imps=collections.defaultdict(set)
for dd in ('obj_rw','obj_contrib_rw'):
    for p in (HERE/dd).glob('*.obj'):
        for i,nm,v,sec,ty,sc,naux,o in coffrw.symbols(p.read_bytes()):
            if nm.startswith('__imp_') and sec==0: imps[nm].add(p.name)
sa=json.load(open(HERE/'symaddr.json')); gmap=collections.defaultdict(set)
for _u,_d in sa.items():
    for _n,_a in _d.items():
        if _n.startswith('__imp_'): gmap[_n].update(_a)
dlls=collections.defaultdict(dict); miss=[]
for nm in imps:
    dec=nm[6:]
    m=re.search(r'(?:IMP|FUN|DAT)_([0-9a-f]{6,8})(?:_import)?@',dec)
    if m:
        va=int(m.group(1),16)
        if va in slot: dlls[slot[va][0]][dec]=slot[va][1]; continue
    ga=gmap.get(nm)
    if ga and len(ga)==1 and next(iter(ga)) in slot:
        d_,n_=slot[next(iter(ga))]; dlls[d_][dec]=n_; continue
    if dec.startswith('_'): und=re.sub(r'@\d+$','',dec[1:])
    elif dec.startswith('?') and re.match(r'\?(\w+)@',dec): und=re.match(r'\?(\w+)@',dec).group(1)
    else: und=dec
    for c in (und, und.replace('fnv_Import_','').replace('fnv_',''), dec, dec[1:]):
        if c in byname: dlls[sorted(byname[c])[0]][dec]=c; break
    else: miss.append(nm)
print({k:len(v) for k,v in dlls.items()}); print('unmatched',len(miss),miss[:30])
out=HERE/'implibs'; out.mkdir(exist_ok=True)
for dll,m in dlls.items():
    base=dll.rsplit('.',1)[0]
    lines=['LIBRARY '+dll,'EXPORTS']+['%s=%s'%(dec,c) if dec!=c else ('%s=%s'%(c[1:],c) if c.startswith('_') else c) for dec,c in sorted(m.items())]
    (out/(base+'.def')).write_text('\n'.join(lines)+'\n')
json.dump(dict(dlls={k:len(v) for k,v in dlls.items()},missing=miss),open(HERE/'implibs.json','w'))
