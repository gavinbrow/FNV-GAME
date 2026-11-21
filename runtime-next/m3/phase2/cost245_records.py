"""Source-view Cost245 array: exact bounded fixture-backed representation."""
import os,json,struct
HEAD=0x011886a0
SYM='?DAT_011886a0@fnv_004a8bb0@@3PAUCost245@1@A'

def build_entry(r,G):
 if (r.get('va')!=HEAD or r.get('size')!=320 or r.get('align')!=4 or r.get('class_symbol')!=SYM or r.get('decl')!=[SYM] or r.get('class_namespace')!='fnv_004a8bb0' or r.get('class_name')!='Cost245' or r.get('count')!=16):raise ValueError('invalid Cost245 source identity')
 a=HEAD;b=a+320
 if G.sec_of(a)!='.data' or a%4:raise ValueError('invalid Cost245 destination')
 with open(os.path.join(G.RN,'data-v3','symbolic.json')) as f:sj=json.load(f)
 fields={G.SEC[x[0]]['va']+x[1] for x in sj['fields']}|G.ORIG_SET
 allowed={a+20*i+4*j for i in range(16) for j in range(1,5)}
 if any(x<a<x+4 or x<b<x+4 for x in fields) or any(x not in G.ORIG_SET or x not in allowed for x in fields if a<=x<b):raise ValueError('unsupported Cost245 field')
 with open(os.path.join(G.RN,'data-v3','out','manifest.json')) as f:chunks=json.load(f)
 if not any(x['section']=='.data' and x['va']<=a and b<=x['va']+x['size'] for x in chunks):raise ValueError('Cost245 crosses chunk')
 raw=G.refbytes(a,320)
 if len(raw)!=320:raise ValueError('short Cost245 bytes')
 cells=[];rel=[];targets=[]
 for i in range(16):
  off=20*i
  if raw[off] not in (0,1) or raw[off+1:off+4]!=b'\0\0\0':raise ValueError('Cost245 bool/padding mismatch')
  cells.append(('b',bool(raw[off])))
  for j in range(1,5):
   p=off+4*j;v=struct.unpack_from('<I',raw,p)[0]
   if a+p in G.ORIG_SET:
    section=G.sec_of(v);d=G.SEC['.data'];bss=d['va']+d['raw']<=v<d['va']+d['vs']
    if section not in ('.text','.data','.rdata','CONST','.tls') and not bss:raise ValueError('Cost245 target outside image')
    cells.append(('p',v));rel.append([p,'',0]);targets.append(v)
   else:cells.append(('i',v))
 if len(rel)!=58:raise ValueError('unexpected Cost245 relocation count')
 return dict(sym=SYM,name='DAT_011886a0',ns='fnv_004a8bb0',va=a,size=320,type='Cost245',tc='Y',section='.data',align=4,ref=raw.hex(),kind='source-view-Cost245',elems=cells,fields=rel,tgts=targets,count=16)

def render_entry(e,ext,G):
 rows=[]
 for i in range(16):
  cells=[]
  for item in e['elems'][i*5:(i+1)*5]:
   if item[0]=='b':cells.append('true' if item[1] else 'false')
   elif item[0]=='i':cells.append('0x%08xu'%item[1])
   else:
    v=item[1];code=G.TLO<=v<G.THI;k='M3F' if code else 'M3D'
    ext[v]=('extern "C" void %s_%08x(void);' if code else 'extern "C" char %s_%08x;')%(k,v);cells.append('(int)&%s_%08x'%(k,v))
  rows.append('{%s}'%', '.join(cells))
 definition='namespace fnv_004a8bb0 { Cost245 DAT_011886a0[16] = {\n'+',\n'.join(rows)+'\n}; }'
 return definition

STRUCT='namespace fnv_004a8bb0 { struct Cost245 { bool disabled; int unk04,unk08,unk0c,unk10; }; typedef char M3CostSize[(sizeof(Cost245)==20 && offsetof(Cost245,disabled)==0 && offsetof(Cost245,unk04)==4 && offsetof(Cost245,unk08)==8 && offsetof(Cost245,unk0c)==12 && offsetof(Cost245,unk10)==16)?1:-1]; }'
