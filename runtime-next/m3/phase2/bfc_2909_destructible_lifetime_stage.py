"""Stage private TESObjectTREE destructible-base lifetime correction."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-bfc-2909-destructible-lifetime';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core,tescontainer_install
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SRC='src/tesobjecttree.cpp';HDR='src/TESObjectTREE.h';SYM='??1BGSDestructibleObjectForm@@QAE@XZ'
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior outputs')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);unit=doc['units'][2909]
 if sha(raw)!=BASE or unit['source']!=SRC or len(unit['functions'])!=45 or unit['symbols'].get('??0BGSDestructibleObjectForm@@QAE@XZ')!='0x00475350' or SYM in unit['symbols']:raise ValueError('input recipe differs')
 data=(F/SRC).read_bytes();text=data.decode('utf-8-sig');nl='\r\n' if '\r\n' in text else '\n';block=('struct DestructibleTail\n{\n    ~DestructibleTail();\n};\n').replace('\n',nl);base=(',\n                      public DestructibleTail').replace('\n',nl)
 if text.count(block)!=1 or text.count(base)!=1 or text.count('DestructibleTail')!=3:raise ValueError('surrogate identity differs')
 newtext=text.replace(block,'',1).replace(base,'',1);h=(F/HDR).read_bytes();ht=h.decode('utf-8-sig');hn='\r\n' if '\r\n' in ht else '\n';needle=('class BGSDestructibleObjectForm : public BaseFormComponent\n{\n  public:\n').replace('\n',hn)
 if ht.count(needle)!=1:raise ValueError('header class differs')
 newhdr=ht.replace(needle,needle+'    ~BGSDestructibleObjectForm();'+hn,1);overrides={SRC:newtext.encode(),HDR:newhdr.encode()}
 candidate=copy.deepcopy(unit);candidate['symbols'][SYM]='0x00475380';newrecipe=tescontainer_install.replace_unit(raw,2909,candidate);changed=json.loads(newrecipe)
 if [i for i,(a,b) in enumerate(zip(doc['units'],changed['units'])) if a!=b]!=[2909] or any(doc[k]!=changed[k] for k in doc if k!='units'):raise ValueError('recipe scope differs')
 mirrors={}
 for i in (2909,2910):
  u=doc['units'][i];a=core.walk(F,u['source'],{});b=core.walk(F,u['source'],overrides)
  if set(a['files'])!=set(b['files']):raise ValueError('include graph differs')
  mirrors[str(i)]={'source':u['source'],'original':a,'candidate':b,'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[]))}
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(newrecipe)
 for rel,d in overrides.items():
  p=O/'payload'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d)
 for i,m in mirrors.items():
  for tag in ('original','candidate'):
   for rel,digest in m[tag]['files'].items():
    d=overrides[rel] if tag=='candidate' and rel in overrides else (F/rel).read_bytes()
    if sha(d)!=digest:raise ValueError('closure changed '+rel)
    p=O/i/tag/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d)
  mm={'schema_version':1,'source':m['source'],'units_sha256':BASE,'original_inputs':m['original']['files'],'original':m['original'],'candidate':m['candidate'],'production_include_order':['/I<mirror>/include'],'limits':['private lifetime hypothesis; no source or recipe integration']};(O/i/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(newrecipe),'source_files':{k:sha(v) for k,v in overrides.items()},'unit':2909,'affected_units':[2909,2910],'function_count':[45,1],'recipe_eh_tails':[5,0],'target_function':'0x0051b6e0','reference_parent_construction_offset':'0x54','reference_cleanup':'0x00ef4a8e','reference_cleanup_target':'0x00475380','original_surrogate_cleanup_offset':'0x5c','hypothesis':'replace spurious empty base destructor with destructor of the actual BGSDestructibleObjectForm base','mirrors':mirrors,'limits':['private hypothesis uncompiled; no live changes','verify all function bytes/relocations, RTTI base graph and all EH actions, pack/layout and original cleanup','the separate native PSA owner transfer requires independently recombined proof']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'units':[2909,2910],'functions':46,'candidate_recipe_sha256':sha(newrecipe)}))
if __name__=='__main__':main()
