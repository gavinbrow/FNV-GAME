"""Prove unresolved externals through same-unit archived immediates, never symbol spelling."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';S=M/'out/phase2-baseformcomponent-core';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 dest=S/'archived-immediate-evidence.json'
 if dest.exists():raise FileExistsError('preserve evidence')
 up=F/'build/units.json'; audit=S/'root-baseline-audit.json'; ev=S/'external-binding-evidence.json';units=json.loads(up.read_text())['units'];a=json.loads(audit.read_text());rows=[x for x in json.loads(ev.read_text())['fields'] if x['status']=='source-binding-not-unique'];pe=Pe(paths.REF_IMAGE);facts=[];groups={}
 if sha(up)!='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160' or len(rows)!=6:raise ValueError('unexpected scope')
 for row in rows:groups.setdefault((row['unit'],row['function']),[]).append(row)
 for (i,address),group in groups.items():
  u=units[i];f=next(x for x in u['functions'] if x['address']==address);old=RN/('pinned-build/obj_v3.bak-20261116/%04d.obj'%i);cur=RN/('pinned-build/obj_v3/%04d.obj'%i);src=F/u['source']
  if sha(cur)!=a['object_sha256'][str(i)]:raise ValueError('current object differs')
  oc=Coff(str(old));cc=Coff(str(cur));chk=compare(oc,pe,dict(u,functions=[f]));ob,orr=relocated(oc,f['symbol'],f['size'],{});cb,crr=relocated(cc,f['symbol'],f['size'],{})
  if len(chk)!=1 or chk[0]['verdict']!='match':raise ValueError('archive does not match reference')
  offsets={int(x['field_va'],16)-int(address,16) for x in group};masked=set(j for off in offsets for j in range(off,off+4))
  if any(x!=y and j not in masked for j,(x,y) in enumerate(zip(ob,cb))) or len(ob)!=len(cb):raise ValueError('whole-function bytes differ outside fields')
  if orr!=[r for r in crr if r[0] not in offsets]:raise ValueError('remaining relocation graph differs')
  for x in group:
   off=int(x['field_va'],16)-int(address,16);rel=[r for r in crr if r[0]==off]
   if any(r[0]==off for r in orr) or len(rel)!=1 or rel[0][1:]!=(6,x['symbol'],0):raise ValueError('unexpected relocation')
   val=ob[off:off+4]
   if val!=pe.read(int(x['field_va'],16),4):raise ValueError('reference disagrees')
   facts.append({'unit':i,'function':address,'field_offset':off,'symbol':x['symbol'],'archived_source_immediate_va':'0x%08x'%int.from_bytes(val,'little'),'old_object_sha256':sha(old),'current_object_sha256':sha(cur),'source_path':u['source'],'source_sha256':sha(src),'reference_field_agrees':True,'whole_function_other_bytes_and_relocations_agree':True})
 dest.write_text(json.dumps({'recipe_sha256':sha(up),'audit_sha256':sha(audit),'reference_sha256':sha(Path(paths.REF_IMAGE)),'scope':'same-unit archived strict-reference COFF; unrelocated source immediate paired with current DIR32 relocation, all other whole-function bytes and relocations match','fields':facts,'limitations':['candidate bindings not installed','full unit strict checks and ownership remain separate']},indent=2));print('proved',len(facts))
if __name__=='__main__':main()
