# derives callee_fixups.json from a v5 run (relocs_v5.tsv.gz): the 48 call/address sites whose resolved target (unit-local/recipe name) is not what the original used
import sys; sys.path.insert(0, "C:/Projects/Decompilation/runtime-next/reloc-v5")
from common import *
import gzip
rows=[]
with gzip.open('relocs_v5.tsv.gz','rt') as f:
    next(f)
    for l in f: rows.append(l.rstrip('\n').split('\t'))
addr2n=collections.defaultdict(list); size={}
for u in UNITS:
    for f in u['functions']:
        a=int(f['address'],16); addr2n[a].append(f['symbol']); size[a]=f['size']
fix={}; detail=[]
for r in rows:
    if r[2]!='a' or r[3]!='disagree': continue
    va=int(r[0],16); exp=int(r[5],16)
    obs=(va+4+struct.unpack('<i',rd(va))[0])&0xffffffff if r[1]=='REL32' else struct.unpack('<I',rd(va))[0]
    if obs not in addr2n: continue          # only when the original target is a function we also have by name
    L=min(size[exp],size[obs]); 
    n_exp=r[6]; n_obs=addr2n[obs][0]
    if n_exp.replace('QAE','QBE')==n_obs or n_exp.replace('QBE','QAE')==n_obs: cause='const-qualifier variant (QAE vs QBE) of the same method'
    elif 'FUN_' in n_obs or 'shell' in n_obs or 'Class' in n_obs or 'cls' in n_obs: cause='source names a real symbol; the original called an address-named function'
    else: cause='source names a different real function than the original called'
    fix[str(va)]=obs
    detail.append(dict(field='0x%08x'%va,kind=r[1],source_callee=n_exp,source_target='0x%08x'%exp,source_target_size=size.get(exp),original_target='0x%08x'%obs,original_callee=n_obs,original_target_size=size[obs],
        identical_bytes=(rd(exp,size[exp])==rd(obs,size[obs]) if size.get(exp)==size[obs] else False),cause=cause))
json.dump(dict(note='reference-assisted: the original target address is read from the reference and accepted only if it is the start of a recipe function; applied only with FNV_V5_FIXUPS=1',fixups=fix,detail=detail),open('callee_fixups.json','w'),indent=1)
print(len(fix),collections.Counter(d['cause'] for d in detail),sum(d['identical_bytes'] for d in detail))
