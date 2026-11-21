"""Package the tested unit425 adapter and independently grounded ctor binding."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-forenderedmenu-node-view';R=M/'out/phase2-forenderedmenu-node-view-mirror';C=M/'out/phase2-forenderedmenu-ctor-proof';O=M/'out/phase2-forenderedmenu-coherent-proposal'
EXPECTED='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 units=F/'build/units.json';manifest=json.loads((P/'manifest.json').read_text());mirror=json.loads((R/'mirror-manifest.json').read_text());compile=json.loads((R/'compile-result.json').read_text());proof=json.loads((C/'proof.json').read_text());nondebug=json.loads((R/'root-nondebug-review.json').read_text())
 if sha(units)!=EXPECTED or proof['recipe_sha256']!=EXPECTED or nondebug['units_sha256']!=EXPECTED:raise ValueError('recipe mismatch')
 if sha(P/'forenderedmenu.cpp')!=manifest['candidate_source_sha256'] or sha(P/'unit-overlay.json')!=manifest['unit_overlay_sha256']:raise ValueError('tested proposal changed')
 if sha(F/manifest['source'])!=manifest['original_source_sha256']:raise ValueError('live source preimage changed')
 for name,digest in mirror['original_inputs'].items():
  if sha(F/name)!=digest:raise ValueError('include closure preimage changed: '+name)
 if sha(R/'mirror-manifest.json')!=proof['mirror_manifest_sha256'] or sha(R/'compile-result.json')!=proof['compile_result_sha256']:raise ValueError('mirror evidence changed')
 if nondebug['nondebug_sections']!=105 or not nondebug['status'].startswith('PASS'):raise ValueError('nondebug review mismatch')
 rows={r['tag']:r for r in compile['outcomes']}
 for tag in ('original','candidate'):
  if rows[tag]['rc'] or not rows[tag]['trace_valid'] or sha(R/(tag+'.obj'))!=rows[tag]['object_sha256']:raise ValueError('compiled object changed')
 if sha(R/'production-baseline.obj')!=mirror['production_object_sha256']:raise ValueError('production baseline changed')
 if sha(C/'2629.obj')!=proof['owner_object_sha256'] or sha(C/'owner.cpp')!=proof['owner_source_sha256'] or sha(C/'units.json')!=EXPECTED or not proof['owner_reference_match']:raise ValueError('constructor owner proof changed')
 if any(proof['results'][t]['matches']!=44 or proof['results'][t]['eh_sections']!=37 or proof['results'][t]['eh_failed'] or proof['results'][t]['eh_errors'] for t in ('production','original','candidate')):raise ValueError('function/EH proof failed')
 unit=json.loads(units.read_bytes())['units'][425];candidate=json.loads((P/'unit-overlay.json').read_text());expected=copy.deepcopy(unit);old=manifest['symbol_change']['before'];new=manifest['symbol_change']['after'];value=expected['symbols'].pop(old);expected['symbols'][new]=value
 if candidate!=expected or value!='0x006838b0' or expected['symbols'].get('??0FUN_004391c0@@QAE@XZ') is not None:raise ValueError('unexpected prior change')
 expected['symbols']['??0FUN_004391c0@@QAE@XZ']='0x004391c0'
 if expected['functions']!=unit['functions'] or expected['flags']!=unit['flags']:raise ValueError('function/flags changed')
 O.mkdir(exist_ok=False);shutil=(P/'forenderedmenu.cpp').read_bytes();(O/'forenderedmenu.generated.cpp').write_bytes(shutil);(O/'unit425.generated.json').write_text(json.dumps(expected,indent=2),encoding='utf8')
 files={'source_preimage':sha(F/unit['source']),'source_candidate':sha(O/'forenderedmenu.generated.cpp'),'unit_payload':sha(O/'unit425.generated.json'),'recipe_preimage':sha(units),
        'proposal_manifest':sha(P/'manifest.json'),'mirror_manifest':sha(R/'mirror-manifest.json'),'compile_result':sha(R/'compile-result.json'),'nondebug_review':sha(R/'root-nondebug-review.json'),
        'constructor_proof':sha(C/'proof.json'),'owner_object':sha(C/'2629.obj'),'owner_source':sha(C/'owner.cpp'),'production_object':sha(R/'production-baseline.obj'),
        'original_object':sha(R/'original.obj'),'candidate_object':sha(R/'candidate.obj')}
 result={'status':'private combined payload; not installed','unit':425,'source':unit['source'],'input_output_sha256':files,
    'changes':[manifest['symbol_change'],{'symbol':'??0FUN_004391c0@@QAE@XZ','reference_target':'0x004391c0','basis':'captured unit2629 source owner and strict object proof'}],
    'proof':{'functions':44,'strict_matches_each_object':44,'ordinary_eh_sections_each_object':37,'ordinary_eh_failures':0,'inferred_eh_names_per_object':5,'nondebug_sections_equal':105},
    'unchanged':['44 mapped functions','compiler flags','original proposal/evidence'],
    'limitations':['five inferred sized-delete names remain separately reported','menu view is not native menu class identity','future combined transaction must validate all preimages and closure','fresh production build, metadata placement, controls and runtime required']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({'manifest_sha256':sha(O/'manifest.json'),'payload_sha256':files['unit_payload'],'source_sha256':files['source_candidate']}))
if __name__=='__main__':main()
