"""Prove unit 2634's independently owned contribution to TESFile EH extent."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';D=O/'phase2-tesfile-recordtype-global';A=O/'phase2-nimem-kind-production-archive';MAP=O/'phase2-nimem-kind-source-bindings-final.json';OUT=D/'eh-outside-owner-proof.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve proof')
 m=json.loads((D/'manifest.json').read_text());proof=json.loads((D/'comparison.json').read_text());inv=json.loads((A/'manifest.json').read_text());op=D/'units.original';np=D/'units.generated'
 if sha(op)!=m['base_recipe_sha256'] or sha(np)!=m['candidate_recipe_sha256'] or proof['candidate_strict_functions']!=87 or inv['recipe_sha256']!=sha(op):raise ValueError('recipe or proof differs')
 old=json.loads(op.read_text())['units'];spec=copy.deepcopy(json.loads(np.read_text())['units'][995]);z=json.loads(MAP.read_text())['units'].get('995',{});spec['symbols'].update({k:v['target'] for k,v in z.items()})
 for n in ('$SG7025','$SG8028','$SG8627','$SG8632'):spec['symbols'].pop(n,None)
 spec['symbols'].update(proof['candidate_derived_bindings']);spec['symbols']['?DAT_011873c8@@3IA']='0x011873c8';pe=Pe(paths.REF_IMAGE);names=recipe_names(old);done=[];results=[]
 for i,path,unit,expected in [(995,D/'candidate.obj',spec,87),(2634,A/'2634.obj',old[2634],139)]:
  if i==995:
   compile=json.loads((D/'compile-result.json').read_text());record=next(x for x in compile['outcomes'] if x['tag']=='candidate')
   if record['rc'] or not record['trace_valid'] or sha(path)!=record['object_sha256']:raise ValueError('candidate object differs')
  else:
   record=next(x for x in inv['objects'] if x['unit']==i)
   if sha(path)!=record['sha256']:raise ValueError('outside owner archive differs')
  c=Coff(str(path));r=compare(c,pe,unit);sections,inf,err=eh_sections(c,pe,unit,r,names)
  if len(r)!=expected or any(x['verdict']!='match' for x in r) or err or any(not x[2] for x in sections):raise ValueError('outside/target strict mismatch')
  done.append({'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}});results.append({'unit':i,'object_sha256':sha(path),'strict_functions':len(r),'eh_sections':len(sections),'inferred_names':len(inf)})
  if i==2634:
   pieces=[x for x in sections if x[0]<0xeeeba3 and 0xeeeb80<x[1]]
   if [(x[0],x[1],x[2],x[3]) for x in pieces]!=[(0xeeeb80,0xeeeb88,True,'0x004745d0'),(0xeeeb88,0xeeeba3,True,'0x004745d0')]:raise ValueError('outside section ownership differs')
 info=struct.unpack('<9I',pe.read(0x11422a8,36));action=struct.unpack('<II',pe.read(info[2],8))
 if pe.read(0x4745d6,4)!=struct.pack('<I',0xeeeb88) or info[0]!=0x19930522 or info[1]!=1 or info[2]!=0x11422a0 or action[1]!=0xeeeb80:raise ValueError('reference handler/xdata differs')
 tails,bad,inferred,_,conf=eh_tails([spec],done,pe)
 if len(tails)!=4 or bad or conf:raise ValueError('listed tails failed')
 OUT.write_text(json.dumps({'scope':'source-corrected TESFile candidate plus independently source-owned neighboring EH contribution','candidate_comparison_sha256':sha(D/'comparison.json'),'binding_map_sha256':sha(MAP),'recipe_sha256':sha(op),'archive_manifest_sha256':sha(A/'manifest.json'),'outside_owner_unit':2634,'outside_source':old[2634]['source'],'outside_source_sha256':sha(F/old[2634]['source']),'outside_parent':'0x004745d0','handler':'0x00eeeb88','funcinfo':'0x011422a8','unwind_map':'0x011422a0','action':'0x00eeeb80','results':results,'requested_tails':len(tails),'bad_tails':bad,'inferred_tails':len(inferred),'conflicts':conf,'limits':['source correction and candidate labels require actual production reproof','final ownership/placement and runtime remain separate']},indent=2));print('PASS candidate 87/87, outside owner 139/139, all four requested tails')
if __name__=='__main__':main()
