"""Read-only audit of the frozen placement backlog and two prior mapping leads."""
import bisect,hashlib,json
from collections import Counter
from pathlib import Path
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';R=M/'out';B=R/'phase2-web-backlog-20261119';O=R/'phase2-local-economy-20261119/reuse-placement'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if O.exists():raise FileExistsError('preserve prior audit')
 paths={'jobs':B/'local-placement-jobs.json','ledger':B/'local-placement-ledger.json','summary':B/'summary.json','produced':M/'inventory/b7_produced.json','census':R/'phase2-class-census/census-v2.json','recipe':F/'build/units.json','automem_header':F/'include/AutoMemContext.h','water_source':F/'src/bsshader/watershader.cpp','water_ownership':R/'phase2-watershader-211-eh-ownership.json','water_trial':R/'phase2-watershader-211-automem-v1-u0211/automem-comparison.json','texture_source':F/'src/fallout_shared/bgstextureusemap.cpp'}
 h={k:sha(p) for k,p in paths.items()};jobs=load(paths['jobs']);ledger=load(paths['ledger']);summary=load(paths['summary']);census=load(paths['census']);recipe=load(paths['recipe']);produced=load(paths['produced'])
 if len(jobs)!=67 or len(ledger)!=4238 or sum(x['size'] for x in ledger)!=190878 or sha(paths['recipe'])!=summary['recipe_sha256']:raise ValueError('backlog or live recipe no longer matches frozen snapshot')
 if [r for job in jobs for r in job['ranges']]!=ledger:raise ValueError('group ledger mismatch')
 # Metadata leads are points, not inferred object bounds or selectable owners.
 points=[]
 for c in census['classes']:points.append((c['type_descriptor_va'],'rtti_type_descriptor',c['type_name']))
 for v in census['vtables']:points.append((v['vtable_va'],'rtti_vtable_lead',v['locator']['type_name']))
 for g in census['hierarchies']:points.append((g['va'],'rtti_hierarchy',None))
 points.sort(key=lambda x:x[0]);addrs=[x[0] for x in points];exact=Counter((int(a),int(n)) for a,n in produced);allrows=[];groups=[]
 for job in jobs:
  labels=Counter();rows=[]
  for r in job['ranges']:
   a=r['va'];z=a+r['size'];lo=bisect.bisect_left(addrs,a);hi=bisect.bisect_left(addrs,z);hits=[{'va':v,'kind':k,'type':n} for v,k,n in points[lo:hi]];types=sorted(set(x['kind'] for x in hits));labels.update(types or ['no_pc_rtti_point']);row={'va':a,'size':r['size'],'section':r['section'],'exact_b7_range_count':exact[(a,r['size'])],'rtti_point_leads':hits,'placement_status':'unproven; original producer, exact declaration, field/extents, relocations and ownership require checks'};rows.append(row);allrows.append(row)
  groups.append({'id':job['id'],'ranges':len(rows),'bytes':sum(x['size'] for x in rows),'ledger_status':job['status'],'rtti_lead_counts':dict(labels),'exact_b7_ranges':sum(x['exact_b7_range_count']>0 for x in rows),'placement_ready_count':0,'reason':'ledger provides range membership only; no per-object source, section, relocation or ownership proof'})
 if sum(x['ranges'] for x in groups)!=4238 or sum(x['bytes'] for x in groups)!=190878:raise ValueError('aggregate changed')
 owner=load(paths['water_ownership']);trial=load(paths['water_trial']);shell=recipe['units'][689];fn=[f for f in shell['functions'] if f['address']=='0x004aa3a0'];auto=paths['automem_header'].read_text();texture=paths['texture_source'].read_text()
 if len(fn)!=1 or 'struct FUN_004aa3d0_shell' not in texture or 'sizeof(AutoMemContext) == 0x4' not in auto:raise ValueError('sample source differs')
 cases={'AutoMemContext':{'upstream_fact':'recorded research: Xbox field +0 iOldMemContext, MEM_CONTEXT','source':'include/AutoMemContext.h','existing_pc_fact':'4-byte class with MEM_CONTEXT at offset 0','unit211_existing':'source-owned original unwind identifies AutoMemContext destructor and -0x1048 local; original 5647-byte parent strictly matched','new_fact':'Xbox record provides candidate original member name and independently agrees old-context interpretation','conflict':'one-word private experiment changes parent extent 5647 to 5649 and stack frame 0x1050 to 0x104c','trial_gates':trial['gates'],'decision':'no source or EH fix proven','unknown':'native source constructor, frame layout, ODR and exact initial assignment remain unresolved'},'BGSTextureUseMap':{'upstream_fact':'recorded research: Xbox method-linked class-name candidate for FUN_004aa3d0_shell','source':'src/fallout_shared/bgstextureusemap.cpp','recipe_unit':689,'pc_anchor':fn[0],'local_existing':'the synthetic shell and a separate namespaced function at 0x004aa3d0 coexist','new_fact':'candidate source-class name from cross-platform linked-method record','conflict':'symbol spelling and stand-in class associations do not prove actual PC class hierarchy or unique ODR identity','decision':'source-name lead only, not an automatic class rename','unknown':'linked method alternatives, exact class/member layout and original metadata ownership remain unproven'}}
 result={'scope':'evidence reuse only; no selection, compiler, recipe, source or queue mutation','input_sha256':h,'mapping_cases':cases,'placement_totals':{'groups':len(groups),'ranges':len(allrows),'bytes':sum(x['size'] for x in allrows),'by_section':dict(Counter(x['section'] for x in allrows)),'range_exact_b7_match_count':sum(x['exact_b7_range_count']>0 for x in allrows),'ranges_with_rtti_points':sum(bool(x['rtti_point_leads']) for x in allrows),'placement_ready_count':0},'groups':groups,'ranges':allrows,'limits':['classification based on metadata available in frozen ledgers, not a fresh COFF or reference-byte placement replay','RTTI points do not establish full table/object boundaries or native ownership','zero selection-ready entries means no sufficient per-object proofs in these inputs, not proof none can exist elsewhere','upstream mapping facts are from the previously recorded research; no fetch or download performed']}
 O.mkdir(parents=True);(O/'audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result['placement_totals']))
if __name__=='__main__':main()
