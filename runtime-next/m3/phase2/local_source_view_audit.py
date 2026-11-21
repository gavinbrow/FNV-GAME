"""Bounded 20-record source-context benchmark; no compiler or source scan."""
import collections,hashlib,json,re,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';P=M/'out/phase2-web-backlog-20261119';O=M/'out/phase2-local-economy-20261119/source-views';sys.path.insert(0,str(H));import rtti_class_registry as reg
h=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def main():
 if O.exists():raise FileExistsError(O)
 start=time.monotonic();report=H/'RESEARCH-BACKLOG-20261119.md';ids=re.findall(r'^\| (P2N19-C-[0-9A-F]{8}) \|',report.read_text(encoding='utf8'),re.M)
 if len(ids)!=20 or len(set(ids))!=20:raise ValueError('pilot sample mismatch')
 ledger=load(P/'class-ledger.json');jobs=load(P/'job-ledger.json');idx=load(P/'source-evidence-index.json');census=load(P/'census.json');recipe=(F/'build/units.json').read_bytes();doc=json.loads(recipe);units=doc['units'];summary=load(P/'summary.json')
 if h(recipe)!=summary['recipe_sha256']:raise ValueError('recipe changed')
 selected=[next(x for x in ledger if x['job']==i) for i in ids];byva={x['type_descriptor_va']:x for x in census['classes']};defs=idx['definitions'];work=collections.defaultdict(set);meta={}
 for x in selected:
  c=byva[x['type_descriptor_va']];name=c['simple_identifier'];meta[x['job']]=(c,name)
  if name:
   for q in defs.get(name,[]):work[q['path']].add(name)
 before={};groups=collections.defaultdict(list);unavailable=[]
 for rel,names in sorted(work.items()):
  path=(F/rel).resolve()
  if not path.is_relative_to(F.resolve()) or rel not in idx['files']:raise ValueError('unindexed/escaping path')
  if not path.is_file():unavailable.append(rel);continue
  b=path.read_bytes();before[rel]=h(b)
  if before[rel]!=idx['files'][rel]['original_sha256']:raise ValueError('source preimage changed '+rel)
  text=b.decode('utf-8-sig',errors='replace')
  for d in reg.definitions(text,names):groups[d['name']].append({'path':rel,'line':d['line'],'keyword':d['keyword'],'lexical_token_sha256':d['lexical_token_sha256']})
 rows=[]
 for x in selected:
  c,name=meta[x['job']];d=groups.get(name,[]);fps=collections.defaultdict(list)
  for z in d:fps[z['lexical_token_sha256']].append({'path':z['path'],'line':z['line'],'keyword':z['keyword']})
  contexts=[]
  paths={z['path'] for z in d}
  for i,u in enumerate(units):
   if u['source'] in paths:contexts.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags']})
  hs=[z for z in census['hierarchies'] if z['bases'] and z['bases'][0]['type_descriptor_va']==x['type_descriptor_va']];vt=[z for z in census['vtables'] if z['locator']['type_descriptor_va']==x['type_descriptor_va']]
  rows.append({'job':x['job'],'type_descriptor_va':x['type_descriptor_va'],'type_name':x['type_name'],'simple_identifier':name,'template_encoded':'?$' in x['type_name'],'source_definition_leads':len(defs.get(name,[])) if name else 0,'bounded_lexical_definitions':len(d),'fingerprint_groups':[{'sha256':k,'occurrences':v} for k,v in sorted(fps.items())],'keywords':sorted({z['keyword'] for z in d}),'direct_recipe_contexts':contexts,'hierarchy_record_vas':[z['va'] for z in hs],'vtable_vas':[z['vtable_va'] for z in vt],'slot_prefix_counts':[len(z['contiguous_code_pointer_prefix_targets']) for z in vt],'unknowns':['lexical grouping does not establish namespace, preprocessing, pack, template specialization, ABI, linkage or ODR','direct recipe contexts omit transitive include consumers','source evidence and observed table prefixes do not prove historical native type or full extent']})
 for rel,digest in before.items():
  if h((F/rel).read_bytes())!=digest:raise ValueError('source changed during audit '+rel)
 O.mkdir(parents=True);result={'scope':'20 fixed census records; exact indexed source paths only, bounded lexical analysis','recipe_sha256':h(recipe),'input_hashes':{str(p.relative_to(R)):h(p.read_bytes()) for p in [report,P/'class-ledger.json',P/'job-ledger.json',P/'source-evidence-index.json',P/'census.json',P/'summary.json',H/'rtti_class_registry.py']},'source_hashes':before,'unavailable_paths':unavailable,'indexed_paths_examined':len(before),'records':rows,'seconds':round(time.monotonic()-start,3),'limits':['no compiler invocation or source changes','lexical hash is a review grouping, not semantic identity','snapshot preimage equality checked before and after; include closure and exact parser context are not established']};(O/'source-view-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps({'records':len(rows),'paths':len(before),'lexical_defs':sum(x['bounded_lexical_definitions'] for x in rows),'seconds':result['seconds']}))
if __name__=='__main__':main()
