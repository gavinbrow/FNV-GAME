"""Bound type_info provider evidence and count the same archived library pattern."""
import hashlib,json,pickle,struct,sys
from collections import Counter
from pathlib import Path
M=Path(__file__).resolve().parent.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';E=R/'phase2-native-source-positive/evidence';O=R/'phase2-local-economy-20261119/reuse-placement/ctype-typeinfo-audit.json';sys.path[:0]=[str(RN/'data-v1'),str(F/'tools'),str(RN)]
import place,paths
from compare import Pe
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve previous evidence')
 placed=E/'data-v1-scratch/dv1_placed.pkl';p0=E/'data-v1-scratch/dv1_phase0.pkl';recipe=E/'units.json';s=pickle.loads(placed.read_bytes());raw=pickle.loads(p0.read_bytes())['res'];units=json.loads(recipe.read_text())['units'];pe=Pe(paths.REF_IMAGE);name='??_7type_info@@6B@';references=[]
 for u,section,va in ((230,6,0x01186744),(75,22,0x0119dc4c)):
  z=next(x for x in raw[u]['secs'] if x['k']==section);r=[x for x in z['relocs'] if x[2]==name]
  if len(r)!=1 or r[0][0]!=0 or r[0][1]!=6 or r[0][6]!=0 or r[0][7]!='c' or r[0][8]!=0x010f1ee0 or struct.unpack('<I',pe.read(va,4))[0]!=r[0][8]:raise ValueError('project relocation mismatch')
  if name in units[u]['symbols']:raise ValueError('resolution unexpectedly unit-local')
  references.append({'unit':u,'source':units[u]['source'],'section_index':section,'descriptor_va':'0x%08x'%va,'kind':6,'offset':0,'addend':0,'symbol':name,'archived_resolver':'c','resolved_value':'0x010f1ee0','reference_target_matches':True})
 maps=[{'unit':i,'source':u['source'],'value':u['symbols'][name]} for i,u in enumerate(units) if name in u.get('symbols',{})]
 if len(maps)!=3 or any(x['value']!='0x010f1ee0' for x in maps):raise ValueError('recipe symbol consensus differs')
 hits=[(k,t) for k,(a,t) in s.placed.items() if a==0x011ac8e0 and len(s.SEC[k]['data'])==29]
 if len(hits)!=1:raise ValueError('ctype candidate identity differs')
 key,tier=hits[0];z=s.SEC[key];r=z['relocs']
 if len(r)!=1 or r[0][0]!=0 or r[0][1]!=6 or r[0][2]!=name or r[0][6]!=0 or s.resolve(z)[0] or struct.unpack('<I',pe.read(0x011ac8e0,4))[0]!=0x010f1ee0:raise ValueError('library relocation identity differs')
 providers=[{'units':v['units'],'section':v['name'],'size':v['size'],'placed':key2 in s.placed} for key2,v in s.SEC.items() if any(d[0]==name for d in v['defs'])]
 if s.gdef.get(name) is not None:raise ValueError('archived provider unexpectedly resolves')
 count=Counter();examples=[]
 for k,v in s.SEC.items():
  if v['kind']!='rtti0' or not v['units'] or any(i<100000 for i in v['units']):continue
  rr=v['relocs']
  if len(rr)!=1 or rr[0][0]!=0 or rr[0][1]!=6 or rr[0][2]!=name or rr[0][6]!=0:continue
  count['library_only_rtti0_same_pattern']+=1
  if k in s.placed:
   addr,t=s.placed[k];count['placed_candidates']+=1;count['tier_'+t]+=1
   try:
    if struct.unpack('<I',pe.read(addr,4))[0]==0x010f1ee0:count['reference_target_matches']+=1
    else:count['reference_target_differs']+=1
   except ValueError:count['reference_unreadable']+=1
   if s.resolve(v)[0]:count['archived_resolution_available']+=1
   else:count['archived_resolution_missing']+=1
   if len(examples)<3:examples.append({'va':'0x%08x'%addr,'units':v['units'],'tier':t})
 result={'input_sha256':{'archived_phase0':sha(p0),'archived_placed':sha(placed),'archived_recipe':sha(recipe),'reference':sha(Path(paths.REF_IMAGE))},'project_references':references,'recipe_symbol_consensus':maps,'library_ctype':{'va':'0x011ac8e0','size':29,'units':z['units'],'tier':tier,'kind':6,'offset':0,'addend':0,'symbol':name,'reference_target':'0x010f1ee0','archived_resolver_result':'unresolved','provider_gdef':'absent'},'provider_sections':providers,'pattern_count':dict(count),'sample_placed':examples,'conclusion':'same exact external symbol and unit recipe consensus support a global address binding as existing project metadata; archived library resolver did not consult that project consensus and has no placed gdef. The sole matching library provider section is unplaced, so actual source/native producer ownership is not proven. Current library opt-in also rejects relocatable sections. No selector or alias changes were made.','limits':['project consensus and exact matching reference relocations are supporting address evidence, not proof of native or linked provider ownership','placed-candidate count is archival state only, not accepted selection or new coverage','original library archive/member identities beyond existing archived metadata remain separate']}
 O.write_text(json.dumps(result,indent=2));print(json.dumps({'counts':dict(count),'providers':providers,'sha256':sha(O)}))
if __name__=='__main__':main()
