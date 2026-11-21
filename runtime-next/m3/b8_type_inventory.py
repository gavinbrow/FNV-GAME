import os,sys,json,re,collections,bisect
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.argv=[sys.argv[0]]
s=open('b7_select.py').read().split('entries = [];')[0]
exec(compile(s,'b7_select.py','exec'),globals())
rows=[]; counts=collections.Counter()
for n in ('.data','.rdata'):
    sec=SEC[n]; lo=sec['va']; arr=bytes(tag[n])
    for m in re.finditer(b'\x00+',arr):
        ra,rb=lo+m.start(),lo+m.end()
        cuts=[ra]+bnds[bisect.bisect_right(bnds,ra):bisect.bisect_left(bnds,rb)]+[rb]
        for x,y in zip(cuts,cuts[1:]):
            if x not in bnd: continue
            dc,why=decl_class(x)
            if why not in ('multi-type','global-non-scalar'): continue
            g=inv.get(x,{})
            raw=refbytes(x,y-x)
            fs={ns:sorted(ts) for ns,ts in forms[x].items()}
            sizes=[]
            for ns,ts in fs.items():
                for t in ts:
                    code=t
                    if code in TYPES: sizes.append(dict(namespace=ns,code=code,kind='scalar',size=TYPES[code][1],type=TYPES[code][0]))
                    elif code.startswith(('P','Q')) and g.get('decls') and all('*' in d and not re.search(r'\bDAT_[0-9a-f]{8}\s*\[', d) for d in g['decls']): sizes.append(dict(namespace=ns,code=code,kind='pointer_or_decay',size=4,type=None))
                    else: sizes.append(dict(namespace=ns,code=code,kind='unknown',size=None,type=None))
            vals=sorted(set(v['size'] for v in sizes if v['size'] is not None))
            all_known=bool(sizes) and all(v['size'] is not None for v in sizes)
            extent=vals[0] if all_known and len(vals)==1 and vals[0]<=y-x else None
            rows.append(dict(va=x,section=n,bucket=why,interval_size=y-x,interval_nonzero=sum(bool(q) for q in raw),declarations=g.get('decls',[]),mangled_declarations=sorted(full[x]),type_observations=sizes,agreed_declared_size=extent,extent_status='size agreement only; declaration conflict unresolved' if extent and why=='multi-type' else ('single encoded scalar/pointer size; semantic type and placement unverified' if extent else 'unresolved'),tail_start=x+extent if extent is not None else None,tail_size=y-x-extent if extent is not None else None,notes='Interval boundary is not object extent; candidates require source compatibility, relocation and field-boundary checks.'))
            counts[why]+=sum(bool(q) for q in raw)
assert counts['multi-type']==38230 and counts['global-non-scalar']==18330,counts
out={'schema_version':1,'description':'Batch 7 skipped interval reproduction; no selection or source modification. Sizes are x86 declaration encoding observations, not proven definitions.','inputs':['b7_select.py frozen inputs','fnv_decomp/build/units.json','inventory/dat_globals.json','reference image read-only'],'counts_nonzero':dict(counts),'rows':rows}
with open('inventory/b8_type_candidates.json','w') as f: json.dump(out,f,indent=2)
print('rows',len(rows),'nonzero',dict(counts))
for bucket in ('multi-type','global-non-scalar'):
 a=[r for r in rows if r['bucket']==bucket]; fixed=[r for r in a if r['agreed_declared_size'] is not None]
 print(bucket,'intervals',len(a),'size-agree',len(fixed),'extent bytes',sum(r['agreed_declared_size'] for r in fixed),'tails',sum(r['tail_size'] for r in fixed),'unknown',len(a)-len(fixed))



