"""Read verified exported evidence for one exact PC class identity; no AI or database scan."""
import argparse,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[3]
def query(index,job=None,name=None,field_shapes=None):
 data=json.loads(index.read_bytes());records=data['records']
 if job:
  if not re.fullmatch(r'P2N19-C-[0-9A-F]{8}',job):raise ValueError('invalid job identity')
  rows=[r for r in records if r['job']==job]
 else:rows=[r for r in records if r['pc_type_name']==name]
 if len(rows)!=1:raise ValueError('require one exact PC identity; matched '+str(len(rows)))
 row=rows[0];path=(index.parent/row['card']).resolve()
 if not path.is_relative_to(index.parent.resolve()):raise ValueError('card path escapes index')
 raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=row['card_sha256']:raise ValueError('evidence card changed')
 card=json.loads(raw)
 if card['job']!=row['job'] or card['pc_type_name']!=row['pc_type_name']:raise ValueError('identity mismatch')
 if field_shapes:
  supplemental=json.loads(field_shapes.read_bytes())
  if supplemental['index_sha256']!=hashlib.sha256(index.read_bytes()).hexdigest():raise ValueError('field-shape evidence belongs to another index')
  by_id={r['field_member_id']:r for r in supplemental['rows']}
  for d in card['definitions']:
   for m in d['members']:
    extra=by_id.get(m['field_member_id'])
    if extra:
     if (extra['program'],extra['type_index'])!=(m['program_id'],m['referenced_type_index']):raise ValueError('field-shape type identity mismatch')
     m['supplemental_xbox_field_shape']=extra
 return card
if __name__=='__main__':
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--job');g.add_argument('--name',help='Exact decorated PC RTTI name, not a simple spelling');ap.add_argument('--index',type=Path,default=R/'runtime-next/m3/out/non-ai-continuation-20261119/atlas-index/index.json');ap.add_argument('--field-shapes',type=Path,help='Optional verified supplemental shape result; Xbox evidence only');a=ap.parse_args();print(json.dumps(query(a.index,a.job,a.name,a.field_shapes),indent=2))
