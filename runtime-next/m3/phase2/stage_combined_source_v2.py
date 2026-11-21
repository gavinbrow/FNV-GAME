"""Stage source-local literal and graph bindings on combined recipe; no compile/live edit."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';V=O/'phase2-source-integration6757';L=O/'phase2-source-integration6757-lane';T=O/'phase2-source-integration6757-v2';sys.path[:0]=[str(H),str(F/'tools'),str(R/'runtime-next')]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
import tescontainer_install,paths,class_metadata_compare as cm
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if T.exists():raise FileExistsError(T)
 if h(V/'manifest.json')!='81547b70a3471f423953800494083534349dab885afba119b525b6e522b37a41' or h(V/'units.generated')!='e71caa504effee614c560412dea1ecf8dc40f1317663e4799663cafc54b6c2ec':raise ValueError('v1 changed')
 base=(V/'units.generated').read_bytes();doc=json.loads(base);units=doc['units'];changes={};proofs={}
 proof253=O/'phase2-bfc-253-sized-delete/comparison.json';p=j(proof253);obj=L/'253/candidate.obj';c=Coff(str(obj));m={}
 for x in p['original_to_candidate_literals']:
  s=c.named(x['after']);data=c.sections[s['section']]['data']
  if s['value']!=x['pool_offset'] or hashlib.sha256(data).hexdigest()!=x['pool_sha256'] or x['after'] in m:raise ValueError('253 literal pool changed')
  m[x['after']]=x['bound_va']
 if len(m)!=26:raise ValueError('253 literal count')
 changes[253]=m;proofs['253']={'proof_sha256':h(proof253),'combined_object_sha256':h(obj),'pool_entries':len(m)}
 proof2909=O/'phase2-bfc-2909-destructible-lifetime/comparison-v2.json';v=j(proof2909);m=v['results']['2909']['paired_source_literal_bindings'];obj=L/'2909/candidate.obj';prior=O/'phase2-bfc-2909-destructible-lifetime/2909/candidate.obj'
 if h(prior)!=v['results']['2909']['candidate']['object_sha256'] or len(m)!=4:raise ValueError('2909 prior object')
 a=Coff(str(prior));b=Coff(str(obj))
 for name in m:
  x=a.named(name);y=b.named(name)
  if x['value']!=y['value'] or a.sections[x['section']]['data']!=b.sections[y['section']]['data']:raise ValueError('2909 pool changed')
 changes[2909]=m;proofs['2909']={'proof_sha256':h(proof2909),'prior_object_sha256':h(prior),'combined_object_sha256':h(obj),'pool_entries':len(m)}
 graph=O/'phase2-bgsbodypart-native-destructor-rebase6757/graph-unit.json';prior=j(graph)['symbols'];existing=units[620]['symbols'];conflicts={k for k,v in prior.items() if k in existing and existing[k]!=v}
 if conflicts:raise ValueError('graph conflict')
 e='??_ETESModelPSA@@UAEPAXI@Z';extra={k:v for k,v in prior.items() if k not in existing};weak=extra.pop(e)
 if len(extra)!=9 or weak!='0x005e3c30':raise ValueError('graph delta mismatch')
 changes[620]=extra;proofs['620']={'prior_graph_unit_sha256':h(graph),'combined_object_sha256':h(L/'620/candidate.obj'),'source_binding_count':9,'diagnostic_only_weak_E':{e:weak}}
 new=base
 for i,bind in sorted(changes.items()):
  u=copy.deepcopy(json.loads(new)['units'][i]);conflicts={k for k,v in bind.items() if k in u['symbols'] and u['symbols'][k]!=v}
  if conflicts:raise ValueError('binding conflict')
  u['symbols'].update(bind);new=tescontainer_install.replace_unit(new,i,u)
 updated=json.loads(new);dif=[i for i,(a,b) in enumerate(zip(units,updated['units'])) if a!=b]
 if dif!=[253,620,2909] or any(units[i][k]!=updated['units'][i][k] for i in dif for k in units[i] if k!='symbols'):raise ValueError('out-of-scope edits')
 pe=Pe(paths.REF_IMAGE);names=recipe_names(updated['units']);results={}
 for i in (253,370,425,620,621,2909,2910):
  p=L/str(i)/'candidate.obj';c=Coff(str(p));spec=updated['units'][i];rows=compare(c,pe,spec);sections,inferred,errors=eh_sections(c,pe,spec,rows,names);results[str(i)]={'object_sha256':h(p),'functions':len(rows),'matches':sum(x['verdict']=='match' for x in rows),'failures':[{'address':x['address'],'errors':x['errors']} for x in rows if x['verdict']!='match'],'eh_sections':len(sections),'eh_failed':sum(not x[2] for x in sections),'eh_errors':errors,'eh_inferred':{k:hex(v) for k,v in inferred.items()}}
 census=j(O/'phase2-class-census/census-6757.json');object620=L/'620/candidate.obj';graphs={}
 for tag in ('source_bindings','diagnostic_weak_E'):
  unit=copy.deepcopy(updated['units'][620]);
  if tag=='diagnostic_weak_E':unit['symbols'][e]=weak
  graphs[tag]={name:cm.compare_class(object620,unit,updated['units'],census,name) for name in ('.?AVBGSBodyPart@@','.?AVTESModelPSA@@')}
 T.mkdir();(T/'units.original').write_bytes(base);(T/'units.generated').write_bytes(new)
 out={'status':'private v2 recipe binding proposal; not installed','base_recipe_sha256':h(V/'units.generated'),'generated_recipe_sha256':h(T/'units.generated'),'source6757_sha256':h(F/'build/units.json'),'changed_units':dif,'binding_deltas':changes,'proofs':proofs,'function_and_eh_replay':results,'metadata':graphs,'limitations':['weak E binding is diagnostic only and is absent from proposed recipe','fresh production namespace/provider/COMDAT and image gates required','all objects are saved private combined fixture; no new compilation']}
 (T/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'recipe':h(T/'units.generated'),'manifest':h(T/'manifest.json'),'results':{k:(v['matches'],v['functions'],v['eh_failed'],len(v['eh_errors'])) for k,v in results.items()},'graph':{tag:{k:sum(s['match'] for t in v['tables'] for s in t['slots']) for k,v in q.items()} for tag,q in graphs.items()}}))
if __name__=='__main__':main()
