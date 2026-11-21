"""Explain failed 6757 EH tail coverage under reviewed non-immediate maps."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out/phase2-nimem-kind-cohort-run';A=M/'out/phase2-nimem-kind-production-archive';B=M/'out/phase2-nimem-kind-source-bindings-final.json';I=M/'out/phase2-nimem-kind-eh-reviewed-bindings.json';OUT=M/'out/phase2-nimem-kind-eh-tail-gap-diagnostic.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 data=json.loads(I.read_text());units=json.loads((R/'units.snapshot.json').read_text())['units'];progress=json.loads((R/'progress.json').read_text());maps=json.loads(B.read_text())['units'];bad=data['summary']['production']['bad_tails'];pe=Pe(paths.REF_IMAGE);names=recipe_names(units);gaps={}
 for va,n in bad.items():gaps[va]={'start':int(va,16),'size':n,'overlaps':[]}
 for row in progress['units']:
  i=row['unit'];spec=copy.deepcopy(units[i])
  for n,z in maps.get(str(i),{}).items():
   if z['evidence']!='same-unit-strict-archive-immediate':spec['symbols'][n]=z['target']
  if i==995:
   for n in ('$SG7025','$SG8028','$SG8627','$SG8632'):spec['symbols'].pop(n,None)
  c=Coff(str(A/('%04d.obj'%i)));r=compare(c,pe,spec);sec,_,_=eh_sections(c,pe,spec,r,names)
  for start,end,ok,parent,inferred in sec:
   for va,g in gaps.items():
    if start<g['start']+g['size'] and g['start']<end:g['overlaps'].append({'unit':i,'start':'0x%08x'%start,'end':'0x%08x'%end,'match':ok,'parent':parent,'inferred':inferred})
 for va,g in gaps.items():
  start=g['start'];size=g['size'];data=pe.read(start,size);good=set();failed=set()
  for z in g['overlaps']:
   a=max(start,int(z['start'],16));b=min(start+size,int(z['end'],16));(good if z['match'] else failed).update(range(a,b))
  missing=[start+i for i in range(size) if start+i not in good and (data[i]!=0xcc or start+i in failed)]
  spans=[]
  for q in missing:
   if spans and spans[-1][1]==q:spans[-1][1]+=1
   else:spans.append([q,q+1])
  g['missing_nonpadding_or_failed_spans']=[['0x%08x'%a,'0x%08x'%b] for a,b in spans];g['requested_start']='0x%08x'%g.pop('start')
 OUT.write_text(json.dumps({'scope':'production archive ordinary EH; field-scoped immediates excluded, no candidate substitution','input_review_sha256':sha(I),'recipe_sha256':sha(R/'units.snapshot.json'),'archive_manifest_sha256':sha(A/'manifest.json'),'tails':gaps,'limits':['presence of overlapping source section does not establish unreferenced bytes','outside-owner contributions require independently anchored function/xdata/source proof','failed located sections and global target errors remain separate']},indent=2));print(json.dumps({k:len(v['missing_nonpadding_or_failed_spans']) for k,v in gaps.items()}))
if __name__=='__main__':main()
