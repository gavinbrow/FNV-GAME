"""Freeze private PIECES candidates with optional whole atan-table owner."""
import json,hashlib,sys
from pathlib import Path
M=Path(__file__).resolve().parent.parent;D=M/'out/phase2-library-splits';D.mkdir(parents=True,exist_ok=True);whole=json.load(open(M/'out/phase2-library/selection.json'));sp=json.load(open(M/'phase2/library_split_candidates.json'));selected=[];atan=[]
for r in sp['candidates']:
 if r['section_start']==0 and r['section_end']==r['section_size']:
  if r['va']==0x10ff040 and r['size']==6160:atan.append(dict(r))
  continue
 x=dict(r);x['compiler_bytes_sha256']=x.pop('slice_sha256');x['split_section']=True;selected.append(x)
assert len(selected)==34 and sum(x['size'] for x in selected)==4196 and len(atan)==1
allc=sorted(whole['candidates']+selected,key=lambda x:x['va']);assert all(x['va']+x['size']<=y['va'] for x,y in zip(allc,allc[1:]));p=D/'selection.json';doc={'scope':'Private existing validated whole-section proposals plus PIECES-backed symbol-boundary slices; full validation pending.','candidate_count':len(allc),'candidate_bytes':sum(x['size'] for x in allc),'candidates':allc};p.write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8');print(p.name,hashlib.sha256(p.read_bytes()).hexdigest())
x=atan[0];x['compiler_bytes_sha256']=x.pop('slice_sha256');c=sorted(allc+[x],key=lambda z:z['va']);assert all(a['va']+a['size']<=b['va'] for a,b in zip(c,c[1:]));doc={'scope':'Experimental deterministic whole+split selection; atan complete compiler section preferred over overlapping unselected library aliases.','candidate_count':len(c),'candidate_bytes':sum(z['size'] for z in c),'candidates':c};p=D/'selection-with-atan.json';p.write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8');print(p.name,hashlib.sha256(p.read_bytes()).hexdigest())
