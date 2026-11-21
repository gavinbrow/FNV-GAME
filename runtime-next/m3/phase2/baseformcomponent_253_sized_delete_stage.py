"""Prepare private unit-253 sized-delete source/recipe and production-layout mirrors."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';OUT=M/'out/phase2-bfc-253-sized-delete';sys.path.insert(0,str(H));import rtti_mirror_prepare as prep,tescontainer_install
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SOURCE='src/fallout/ai/actor.cpp';SYMBOL='??3MagicHitEffectEx@@SAXPAXI@Z'
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior outputs')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);unit=doc['units'][253]
 if sha(raw)!=BASE or unit['source']!=SOURCE or len(unit['functions'])!=807 or unit['compiler']!='sp1' or unit['symbols'].get('??2MagicHitEffectEx@@SAPAXI@Z')!='0x00aa13e0' or SYMBOL in unit['symbols']:raise ValueError('unexpected recipe')
 owner=[(i,x) for i,u in enumerate(doc['units']) for x in u['functions'] if x['address']=='0x00aa1460']
 if len(owner)!=1 or owner[0][0]!=1664 or owner[0][1]['size']!=34:raise ValueError('sized delete owner differs')
 path=F/SOURCE;old=path.read_bytes();start=old.find(b'struct MagicHitEffectEx : public HitEffectBase');end=old.find(b'\n};',start)
 if start<0 or end<0:raise ValueError('class not found')
 block=old[start:end];needle=b'    static void* operator new(unsigned int size);'
 if block.count(needle)!=1 or b'operator delete' in block or block.count(b'int unk')!=26:raise ValueError('class shape changed')
 newline=b'\r\n' if b'\r\n' in block else b'\n';new=old[:start]+block.replace(needle,needle+newline+b'    static void operator delete(void*, unsigned int);',1)+old[end:]
 candidate=copy.deepcopy(unit);candidate['symbols'][SYMBOL]='0x00aa1460';generated=tescontainer_install.replace_unit(raw,253,candidate);after=json.loads(generated)
 if [i for i,(x,y) in enumerate(zip(doc['units'],after['units'])) if x!=y]!=[253] or any(doc[k]!=after[k] for k in doc if k!='units'):raise ValueError('recipe scope')
 orig=prep.walk(F,SOURCE,{});cand=prep.walk(F,SOURCE,{SOURCE:new})
 if set(orig['files'])!=set(cand['files']):raise ValueError('closure changed')
 OUT.mkdir();(OUT/'units.original').write_bytes(raw);(OUT/'units.generated').write_bytes(generated)
 for tag,graph in [('original',orig),('candidate',cand)]:
  for rel,digest in graph['files'].items():
   data=new if tag=='candidate' and rel==SOURCE else (F/rel).read_bytes()
   if sha(data)!=digest:raise ValueError('source changed '+rel)
   q=OUT/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 meta={'schema_version':1,'source':SOURCE,'units_sha256':BASE,'unit':253,'function_count':807,'original_inputs':orig['files'],'original':orig,'candidate':cand,'overrides':{SOURCE:sha(new)},'production_include_order':['/I<mirror>/include'],'candidate_recipe_sha256':sha(generated),'proposed_symbol':SYMBOL,'proposed_target':'0x00aa1460','owner_unit':1664,'owner_source':doc['units'][1664]['source'],'owner_source_sha256':sha((F/doc['units'][1664]['source']).read_bytes()),'limits':['private candidate: layout size and compiler decorated delete symbol require object verification','all 807 functions, SG pool provenance, exception FuncInfo and ownership must pass before integration','current recipe and source remain unchanged']}
 (OUT/'mirror-manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'closure_files':len(orig['files']),'functions':807,'candidate_recipe_sha256':sha(generated)}))
if __name__=='__main__':main()
