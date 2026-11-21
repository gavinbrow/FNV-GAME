import hashlib,json,sys,os
from pathlib import Path
ROOT=Path(os.environ.get('FNV_PROJ_ROOT',r'C:\path\to\Decompilation')); M=ROOT/'runtime-next/m3'; D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'fnv_decomp/tools'));from compare import Coff
from validate_type_name_literal import validate
PIN='59fbed5c6fec9a608235dda7c58deb0b60a0af4f94c411c18bbe57d915afb595'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prepare_selector(st,sj,SEC,orig,read_ref,chunks,m3rng,object_dir):
 p=D/'rtti-descriptor-allowlist.json'
 if sha(p)!=PIN:raise ValueError('allowlist digest')
 pins=json.loads(p.read_bytes())['records'];fields=[(SEC[r[0]]['va']+r[1],r[4],r[2]) for r in sj['fields']];found=[];objects={}
 for x in pins:
  va,n=x['va'],x['size'];key=st.KEYOF[(x['unit'],x['unit_section_index'])];s=st.SEC[key];a,tier=st.placed[key]
  if a!=va or tier!='B' or s['kind']!='rtti0' or x['unit'] not in s['units']:raise ValueError('placement identity')
  op=Path(object_dir)/('%04d.obj'%x['unit']);objects[str(op)]=sha(op);obj=Coff(op);sym=obj.named(x['symbol']);sec=obj.sections[sym['section']]
  if (sym['section'],sym['value'],sym['storage'])!=(x['unit_section_index'],0,2) or bytes(sec['data'])!=bytes(s['data']):raise ValueError('actual COFF identity')
  if [(a,obj.symbols[i]['name'],k) for a,i,k in sec['relocs']]!=[(0,'??_7type_info@@6B@',6)]:raise ValueError('actual COFF reloc')
  defs=[q[0] for q in s['defs'] if q[2]==2]
  resolved,_=st.resolve(s);rr=s['relocs']
  if len(rr)!=1 or rr[0][0]!=0 or rr[0][1]!=6 or rr[0][2]!='??_7type_info@@6B@' or rr[0][6]!=0 or resolved.get(0)!=0x10f1ee0:raise ValueError('placed COFF relocation')
  fs=[f for f in fields if va-3<=f[0]<va+n]
  if any(f[0]<va<f[0]+4 or f[0]<va+n<f[0]+4 for f in fs):raise ValueError('field boundary')
  record={'va':va,'size':n,'unit':x['unit'],'kind':s['kind'],'section':'.data','tier':tier,'names':defs}
  field=validate(record,bytes(s['data']),[(0,6,'??_7type_info@@6B@',0,0x10f1ee0)],[f for f in fs if f[1]=='value-rule'],sorted(v for v in orig if va<=v<va+n),read_ref(va,n),(x['unit'],x['unit_section_index']),chunks,m3rng,[(0xfdf000,0xfdf000+1188),(0x118062c,0x118062c+6688),(0x110147c,0x110147c+24)],x)
  found.append((x,field))
 return found,objects

def finish(proven,objects,pieces,dv1_path,recipe,reference,placement):
 out=[]
 for p,f in proven:
  matches=[x for x in pieces if x['va']==p['va']]
  if len(matches)!=1:raise ValueError('candidate was not uniquely selected')
  x=matches[0]
  if (x['size'],x['unit'],x['kind'],x['names'],x['relocs'])!=(p['size'],p['unit'],'rtti0',[p['symbol']],[[0,0x10f1ee0,0]]):raise ValueError('selected candidate differs')
  out.append({'va':p['va'],'size':p['size'],'unit':p['unit'],'symbol':p['symbol'],'value_field':f})
 return {'schema':1,'removed_value_fields':sorted(x['value_field'] for x in out),'selected':out,'objects_sha256':objects,'recipe_sha256':sha(recipe),'reference_sha256':sha(reference),'dv1_pieces_sha256':dv1_path,'placement_sha256':sha(placement),'bridge_sha256':sha(__file__),'validator_sha256':sha(D/'validate_type_name_literal.py'),'allowlist_sha256':sha(D/'rtti-descriptor-allowlist.json')}


def require_epoch(env,pickle_path,recipe_path):
    import re
    for key,path in (("FNV_M3_RTTI_RECIPE_SHA256",recipe_path),("FNV_M3_RTTI_PLACEMENT_SHA256",pickle_path)):
        expected=env.get(key,"")
        if re.fullmatch(r"[0-9a-f]{64}",expected) is None or sha(path)!=expected:raise ValueError("missing or mismatched "+key)
