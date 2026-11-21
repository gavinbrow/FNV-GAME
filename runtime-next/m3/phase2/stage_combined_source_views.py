"""Stage private semantic integration; no live edits or compiler invocation."""
import copy,hashlib,json,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';T=O/'phase2-source-integration6757';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core,tescontainer_install
h=lambda b:hashlib.sha256(b).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if T.exists():raise FileExistsError(T)
 raw=(F/'build/units.json').read_bytes();base=j(F/'build/units.json');u=base['units']
 if h(raw)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('recipe changed')
 p253=O/'phase2-bfc-253-sized-delete';p370=O/'phase2-bfc-370-pointer-split';p425=O/'phase2-forenderedmenu-coherent-proposal';life=O/'phase2-bfc-2909-destructible-lifetime';owner=O/'phase2-psa-owner-transfer';forward=O/'phase2-bgs-native-header-forwarders-v2';fb=forward/'payload/forwarded'
 evidence=[p253/'mirror-manifest.json',p253/'comparison.json',p370/'manifest.json',O/'phase2-bfc-370-pointer-split-mirror/diagnostic-proof.json',p425/'manifest.json',life/'manifest.json',life/'comparison-v2.json',owner/'manifest.json',forward/'manifest.json',forward/'independent-review.json']
 for p in evidence:
  if not p.exists():raise FileNotFoundError(p)
 overlays={}
 def add(rel,p,expected=None):
  data=p.read_bytes();old=(F/rel)
  if expected and (not old.exists() or h(old.read_bytes())!=expected):raise ValueError('source preimage '+rel)
  if rel in overlays and overlays[rel]!=data:raise ValueError('conflicting payload '+rel)
  overlays[rel]=data
 m253=j(p253/'mirror-manifest.json');add('src/fallout/ai/actor.cpp',p253/'candidate/src/fallout/ai/actor.cpp',m253['original_inputs']['src/fallout/ai/actor.cpp'])
 m370=j(p370/'manifest.json');add('src/fallout/ai/middlehighprocess.cpp',p370/'middlehighprocess.cpp',m370['source_sha256'])
 m425=j(p425/'manifest.json');add('src/fallout/interface/forenderedmenu.cpp',p425/'forenderedmenu.generated.cpp',m425['input_output_sha256']['source_preimage'])
 ml=j(life/'manifest.json')
 for rel,digest in ml['mirrors']['2909']['original']['files'].items():
  if h((F/rel).read_bytes())!=digest:raise ValueError('lifetime closure '+rel)
 for rel in ('src/tesobjecttree.cpp','src/TESObjectTREE.h'):add(rel,life/'payload'/rel,ml['mirrors']['2909']['original']['files'][rel])
 for p in fb.rglob('*'):
  if p.is_file():
   rel=p.relative_to(fb).as_posix();q=F/rel
   if rel.startswith('include/') or rel.endswith('_native.h'):
    if q.exists():raise ValueError('canonical path already exists '+rel)
   add(rel,p)
 # Verify forwarder bodies are exact saved outputs of the independently compiled candidate.
 om=j(owner/'manifest.json');fm=j(forward/'manifest.json')
 if fm['tested_fixture_manifest_sha256']!=om['candidate_bgs_manifest_sha256']:raise ValueError('BGS lineage mismatch')
 for n in fm['classes']:
  if overlays['include/'+n]!=(owner/'bgs-candidate/620'/n).read_bytes() or overlays['include/'+n]!=(owner/'bgs-candidate/621'/n).read_bytes():raise ValueError('class header changed '+n)
 if b'virtual ~TESModelPSA' in overlays['include/TESModelPSA_native.h']:raise ValueError('bad explicit PSA destructor')
 generated={253:j(p253/'units.generated')['units'][253],370:j(p370/'unit-overlay.json'),425:j(p425/'unit425.generated.json'),620:j(owner/'units.generated')['units'][620],2909:j(owner/'units.generated')['units'][2909]}
 generated[370]['symbols'].update({'$SG58544':'0x010898c0','$SG27297':'0x01088220'})
 lunit=j(life/'units.generated')['units'][2909]
 if any(lunit[k]!=u[2909][k] for k in lunit if k!='symbols'):raise ValueError('lifetime changes unexpected')
 generated[2909]['symbols']=lunit['symbols']
 for i,z in generated.items():
  if any(z[k]!=u[i][k] for k in ('source','compiler','flags')):raise ValueError('compile flags changed '+str(i))
 before=Counter((x['address'],x['size']) for z in u for x in z['functions']);doc=copy.deepcopy(base)
 for i,z in generated.items():doc['units'][i]=z
 if before!=Counter((x['address'],x['size']) for z in doc['units'] for x in z['functions']):raise ValueError('global function span changed')
 new=raw
 for i,z in sorted(generated.items()):new=tescontainer_install.replace_unit(new,i,z)
 if json.loads(new)!=doc:raise ValueError('recipe encoding changed semantics')
 units=(253,370,425,620,621,2909,2910);closure={}
 for i in units:
  orig=core.walk(F,u[i]['source'],{});cand=core.walk(F,u[i]['source'],overlays);closure[str(i)]={'source':u[i]['source'],'original':orig,'candidate':cand,'functions_before':len(u[i]['functions']),'functions_after':len(doc['units'][i]['functions'])}
 T.mkdir();(T/'units.original').write_bytes(raw);(T/'units.generated').write_bytes(new)
 files={}
 for rel,data in overlays.items():
  p=T/'payload'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);q=F/rel;files[rel]={'preimage':h(q.read_bytes()) if q.exists() else None,'candidate':h(data)}
 result={'status':'PRIVATE combined hypothesis; not compiled or installed','base_recipe_sha256':h(raw),'candidate_recipe_sha256':h(new),'function_address_size_multiset_unchanged':True,'compiler_flags_unchanged':True,'changed_recipe_units':sorted(generated),'source_files':files,'closure':closure,'evidence_sha256':{str(p.relative_to(R)).replace('\\','/'):h(p.read_bytes()) for p in evidence},'limitations':['combined 2909 lifetime and PSA transfer require fresh compiler, ordinary EH and metadata checks','620/621 forwarded header resolution and implicit PSA weak/COMDAT ownership require fresh combined proof','other transitive consumers require explicit independent cohort review','unit 260, unit 258 and NiMem 750 excluded','not a whole phase or class-completion claim']}
 (T/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({'recipe':h(new),'files':len(files),'units':sorted(generated),'manifest':h((T/'manifest.json').read_bytes()),'closure_sizes':{k:len(v['candidate']['files']) for k,v in closure.items()}}))
if __name__=='__main__':main()
