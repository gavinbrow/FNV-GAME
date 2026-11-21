"""Prove the adjacent unit 1029 contribution to unit 1027's listed EH extent."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';I=O/'phase2-bfc-core-proof-index.json';B=O/'phase2-bfc-cohort-production-archive';U=O/'phase2-flags-script-production-before/units.json';X=RN/'pinned-build/obj_v3.bak-20261116/1029.obj';DEST=O/'phase2-bfc-eh-unit1027-contribution.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if DEST.exists():raise FileExistsError('preserve evidence')
 idx=json.loads(I.read_text());units=json.loads(U.read_text())['units'];z=next(x for x in idx['units'] if x['unit']==1027);report=M/z['report'];src=F/units[1029]['source'];c=Coff(str(X));pe=Pe(paths.REF_IMAGE);names=recipe_names(units)
 if sha(U)!=idx['recipe_sha256'] or sha(report)!=z['report_sha256'] or sha(B/'1027.obj')!=z['production_object_sha256']:raise ValueError('pinned baseline differs')
 extrows=compare(c,pe,units[1029]);extsec,extinf,exterr=eh_sections(c,pe,units[1029],extrows,names)
 if len(extrows)!=7 or any(x['verdict']!='match' for x in extrows) or exterr:raise ValueError('owner not strict')
 owner=next(f for f in units[1029]['functions'] if f['address']=='0x0050adf0');parentbytes=pe.read(int(owner['address'],16),owner['size'])
 if parentbytes.find(struct.pack('<I',0xef3c8e))<0:raise ValueError('handler reference absent')
 points=[x for x in extsec if 0xef3c70<=x[0]<0xef3ca9]
 if not points or min(x[0] for x in points)!=0xef3c70 or max(x[1] for x in points)!=0xef3ca9 or any(not x[2] or x[3]!='0x0050adf0' for x in points):raise ValueError('owner sections do not match')
 def info(addr):
  x=struct.unpack('<10I',pe.read(addr,40));return {'magic':hex(x[0]),'max_state':x[1],'unwind_map':hex(x[2]),'actions':[hex(struct.unpack('<II',pe.read(x[2]+8*i,8))[1]) for i in range(x[1])]}
 infos=[info(0x1146450),info(0x11464ec)]
 if infos[0]['actions']!=['0xef3bd0','0xef3bd8','0xef3be3'] or infos[1]['actions']!=['0xef3c70','0xef3c78','0xef3c83']:raise ValueError('FuncInfo differs')
 out=[]
 for tag,path,h in [('production',B/'1027.obj',z['production_object_sha256']),('original_mirror',report.parent/'original.obj',z['objects']['original']),('candidate',report.parent/'candidate.obj',z['objects']['candidate'])]:
  if sha(path)!=h:raise ValueError('1027 object changed')
  obj=Coff(str(path));rows=compare(obj,pe,units[1027]);sections,inferred,errors=eh_sections(obj,pe,units[1027],rows,names)
  if any(x['verdict']!='match' for x in rows) or errors:raise ValueError('1027 strict check failed')
  done=[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}},{'eh_sections':extsec,'eh_inferred':{k:'0x%08x'%v for k,v in extinf.items()}}];tails,bad,inf,_,conf=eh_tails([units[1027]],done,pe)
  if len(tails)!=2 or bad or conf:raise ValueError('ordinary tail check failed')
  out.append({'tag':tag,'object_sha256':h,'strict_functions':len(rows),'ordinary_tails_passed':len(tails),'inferred_tails':len(inf),'conflicts':conf})
 DEST.write_text(json.dumps({'scope':'unit 1027 listed extents use adjacent independently owned unit 1029 constructor EH; no ICF equivalence claim','cohort_index_sha256':sha(I),'recipe_sha256':sha(U),'reference_sha256':sha(Path(paths.REF_IMAGE)),'outside_unit':1029,'outside_object_sha256':sha(X),'outside_source':units[1029]['source'],'outside_source_sha256':sha(src),'outside_functions_strict':7,'outside_parent':'0x0050adf0','outside_handler':'0x00ef3c8e','outside_contribution':['0x00ef3c70','0x00ef3ca9'],'first_destructor_targets':['0x0050f740','0x0050e9f0'],'funcinfos':infos,'results':out,'limitations':['unit 1029 object is archived from 2026-11-16, not a fresh 6757 production build','linker placement and full image remain separate']},indent=2));print(json.dumps(out))
if __name__=='__main__':main()
