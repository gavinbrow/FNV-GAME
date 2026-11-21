"""Run ordinary EH-section/tail oracle on archived d569 BFC production and candidates."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';S=O/'phase2-baseformcomponent-core';I=O/'phase2-bfc-core-proof-index.json';B=O/'phase2-flags-script-production-before';DEST=O/'phase2-bfc-core-ordinary-eh-audit-v2.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if DEST.exists():raise FileExistsError('preserve evidence')
 index=json.loads(I.read_text());manifest=json.loads((S/'manifest.json').read_text());up=B/'units.json'
 if sha(up)!=index['recipe_sha256']:raise ValueError('archived recipe mismatch')
 units=json.loads(up.read_text())['units'];maps={}
 def add(i,k,v):
  d=maps.setdefault(i,{})
  if k in d and d[k]!=v:raise ValueError('conflicting same-unit binding')
  d[k]=v
 for name in ('local-string-evidence-v2.json','local-string-evidence-v3.json'):
  p=S/name
  if sha(p)!=index['pinned_inputs'][str(p.relative_to(M)).replace('\\','/')]:raise ValueError('binding evidence changed')
  e=json.loads(p.read_text())
  for i,items in e['source_derived_local_bindings'].items():
   for k,v in items.items():add(int(i),k,v)
 for name in ('external-binding-evidence.json','archived-immediate-evidence.json'):
  p=S/name
  if sha(p)!=index['pinned_inputs'][str(p.relative_to(M)).replace('\\','/')]:raise ValueError('binding evidence changed')
  for x in json.loads(p.read_text())['fields']:
   if name.startswith('external') and x['status']=='source-unique-reference-agree':add(x['unit'],x['symbol'],x['source_target'])
   elif name.startswith('archived'):add(x['unit'],x['symbol'],x['archived_source_immediate_va'])
 pe=Pe(paths.REF_IMAGE);names=recipe_names(units);allunits=[];done={'production':[],'original_mirror':[],'candidate':[]};details=[]
 for z in index['units']:
  i=z['unit'];unit=copy.deepcopy(units[i]);unit['symbols'].update(maps.get(i,{}));allunits.append(unit);report=M/z['report'];q=json.loads(report.read_text());d=report.parent
  if sha(report)!=z['report_sha256']:raise ValueError('report changed')
  candidate=copy.deepcopy(unit)
  for x in q['production_to_mirror_literals']+q['mirror_to_candidate_literals']:
   if 'bound_va' in x:candidate['symbols'][x['after']]=x['bound_va']
  pp=(B/('%04d.obj'%i)) if i in (2,1111,1112) else RN/('pinned-build/obj_v3/%04d.obj'%i)
  original=copy.deepcopy(unit)
  for x in q['production_to_mirror_literals']:
   if 'bound_va' in x:original['symbols'][x['after']]=x['bound_va']
  objects={'production':(O/'phase2-bfc-cohort-production-archive'/('%04d.obj'%i),unit,z['production_object_sha256']),'original_mirror':(d/'original.obj',original,z['objects']['original']),'candidate':(d/'candidate.obj',candidate,z['objects']['candidate'])};one={'unit':i,'recipe_eh_tails':z['ordinary_recipe_eh_tails']}
  for label,(path,spec,h) in objects.items():
   if sha(path)!=h:raise ValueError('object changed '+str(i)+' '+label)
   c=Coff(str(path));rows=compare(c,pe,spec);bad=[r['address'] for r in rows if r['verdict']!='match']
   if bad:raise ValueError('function prerequisite failed '+str((i,label,bad)))
   sections,inferred,errors=eh_sections(c,pe,spec,rows,names)
   done[label].append({'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}});one[label]={'object_sha256':h,'located_sections':len(sections),'failed_sections':sum(not x[2] for x in sections),'errors':errors,'inferred':{k:'0x%08x'%v for k,v in inferred.items()}}
  details.append(one)
 summary={}
 for label in done:
  tails,bad,inferred,count,conflicts=eh_tails(allunits,done[label],pe);summary[label]={'recipe_tails':len(tails),'bad':bad,'inferred_tails':inferred,'inferred_name_count':count,'inference_conflicts':conflicts,'unit_errors':sum(len(x[label]['errors']) for x in details),'failed_sections':sum(x[label]['failed_sections'] for x in details)}
 DEST.write_text(json.dumps({'scope':'unmodified ordinary build_and_match EH oracle over archived d569 production, original and candidate mirror objects','cohort_index_sha256':sha(I),'recipe_sha256':sha(up),'reference_sha256':sha(Path(paths.REF_IMAGE)),'summary':summary,'units':details,'limitations':['reference-based inference is identified separately','actual 6757 source transition requires new mirrors for 2/1111/1112','full linker ownership/generated data and final image remain separate']},indent=2));print(json.dumps(summary))
if __name__=='__main__':main()
