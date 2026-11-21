"""Classify BFC baseline fields using unique source bindings for true COFF externals only."""
import collections,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';S=M/'out/phase2-baseformcomponent-core';O=S/'external-binding-evidence.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
import paths
D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 uf=F/'build/units.json';af=S/'root-baseline-audit.json';manifest=S/'manifest.json';audit=json.loads(af.read_text())
 if sha(uf)!=D or audit['recipe_sha256']!=D or audit['manifest_sha256']!=sha(manifest):raise ValueError('baseline recipe/manifest mismatch')
 units=json.loads(uf.read_text())['units'];sources=collections.defaultdict(lambda:collections.defaultdict(list))
 for i,u in enumerate(units):
  for name,value in u.get('symbols',{}).items():
   if not name.startswith('$'):sources[name][int(value,0)].append(i)
  for f in u['functions']:
   for name in [f['symbol']]+f.get('fold_aliases',[]):
    if not name.startswith('$'):sources[name][int(f['address'],0)].append(i)
 pe=Pe(paths.REF_IMAGE);records=[];counts=collections.Counter()
 for row in audit['units']:
  if row['unit_only_matches']==row['functions']:continue
  i=row['unit'];obj=RN/('pinned-build/obj_v3/%04d.obj'%i)
  if sha(obj)!=audit['object_sha256'][str(i)]:raise ValueError('production object changed '+str(i))
  c=Coff(str(obj));results=compare(c,pe,units[i])
  for f in results:
   for rel in f['relocations']:
    if rel.get('match'):continue
    name=rel['symbol'];symbols=c.by_name.get(name,[]);field=int(f['address'],16)+rel['offset'];typ=rel['kind'];status='unproved';candidate=None;source_units=[]
    if name.startswith('$'):status='local-label-deferred'
    elif len([x for x in symbols if x['section']==0 and x['storage']==2])!=1 or any(x['section']>0 for x in symbols):status='not-unique-undefined-external'
    elif len(sources.get(name,{}))!=1:status='source-binding-not-unique'
    else:
     candidate,source_units=next(iter(sources[name].items()));spec=next(x for x in units[i]['functions'] if x['address']==f['address']);ss=c.named(spec['symbol']);sec=c.sections[ss['section']];add=struct.unpack_from('<i',sec['data'],ss['value']+rel['offset'])[0];raw=pe.read(field,4);value=struct.unpack('<I',raw)[0]
     observed=(field+4+struct.unpack('<i',raw)[0])&0xffffffff if typ==0x14 else value if typ==6 else None
     resolved=(candidate+add)&0xffffffff
     status='source-unique-reference-agree' if observed==resolved else 'source-reference-disagree'
    counts[status]+=1;records.append({'unit':i,'function':f['address'],'field_va':'0x%08x'%field,'symbol':name,'status':status,'source_target':'0x%08x'%candidate if candidate is not None else None,'source_units':sorted(set(source_units))})
 data={'scope':'diagnostic only; unique global source bindings considered solely for actually undefined strong externals; local labels explicitly excluded','units_sha256':sha(uf),'baseline_audit_sha256':sha(af),'counts':dict(counts),'fields':records,'limitations':['does not alter unit-only baseline or production recipe','weak external behavior and local string-label provenance require independent proof','field reference agreement alone does not establish class identity or ownership']}
 O.write_text(json.dumps(data,indent=2));print(json.dumps({'fields':len(records),'counts':counts}))
if __name__=='__main__':main()
