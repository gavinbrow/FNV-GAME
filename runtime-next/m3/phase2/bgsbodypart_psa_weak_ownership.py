"""Finite private PSA weak-fallback ownership evidence; never resolves a link."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-bgsbodypart-split-headers-proposal';OUT=O/'psa-weak-ownership.json'
sys.path[:0]=[str(H),str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
PRIMARY='??_ETESModelPSA@@UAEPAXI@Z';FALLBACK='??_GTESModelPSA@@UAEPAXI@Z';DTOR='??1TESModelPSA@@UAE@XZ'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 unitsfile=F/'build/units.json';units=json.loads(unitsfile.read_bytes())['units'];obj=O/'0620.mirror.obj';owner=M/'out/phase2-bfc-cohort-production-archive/2909.obj';c=Coff(str(obj));oc=Coff(str(owner))
 compiled=json.loads((O/'lane-compile.json').read_text());row=next(x for x in compiled['outcomes'] if x['unit']==620 and x['tag']=='mirror')
 if row['rc'] or row['object_sha256']!=sha(obj):raise ValueError('candidate compiler evidence changed')
 weak=[(i,x) for i,x in c.symbols.items() if x['name']==PRIMARY and x['storage']==105]
 if len(weak)!=1:raise ValueError('weak primary ambiguous')
 symptr=struct.unpack_from('<I',c.data,8)[0];idx,kind=struct.unpack_from('<II',c.data,symptr+18*(weak[0][0]+1))
 if kind!=2 or c.symbols[idx]['name']!=FALLBACK:raise ValueError('weak fallback mismatch')
 defs=[x for x in c.by_name.get(FALLBACK,[]) if x['section']>0 and x['storage']==2]
 if len(defs)!=1:raise ValueError('fallback definition ambiguous')
 occupied=[]
 for va,size in ((0x5e3c30,44),(0x51b950,19)):
  hits=[{'unit':i,'symbol':f['symbol'],'address':f['address'],'size':f['size']} for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<va+size and va<int(f['address'],16)+f['size']]
  occupied.append({'address':hex(va),'size':size,'owners':hits})
 if len(occupied[0]['owners'])!=1 or occupied[0]['owners'][0]['unit']!=620 or len(occupied[1]['owners'])!=1 or occupied[1]['owners'][0]['unit']!=2909:raise ValueError('source placement owner ambiguity')
 old='?FUN_005e3c30@BGSTextureModel@@QAEPAXI@Z';source='?FUN_0051b950@FUN_0051b950_shell@@QAEXXZ'
 a,ar=relocated(c,FALLBACK,44,{DTOR:'??1BGSTextureModel@@UAE@XZ'});b,br=relocated(c,old,44,{})
 if a!=b or ar!=br:raise ValueError('wrapper body/relocations differ')
 a,ar=relocated(c,DTOR,19,{'??1TESModel@@UAE@XZ':'??1TESModel@@QAE@XZ'});b,br=relocated(oc,source,19,{})
 if a!=b or ar!=br:raise ValueError('implicit destructor differs from source owner')
 spec=copy.deepcopy(units[620]);spec['functions']=[dict(next(f for f in units[620]['functions'] if f['address']=='0x005e3c30'),symbol=FALLBACK)];spec['symbols'][DTOR]='0x0051b950';r=compare(c,Pe(paths.REF_IMAGE),spec)
 if len(r)!=1 or r[0]['verdict']!='match':raise ValueError('fallback reference mismatch')
 recipe_bindings=[]
 for i,u in enumerate(units):
  for name in (PRIMARY,FALLBACK,DTOR):
   if name in u['symbols']:recipe_bindings.append((i,name,u['symbols'][name]))
   for f in u['functions']:
    if name==f['symbol'] or name in f.get('fold_aliases',[]):recipe_bindings.append((i,name,f['address']))
 if recipe_bindings:raise ValueError('unexpected existing native binding')
 icf=RN/'build-v7/icf_map.json';overlay=RN/'reloc-v7/binding_overlay.json';imap=json.loads(icf.read_bytes());ov=json.loads(overlay.read_bytes());field=0x104541c
 namespace={'icf':imap.get(PRIMARY),'global_name':ov['global_name'].get(PRIMARY),'unit_names':[(k,v[PRIMARY]) for k,v in ov['by_unit_name'].items() if PRIMARY in v],'field_overrides':[(k,v) for k,v in ov['by_field'].items() if int(k,16)==field]}
 if any(namespace.values()):raise ValueError('active lookup override')
 provider=M/'out/phase2-vtable-provider-closure.json';prov=json.loads(provider.read_bytes());strong=prov.get('strong_definitions',{}).get(PRIMARY)
 if strong is None:raise ValueError('primary absent from provider query')
 report={'scope':'finite private candidate evidence; not a live linker resolution','candidate_object_sha256':sha(obj),'candidate_compile_sha256':sha(O/'lane-compile.json'),
   'owner_2909_object_sha256':sha(owner),'units_sha256':sha(unitsfile),'source_hashes':{str(p.relative_to(F)):sha(p) for p in (F/'src/fallout_shared/bgsbodypart.cpp',F/'src/tesobjecttree.cpp')},
   'primary':PRIMARY,'fallback':FALLBACK,'weak_characteristics':kind,'fallback_definition_count':len(defs),'wrapper_equal_to_source_owner':True,'implicit_dtor_equal_to_unit2909_source_owner':True,'strict_wrapper_reference_match':True,
   'recipe_owners':occupied,'native_recipe_bindings':recipe_bindings,'field_va':hex(field),'current_icf_sha256':sha(icf),'current_overlay_sha256':sha(overlay),'current_namespace':namespace,'v7_reloc_log_sha256':sha(RN/'build-v7/relocs_v7.tsv.gz'),
   'provider_snapshot_sha256':sha(provider),'provider_snapshot_recipe_hashes':prov.get('manifests_sha256',{}),'provider_primary_strong':strong,'provider_missing':len(prov.get('missing',[])),
   'limitations':['provider closure uses older d569 recipe and does not include this candidate as final production input','1087 contribution objects missing in provider snapshot; serialized V7 contribution treatment must be verified','candidate vtable not yet placed; current placed/global and V7 symbol namespaces must be freshly audited after production build','no generic SEARCH_LIBRARY behavior or binding activated','full native destructor fixture and final source/RTTI/EH ownership not yet accepted']}
 OUT.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'candidate':sha(obj),'wrapper_and_dtor':True,'provider_primary_strong':strong,'output':str(OUT)}))
if __name__=='__main__':main()
