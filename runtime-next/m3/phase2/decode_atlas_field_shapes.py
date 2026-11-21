"""Decode retained CodeView array/bitfield shapes; keep Xbox provenance, never emit PC layouts."""
import argparse,functools,hashlib,json,sqlite3,struct,collections
from pathlib import Path
R=Path(__file__).resolve().parents[3]
SIMPLE={0x10:('signed char',1),0x20:('unsigned char',1),0x70:('char',1),0x11:('short',2),0x21:('unsigned short',2),0x74:('int',4),0x75:('unsigned int',4),0x12:('long',4),0x22:('unsigned long',4),0x40:('float',4),0x41:('double',8),0x30:('bool',1),0x71:('wchar_t',2),0x72:('int16',2),0x73:('uint16',2),0x13:('long long',8),0x23:('unsigned long long',8)}
def numeric(b,o):
 n=struct.unpack_from('<H',b,o)[0]
 if n<0x8000:return n,o+2
 forms={0x8000:'b',0x8001:'h',0x8002:'H',0x8003:'i',0x8004:'I',0x8009:'q',0x800a:'Q'}
 if n not in forms:raise ValueError('unsupported numeric leaf '+hex(n))
 fmt='<'+forms[n];return struct.unpack_from(fmt,b,o+2)[0],o+2+struct.calcsize(fmt)
class Decoder:
 def __init__(self,c):self.c=c
 @functools.lru_cache(None)
 def decode(self,program,ti,depth=0):
  if depth>20:raise ValueError('type recursion limit')
  if ti<0x1000:
   mode=(ti>>8)&15;kind=ti&255
   if kind not in SIMPLE:raise ValueError('unsupported primitive '+hex(ti))
   name,size=SIMPLE[kind]
   if mode:
    if mode!=4:raise ValueError('unsupported simple pointer mode')
    return {'kind':'pointer','byte_size':4,'target':{'kind':'primitive','name':name,'byte_size':size},'type_index':ti}
   return {'kind':'primitive','name':name,'byte_size':size,'type_index':ti}
  r=self.c.execute('select type_record_id,leaf_kind,raw_body,raw_body_sha256 from codeview_type_records where program_id=? and type_index=?',(program,ti)).fetchone()
  if not r:raise ValueError('missing type record '+hex(ti))
  rid,leaf,raw,digest=r;b=bytes(raw)
  if hashlib.sha256(b).hexdigest()!=digest:raise ValueError('raw record hash mismatch')
  tags=self.c.execute('select tag_kind,size_value,display_name,unique_name,is_forward_reference,underlying_type_index from codeview_tag_layouts where type_record_id=?',(rid,)).fetchall()
  if tags:
   t=tags[0]
   if t[4]:
    alternatives=self.c.execute('select tag_kind,size_value,display_name,unique_name,is_forward_reference,underlying_type_index from codeview_tag_layouts where program_id=? and unique_name=? and is_forward_reference=0',(program,t[3])).fetchall()
    if not alternatives or len({(a[0],a[1],a[2],a[3],a[5]) for a in alternatives})!=1:raise ValueError('ambiguous/missing complete tag')
    t=alternatives[0]
   if t[0]=='enum':size=self.decode(program,t[5],depth+1)['byte_size']
   else:size=int(t[1])
   return {'kind':'tag','tag_kind':t[0],'name':t[2],'unique_name':t[3],'byte_size':size,'type_index':ti,'raw_body_sha256':digest}
  if leaf==0x1503:
   elem,index=struct.unpack_from('<II',b);size,o=numeric(b,8)
   if size<0 or b.find(b'\0',o)<0:raise ValueError('invalid array size/name')
   child=self.decode(program,elem,depth+1);es=child['byte_size']
   if es<=0 or size%es:raise ValueError('array size is not an exact element multiple')
   shape={'kind':'array','byte_size':size,'element_count':size//es,'element':child,'index_type_index':index}
  elif leaf==0x1002:
   target,attrs=struct.unpack_from('<II',b);size=(attrs>>13)&255;mode=(attrs>>5)&7
   if size!=4 or mode not in (0,1,4):raise ValueError('unsupported pointer representation')
   shape={'kind':'pointer','byte_size':size,'pointer_mode':mode,'attributes':attrs,'target':self.decode(program,target,depth+1)}
  elif leaf==0x1205:
   target,width,pos=struct.unpack_from('<IBB',b);child=self.decode(program,target,depth+1)
   if width==0 or pos+width>child['byte_size']*8:raise ValueError('bitfield exceeds storage')
   shape={'kind':'bitfield','byte_size':child['byte_size'],'bit_width':width,'bit_offset':pos,'storage':child}
  elif leaf==0x1001:
   target,attrs=struct.unpack_from('<IH',b);child=self.decode(program,target,depth+1);shape={'kind':'qualified','byte_size':child['byte_size'],'attributes':attrs,'target':child}
  else:raise ValueError('unsupported leaf '+hex(leaf))
  return dict(shape,type_index=ti,raw_body_sha256=digest)
def run(index,db,out):
 assert not out.exists();out.mkdir(parents=True);c=sqlite3.connect(db.resolve().as_uri()+'?mode=ro&immutable=1',uri=True);decoder=Decoder(c);d=json.loads(index.read_bytes());members={}
 for row in d['records']:
  raw=(index.parent/row['card']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['card_sha256']
  for tag in json.loads(raw)['definitions']:
   for m in tag['members']:
    if m['member_kind']=='data_member' and 'type_0x' in (m['rendered_type'] or ''):members.setdefault(m['field_member_id'],m)
 rows=[]
 for fid,m in sorted(members.items()):
  row={'field_member_id':fid,'member_name':m['member_name'],'program':m['program_id'],'type_index':m['referenced_type_index'],'previous_rendered_type':m['rendered_type'],'xbox_member_byte_offset':m['member_offset_value']}
  try:row['shape']=decoder.decode(m['program_id'],m['referenced_type_index']);row['status']='decoded'
  except (ValueError,struct.error,TypeError) as e:row['status']='held';row['reason']=str(e)
  rows.append(row)
 result={'scope':'Raw CodeView structural decoding only. Xbox byte sizes, bit positions, array counts and pointer shapes are not PC layout or native class approval.','sources':['LLVM llvmorg-20.1.8 TypeRecord.h, TypeRecordMapping.cpp, TypeIndex.h'],'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'counts':dict(collections.Counter(r['status'] for r in rows)),'shape_counts':dict(collections.Counter(r['shape']['kind'] for r in rows if r['status']=='decoded')),'rows':rows,'native_class_accepted':False,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({'counts':result['counts'],'shapes':result['shape_counts']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(R/'runtime-next/m3/out/non-ai-continuation-20261119/atlas-index/index.json',R/'runtime-next/m3/out/non-ai-benchmark-20261119/atlas/fnv-source-atlas-data-0.5.0/fnv-source-atlas.sqlite',a.out)
