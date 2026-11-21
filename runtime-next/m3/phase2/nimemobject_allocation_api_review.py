"""Review private NiMemObject allocation API emitted effects."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-nimemobject-allocation-api';OUT=D/'independent-review.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 m=json.loads((D/'manifest.json').read_text());rp=F/'build/units.json'
 if sha(rp)!=m['recipe_sha256']:raise ValueError('recipe changed')
 u=json.loads(rp.read_text())['units'];pe=Pe(paths.REF_IMAGE);details={};allobjs={}
 if u[612]['symbols'].get('??2NiMemObject@@SAPAXI@Z')!='0x00aa13e0' or u[612]['symbols'].get('??3NiMemObject@@SAXPAXI@Z')!='0x00aa1460':raise ValueError('source binding differs')
 for i in (1484,1503):
  d=D/str(i);run=json.loads((d/'compile-result.json').read_text());mm=d/'mirror-manifest.json'
  if run['unit_index']!=i or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('compile mismatch')
  objs={};details[str(i)]={}
  for tag in ('original','candidate'):
   row=next(x for x in run['outcomes'] if x['tag']==tag);p=d/(tag+'.obj')
   if row['rc'] or not row['trace_valid'] or sha(p)!=row['object_sha256']:raise ValueError('object differs')
   c=Coff(str(p));r=compare(c,pe,u[i]);sec,inf,err=eh_sections(c,pe,u[i],r,recipe_names(u))
   if any(x['verdict']!='match' for x in r) or err or any(not x[2] for x in sec):raise ValueError('function/EH mismatch')
   objs[tag]=c;details[str(i)][tag]={'object_sha256':sha(p),'strict_functions':len(r),'ordinary_eh_sections':len(sec)}
  for f in u[i]['functions']:
   a,ar=relocated(objs['original'],f['symbol'],f['size'],{});b,br=relocated(objs['candidate'],f['symbol'],f['size'],{})
   if a!=b or ar!=br:raise ValueError('mapped function changed '+f['address'])
  allobjs[i]=objs
 bodies={}
 for tag,c in allobjs[1503].items():
  x=c.named('??_GNiRefObject@@UAEPAXI@Z');s=c.sections[x['section']];data=s['data'][x['value']:];rr=[(o,k,c.symbols[j]['name']) for o,j,k in s['relocs']];ops=[(z.mnemonic,z.op_str) for z in Cs(CS_ARCH_X86,CS_MODE_32).disasm(data,0)]
  if (tag=='original' and (len(data)!=42 or not any(z[2]=='??3@YAXPAX@Z' for z in rr))) or (tag=='candidate' and (len(data)!=44 or not any(z[2]=='??3NiMemObject@@SAXPAXI@Z' for z in rr) or ('push','8') not in ops)):raise ValueError('fallback behavior differs')
  bodies[tag]={'size':len(data),'relocations':rr,'has_push_size8':('push','8') in ops}
 OUT.write_text(json.dumps({'scope':'private allocation API two-unit emission experiment','recipe_sha256':sha(rp),'manifest_sha256':sha(D/'manifest.json'),'results':details,'fallback':bodies,'reference_slot0':'0x004968e0','reference_slot0_size':46,'reference_sized_deallocation_target':'0x00aa1460','source_binding_unit':612,'limitations':['126 lexical consumers remain unverified; changed emitted allocation semantics can affect functions and EH elsewhere','native fallback is 44-byte O2, not the 46-byte Od reference wrapper','no weak fallback binding, COMDAT, final placement or runtime claim']},indent=2));print('PASS 13 mapped functions; fallback now calls sized class delete with size 8; 126-unit scope remains')
if __name__=='__main__':main()
