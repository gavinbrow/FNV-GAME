import json,os,sys,struct,bisect,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent; RN=HERE.parent.parent; PROJ=RN.parent
sys.path.insert(0,str(PROJ/'fnv_decomp'/'tools')); sys.path.insert(0,str(HERE.parent))
from compare import Coff
import gen_m3 as G
units=json.load(open(PROJ/'fnv_decomp'/'build'/'units.json'))['units']; evidence=HERE.parent/'out'/'batch8-promoted-default-verified'/'evidence'
manifest=json.load(open(evidence/'m3_manifest.json'))['entries']; pieces=json.load(open(evidence/'dv1_pieces.json'))['pieces']; coverage=sorted((x['va'],x['va']+x['size']) for x in manifest+pieces); starts=[a for a,b in coverage]; maxends=[]; end=0
for a,b in coverage: end=max(end,b); maxends.append(end)
def overlaps(a,b):
 i=bisect.bisect_left(starts,b)-1
 return i>=0 and maxends[i]>a
rows=[]
for idx,u in enumerate(units):
 matches=[(k,int(v,0)) for k,v in u.get('symbols',{}).items() if k.startswith('??_7')]
 if not matches:continue
 path=RN/'pinned-build'/'obj_v3'/('%04d.obj'%idx)
 if not path.exists():continue
 try:c=Coff(path)
 except Exception:continue
 for nm,va in matches:
  try:sy=c.named(nm)
  except Exception:continue
  if sy['section']<=0:continue
  sec=c.sections[sy['section']]; off=sy['value']; size=len(sec['data'])-off
  if size<=0 or size>2048 or va<0xfdf000 or G.sec_of(va)!='.rdata' or overlaps(va,va+size):continue
  rr=[]
  for o,si,k in sec['relocs']:
   if not off<=o<off+size or k!=6:continue
   target=c.symbols[si]['name']; rv=struct.unpack('<I',G.refbytes(va+o-off,4))[0]
   mapped=u.get('symbols',{}).get(target); mapped=int(mapped,0) if mapped else None
   rr.append({'offset':o-off,'symbol':target,'reference_target':rv,'unit_target':mapped,'target_section':c.symbols[si]['section']})
  unknown=[x for x in rr if x['unit_target'] is None and x['target_section']<=0]; mismatch=[x for x in rr if x['unit_target'] is not None and x['unit_target']!=x['reference_target']]
  if not unknown and not mismatch:continue
  rows.append({'unit':idx,'va':va,'size':size,'symbol':nm,'source':u.get('source') or u.get('path') or u.get('file'),'relocations':rr,'unknown':len(unknown),'mismatch':len(mismatch)})
  if len(rows)>=120:break
 if len(rows)>=120:break
rows.sort(key=lambda x:(x['unknown']+x['mismatch'],x['size']))
json.dump({'note':'read-only heuristic triage: unresolved unit map does not prove resolver failure; section ends may exceed actual vtable object; range overlap checks final saved M3/DV1 only; candidates require original placement corroboration','rows':rows},open(HERE/'vtable_triage.json','w'),indent=2)
for r in rows[:12]: print('unit',r['unit'],'va',hex(r['va']),'size',r['size'],'symbol',r['symbol'],'unknown',r['unknown'],'mismatch',r['mismatch'],'rels',len(r['relocations']))

