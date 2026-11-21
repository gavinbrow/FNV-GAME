"""Export exact-identity debug evidence without merging classes or generating game code."""
import argparse,collections,hashlib,json,sqlite3,time
from pathlib import Path
R=Path(__file__).resolve().parents[3]
DB_SHA='a2adbbfb992be9b9d22b747e365bef31c8cbe8398e07030d34db43bd95da3485'
CENSUS_SHA='7db4154e2f19978cbae22387803969667318f9d80cbc0e9ac9507621fa702be9'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def export(db,census_path,ledger_path,out):
 start=time.monotonic();assert not out.exists(),'refuse overwrite'
 assert sha(db)==DB_SHA and sha(census_path)==CENSUS_SHA
 census=json.loads(census_path.read_bytes());ledger=json.loads(ledger_path.read_bytes());byva={r['type_descriptor_va']:r['job'] for r in ledger};assert len(byva)==2999
 c=sqlite3.connect(db.resolve().as_uri()+'?mode=ro&immutable=1',uri=True);c.row_factory=sqlite3.Row
 tags=collections.defaultdict(list)
 for t in c.execute('select * from codeview_tag_layouts where is_forward_reference=0'):tags[t['unique_name']].append(dict(t))
 type_names={}
 for r in c.execute('select r.program_id,r.type_index,t.unique_name from codeview_type_records r join codeview_tag_layouts t using(type_record_id)'):
  key=(r['program_id'],r['type_index']);assert key not in type_names or type_names[key]==r['unique_name'];type_names[key]=r['unique_name']
 graphs=collections.defaultdict(list)
 for g in census['hierarchies']:
  if not g['bases']:continue
  va=g['bases'][0]['type_descriptor_va'];direct=[{'unique_name':b['type_name'][3:],'offset':b['pmd'][0],'pmd':b['pmd']} for b in g['bases'] if b['preorder_parent_index']==0]
  if direct not in graphs[va]:graphs[va].append(direct)
 out.mkdir(parents=True);cards=out/'cards';cards.mkdir();index=[];kinds=collections.Counter();definition_totals=collections.Counter();seen_fields=set();seen_methods=set();errors=collections.Counter()
 for n,cl in enumerate(census['classes']):
  va=cl['type_descriptor_va'];unique=cl['type_name'][3:];definitions=[];pc=graphs[va]
  for t in tags.get(unique,[]):
   ms=[dict(m) for m in c.execute('select f.*,u.ordinal from codeview_tag_member_uses u join codeview_field_members f using(field_member_id) where u.tag_layout_id=? order by u.ordinal',(t['tag_layout_id'],))]
   bases=[]
   for m in ms:
    m.pop('created_at',None);kinds[m['member_kind']]+=1
    if m['member_kind']=='data_member':seen_fields.add(m['field_member_id'])
    if m['member_kind']=='one_method':seen_methods.add(m['field_member_id'])
    if m['method_list_type_index'] is not None:
     m['overloads']=[dict(z) for z in c.execute('select * from codeview_method_overloads where extraction_id=? and method_list_type_index=? order by ordinal',(m['extraction_id'],m['method_list_type_index']))]
     for z in m['overloads']:z.pop('created_at',None)
    if m['member_kind']=='base_class':bases.append({'unique_name':type_names.get((t['program_id'],m['base_type_index'])),'offset':int(m['member_offset_value'])})
   diags=[dict(d) for d in c.execute('select * from codeview_layout_diagnostics where tag_layout_id=? order by ordinal',(t['tag_layout_id'],))]
   for d in diags:d.pop('created_at',None);errors[d['code']]+=1
   t.pop('created_at',None)
   flags={'has_pc_direct_base_evidence':bool(pc),'ordered_base_names_agree':any([b['unique_name'] for b in bases]==[b['unique_name'] for b in bs] for bs in pc),'ordered_base_offsets_agree':any(bases==[{k:b[k] for k in ('unique_name','offset')} for b in bs] for bs in pc),'has_decode_diagnostics':bool(diags)}
   for k,v in flags.items():definition_totals[k]+=bool(v)
   definitions.append({'tag':t,'members':ms,'direct_bases':bases,'diagnostics':diags,'cross_platform_flags':flags})
  job=byva[va];card={'schema':1,'job':job,'pc_type_name':cl['type_name'],'pc_type_descriptor_va':va,'exact_unique_name':unique,'pc_direct_base_alternatives':pc,'debug_platform':'Xbox360 release MemDebug; not PC layout proof','definitions':definitions,'native_class_accepted':False}
  path=cards/(job+'.json');dump(path,card)
  flags={'has_exact_definition':bool(definitions),'ambiguous_definitions':len(definitions)>1,'has_decode_diagnostics':any(d['diagnostics'] for d in definitions),'any_ordered_base_names_agree':any(d['cross_platform_flags']['ordered_base_names_agree'] for d in definitions),'any_ordered_base_offsets_agree':any(d['cross_platform_flags']['ordered_base_offsets_agree'] for d in definitions)}
  index.append({'job':job,'pc_type_name':cl['type_name'],'pc_type_descriptor_va':va,'definition_count':len(definitions),'card':str(path.relative_to(out)),'card_sha256':sha(path),**flags})
  if (n+1)%500==0:print('exported',n+1,flush=True)
 counts={'pc_records':len(index),'definitions':sum(r['definition_count'] for r in index),'unique_data_member_records':len(seen_fields),'unique_single_method_records':len(seen_methods),**{k:sum(r[k] for r in index) for k in flags}}
 result={'schema':1,'scope':'Exact debug identity/fact retrieval and ordered PC RTTI base comparison; not native class recovery','inputs':{'database_sha256':DB_SHA,'census_sha256':CENSUS_SHA,'ledger_sha256':sha(ledger_path),'generator_sha256':sha(Path(__file__))},'counts':counts,'member_occurrences_by_kind':dict(kinds),'definition_flags':dict(definition_totals),'decode_diagnostic_occurrences':dict(errors),'seconds':time.monotonic()-start,'records':index,'limits':['No spelling-only or fuzzy merge','Every Xbox layout/member/virtual hypothesis still needs PC checks','Base graph agreement does not validate fields, size, return ABI or providers','Missing definitions and decode diagnostics are retained, never silently approved','No protected source, queue, selection or production code changes']}
 dump(out/'index.json',result);print(json.dumps(counts));return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--db',type=Path,default=R/'runtime-next/m3/out/non-ai-benchmark-20261119/atlas/fnv-source-atlas-data-0.5.0/fnv-source-atlas.sqlite');v=a.parse_args()
 export(v.db,R/'runtime-next/m3/out/phase2-web-backlog-20261119/census.json',R/'runtime-next/m3/out/phase2-web-backlog-20261119/class-ledger.json',v.out)
