"""Compare independently preserved evidence sources, never approve ABI from agreement."""
from pathlib import Path
import argparse,hashlib,json,collections,time
R=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compare(index,community,out):
 assert not out.exists();start=time.monotonic();ih=sha(index);ch=sha(community);i=json.loads(index.read_bytes());pc=json.loads(community.read_bytes())['structs'];rows=[]
 for x in i['records']:
  path=index.parent/x['card'];assert sha(path)==x['card_sha256'];card=json.loads(path.read_bytes());alternatives=[]
  for d in card['definitions']:
   name=d['tag']['display_name'];candidates=[(k,v) for k,v in pc.items() if v.get('full_name',k)==name]
   for key,c in candidates:
    fields=c.get('fields',[]);named={f['name']:f for f in fields};matches=[]
    for f in d['members']:
     if f['member_kind']!='data_member' or f['member_name'] not in named:continue
     pf=named[f['member_name']]
     matches.append({'name':f['member_name'],'xbox_offset':f['member_offset_value'],'community_offset':pf.get('offset'),'offset_equal':str(pf.get('offset'))==f['member_offset_value'],'xbox_type':f['rendered_type'],'community_type':pf.get('type'),'same_name_is_not_identity_proof':True})
    alternatives.append({'debug_tag_layout_id':d['tag']['tag_layout_id'],'exact_display_name':name,'community_key':key,'xbox_size':d['tag']['size_value'],'community_size':c.get('size'),'sizes_equal':str(c.get('size'))==d['tag']['size_value'],'community_has_field_records':bool(fields),'community_bases':c.get('bases',[]),'exact_field_spelling_comparisons':matches,'source_evidence_only':True})
  rows.append({'job':x['job'],'pc_type_name':x['pc_type_name'],'debug_definition_count':x['definition_count'],'alternatives':alternatives,'native_approved':False})
 assert sha(index)==ih and sha(community)==ch
 counts={'pc_records':len(rows),'with_exact_debug_and_community_names':sum(bool(r['alternatives']) for r in rows),'any_equal_size_alternative':sum(any(a['sizes_equal'] for a in r['alternatives']) for r in rows),'only_different_size_alternatives':sum(bool(r['alternatives']) and not any(a['sizes_equal'] for a in r['alternatives']) for r in rows),'same_spelling_field_comparisons':sum(len(a['exact_field_spelling_comparisons']) for r in rows for a in r['alternatives']),'different_offset_field_occurrences':sum(not f['offset_equal'] for r in rows for a in r['alternatives'] for f in a['exact_field_spelling_comparisons'])}
 out.mkdir(parents=True);result={'scope':'Exact debug/community name and size/field-offset comparison; names, size or offsets alone never prove native layout or inheritance','input_hashes':{'index':ih,'community':ch,'tool':sha(Path(__file__))},'counts':counts,'seconds':time.monotonic()-start,'records':rows,'native_classes_approved':0}
 (out/'comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps(counts))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);v=a.parse_args();O=R/'runtime-next/m3/out/non-ai-continuation-20261119';compare(O/'atlas-index/index.json',O/'importer/before.json',v.out)
