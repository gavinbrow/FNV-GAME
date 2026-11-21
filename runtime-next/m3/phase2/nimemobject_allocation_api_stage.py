"""Stage separate NiMemObject allocation API hypothesis without altering kind fix."""
import hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-nimemobject-allocation-api';S=M/'out/phase2-nirefobject-classkey-consumers.json';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';PRE='646bff1721bef044e8fa55d4827e02e26199f9e728664684934131e135f98f04';HDR='include/NiMemObject.h'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve proposal')
 raw=(F/'build/units.json').read_bytes();unit=json.loads(raw)['units'];old=(F/HDR).read_bytes();scope=json.loads(S.read_text())
 if sha(raw)!=BASE or sha(old)!=PRE or scope['recipe_sha256']!=BASE:raise ValueError('input preimage differs')
 anchor=b'  public:';nl=b'\r\n' if b'\r\n' in old else b'\n'
 if old.count(anchor)!=1 or b'operator new' in old or b'operator delete' in old:raise ValueError('class shape changed')
 inserted=anchor+nl+b'    static void* operator new(unsigned int);'+nl+b'    static void operator delete(void*, unsigned int);';new=old.replace(anchor,inserted,1);ov={HDR:new}
 rows=[]
 for i in (1484,1503):
  a=core.walk(F,unit[i]['source'],{});b=core.walk(F,unit[i]['source'],ov)
  if HDR not in a['files'] or set(a['files'])!=set(b['files']):raise ValueError('closure differs')
  rows.append({'unit':i,'source':unit[i]['source'],'functions':len(unit[i]['functions']),'eh_tails':len(unit[i].get('eh_tails',[])),'original':a,'candidate':b})
 affected=[x for x in scope['units'] if HDR in x['target_headers']]
 if len(affected)!=126:raise ValueError('consumer scope changed')
 O.mkdir();(O/'header.original').write_bytes(old);(O/'header.generated').write_bytes(new)
 for x in rows:
  i=x['unit'];d=O/str(i)
  for tag in ('original','candidate'):
   for rel,digest in x[tag]['files'].items():
    data=new if tag=='candidate' and rel==HDR else (F/rel).read_bytes()
    if sha(data)!=digest:raise ValueError('closure input changed')
    p=d/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
  mm={'schema_version':1,'source':x['source'],'units_sha256':BASE,'original_inputs':x['original']['files'],'original':x['original'],'candidate':x['candidate'],'production_include_order':['/I<mirror>/include'],'limits':['private API hypothesis, independent of the NiMemObject class-key candidate']};(d/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 m={'recipe_sha256':BASE,'header':HDR,'before_sha256':sha(old),'after_sha256':sha(new),'source_recipe_reference_owner':{'allocation':'0x00aa13e0','sized_delete':'0x00aa1460','evidence_unit':612,'reference_wrapper':'0x004968e0','object_size':8},'proposed_symbols':{'??2NiMemObject@@SAPAXI@Z':'0x00aa13e0','??3NiMemObject@@SAXPAXI@Z':'0x00aa1460'},'candidate_units':rows,'full_lexical_consumers':[x['unit'] for x in affected],'lexical_consumer_count':len(affected),'lexical_consumer_functions':sum(x['functions'] for x in affected),'lexical_consumer_eh_tails':sum(x['eh_tails'] for x in affected),'limits':['separate API hypothesis; class-key-only proposal remains untouched','operator declarations may change every active new/delete expression and emitted weak bodies','allocation owner has a guessed staging return signature; source/native identity and allocator semantics require independent proof','reference 46-byte Od deleting wrapper and candidate O2 fallback cannot be equated by name or size','all 126 lexical consumers, source-backed function/relocation/EH and actual placement gates required']}
 (O/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'fixture_units':[1484,1503],'affected_units':len(affected),'functions':m['lexical_consumer_functions'],'eh_tails':m['lexical_consumer_eh_tails']}))
if __name__=='__main__':main()
