"""Read-only production COFF/assembler provenance for TESForm and BGS caller."""
import gzip,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(RN/'build-v7')]
from compare import Coff,Pe,compare
import paths,sgmap_w2
O=M/'out/phase2-production-class-baseline';EXPECTED='e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 unitsfile=F/'build/units.json';sidefile=RN/'build-v7/sg_sidecar_w2.json';log=RN/'build-v7/relocs_v7.tsv.gz'
 if sha(unitsfile)!=EXPECTED:raise ValueError('unit recipe changed')
 units=json.loads(unitsfile.read_text())['units'];pe=Pe(paths.REF_IMAGE);details={};fields=set()
 for i in (998,621):
  obj=RN/('pinned-build/obj_v3/%04d.obj'%i);c=Coff(str(obj));rows=compare(c,pe,units[i]);bad=[]
  for x in rows:
   for rel in x['relocations']:
    if not rel.get('match'):
     va=int(x['address'],16)+rel['offset'];fields.add(va);bad.append({'function':x['address'],'field_va':'0x%08x'%va,'offset':rel['offset'],'symbol':rel['symbol'],'error':rel.get('error')})
  details[str(i)]={'object_sha256':sha(obj),'functions':len(rows),'reference_matches':sum(x['verdict']=='match' for x in rows),'nonmatching_fields':bad,'eh_tails':units[i].get('eh_tails',[])}
 side=json.loads(sidefile.read_text())['998'];coff=Coff(str(RN/'pinned-build/obj_v3/0998.obj'));remap=sgmap_w2.remap(coff,units[998]['symbols'],side)
 for row in details['998']['nonmatching_fields']:row['sidecar_binding']=remap.get(row['symbol'])
 tail=units[621]['eh_tails'][0];lo=int(tail['address'],16);hi=lo+tail['size'];logs=[];tail_logs=[]
 with gzip.open(log,'rt',encoding='utf8') as f:
  header=next(f).strip().split('\t')
  for line in f:
   cols=line.rstrip('\n').split('\t')
   try:va=int(cols[0],16)
   except ValueError:continue
   if va in fields:logs.append(dict(zip(header,cols)))
   if lo<=va<hi:tail_logs.append(dict(zip(header,cols)))
 details['998']['normal_v7_fields']=logs;details['621']['normal_v7_tail_fields']=tail_logs
 O.mkdir(exist_ok=True);out=O/'comparison.json'
 if out.exists():raise FileExistsError('refusing overwrite')
 out.write_text(json.dumps({'units_sha256':sha(unitsfile),'sidecar_sha256':sha(sidefile),'relocation_log_sha256':sha(log),'unit_evidence':details,'limitations':['strict recipe comparator does not use sidecars or assembler global symbol resolution','normal V7 log is separately observed and no recipe or oracle is altered','unit621 mapped code and EH relocation checks do not establish cross-TU class ODR']},indent=2));print(json.dumps({'998_matches':details['998']['reference_matches'],'998_unresolved_or_mismatched_fields':len(details['998']['nonmatching_fields']),'998_normal_log_agree':sum(x['status']=='agree' for x in logs),'621_matches':details['621']['reference_matches'],'621_tail_fields':len(tail_logs),'621_tail_agree':sum(x['status']=='agree' for x in tail_logs)}))
if __name__=='__main__':main()
