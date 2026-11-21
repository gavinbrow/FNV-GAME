"""Stage protected-file payloads for narrow reviewed Phase 2 experiments, never install."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-next-source-proposals-v4';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,tescontainer_install as ti,rtti_tesform_bindings_transaction as tx,rtti_tesform_altered_paired_compare as tes,rtti_bgse_six_compare as bg
BASE=M/'out/phase2-tesform-binding-repair-v3';FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';OLD='e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576'
PROOFS={'phase2-tescontainer-651-forward-mirror/comparison-v1.json':'e925cae7e29a53be34802693fd04975cd76f56371cfe47d9828a4135894b8d23','phase2-tescontainer-980-forward-mirror/literal-analysis.json':'695d0e4a1ce42e8dfbb6830f9370bcff0803fa6e0c79b1b48e51ff77bff57b99','phase2-tescontainer-forward-probes/compile-result.json':'efcbd6d0640a55e2e787e5c9db0faeb64f068f6f4ff64e1e98302f7be85a8f00','phase2-bgs-slot21-noop-mirror/comparison-v1.json':'6984df400ff72995c8500e010ec0e191b6268a58d270ed229d01b86b6f546141','phase2-tesform-noop-mirror/whole-unit-proof.json':'3b098bfdb2fbb5906d709187f4b594f8f5b27480d4d4dbc0a8950add83a06ca5','phase2-tesform-binding-repair-v3/manifest.json':'7242e851405ec30aed816f65d1c134405f229b4458ee6ec3f4a5bca4cb327c59','phase2-tesform-noop-mirror/noop-comparison.json':'be550c84c6bd6b1bf3fdbdf1f7dcb9f812821b31514e30857750597f7949c3ef'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(path):return json.loads(path.read_text())
def exact(path,digest):
 b=path.read_bytes()
 if sha(b)!=digest:raise ValueError('digest mismatch '+path.name)
 return b
def write_payloads(out,rows):
 out.mkdir();facts=[]
 for i,(rel,new,old) in enumerate(rows):
  current=(F/rel).read_bytes()
  if sha(current)!=old:raise ValueError('protected source changed '+rel)
  (out/(str(i)+'.original')).write_bytes(current);(out/(str(i)+'.generated')).write_bytes(new)
  facts.append({'path':rel,'old_sha256':sha(current),'new_sha256':sha(new),'original':str(i)+'.original','generated':str(i)+'.generated'})
 return facts
def main():
 old=(BASE/'units.original').read_bytes();raw=(BASE/'units.generated').read_bytes();e=load(BASE/'manifest.json');tx.validate_payloads(old,raw,e)
 if sha(old)!=OLD or sha(raw)!=FA:raise ValueError('reviewed recipe transition mismatch')
 if (F/'build/units.json').read_bytes()!=raw:raise ValueError('live recipe is not exact reviewed base')
 for rel,digest in PROOFS.items():exact(M/'out'/rel,digest)
 unitdoc=json.loads(raw);units=unitdoc['units'];f651=M/'out/phase2-tescontainer-651-forward-mirror';f980=M/'out/phase2-tescontainer-980-forward-mirror';tobj=M/'out/phase2-tesform-noop-mirror';bobj=M/'out/phase2-bgs-slot21-noop-mirror'
 c651=load(f651/'comparison-v1.json');c980=load(f980/'literal-analysis.json');bp=load(bobj/'comparison-v1.json');tp=load(tobj/'whole-unit-proof.json');probes=load(M/'out/phase2-tescontainer-forward-probes/compile-result.json')
 if len(c651['functions'])!=4 or any(not x['bytes_equal'] or not x['relocations_equal'] for x in c651['functions']) or any(any(y['verdict']!='match' for y in v) for v in c651['reference'].values()) or len(c651['exception_sections']['common_exact'])!=len(c651['exception_sections']['original']) or c651['exception_sections']['original_only'] or c651['exception_sections']['candidate_only']:raise ValueError('unit651 proof incomplete')
 if len(c980['functions'])!=31 or c980['baseline_reference_matches']!=31 or c980['candidate_reference_matches']!=31 or c980['literal_changes']:raise ValueError('unit980 proof incomplete or literal changed')
 if len(probes['outcomes'])!=2 or any(x['rc'] or not x['expected_guard_context_observed'] for x in probes['outcomes']):raise ValueError('header guard probes failed')
 if len(bp['functions'])!=24 or any(not x.get('bytes_equal') or not x.get('relocations_equal') for x in bp['functions']) or any(any(y['verdict']!='match' for y in v) for v in bp['reference'].values()):raise ValueError('BGSE proof failed')
 if (tp['recipe_sha256'],tp['functions'],tp['raw_equal'],tp['normalized_relocations_equal'],tp['strict_reference_matches'])!=(FA,128,128,128,128):raise ValueError('TESForm proof failed')
 fmanifest=load(f651/'mirror-manifest.json');bmanifest=load(bobj/'mirror-manifest.json');tm=load(M/'out/phase2-tesform-noop-slots/manifest.json');bm=load(M/'out/phase2-bgsencounterzone-slot21-corrected/manifest.json')
 rowsF=[('include/TESContainer.h',(M/'out/phase2-tescontainer-forward-decls/TESContainer.h').read_bytes(),fmanifest['original_inputs']['include/TESContainer.h']),('src/fallout_shared/bgsloadedreferencecollection.cpp',(f651/'candidate/src/fallout_shared/bgsloadedreferencecollection.cpp').read_bytes(),fmanifest['original_inputs']['src/fallout_shared/bgsloadedreferencecollection.cpp'])]
 rowsC=[]
 for src,rel in [(tobj,'src/fallout_shared/tesform.cpp'),(tobj,'src/fallout_shared/tesform_TESForm.h'),(bobj,'src/bgsencounterzone.cpp'),(bobj,'src/bgsencounterzone_decls.h'),(bobj,'src/bgsencounterzone_TESForm.h')]:
  mm=load(src/'mirror-manifest.json');rowsC.append((rel,(src/'candidate'/rel).read_bytes(),mm['original_inputs'][rel]))
 tunit,norm=tes.tes_unit(units[998],tm);tunit['symbols'].update(tp['literal_bindings']);bunit,bnorm=bg.make_unit(units[2],bm)
 proof=load(tobj/'noop-comparison.json');fold=tm['proposed_noop_fold'];owners=[f for x in units for f in x['functions'] if f['address']==fold['source_address']]
 oldowners=[f for x in json.loads(old)['units'] for f in x['functions'] if f['address']==fold['source_address']]
 if proof.get('object_sha256')!=sha((tobj/'candidate.obj').read_bytes()) or proof.get('recipe_sha256')!=OLD or proof.get('identical_bodies') is not True or proof.get('size')!=11 or {x['symbol'] for x in proof.get('bodies',[])}!=set(fold['new_symbols']+[fold['source_body_symbol']]) or len(owners)!=1 or oldowners!=owners or owners[0]['symbol']!=fold['source_body_symbol']:raise ValueError('no-op fold proof missing')
 target=[x for x in tunit['functions'] if x['address']==fold['source_address']]
 if len(target)!=1 or target[0].get('fold_aliases'):raise ValueError('no-op owner already has aliases')
 target[0]['fold_aliases']=fold['new_symbols']
 for x in tm['proposed_function_symbol_changes']:
  if x['after'] in bunit['symbols'] and bunit['symbols'][x['after']]!=x['address']:raise ValueError('BGSE symbol collision')
  bunit['symbols'][x['after']]=x['address']
 pe=Pe(paths.REF_IMAGE)
 for path,unit,count in [(tobj/'candidate.obj',tunit,128),(bobj/'candidate.obj',bunit,24)]:
  r=compare(Coff(str(path)),pe,unit)
  if len(r)!=count or any(x['verdict']!='match' for x in r):raise ValueError('candidate strict code gate failed '+path.name)
 recipe=ti.replace_unit(raw,2,bunit);recipe=ti.replace_unit(recipe,998,tunit);newdoc=json.loads(recipe)
 if [i for i,(x,y) in enumerate(zip(unitdoc['units'],newdoc['units'])) if x!=y]!=[2,998]:raise ValueError('unreviewed recipe scope')
 if O.exists():raise FileExistsError('refusing overwrite')
 O.mkdir();forward=write_payloads(O/'forward',rowsF);classes=write_payloads(O/'classes',rowsC);(O/'classes/units.original').write_bytes(raw);(O/'classes/units.generated').write_bytes(recipe)
 tables=bp['class_metadata']['tables'];slots=[s for t in tables for s in t['slots']];evidence={str(p.relative_to(M)).replace('\\','/'):sha(p.read_bytes()) for p in [f651/'comparison-v1.json',f980/'literal-analysis.json',M/'out/phase2-tescontainer-forward-probes/compile-result.json',bobj/'comparison-v1.json',tobj/'whole-unit-proof.json',BASE/'manifest.json']}
 closures={}
 for label,path in [('unit651',f651),('unit980',f980),('unit998',tobj),('unit2',bobj)]:
  cp=path/'mirror-manifest.json';cm=load(cp);closures[label]={'manifest_sha256':sha(cp.read_bytes()),'original_files':cm['original']['files'],'candidate_files':cm['candidate']['files'],'original_unresolved':cm['original']['unresolved'],'candidate_unresolved':cm['candidate']['unresolved']}
 meta={'base_units_sha256':FA,'verified_transition_from':OLD,'include_closures':closures,'forward':{'files':forward,'recipe_change':False,'gates':{'unit651':4,'unit980':31,'guard_probes':2},'remaining':['all 31 functions and literal mappings must be rechecked in actual production object','full canonical image, relocations, saved controls and gameplay required']},'classes':{'files':classes,'recipe_old_sha256':FA,'recipe_new_sha256':sha(recipe),'recipe_changed_units':[2,998],'unit2_function_remaps':bm['proposed_function_symbol_changes'],'unit998_function_remaps':tm['proposed_function_symbol_changes'],'unit998_provisional_fold_aliases':fold,'unit998_mirror_literal_bindings':tp['literal_bindings'],'observed_slots_matched':sum(x['match'] for x in slots),'observed_slots_total':len(slots),'slot21':[x for x in slots if x['index']==21],'slot22':[x for x in slots if x['index']==22],'blockers':['reference slot22 remains mismatched','57 observed slot targets unresolved or wrong','no-op whole-image ICF placement not proven','mirror literal labels require actual production COFF rederivation','full global ODR unresolved; no install until these findings are resolved']},'evidence_sha256':evidence,'preserved_default_selection_sha256':'2dc3eb28083648d0d701268d8aa858a4d90fddd45e6ffb2613073cbb83672045','preserved_default_library_sha256':'da19c0a782f6ba4ac986e992daf4af7ed67c282d0b70f35e8804a22227bce645','expected_exe_sha256':'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f','status':'private snapshots only; not installed; class payload explicitly blocked pending metadata and placement proof'}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'forward_files':len(forward),'class_files':len(classes),'class_recipe_sha256':sha(recipe),'slots_matched':sum(x['match'] for x in slots),'slots_total':len(slots)}))
if __name__=='__main__':main()

