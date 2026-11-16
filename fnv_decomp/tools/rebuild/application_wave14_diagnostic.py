"""Private V14 composition core; caller must authenticate all inputs and modules.

This pure core is not an operational entry, and its injectable module seam is
only for authored fixtures. A future public wrapper must bind fixed source and
inputs, capture its own watchdog/lease authority and preserve stable bindings.
"""
import copy
import json


def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',', ':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def _require(ok, message):
    if not ok: raise ValueError(message)


def _compose(*, report, old_fields, observation, fields, uuid_evidence, old_providers,
             noncode_definitions, code21_providers, prior_iat, current_iat, iat_rows, prior_crt,
             crt_bytes, crt_validation, baseline_response, fresh_identity, paths, modules, expected):
    """Compose checked records; never authenticate a caller's data or authorize IO."""
    _require(set(modules)=={'cohort','uuid','crt','response'},'fixed module set required')
    _require(type(old_fields) is list and type(fields) is list and
             len(old_fields)==expected['old_fields'] and len(fields)==expected['fields'] and
             _canonical(fields[:len(old_fields)])==_canonical(old_fields), 'old fields changed')
    _require(type(code21_providers) is list and len(code21_providers)==expected['batch_providers'] and
             len(old_providers)==expected['old_providers'], 'provider census differs')
    qualified=modules['uuid'].consume(uuid_evidence)
    _require(len(qualified['providers'])==1 and len(qualified['mapped_fields'])==9 and
             qualified['base_closure_observed'] is False and qualified['full_serialization_eligible'] is False and
             all(qualified[k] is False for k in ('provider_selected','runtime_eligible','ABI_verified',
                                                  'link_ready','UUID_selected_or_loaded')),
             'UUID negative or provider scope differs')
    _require(_canonical(fields[-9:])==_canonical(qualified['mapped_fields']), 'UUID normative fields differ')
    namespace=modules['cohort'].disjoint_providers([code21_providers,qualified['providers']],
                 baseline_providers=old_providers,existing_noncode_definitions=noncode_definitions)
    _require(_canonical(namespace)==_canonical(observation['provider_namespace']) and
             namespace['physical_owners']==namespace['original_addresses']==expected['providers'],
             'complete provider namespace differs')
    gate=modules['crt'].validate(crt_bytes['plan'],crt_bytes['review'],crt_bytes['response'],fields,namespace['symbols'])
    _require(_canonical(gate)==_canonical(crt_validation),'complete CRT consumer validation differs')
    _require(gate['inherited_tokens_to_remove']==prior_crt,'inherited CRT aliases differ')
    _require(type(current_iat) is list and len(set(current_iat))==len(current_iat) and
             set(current_iat).issubset(set(prior_iat)), 'IAT aliases differ')
    output=modules['response'].transform(baseline_response,old_out=paths['old_out'],new_out=paths['new_out'],
        batch_archive=paths['batch_archive'],uuid_archive=paths['uuid_archive'],prior_iat=prior_iat,
        prior_crt=prior_crt,current_iat=current_iat,current_crt=gate['tokens'],
        fresh_uuid_identity=fresh_identity,qualified_uuid=qualified)
    result=copy.deepcopy(report)
    for provider in code21_providers+qualified['providers']:
        result['provenance'].setdefault(provider['canonical'],[]).append(copy.deepcopy(provider))
    for field in fields[len(old_fields):]:
        result['provenance'].setdefault(field['canonical'],[]).append(copy.deepcopy(field))
    result['selected_supplementary_providers'].extend(copy.deepcopy(code21_providers+qualified['providers']))
    result.update(kind='fixed-V14-combined-diagnostic',status='prepared-no-native-LINK',
        selected_game_function_provider_count=expected['providers'],ordinary_prepared_count=14550,
        full_included_field_count=len(fields),wave14_namespace=copy.deepcopy(namespace),
        CRT_diagnostic_bindings=copy.deepcopy(gate),aliases=copy.deepcopy(iat_rows),
        command=[report['command'][0], '@'+str(Path(paths['new_out'])/'link.rsp')],
        uuid_source_evidence=copy.deepcopy(qualified),
        response_sha256=output['response_sha256'],native_LINK_performed=False,executable_execution=False,
        runtime_eligible=False,provider_adopted=False,provider_selected=False,link_ready=False)
    return result,output


def _iat_gate(*, old, producer, annotations, native, request, request_sha256, parsed,
              originals, expected_sources, fields, catalog, libraries, library_refs, prior_iat):
    """Replay authenticated fixed native evidence and complete current census.

    The future fixed wrapper authenticates inputs and the physical libraries;
    this private seam must not be exported as an authority-bearing API.
    """
    reconciled=old.native_evidence(native,request,request_sha256,parsed,producer,originals,expected_sources)
    native_rows=[reconciled['library']]+reconciled['unchanged_libraries']
    _require(len(native_rows)==4 and {row['file'] for row in native_rows}==set(libraries)==set(library_refs) and
             all(library_refs[row['file']]=={'sha256':row['sha256'],'bytes':row['bytes']} for row in native_rows),
             'selected import library provenance differs')
    rows=old.joins.import34_alias_census(reconciled['proposed_pointer_aliases'],
        annotations.census_view(fields,catalog),catalog,libraries)
    _require(type(rows) is list and len(rows)==34 and type(prior_iat) is list and len(prior_iat)==34,
             'exact inherited IAT scope required')
    proposals=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in rows]
    _require(len(set(proposals))==34 and set(proposals)==set(prior_iat),'changed IAT proposals')
    enriched=[]
    for row in rows:
        item=copy.deepcopy(row)
        item['evaluation_view_sha256']=hashlib.sha256(_canonical(row['complete_actual_uses'])).hexdigest()
        actual=[copy.deepcopy(field) for field in fields if field['canonical']==row['canonical']]
        _require(type(row['use_count']) is int and len(actual)==row['use_count'] and
                 type(row['enabled']) is bool,'IAT current full-field census differs')
        item['complete_actual_uses']=actual;item['compact_proofs_preserved']=True
        enriched.append(item)
    return enriched,[proposal for proposal,row in zip(proposals,rows) if row['enabled']]

# Private guard draft copied/adapted from the independently reviewed observer;
# fixed authority, paths and review are separate for the new operation.
from datetime import datetime, timezone, timedelta
import hashlib
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
WATCHDOG_STARTED_PATH='build/rebuild/application-wave14-prepare-control-v2/started.json'
LEASE_LOCK_PATH='build/rebuild/application-frontier-dispatch-v1/resource-leases.lock'
LEASE_REGISTRY_PATH='build/rebuild/application-frontier-dispatch-v1/resource-leases.json'
EXPECTED_INTERPRETER={'requested_path':r'C:\Python312\python.exe','path':r'C:\Python312\python.exe',
 'sha256':'4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a',
 'size':104952,'device':11251121510599050284,'inode':112871465661098146}
require=_require
def bounded_json(data,limit):
    require(type(data) is bytes and len(data)<=limit,'bounded JSON required')
    return json.loads(data)

def _watchdog_started(review,source_sha,inputs_sha,review_sha,request_sha,psutil_module):
    """Require the actual watchdog-created child, never a detached invocation."""
    path=ROOT/WATCHDOG_STARTED_PATH
    with path.open('rb') as stream:data=stream.read(65537)
    require(len(data)<=65536,'watchdog child record too large');record=bounded_json(data,65536)
    require(type(record) is dict and set(record)=={'kind','child','pins','slot','handshake_nonce'} and
       record['kind']=='wave14-prepare-watchdog-child-started' and type(record['slot']) is int and record['slot'] in (1,2),
       'watchdog child record schema differs')
    nonce=record['handshake_nonce']
    require(type(nonce) is str and re.fullmatch('[0-9a-f]{64}',nonce) and
            os.environ.get('FNV_WAVE14_PREPARE_HANDSHAKE_NONCE')==nonce,'watchdog handshake nonce differs')
    child=record['child'];pins=record['pins'];current=psutil_module.Process()
    require(type(child) is dict and set(child)=={'pid','parent_pid','create_time','executable'} and
       type(child['pid']) is int and type(child['parent_pid']) is int and type(child['create_time']) is float and
       child['pid']==os.getpid()==current.pid and child['parent_pid']==os.getppid()==current.ppid() and
       child['create_time']==current.create_time() and child['executable']==current.exe()==EXPECTED_INTERPRETER['path'],
       'watchdog child physical identity differs')
    expected={'request':request_sha,'source':source_sha,'source_tests':review['tests_sha256'],
       'watchdog_tests':review['watchdog_tests_sha256'],'inputs':inputs_sha,'review':review_sha,
       'watchdog':review['watchdog_sha256'],'interpreter':EXPECTED_INTERPRETER['sha256']}
    require(type(pins) is dict and pins==expected,'watchdog started pins differ')
    return record,hashlib.sha256(data).hexdigest()


def _active_lease(slot,request_sha,source_sha,review_sha):
    """Read the docs-owned lease atomically around its cooperative lock."""
    lock=ROOT/LEASE_LOCK_PATH;registry=ROOT/LEASE_REGISTRY_PATH
    require(not lock.exists(),'lease registry locked')
    with registry.open('rb') as stream:data=stream.read(4*1024*1024+1)
    require(len(data)<=4*1024*1024 and not lock.exists(),'lease registry read unsafe')
    state=bounded_json(data,4*1024*1024);require(state.get('schema_version')==1,'lease registry schema')
    pins={'application-wave14-prepare-request-v2.json':request_sha,'application_wave14_diagnostic.py':source_sha,
       'application-wave14-prepare-independent-review-v2.json':review_sha}
    rows=[r for r in state.get('leases',[]) if r.get('owner')=='/root/rebuild_startup_host' and
          r.get('resource')=='lightweight_metadata' and r.get('state') in ('granted','running') and
          r.get('review_sha256')==review_sha and r.get('input_pins')==pins]
    require(len(rows)==1 and rows[0].get('slot')==slot,'unique matching active metadata lease required');r=rows[0]
    require(type(r.get('slot')) is int and type(r.get('max_seconds')) is int and r['max_seconds']>0,'lease identity differs')
    granted=datetime.fromisoformat(r['granted_utc'].replace('Z','+00:00'))
    require(granted.tzinfo is not None and granted.utcoffset()==timedelta(0),'lease UTC required')
    now=datetime.now(timezone.utc);require(granted<=now<granted+timedelta(seconds=r['max_seconds']),'lease not live')
    return (r['owner'],r['resource'],r['slot'],r['granted_utc'],r['max_seconds'],request_sha,source_sha,review_sha)


OUTPUT_PATH='build/rebuild/application-link-diagnostic-v14-combined'
MAX_OUTPUT_BYTES=128*1024*1024

def _publish_private(*, out, report, response, bindings, guard, stable_utility, stable_fn, start, clock):
    """Private fixture seam; fixed production entry must bind real guard/delegate.

    Each call to stable_phase constructs a fresh exact-record selection. This
    reduces duplicate observations *within* a phase, not across phases.
    """
    _require(Path(out)==ROOT/OUTPUT_PATH and not Path(out).exists(),'exclusive fixed output required')
    _require(type(response) is bytes and 0<len(response)<=MAX_OUTPUT_BYTES,'response size differs')
    _require(callable(guard) and callable(stable_fn),'runtime guard and stability checker required')
    checks=[]
    def phase(label,phase_name):
        _require(clock()-start<480,'time budget exceeded')
        guard()
        facts=stable_utility.stable_phase(bindings,phase=phase_name,stable_fn=stable_fn)
        guard();checks.append({'stage':label,'selection':facts})
    phase('before-publication','pre')
    result=copy.deepcopy(report)
    result['input_bindings']=copy.deepcopy(bindings)
    result['response_sha256']=hashlib.sha256(response).hexdigest()
    result['stability_policy']={'exact_unique_records_within_each_phase':True,
       'reduced_within_phase_observations':True,'cross_phase_cache_used':False,
       'full_input_binding_ledger_preserved':True,'no_unconditional_equivalence_claim':True}
    content=_canonical(result)+b'\n'
    _require(len(content)+len(response)<=MAX_OUTPUT_BYTES,'aggregate output cap')
    out=Path(out);out.mkdir(exist_ok=False)
    for name,data in (('link.rsp',response),('receipt.json',content)):
        phase('before-'+name,'post')
        with (out/name).open('xb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        _require((out/name).read_bytes()==data,'output post-read differs')
        phase('after-'+name,'post')
    phase('after-publication','post')
    return result,checks


def _baseline_namespace(report, old_observation, diagnostic, cohort, expected_count):
    """Reconstruct provider records from the complete saved V13 provenance."""
    baseline=[copy.deepcopy(row) for group in report['provenance'].values() for row in group
              if row.get('component')=='current-CODE-definition']
    baseline.extend(copy.deepcopy(report['selected_supplementary_providers']))
    baseline.append(dict(component='actual-entry',member='application-entry.lib',
        canonical=diagnostic.partial.CANONICAL,recipe_id=diagnostic.partial.IDENTITY['recipe_id'],
        object_sha256=diagnostic.partial.IDENTITY['object_sha256'],
        symbol_index=diagnostic.partial.IDENTITY['symbol_index'],original_address='0x0086a850'))
    _require(len(baseline)==expected_count,'baseline provider census differs')
    noncode=[name for name,kind in old_observation['provider_namespace']['symbols'].items()
             if kind=='existing-noncode']
    actual=cohort.disjoint_providers([],baseline_providers=baseline,existing_noncode_definitions=noncode)
    _require(_canonical(actual)==_canonical(old_observation['provider_namespace']),
             'baseline namespace differs')
    return baseline,noncode


def _validate_observation(receipt, old_fields, fields, diagnostic):
    """Validate receipt/field relationships after fixed raw hashes and peer review."""
    _require(receipt.get('kind')=='wave14-CODE21-UUID-field-observation' and
      receipt.get('status')=='observed-not-adopted' and receipt.get('complete_field_count')==46292 and
      receipt.get('selected_Game_function_candidates')==14555 and receipt.get('ordinary_prepared_count')==14550 and
      receipt.get('baseline_field_count')==46237 and receipt.get('code21_field_count')==46 and
      receipt.get('uuid_field_count')==9 and len(old_fields)==46237 and len(fields)==46292,
      'combined observer scope differs')
    _require(_canonical(fields[:46237])==_canonical(old_fields) and
      hashlib.sha256(_canonical(old_fields)).hexdigest()==receipt['baseline_ordered_digest'],
      'ordered baseline fields differ')
    ordered=sorted(fields,key=diagnostic.canonical)
    _require(diagnostic.digest(diagnostic.canonical(ordered))==receipt['fields_canonical_sha256']==
        '08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4',
        'combined canonical field hash differs')
    _require(receipt['uuid_base_closure_observed'] is False and receipt['uuid_full_serialization_eligible'] is False and
      all(receipt[k] is False for k in ('source_ABI_verified','provider_selected','runtime_eligible','link_ready',
       'application_cohort_adopted','native_tools_run','executable_link_performed','game_execution_performed')),
      'observer promotion or UUID negative differs')
    _require(len(receipt['providers'])==22 and len(receipt['uuid_original_negative_occurrences'])==3,
             'observer provider or UUID negative occurrence scope differs')
    quarantines=receipt['producer_prior_quarantines']
    _require(type(quarantines) is list and len(quarantines)==6 and set(quarantines)==
        {'0x00452580','0x004e6370','0x004e6620','0x0086beb0','0x0086ff70','0x009781d0'} and
        receipt['producer_new_blocked']==[], 'prior quarantines or new terminal outcome differs')


# Loader draft: the final approved source graph/order must be filled before use.
import importlib.util
import importlib.machinery
import sys
import types
# Fixed source inventory; changes require a new independently reviewed packet.
SOURCE_PINS={'application_link_diagnostic': {'path': 'tools/rebuild/application_link_diagnostic.py', 'sha256': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379'}, 'application_link_cohort': {'path': 'tools/rebuild/application_link_cohort.py', 'sha256': 'a5feab657f68e7e0e0243250128d477358311d36dc10c23c5d71c88e0959ee32'}, 'application_link_frontier': {'path': 'tools/rebuild/application_link_frontier.py', 'sha256': 'b371e8eab1c7928395b990a8a5507d9a68c630e68b02d23247ee73ef79439d7c'}, 'application_import34_diagnostic': {'path': 'tools/rebuild/application_import34_diagnostic.py', 'sha256': '25a856c6417e073fc1b8f9681c112f45071bd3c20841b2e055823b6a4ec8bbe6'}, 'import_kernel32_fifteen': {'path': 'tools/rebuild/import_kernel32_fifteen.py', 'sha256': '57828dc1894e3fe5001cc14ad1aafb0f99d4043d41ce63df05e9bf76edd81d1f'}, 'application_uuid2768': {'path': 'tools/rebuild/application_uuid2768.py', 'sha256': 'e04ec719cb4bf1fdc921b409ac510c85a1cd51255a5b165db9b820868814919a'}, 'application_combined_response': {'path': 'tools/rebuild/application_combined_response.py', 'sha256': '25b508d86b9cc48ffe8182c3ed35fe5e3ff2097b3fb96dcd90625eeac9a68f30'}, 'iat_code21_annotations': {'path': 'tools/rebuild/iat_code21_annotations.py', 'sha256': '444ae281373f3a708ea6a31deb91b7be346fa9a0306dd8b6da390e449e32bfe5'}, 'crt_v14_four_alias_contract': {'path': 'tools/rebuild/crt_v14_four_alias_contract.py', 'sha256': 'bd32c25a2e17cfaf04a642ab866b29896a0ebb00b21dfb8dfad4d40dbb38ddc2'}, 'exact_binding_stability': {'path': 'tools/rebuild/exact_binding_stability.py', 'sha256': 'cac9a4b2c163daa6c4b7d45a66f7bfb3eee4917e6e95cfc26507108415a59308'}, 'application_link_inputs': {'path': 'tools/rebuild/application_link_inputs.py', 'sha256': 'e1669081b88f43144f71c3a48f9bd2ff159f9be33a2c16052c6fbd850cfafd8f'}, 'coff_code_archive': {'path': 'tools/rebuild/coff_code_archive.py', 'sha256': '76244d2d4dca4c1f8aa72224be1ef5c92f68976b5cda7d31b5cfe23d3cc29e64'}, 'toolchain': {'path': 'tools/rebuild/toolchain.py', 'sha256': '9cb837b0a11d9e5fa8db98dbf195b3d54b1cfeebed7d7531f97a0e29d03436fd'}, 'application_wave10_diagnostic': {'path': 'tools/rebuild/application_wave10_diagnostic.py', 'sha256': 'd3a4b5ac465ed38ce5bbbd6e2ef67f41a3c53847dade2bdc348201ce5e67d308'}, 'application_import34_inputs': {'path': 'tools/rebuild/application_import34_inputs.py', 'sha256': '67a6b3940e7a0949492b30a7a7cc881a9b83eb61654cb90e4fce8951696efa87'}, 'normal_import_archive': {'path': 'tools/rebuild/normal_import_archive.py', 'sha256': '42a0eff5852d89aaadb1f239baf3884e7a2dcd4216870407d7e8510a6d68bf28'}, 'iat_code68_annotations': {'path': 'tools/rebuild/iat_code68_annotations.py', 'sha256': '199e3d51b1ce2eb0e64cb1f780b81c2231cbd8b91a5fdc0460d196b07d7beed9'}, 'crt_v10_four_alias_contract': {'path': 'tools/rebuild/crt_v10_four_alias_contract.py', 'sha256': '09b0dfcdd59fb2834dd2b798a70dbddb88641630c6003b5ccf690fdd49f6570d'}, 'assess_v10_imports': {'path': 'tools/rebuild/assess_v10_imports.py', 'sha256': 'fe148aafdcd4af8dca5b89b2815df8acebbbc7832fbacdde6aa68b63d48a2a68'}, 'import_projection': {'path': 'tools/rebuild/import_projection.py', 'sha256': 'b13a2e805950ff4dc79fdaa1a8d12b00bb8a9c171853d77180ddb069857df865'}, 'import_kernel32_extension': {'path': 'tools/rebuild/import_kernel32_extension.py', 'sha256': '15177c10e9b6469e0abab5c54e0ec6ef18afb9829cc275bef831795e9f358307'}, 'iat_field_annotations': {'path': 'tools/rebuild/iat_field_annotations.py', 'sha256': '5ce0b3ae5069cde206b334bddc94515b308e611ef1cc269783cbd386fd778ae6'}, 'iat_code56_annotations': {'path': 'tools/rebuild/iat_code56_annotations.py', 'sha256': '67109cc15e51801ff2a18c2f169abbbede77417eb43af79d6093b3ef0cb485e9'}, 'crt_v13_four_alias_contract': {'path': 'tools/rebuild/crt_v13_four_alias_contract.py', 'sha256': '9f38865f6389bb70876a45f7a1066873663024bf21f4a737984f77f8b17bca26'}, 'crt_v14_four_alias_plan': {'path': 'tools/rebuild/crt_v14_four_alias_plan.py', 'sha256': 'ba3f7b56c677d14376d7ed27a5423db9aa95ac7aefdc7a54c88c3cf8ed443b41'}, 'coff_inventory': {'path': 'tools/rebuild/coff_inventory.py', 'sha256': '3518c044738046e7cd9c8be37a3b1077af750fb2e7a19db793b09999a07ee0d2'}, 'game_startup_host': {'path': 'tools/rebuild/game_startup_host.py', 'sha256': 'ef32b867ea948c96f416d94dc26d0fef2010f0323cfa65560a0cad77c0998867'}, 'application_wave8_diagnostic': {'path': 'tools/rebuild/application_wave8_diagnostic.py', 'sha256': '5643730f3031086829286d14c102e7a374da10f16cec187532a6ab89c3e09669'}, 'application_wave9_diagnostic': {'path': 'tools/rebuild/application_wave9_diagnostic.py', 'sha256': 'd54916fcb1880eea03217cf5067684cd9ddc02af18bfaab6fc5b63a3b0e65cc7'}, 'application_wave9_inputs': {'path': 'tools/rebuild/application_wave9_inputs.py', 'sha256': '27aab788d3b2ab887a2ff3eca2ba2cba98894110d261a71b0868b40e5cc8f596'}, 'import_v8_four_successor': {'path': 'tools/rebuild/import_v8_four_successor.py', 'sha256': '374b12b74f0290341b5f57b028f7a0319a9d36fe8a1b1fe76c859a6c1b1cf5fe'}, 'crt_frontier_adoption_contract': {'path': 'tools/rebuild/crt_frontier_adoption_contract.py', 'sha256': 'cd664da3365ce583429ef6ef2af6c5329755405e63545967f292d7a3c0b17256'}, 'crt_v10_four_alias_plan': {'path': 'tools/rebuild/crt_v10_four_alias_plan.py', 'sha256': 'b14e30e5bc3922281fabb54589f38378928dc228b9098f0f8f60a1dfb55b6d81'}, 'runtime_code_pool': {'path': 'tools/rebuild/runtime_code_pool.py', 'sha256': '729f189e2893c7f3a3e3cd97df7d7381ac115169e1d75cf664e6bbc1c587b277'}, 'crt_v13_four_alias_plan': {'path': 'tools/rebuild/crt_v13_four_alias_plan.py', 'sha256': '2d4236366e952ccd599c482f72d13021d383d0decab98815e4a28a35a2c94a3c'}, 'application_frontier_inputs': {'path': 'tools/rebuild/application_frontier_inputs.py', 'sha256': '2f47fc9ec0893b1be1168c328f4418be8df340a6aec4c39354bf4fce32406cd2'}, 'crt_v8_four_alias_contract': {'path': 'tools/rebuild/crt_v8_four_alias_contract.py', 'sha256': '005918b1a35993e54769dc68fc60c3077f332b4fb5565ebf2f2c19da9135fbe1'}, 'crt_v9_four_alias_contract': {'path': 'tools/rebuild/crt_v9_four_alias_contract.py', 'sha256': '52702e719f09679bc8dcc33b77c632f8e1db1efd49061f4a93eedb6d04bf964b'}, 'crt_adoption_consumer_contract': {'path': 'tools/rebuild/crt_adoption_consumer_contract.py', 'sha256': 'cb724fdf907898f68577ef6a25774d4e38111562ea7e2020cc44c747d147448c'}, 'crt_frontier_adoption_plan': {'path': 'tools/rebuild/crt_frontier_adoption_plan.py', 'sha256': '334a6ce0fa240ab258ba7c497ca00aa0c197ead9f8c57b96198a1c250a03b976'}, 'application_link_wave10': {'path': 'tools/rebuild/application_link_wave10.py', 'sha256': '0370d085d4c2eb411a927abef1e149623859b077c907146a4106e24903893c68'}, 'compare': {'path': 'tools/compare.py', 'sha256': 'cfcf5921b71b7a58b6f430d999a511fab9a68f037791bc60295a3083535544d1'}, 'build_and_match': {'path': 'tools/build_and_match.py', 'sha256': 'e4c5f0d8ef8546d1ff82f4f2092e5f65164495daa867c4ff25efd9e45a25d727'}, 'coff_rewrite': {'path': 'tools/rebuild/coff_rewrite.py', 'sha256': '48cea438b05a1c2de992eea4200b45a1eb14e49a27704a5c6fff98f941b1ae4c'}, 'application_link_wave13': {'path': 'tools/rebuild/application_link_wave13.py', 'sha256': 'b5a61acc14d39a0c16683572c30013c56a1427b6971fdb4ab57f843f8ccb91ac'}, 'import_kernel32_nine': {'path': 'tools/rebuild/import_kernel32_nine.py', 'sha256': '696903fd3d5affaf0158da5ccbed7278f05a3b1f3da775c331b72eab22cd3864'}, 'crt_v8_four_alias_plan': {'path': 'tools/rebuild/crt_v8_four_alias_plan.py', 'sha256': '9dddcb3ad9b015d6008938185e576097fe9f7907e403d5ce36950cda23a0ac3b'}, 'crt_v9_four_alias_plan': {'path': 'tools/rebuild/crt_v9_four_alias_plan.py', 'sha256': 'b46d074c74c4f603dcb7f99b992f92b8d0293ad1c68e1bf51d5d127d539127ba'}, 'crt_provider_adoption_plan': {'path': 'tools/rebuild/crt_provider_adoption_plan.py', 'sha256': '7e17f4d0d951447967ccd9d98709e81e6ed4c93612de20d34a1ffdcaddfeb604'}, 'function_spans': {'path': 'tools/function_spans.py', 'sha256': '8e1f9134d9f207dcc8b524b6bac63cf1319f64860903fef5d2a6996709444727'}, 'frontier_code_factory': {'path': 'tools/rebuild/frontier_code_factory.py', 'sha256': '1ded932d2a398724b9595d9ea948cfefbc0faf6adcb77b78767e6f7858bb2f8f'}, 'ordinary_relocation_factory': {'path': 'tools/rebuild/ordinary_relocation_factory.py', 'sha256': 'f431d8599d7e91e2c67ed5570ccd067bdf80fbd8a92ee4c6daa3473cc26c928b'}, 'current_code_frontier': {'path': 'tools/rebuild/current_code_frontier.py', 'sha256': '34ad6b6aacf0a9c5b0cfd68cf26fdd57e18cec4f9b74e24b48296049703397bc'}, 'ordinary_code_projection': {'path': 'tools/rebuild/ordinary_code_projection.py', 'sha256': 'e01437aed27549d8892035d3ea7f1500a5e15150bb14a8d56db95ff17c1dac8d'}, 'ordinary_relocation_projection': {'path': 'tools/rebuild/ordinary_relocation_projection.py', 'sha256': '30e149e02e4ba514cf5bf4ad6dce41625a46df19c2585874c90e97305ee3c732'}, 'prepared_code_exclusions': {'path': 'tools/rebuild/prepared_code_exclusions.py', 'sha256': 'c53cdc375872ec1cf58dbf2da1dc3823d8e6d00ec9822883b333b4b4e96e4774'}, 'composed_relocation_factory': {'path': 'tools/rebuild/composed_relocation_factory.py', 'sha256': '34e9ad9ccfb10943c2fc4c10ea57e28dae8312dc442621ed8045cbeb2b649477'}, 'root_code_closure': {'path': 'tools/rebuild/root_code_closure.py', 'sha256': '4bfdb5001380a3d7e5db7517033285d49ab211be68e2fcba15964f0ad5b03c53'}, 'scalableordinary_root_collect': {'path': 'tools/rebuild/scalableordinary_root_collect.py', 'sha256': 'e7e5b45df15af0a2bd5cb4a65b36d85ca21eb753656714c0a9a5d8dd919e58ad'}, 'bulk_code_pool': {'path': 'tools/rebuild/bulk_code_pool.py', 'sha256': '4e6d697c1881c56c4c3f6a84788df6e0e2617b284d8e0226805828829bce49ed'}, 'runtime_code_inventory': {'path': 'tools/rebuild/runtime_code_inventory.py', 'sha256': 'c2fdbd52b4b7f4b7c68f9d80ad03708ba57d42b29e5938dfcf9769366a1ffd0b'}, 'composed_relocation_projection': {'path': 'tools/rebuild/composed_relocation_projection.py', 'sha256': 'ae434691badad5ad41eb6c2b65a7dad026c71b7f80512e8f2cc3dcdbcaff96bc'}, 'data_plan': {'path': 'tools/rebuild/data_plan.py', 'sha256': 'e013ed5f217f9beeeaf571d089a36df22b645559063e826554179cea506f5bf8'}, 'runtime_gaps': {'path': 'tools/rebuild/runtime_gaps.py', 'sha256': '0399e0f91e94de781512a153ac598f4d5eb6210920bc58241542339c72904116'}, 'import_plan': {'path': 'tools/rebuild/import_plan.py', 'sha256': '6b9237ab5951e7d4a2ac2f9b0c3435f0a667a9fdebac02a4534ba0e30ba98d9c'}, 'root_certificate_composer': {'path': 'tools/rebuild/root_certificate_composer.py', 'sha256': '9d24c9d522cd62618e4335dee10799c8bd1954822382ade548a4c2ea8fb76b7f'}, 'local_label_projection': {'path': 'tools/rebuild/local_label_projection.py', 'sha256': '57cecc88c2f2aaccdf87ca8605fe84461c31a4c391884d503240329636e5f826'}, 'ordinary_initialized_data_omission': {'path': 'tools/rebuild/ordinary_initialized_data_omission.py', 'sha256': '1a0e8aa2271218f59c11497c1363b41f099bb259791e19adac7d80718e7a5d7b'}, 'application_link_wave14': {'path': 'tools/rebuild/application_link_wave14.py', 'sha256': '5021fbfbf1c4efd4a52e8b65b84bc49b623a009673bebf390724f0c17eb72667'}}
SOURCE_ORDER=None
def file_identity(path,cap=None):
    path=Path(path).absolute();resolved=path.resolve(strict=True);stat=resolved.stat()
    require(resolved.is_file() and (cap is None or stat.st_size<=cap),'input identity/size differs')
    h=hashlib.sha256()
    with resolved.open('rb') as f:
        while True:
            part=f.read(1024*1024)
            if not part:break
            h.update(part)
    post=resolved.stat()
    require((stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns)==
            (post.st_dev,post.st_ino,post.st_size,post.st_mtime_ns),'input changed while hashing')
    return dict(requested_path=str(path),path=str(resolved),sha256=h.hexdigest(),size=stat.st_size,
                device=stat.st_dev,inode=stat.st_ino)


def bind(path,expected,bindings,cap=128*1024*1024):
    path=Path(path);require(path.is_absolute() and path.resolve(strict=True).is_relative_to(ROOT),'path escapes workspace')
    ident=file_identity(path,cap);require(ident['sha256']==expected,'fixed input hash differs')
    bindings.append(ident)  # Deliberately preserve duplicates; inherited ledger semantics.
    return path



class _SnapshotFinder:
    """Lazy in-memory module loader for a fully preauthenticated source graph.

    It must remain installed while any graph module can perform late imports.
    Caller controls graph bytes, path removal and runtime trust scope.
    """
    def __init__(self, snapshots, paths, workspace):
        self.workspace=Path(workspace).resolve()
        _require(type(snapshots) is dict and set(snapshots)==set(paths),'exact snapshot set required')
        self.snapshots=dict(snapshots);self.paths=dict(paths)
    def find_spec(self,fullname,path=None,target=None):
        if fullname not in self.snapshots:
            spec=importlib.machinery.PathFinder.find_spec(fullname,path)
            origins=[]
            if spec is not None:
                if spec.origin and spec.origin not in ('built-in','frozen'):origins.append(spec.origin)
                if spec.submodule_search_locations is not None:origins.extend(spec.submodule_search_locations)
                for origin in origins:
                    resolved=Path(origin).resolve()
                    if resolved==self.workspace or resolved.is_relative_to(self.workspace):
                        raise ImportError('unreviewed project source rejected: '+fullname)
            rootname=fullname.split('.')[0]
            if rootname not in sys.stdlib_module_names and rootname!='psutil':
                raise ImportError('unreviewed external runtime dependency rejected: '+fullname)
            if rootname in sys.stdlib_module_names:
                stdlib_root=Path(EXPECTED_INTERPRETER['path']).parent.resolve()
                for origin in origins:
                    resolved=Path(origin).resolve()
                    if (resolved!=stdlib_root and not resolved.is_relative_to(stdlib_root)) or \
                       'site-packages' in (part.lower() for part in resolved.parts):
                        raise ImportError('stdlib origin outside trusted interpreter: '+fullname)
            return None
        _require(path is None and target is None,'project module reload/package import rejected')
        return importlib.util.spec_from_loader(fullname,self,origin=self.paths[fullname])
    def create_module(self,spec):return None
    def exec_module(self,module):
        name=module.__name__
        _require(name in self.snapshots,'unreviewed project module rejected')
        module.__file__=self.paths[name]
        exec(compile(self.snapshots[name],module.__file__,'exec'),module.__dict__)


def _restricted_project_search_paths(paths, workspace):
    """Return interpreter paths excluding cwd/workspace project fallbacks."""
    workspace=Path(workspace).resolve()
    retained=[]
    for entry in paths:
        _require(type(entry) is str,'interpreter search path must be string')
        if not entry:continue
        resolved=Path(entry).resolve()
        if resolved==workspace or resolved.is_relative_to(workspace):continue
        retained.append(entry)
    return retained


def _source_snapshots(graph,bindings):
    """Bind every reviewed source before importing any of them."""
    _require(type(graph) is dict and graph and len(graph)<=80,'bounded source graph required')
    _require(not any(name in sys.modules for name in graph),'preloaded project module rejected')
    snapshots={};paths={};total=0
    for name,ref in graph.items():
        _require(type(name) is str and re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',name) and
                 type(ref) is dict and set(ref)=={'path','sha256'} and
                 type(ref['path']) is str and ref['path'].startswith('tools/') and
                 type(ref['sha256']) is str and re.fullmatch('[0-9a-f]{64}',ref['sha256']),
                 'source graph entry differs')
        path=bind(ROOT/ref['path'],ref['sha256'],bindings,cap=4*1024*1024)
        with path.open('rb') as stream:data=stream.read(4*1024*1024+1)
        total+=len(data)
        _require(len(data)<=4*1024*1024 and total<=8*1024*1024 and
                 hashlib.sha256(data).hexdigest()==ref['sha256'],'source snapshot changed')
        snapshots[name]=data;paths[name]=str(path)
    return snapshots,paths

INPUT_PATH='build/rebuild/application-wave14-prepare-inputs-v2.json'
REVIEW_PATH='build/rebuild/application-wave14-prepare-independent-review-v2.json'
REQUEST_PATH='build/rebuild/application-wave14-prepare-request-v2.json'
SOURCE_PATH='tools/rebuild/application_wave14_diagnostic.py'
TEST_PATH='tests/rebuild/test_application_wave14_diagnostic.py'
FIXED_INPUTS={'v13_report': {'path': 'build/rebuild/application-link-diagnostic-v13-code56/receipt.json', 'sha256': '4444564a7507bd835b07284acfa73d2ca1ac7077da72056625a57f947f6980b0'}, 'v13_observation': {'path': 'build/rebuild/application-wave13-cohort-observation-v1/receipt.json', 'sha256': 'e19302008032c9bb733eeaa32e2db1f075aa420ef5067332cf0857eaab094c69'}, 'v13_fields': {'path': 'build/rebuild/application-wave13-cohort-observation-v1/fields.json.gz', 'sha256': 'b7823e8892a4a5051d42b6447078058f5d0be4d3db0dc3bfbf5630621b73f23a'}, 'v14_observation': {'path': 'build/rebuild/application-wave14-cohort-observation-v2/receipt.json', 'sha256': 'b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185'}, 'v14_fields': {'path': 'build/rebuild/application-wave14-cohort-observation-v2/fields.json.gz', 'sha256': '73a57a716b97cf116e625f2a585039a494b7d8a06293be5810672d229b211075'}, 'v14_observation_peer': {'path': 'build/rebuild/application-wave14-cohort-observation-v2/independent-outcome-review.json', 'sha256': '6fb2797b42d8c874b901461a900867c62aee64badf13ab6148b7b69a1d47b8fd'}, 'baseline_response': {'path': 'build/rebuild/application-link-diagnostic-v13-code56/link.rsp', 'sha256': 'd90fe3f379b130927fc5fe98821919f7016e69d657cc2023072556ef3d60d389'}, 'crt_plan': {'path': 'build/rebuild/application-crt-v14-four-contract-v1.json', 'sha256': 'e832d09148559e859cb4358530407edb0be39fa678d5ad4e0c524dc587e2a7be'}, 'crt_review': {'path': 'build/rebuild/application-crt-v14-four-contract-peer-v1.json', 'sha256': 'e18ef6adc4c878240c4daad02e1d2fbaaed925a59740916ad298569d548f9e25'}, 'crt_response': {'path': 'build/rebuild/application-crt-v14-four-proposal-v1.rsp', 'sha256': 'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'}, 'crt_consumer_peer': {'path': 'build/rebuild/crt-v14-four-consumer-peer-v1.json', 'sha256': 'd70694cbb3d715e266458be73a60f3cf6c44e42e1cdea94654b325132fc7cd4f'}, 'uuid_receipt': {'path': 'build/rebuild/uuid2768-factory-result-v2/receipt.json', 'sha256': 'fdec31d202ebbed1e846c0c8198a384db995d05aab5433b75d475b4f820ba98c'}, 'uuid_object': {'path': 'build/rebuild/uuid2768-factory-result-v2/uuid2768.obj', 'sha256': '6fcd604987e08477566cbf9b6901f3200304eb557fdc8f7c356fedaf27d633b3'}, 'uuid_archive': {'path': 'build/rebuild/uuid2768-factory-result-v2/uuid2768.lib', 'sha256': 'b921ee8a8d6baf9a751f1a488aa10a763627ede51b2b475668c97455a4e9eb53'}, 'uuid_proof': {'path': 'build/rebuild/uuid2768-factory-result-v2/field-proofs.jsonl.gz', 'sha256': '4b7cb6ce64a9a84d461ef0ef536cd17c5952fe03b697e45e652e18c2f5e7cc31'}, 'uuid_base_review': {'path': 'build/rebuild/uuid2768-factory-result-v2/independent-outcome-review.json', 'sha256': 'dc5553cc029f0821b01c645a4975a70bdabc1a959f95178919df534f51d6b89e'}, 'uuid_continuity': {'path': 'build/rebuild/uuid2768-factory-result-v2/independent-directive-continuity-review.json', 'sha256': 'e5bead380f35dbb91947ecf14d2f3d776e5b4cf7523cf8aa28348e8aaf09e8db'}, 'uuid_native_receipt': {'path': 'build/rebuild/uuid2768-native-conformance-v1/receipt.json', 'sha256': '12dae2e56d941949650dbc8c0d72a0660c4d8da5d4d14f2209db4f79e2c852f1'}, 'uuid_native_review': {'path': 'build/rebuild/uuid2768-native-conformance-v1/independent-outcome-review.json', 'sha256': 'f161af6ac5ce40e02088724ba156f7737484def6b5aafadc4f8bda104587b7f6'}, 'uuid_declaration': {'path': 'build/rebuild/uuid-prefix-dependency-v1/declaration.json', 'sha256': '2cf2f061f003d027213cbfa77e53f2a15be34de8db62fa32712148ff6dbb51ac'}, 'uuid_context': {'path': 'build/rebuild/uuid-prefix-dependency-v1/context.json', 'sha256': '8b044fe51ce0b455ea6baac1c88441d566ec1514e4def0866b7102382b1b784f'}, 'uuid_declaration_review': {'path': 'build/rebuild/uuid-prefix-dependency-v1/review.json', 'sha256': '9cce2a0d39394c9bf0b564a8f872a83b655f83bb22a6db036f306643f15c9dfd'}, 'uuid_declaration_audit': {'path': 'build/rebuild/uuid-prefix-dependency-v1/independent-declaration-audit.json', 'sha256': '32481c04d52919500766a9e10b1a0d2ffe801254a1d542721e49773c6daad1dd'}, 'uuid_handoff': {'path': 'build/rebuild/uuid2768-typed-export-handoff-v1.json', 'sha256': '4ce4f515e43a04f622b1efaa70ac47753f16109111944f73ca0aefeb915b06a1'}, 'uuid_handoff_review': {'path': 'build/rebuild/uuid2768-typed-handoff-source-v1/independent-output-review-v1.json', 'sha256': '7b879e3baa1bf55e81c9a9884f692b27feff025c0d5fe55a30d7c3d60135ab9d'}, 'iat_ancestry_catalog': {'path': 'build/rebuild/import-plan-native-v3.json', 'sha256': 'e39b8db63ef73aea57b5dd4963ff29310524644ca36e137cd8b5461a3c90a23f'}, 'iat_ancestry_assessment': {'path': 'build/rebuild/v10-import-assessment-v1/assessment.json', 'sha256': 'e3ee933ca871553453ff0bac698b33a6eb44bf6c2442405c83acfe95b0075abe'}, 'iat_ancestry_assessment_review': {'path': 'build/rebuild/v10-import-assessment-v1/independent-outcome-review.json', 'sha256': 'd5f52a7b43938c03a9ecdd503d4dd51505c90b18c88e81d7bf776b8615c6a2ad'}, 'iat_ancestry_fields': {'path': 'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz', 'sha256': '03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978'}, 'iat_ancestry_groups': {'path': 'build/rebuild/application-link-diagnostic-v10-wave/unresolved-groups.json', 'sha256': '808c27db9ffdfa170c720c26edab50a42ca4b90bc471c78401203ec9b44f0b8a'}, 'iat_ancestry_prior_native': {'path': 'build/rebuild/import-v8-four-native-v1/collection.json', 'sha256': '0ec9b50fd9d94fb518b820075a3596da8eb9bea0f20d44f36606d37f53581ea3'}, 'iat_ancestry_prior_review': {'path': 'build/rebuild/import-v8-four-native-v1/independent-outcome-review.json', 'sha256': 'b1fe585cf034ef88ca6651fd62bd2512602f921c5760cbe197d0adec8c3910ea'}, 'iat_request': {'path': 'build/rebuild/import-kernel32-fifteen-v1/preparation.json', 'sha256': 'b4bd7a2683c6f99469d52f86f181ce40388df68fe9c9cb41fc0f1b9ad00464dc'}, 'iat_native': {'path': 'build/rebuild/import-kernel32-fifteen-native-v1/collection.json', 'sha256': '6824931642112f42877c75e51a8a34f705738070b49618b635aad7fa2bee10c1'}, 'iat_kernel': {'path': 'build/rebuild/import-kernel32-fifteen-native-v1/kernel32-fifteen.lib', 'sha256': '7485983d540767fad6c69366f7b89c7943654fdfd4ef501067fbb43ff073fe04'}, 'iat_user32': {'path': 'build/rebuild/import-v8-four-native-v1/user32-sixteen.lib', 'sha256': '19c6cb80185784829b38c2e6d03672c5b06cbf2e96c4245a4c6b73adc973e132'}, 'iat_provider000': {'path': 'build/rebuild/application-link-inputs-v2/provider-000.lib', 'sha256': '2627bd866f27b6d867d85f305e1d0fd0a002c4dc14f5037189c1f645d0dfdd91'}, 'iat_provider002': {'path': 'build/rebuild/application-link-inputs-v2/provider-002.lib', 'sha256': 'ed07b437804514dbd5f61888fb2051a83a694ab3563585183146547ec0045c9a'}, 'code21_archive': {'path': 'build/rebuild/cached-frontier-code-v13-v1/CACHED-code.lib', 'sha256': '80444a67d2e4c8656de45f32ba7f879a8fd281629b2600c8c0984e7296600607'}, 'units': {'path': 'build/units.json', 'sha256': '62f2c8da5f0daa912abdf4576328706711c6561eef7f01c93a89cb71ad46fb6c'}, 'source_main': {'path': 'src/fallout/misc/main.cpp', 'sha256': '89d09f8b4ba6d9758fca0ac3ebd32e18c9cc82c68a739c044457ed5c005ae3c5'}, 'source_staging': {'path': 'src/staging/blk_00440000_od.cpp', 'sha256': '9236184acd1d32db546f728d2b587b9794836daf4cba13b01560029d1c3d6587'}, 'source_taskqueue': {'path': 'src/fallout/misc/taskqueueinterface.cpp', 'sha256': '528f0b219a8221cfc8c948b3e8bb66d098d63d00e3b877fbaf0d6dcb4e6e71fa'}, 'crt_extra_43': {'path': 'build/rebuild/application-crt-v13-four-contract-v1.json', 'sha256': 'd47b3b0efe542808e1fc22481da41888f6daa11d3d6c928279e397344dec5721'}, 'crt_extra_44': {'path': 'build/rebuild/application-crt-v13-four-contract-peer-v1.json', 'sha256': 'd020b039377efe24821028b8d4c667f9953ce2116db0bb52871966e652e87b27'}, 'crt_extra_45': {'path': 'build/rebuild/application-crt-v13-four-proposal-v1.rsp', 'sha256': 'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'}, 'crt_extra_46': {'path': 'build/rebuild/crt-v13-four-consumer-peer-v1.json', 'sha256': 'a53697ce5f29aa076187acc87f6b9dfa68753560d4a63f77bbe9189f32253faa'}, 'crt_extra_47': {'path': 'build/rebuild/application-wave14-CRT-input-handoff-v1.json', 'sha256': '63f20780783a550170721794bc657d8256414692973ab2e674ecbbd92577c6ec'}, 'crt_extra_48': {'path': 'build/rebuild/cached-frontier-code-v13-v1/members.json', 'sha256': '91ec69b946927f0650aa66df1c78544c95445ad463a463e8b8a2a287b8b9818c'}, 'crt_extra_49': {'path': 'build/rebuild/cached-frontier-code-v13-v1/field-proofs.jsonl.gz', 'sha256': '9f4718e8e3273c088ae671db68c7a9314e33848e3912cb79844c8f9b0b210eb8'}, 'crt_extra_50': {'path': 'build/rebuild/cached-frontier-code-v13-export-handoff-v1.json', 'sha256': '8fadcc041ae90788a4bf669091ff602a92756ff24f9e56659708d1b890665b11'}, 'crt_extra_51': {'path': 'build/rebuild/code-lane01-analysis-v1/cached-frontier-code-v13-handoff-review-v1.json', 'sha256': '001fbc4fadd6683b8ce3cc7c484329ae11046b2f7054118ea5c34db062b76605'}, 'crt_extra_52': {'path': 'build/rebuild/application-wave14-verifier-source-independent-review.json', 'sha256': 'ebf8bc0c11f2fc8714294fc05d0beae74a18371fc4150014d5a640b6d2213894'}, 'crt_extra_53': {'path': 'build/rebuild/crt-v14-input-triage-v1.json', 'sha256': '2ab80c3f4720af41a2d7793ba832ad1406ff203cc4c80cb8c9a9d8464042314f'}, 'crt_extra_54': {'path': 'build/rebuild/crt-v14-GS-source-boundary-peer-v1.json', 'sha256': 'aedce9c3ac33bbe85861afdfaa3f65380842cadb0c055fab4be9327e88860e6c'}, 'crt_test_55': {'path': 'tests/rebuild/test_crt_v14_four_alias_contract.py', 'sha256': '6679b2d095f86795c90d50c4288eafecb8bddee381282e16c8fe0d2b42537f27'}, 'crt_test_56': {'path': 'tests/rebuild/test_crt_v13_four_alias_contract.py', 'sha256': 'cd88d25d269dbb3d2df2250996edfe8236e02504b1ddd8b213d4612f17d50de9'}, 'crt_test_57': {'path': 'tests/rebuild/test_crt_v10_four_alias_contract.py', 'sha256': '6f64218efca7dc6cb27d771b911a8c90a158b45f36b6afcb82a52bc303222f0e'}, 'crt_test_58': {'path': 'tests/rebuild/test_crt_v9_four_alias_contract.py', 'sha256': '98c0fd2831a73b200e453e968bff5b0f30a7e5c12c08d66971192d7ee1b2bb4f'}, 'crt_test_59': {'path': 'tests/rebuild/test_crt_v8_four_alias_contract.py', 'sha256': '691de29bf153d9a961fd5e28731c52a756cb44b7a1ad5efdcc678938ee00b573'}, 'crt_test_60': {'path': 'tests/rebuild/test_crt_v14_four_alias_plan.py', 'sha256': 'f7c7acb88f8e8e188ef2c6f20a57ba9f890531b0181cf5bc0d642597d32ea0fa'}, 'v13_peer': {'path': 'build/rebuild/application-link-diagnostic-v13-code56/independent-outcome-review.json', 'sha256': '87ddc7b3072e34589663feec02e1db797b3142ee4d208f69a8272756883b57ba'}, 'v13_observation_peer': {'path': 'build/rebuild/application-wave13-cohort-observation-v1/independent-outcome-review.json', 'sha256': 'aecffece805bad88152f80a340a2074349795b59164390d7376df687c3d008ce'}, 'iat_request_peer': {'path': 'build/rebuild/import-kernel32-fifteen-v1/independent-source-input-review.json', 'sha256': 'c4e45d292e089f3194046a9b7bffb7154282ffdc28c6b7ff9c23cb4bf06a3ff2'}, 'iat_native_peer': {'path': 'build/rebuild/import-kernel32-fifteen-native-v1/independent-outcome-review.json', 'sha256': 'd3283033752d0c8ad33ff8173c1196cd3f07d9d4649e615bb4eb3c328299654d'}, 'graph_inventory': {'path': 'build/rebuild/v14-import-source-inventory-v1/source-import-graph-v3.json', 'sha256': 'ea008f0fdf60fe58a30f9c0d7d6ceaa1376fb42a343330202dd7d749f75a1d95'}, 'crt_inherited_plan_test_1': {'path': 'tests/rebuild/test_crt_v8_four_alias_plan.py', 'sha256': '747bca44a7c8c41ae74cc38bc145d7d1c5f4516130d5a77e58ddc7efe79d6ec0'}, 'crt_inherited_plan_test_2': {'path': 'tests/rebuild/test_crt_v9_four_alias_plan.py', 'sha256': '00a1c7ffb348cb8f05e9839756e4e3484bdb4cc5ab6de12e3d2183d9957eb3ea'}, 'crt_inherited_plan_test_3': {'path': 'tests/rebuild/test_crt_v10_four_alias_plan.py', 'sha256': 'ea52bccf6ed00d82a7162a22112fc106869362993f2d1920675f18980c17a94d'}, 'crt_inherited_plan_test_4': {'path': 'tests/rebuild/test_crt_v13_four_alias_plan.py', 'sha256': 'b3faba93a02bd47b25849c69d22343685e9fd36602c6419dc5f80dd4f1b818d3'}}  # Requires final accepted CRT and full reviewed input manifest.

def _verify_fixed_manifest(manifest,review,*,source_sha,tests_sha,inputs_sha,expected_inputs,expected_sources,third_party):
    """Only a separately hash-bound independent review authorizes this manifest."""
    _require(type(expected_inputs) is dict and expected_inputs and type(expected_sources) is dict and expected_sources,
             'reviewed exact inputs and source graph required')
    path_pins={}
    for mapping in (expected_inputs,expected_sources):
        for row in mapping.values():
            _require(type(row) is dict and set(row)=={'path','sha256'},'exact path pin required')
            path,sha=row['path'],row['sha256']
            _require(type(path) is str and bool(path) and type(sha) is str and re.fullmatch('[0-9a-f]{64}',sha),
                     'valid path pin required')
            _require(path not in path_pins or path_pins[path]==sha,'conflicting path pins')
            path_pins[path]=sha
    _require(type(manifest) is dict and set(manifest)=={'kind','schema_version','inputs','source_pins','limits',
       'output','interpreter','third_party_runtime'} and manifest['kind']=='wave14-fixed-prepare-inputs-v1' and
       type(manifest['schema_version']) is int and manifest['schema_version']==1 and
       manifest['inputs']==expected_inputs and manifest['source_pins']==expected_sources and
       manifest['limits']=={'seconds':480,'rss_bytes':1073741824,'output_bytes':134217728} and
       manifest['output']==OUTPUT_PATH and manifest['interpreter']==EXPECTED_INTERPRETER and
       manifest['third_party_runtime']==third_party,
       'fixed preparer input scope differs')
    _require(type(review) is dict and review.get('kind')=='independent-wave14-combined-prepare-source-input-review' and
       type(review.get('schema_version')) is int and review['schema_version']==1 and review.get('status')=='accepted-metadata-only' and
       review.get('source_sha256')==source_sha and review.get('tests_sha256')==tests_sha and
       review.get('inputs_sha256')==inputs_sha and review.get('third_party_runtime')==third_party and
       all(type(review.get(k)) is str and re.fullmatch('[0-9a-f]{64}',review[k]) for k in
          ('source_sha256','tests_sha256','inputs_sha256','request_sha256','watchdog_sha256','watchdog_tests_sha256')),
       'independent preparer review differs')


def _reject_preloaded_workspace(workspace,allowed_main_file):
    """Reject cached project modules that bypass the snapshot finder."""
    workspace=Path(workspace).resolve();allowed=Path(allowed_main_file).resolve()
    for name,module in tuple(sys.modules.items()):
        path=getattr(module,'__file__',None)
        if not isinstance(path,str):continue
        resolved=Path(path).resolve()
        if resolved==workspace or resolved.is_relative_to(workspace):
            _require(name=='__main__' and resolved==allowed,'preloaded workspace module rejected: '+name)


PSUTIL_ROOT=Path(__import__('os').path.expandvars(r'%APPDATA%\Python\Python312\site-packages\psutil'))
EXPECTED_PSUTIL={
 'version':'6.1.1',
 'module':{'path':str(PSUTIL_ROOT/'__init__.py'),'sha256':'7538e99b4bf449ad5133381926d82752fe81713c5d3f0c401802ca8bb42e2b45','size':91640},
 'backend':{'path':str(PSUTIL_ROOT/'_pswindows.py'),'sha256':'5313532b9bb767e31e0583f04070a3ab1331205f5e5f8f4362ed0ff44ece296b','size':39271},
 'native_backend':{'path':str(PSUTIL_ROOT/'_psutil_windows.pyd'),'sha256':'dd0ccdeeca681645025ca0f562ea45b5b17a1ebfcf1688cd0647a950a2992e2f','size':67072}}


def load_verified_psutil(bindings):
    """Bind installation indicators; the entire psutil package/bytecode and OS runtime remain trusted."""
    require(not any(n=='psutil' or n.startswith('psutil.') for n in sys.modules),'preloaded psutil is not accepted')
    for k in ('module','backend','native_backend'):
        expected=EXPECTED_PSUTIL[k];actual=file_identity(expected['path'],cap=4*1024*1024)
        require(actual['path']==expected['path'] and actual['sha256']==expected['sha256'] and
                actual['size']==expected['size'],'psutil runtime identity differs')
        bindings.append(actual)
    spec=importlib.util.spec_from_file_location('psutil',EXPECTED_PSUTIL['module']['path'],
                                               submodule_search_locations=[str(PSUTIL_ROOT)])
    require(spec is not None and spec.loader is not None,'psutil loader unavailable')
    module=importlib.util.module_from_spec(spec);sys.modules['psutil']=module;spec.loader.exec_module(module)
    require(module.__version__==EXPECTED_PSUTIL['version'] and
       str(Path(module.__file__).resolve())==EXPECTED_PSUTIL['module']['path'] and
       str(Path(module._psplatform.__file__).resolve())==EXPECTED_PSUTIL['backend']['path'] and
       str(Path(module._psplatform.cext.__file__).resolve())==EXPECTED_PSUTIL['native_backend']['path'],
       'psutil loaded runtime origin differs')
    return module



def _startup_authority(*,inputs_path,inputs_sha256,source_sha256,tests_sha256,review_path,review_sha256):
    """Fixed-runtime entry draft; fails closed until separately reviewed pins exist.

    Not a public API: caller must retain the finder until all work is finished,
    enforce an outer watchdog, and use _publish_private with this exact guard.
    """
    import importlib
    import time
    _require(type(FIXED_INPUTS) is dict and FIXED_INPUTS and type(SOURCE_PINS) is dict and SOURCE_PINS,
             'fixed CRT/input/source authority not yet bound')
    for digest in (inputs_sha256,source_sha256,tests_sha256,review_sha256):
        _require(type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest),'exact external digest required')
    _require(Path(__file__).resolve()==ROOT/SOURCE_PATH and Path(inputs_path).resolve()==ROOT/INPUT_PATH and
             Path(review_path).resolve()==ROOT/REVIEW_PATH and not (ROOT/OUTPUT_PATH).exists(),
             'fixed source, input, review and fresh output required')
    start=time.monotonic();bindings=[]
    def read_bound(path,sha,cap=128*1024*1024):
        path=bind(path,sha,bindings,cap)
        with path.open('rb') as stream:data=stream.read(cap+1)
        _require(len(data)<=cap and hashlib.sha256(data).hexdigest()==sha,'input changed after bind')
        return data
    manifest=bounded_json(read_bound(ROOT/INPUT_PATH,inputs_sha256,4*1024*1024),4*1024*1024)
    read_bound(ROOT/SOURCE_PATH,source_sha256,4*1024*1024)
    review=bounded_json(read_bound(ROOT/REVIEW_PATH,review_sha256,4*1024*1024),4*1024*1024)
    _verify_fixed_manifest(manifest,review,source_sha=source_sha256,tests_sha=tests_sha256,
       inputs_sha=inputs_sha256,expected_inputs=FIXED_INPUTS,expected_sources=SOURCE_PINS,third_party=EXPECTED_PSUTIL)
    read_bound(ROOT/REQUEST_PATH,review['request_sha256'],4*1024*1024)
    psutil_module=load_verified_psutil(bindings)
    started,started_sha=_watchdog_started(review,source_sha256,inputs_sha256,review_sha256,
                                          review['request_sha256'],psutil_module)
    bind(ROOT/WATCHDOG_STARTED_PATH,started_sha,bindings,65536)
    lease_identity=_active_lease(started['slot'],review['request_sha256'],source_sha256,review_sha256)
    finder_slot=[None]
    def guard():
        _require(finder_slot[0] is None or (sys.meta_path and sys.meta_path[0] is finder_slot[0]),
                 'source finder displaced')
        _require(_active_lease(started['slot'],review['request_sha256'],source_sha256,review_sha256)==lease_identity,
                 'lease changed')
        _require(_watchdog_started(review,source_sha256,inputs_sha256,review_sha256,
                 review['request_sha256'],psutil_module)==(started,started_sha),'watchdog child changed')
    guard()
    read_bound(ROOT/TEST_PATH,tests_sha256,4*1024*1024)
    interpreter=file_identity(Path(sys.executable),cap=256*1024*1024)
    _require(interpreter==EXPECTED_INTERPRETER,'interpreter physical identity differs');bindings.append(interpreter)
    _reject_preloaded_workspace(ROOT,ROOT/SOURCE_PATH)
    snapshots,source_paths=_source_snapshots(SOURCE_PINS,bindings)
    finder=_SnapshotFinder(snapshots,source_paths,ROOT)
    _require(not any(name in sys.modules for name in snapshots),'project modules preloaded')
    sys.path[:]=_restricted_project_search_paths(sys.path,ROOT)
    sys.meta_path.insert(0,finder);finder_slot[0]=finder
    try:
        stable_utility=importlib.import_module('exact_binding_stability')
        diagnostic=importlib.import_module('application_link_diagnostic')
        raw={}
        for key,row in FIXED_INPUTS.items():
            guard();raw[key]=read_bound(ROOT/row['path'],row['sha256'])
        stable_utility.stable_phase(bindings,phase='pre',stable_fn=diagnostic.stable)
        guard();_require(time.monotonic()-start<480,'input time cap')
        return dict(manifest=manifest,review=review,review_sha256=review_sha256,raw=raw,bindings=bindings,guard=guard,
                    stable_utility=stable_utility,diagnostic=diagnostic,start=start,finder=finder)
    except BaseException:
        sys.meta_path.remove(finder)
        raise


def _merge_pins(*maps):
    result={}
    for current in maps:
        _require(type(current) is dict,'pin map required')
        for path,sha in current.items():
            _require(type(path) is str and type(sha) is str and re.fullmatch('[0-9a-f]{64}',sha),
                     'invalid source pin')
            _require(path not in result or result[path]==sha,'conflicting source pin')
            result[path]=sha
    return result


def _bounded_gzip_json(data,cap=128*1024*1024):
    import gzip,io
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:expanded=stream.read(cap+1)
    _require(len(expanded)<=cap,'gzip expansion cap')
    return bounded_json(expanded,cap)


def _load_semantics(state,modules):
    """Reconstruct typed data from a fixed, previously authenticated raw packet."""
    raw=state['raw'];refs=FIXED_INPUTS;d=modules['diagnostic'];old=modules['import34'];producer=modules['producer']
    def obj(key):return bounded_json(raw[key],128*1024*1024)
    report=obj('v13_report');v13obs=obj('v13_observation');v14obs=obj('v14_observation')
    _validate_observation_peer(obj('v14_observation_peer'))
    crt_consumer_peer=obj('crt_consumer_peer');_validate_crt_consumer_peer(crt_consumer_peer)
    old_fields=_bounded_gzip_json(raw['v13_fields']);fields=_bounded_gzip_json(raw['v14_fields'])
    # Each legacy ledger is checked as a separately reconstructed phase. No
    # remembered selection or result carries over between phases.
    for label,owner,count in (('v13-report',report,18669),('v13-observation',v13obs,10667),
                              ('v14-observation',v14obs,29428)):
        ledger=owner['input_bindings'];_require(type(ledger) is list and len(ledger)==count,label+' binding ledger required')
        state['guard']();state['stable_utility'].stable_phase(ledger,phase='pre',stable_fn=d.stable);state['guard']()
        state['bindings'].extend(copy.deepcopy(ledger))
    original={}
    for key,path in old.IMPORT_ANCESTRY.items():
        ref=refs['iat_ancestry_'+key]
        _require(ref=={'path':path,'sha256':producer.PINS[key]},'IAT ancestry differs')
        if key!='fields':original[key]=obj('iat_ancestry_'+key)
    _require(refs['iat_request']['path']==old.INPUT_PATHS['import_request'] and
             refs['iat_native']['path']==old.INPUT_PATHS['import_native'] and
             refs['iat_kernel']['path']==old.INPUT_PATHS['kernel_library'], 'IAT fixed path differs')
    kernel=old.import_archive.read_archive(ROOT/refs['iat_kernel']['path'])
    _require(kernel['archive_sha256']==refs['iat_kernel']['sha256'],'kernel archive changed during parse')
    sources=_merge_pins(producer.HELPER_PINS,{'tools/rebuild/import_kernel32_fifteen.py':
              SOURCE_PINS['import_kernel32_fifteen']['sha256']})
    available=_merge_pins({r['path']:r['sha256'] for r in FIXED_INPUTS.values()},
                          {r['path']:r['sha256'] for r in SOURCE_PINS.values()})
    _require(all(available.get(path)==sha for path,sha in sources.items()),
             'IAT replay helper source is not bound')
    selected={'kernel32-fifteen.lib':'iat_kernel','user32-sixteen.lib':'iat_user32',
              'provider-000.lib':'iat_provider000','provider-002.lib':'iat_provider002'}
    libraries={};library_refs={}
    for name,key in selected.items():
        path=ROOT/refs[key]['path'];data=raw[key]
        _require(hashlib.sha256(data).hexdigest()==refs[key]['sha256'] and
                 raw['baseline_response'].decode('utf-8').splitlines().count('"'+str(path)+'"')==1 and
                 any(row.get('requested_path')==str(path) and row.get('path')==str(path) and
                     row.get('sha256')==refs[key]['sha256'] for row in report['input_bindings']),
                 'selected import library binding differs')
        libraries[name]=d.partial.native_archive(data)
        library_refs[name]={'sha256':refs[key]['sha256'],'bytes':len(data)}
    return dict(v13_report=report,v13_observation=v13obs,v14_observation=v14obs,v13_fields=old_fields,v14_fields=fields,
       uuid_evidence={key:raw['uuid_'+key] for key in modules['uuid'].PINS},iat_native=obj('iat_native'),
       iat_request=obj('iat_request'),iat_request_sha256=refs['iat_request']['sha256'],iat_parsed_archive=kernel,
       iat_originals=original,iat_expected_sources=sources,iat_catalog=original['catalog'],iat_libraries=libraries,
       iat_library_refs=library_refs,
       crt_bytes={'plan':raw['crt_plan'],'review':raw['crt_review'],'response':raw['crt_response']},
       crt_consumer_peer=crt_consumer_peer,
       baseline_response=raw['baseline_response'])


def _validate_crt_bound_inputs(crt,*input_maps):
    """Every source and input named by the frozen CRT plan must be manifest-bound."""
    _require(type(crt) is dict and input_maps and all(type(x) is dict for x in input_maps),
             'bound CRT input maps required')
    by_path={}
    for inputs in input_maps:
        for row in inputs.values():
            path=row['path'];sha=row['sha256']
            _require(path not in by_path or by_path[path]==sha,'conflicting fixed path pins')
            by_path[path]=sha
    for key,prefix in (('sources',''),('inputs','build/rebuild/'),('own_sources','')):
        refs=crt[key];_require(type(refs) is dict and refs,'CRT plan bindings missing')
        for path,sha in refs.items():
            _require(by_path.get(prefix+path)==sha,'CRT plan input is not bound')
    _require(by_path.get('build/units.json')==crt['units_sha256'],'CRT units not bound')


def _prepare_from_authority(state):
    """Production wiring draft, fixed wrappers only; entry still needs final pins."""
    import importlib
    state['guard']();_require(sys.meta_path[0] is state['finder'],'source finder displaced')
    names={'diagnostic':'application_link_diagnostic','cohort':'application_link_cohort',
           'uuid':'application_uuid2768','crt':'crt_v14_four_alias_contract',
           'response':'application_combined_response','import34':'application_import34_diagnostic',
           'producer':'import_kernel32_fifteen','annotations':'iat_code21_annotations'}
    modules={key:importlib.import_module(name) for key,name in names.items()}
    state['guard']();_require(sys.meta_path[0] is state['finder'],'source finder displaced')
    _require(modules['diagnostic'] is state['diagnostic'],'diagnostic delegate changed')
    data=_load_semantics(state,modules)
    _validate_crt_bound_inputs(bounded_json(data['crt_bytes']['plan'],128*1024*1024),FIXED_INPUTS,SOURCE_PINS)
    _validate_crt_peer_bindings(data['crt_consumer_peer'],FIXED_INPUTS,SOURCE_PINS)
    state['guard']()
    sdk=modules['diagnostic'].identity(modules['uuid'].EXPECTED_SDK['path'])
    state['bindings'].append(sdk)
    paths={'old_out':str(ROOT/'build/rebuild/application-link-diagnostic-v13-code56'),
           'new_out':str(ROOT/OUTPUT_PATH),
           'batch_archive':str(ROOT/'build/rebuild/cached-frontier-code-v13-v1/CACHED-code.lib'),
           'uuid_archive':str(ROOT/'build/rebuild/uuid2768-factory-result-v2/uuid2768.lib')}
    report,response=_assemble_private(data=data,modules=modules,sdk_identity=sdk,paths=paths)
    state['guard']();_require(sys.meta_path[0] is state['finder'],'source finder displaced')
    report['source_sha256']=state['review']['source_sha256']
    report['tests_sha256']=state['review']['tests_sha256']
    report['inputs_sha256']=state['review']['inputs_sha256']
    report['independent_review_sha256']=state['review_sha256']
    report['third_party_runtime']=copy.deepcopy(EXPECTED_PSUTIL)
    report['entire_psutil_package_bytecode_and_OS_runtime_trusted']=True
    report['source_graph_size']=len(SOURCE_PINS)
    return _publish_private(out=ROOT/OUTPUT_PATH,report=report,response=response['response_bytes'],
        bindings=state['bindings'],guard=state['guard'],stable_utility=state['stable_utility'],
        stable_fn=modules['diagnostic'].stable,start=state['start'],clock=__import__('time').monotonic)


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-sha256',required=True)
    parser.add_argument('--tests-sha256',required=True)
    parser.add_argument('--inputs',required=True)
    parser.add_argument('--inputs-sha256',required=True)
    parser.add_argument('--review',required=True)
    parser.add_argument('--review-sha256',required=True)
    args=parser.parse_args()
    state=_startup_authority(inputs_path=args.inputs,inputs_sha256=args.inputs_sha256,
        source_sha256=args.source_sha256,tests_sha256=args.tests_sha256,
        review_path=args.review,review_sha256=args.review_sha256)
    result,_=_prepare_from_authority(state)
    print(json.dumps({'status':result['status'],'native_LINK_performed':False}))



def _assemble_private(*, data, modules, sdk_identity, paths):
    """Wire fixed semantic gates; only a future reviewed wrapper supplies inputs."""
    _require(set(modules)=={'diagnostic','cohort','uuid','crt','response','import34','producer','annotations'},
             'complete fixed consumer module set required')
    d=modules['diagnostic'];report=data['v13_report'];observation=data['v14_observation']
    old_fields=data['v13_fields'];fields=data['v14_fields']
    _validate_observation(observation,old_fields,fields,d)
    baseline,noncode=_baseline_namespace(report,data['v13_observation'],d,modules['cohort'],14533)
    providers=observation['providers'];_require(type(providers) is list and len(providers)==22,
                                                   'combined extra provider scope differs')
    uuid=modules['uuid'].consume(data['uuid_evidence'])
    _require(_canonical(providers[21:])==_canonical(uuid['providers']), 'observer UUID provider differs')
    _require(_canonical(observation['uuid_source_evidence'])==_canonical(uuid), 'observer UUID evidence differs')
    _require(set(sdk_identity)=={'requested_path','path','sha256','size','device','inode'} and
             sdk_identity['requested_path']==uuid['future_uuid_response_token'] and
             all(type(sdk_identity[k]) is type(v) and sdk_identity[k]==v
                 for k,v in uuid['dependency_identity'].items()) and
             set(uuid['dependency_identity'])=={'path','sha256','size','device','inode'},
             'fresh six-key UUID identity differs')
    crt_plan=bounded_json(data['crt_bytes']['plan'],128*1024*1024)
    _require(all(row['normal_provider']['archive_sha256']==report['default_libraries']['libcmt.lib']['sha256']
                 for row in crt_plan['bindings']), 'normal CRT provider differs')
    prior_iat=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer']
               for row in report['aliases'] if row['enabled']]
    prior_crt=report['CRT_diagnostic_bindings']['tokens']
    iat_rows,current_iat=_iat_gate(old=modules['import34'],producer=modules['producer'],
        annotations=modules['annotations'],native=data['iat_native'],request=data['iat_request'],
        request_sha256=data['iat_request_sha256'],parsed=data['iat_parsed_archive'],
        originals=data['iat_originals'],expected_sources=data['iat_expected_sources'],fields=fields,
        catalog=data['iat_catalog'],libraries=data['iat_libraries'],library_refs=data['iat_library_refs'],prior_iat=prior_iat)
    report,output=_compose(report=report,old_fields=old_fields,observation=observation,fields=fields,
        uuid_evidence=data['uuid_evidence'],old_providers=baseline,noncode_definitions=noncode,
        code21_providers=providers[:21],prior_iat=prior_iat,current_iat=current_iat,iat_rows=iat_rows,
        prior_crt=prior_crt,crt_bytes=data['crt_bytes'],crt_validation=data['crt_consumer_peer']['validation'],
        baseline_response=data['baseline_response'],
        fresh_identity={k:sdk_identity[k] for k in ('path','sha256','size','device','inode')},paths=paths,
        modules={key:modules[key] for key in ('cohort','uuid','crt','response')},
        expected={'old_fields':46237,'fields':46292,'old_providers':14533,'batch_providers':21,'providers':14555})
    _require(type(observation['IAT_fields']) is int and
             sum(row['proof'].get('role')=='iat-cell' for row in fields)==observation['IAT_fields'],
             'complete observed IAT inventory differs')
    report['IAT_actual_fields']=observation['IAT_fields']
    report['producer_prior_quarantines']=copy.deepcopy(observation['producer_prior_quarantines'])
    report['producer_new_blocked']=copy.deepcopy(observation['producer_new_blocked'])
    report['uuid_sdk_identity']=copy.deepcopy(sdk_identity)
    report['wave14_observation_sha256']='b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185'
    report['wave14_observation_peer_sha256']='6fb2797b42d8c874b901461a900867c62aee64badf13ab6148b7b69a1d47b8fd'
    return report,output


def _validate_observation_peer(peer):
    _require(type(peer) is dict and peer.get('kind')=='independent-wave14-combined-observer-outcome-review' and
      type(peer.get('schema_version')) is int and peer['schema_version']==1 and
      peer.get('status')=='accepted-derived-metadata-only', 'observer peer scope differs')
    expected={'receipt_sha256':'b6538d8aa9aff10826da60703500a7cc8b374d5efed6cced3e41debba7332185',
      'fields_sha256':'73a57a716b97cf116e625f2a585039a494b7d8a06293be5810672d229b211075',
      'fields_canonical_sha256':'08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4',
      'source_input_review_sha256':'c068b0d4d82a7f65d32adde62c48cf2fa22173d350754c372deb2e6c6e440f14',
      'terminal_sha256':'e32cfe071bb5f161df795528432f8c0170ca85b2976cff1412b3535a69df1d5d',
      'stdout_sha256':'aceb68ac8ec9574c9d04728fa669363d90ed389e8f9c1368ad000c8638f364bf'}
    _require(all(peer.get(k)==v for k,v in expected.items()) and
      all(type(peer.get(k)) is int and peer[k]==v for k,v in
       (('complete_field_count',46292),('selected_game_function_candidates',14555),
        ('iat_field_count',416),('binding_rows',29428))) and
      all(peer.get(k) is False for k in ('application_cohort_adopted','native_tools_run','runtime_eligible')),
      'observer peer evidence differs')


def _validate_crt_consumer_peer(peer):
    _require(type(peer) is dict and peer.get('kind')=='V14-existing-four-CRT-pure-consumer-review' and
       peer.get('status')=='approved' and peer.get('reviewer')=='crt_lane_04', 'CRT consumer review differs')
    expected={'plan_sha256':'e832d09148559e859cb4358530407edb0be39fa678d5ad4e0c524dc587e2a7be',
       'review_sha256':'e18ef6adc4c878240c4daad02e1d2fbaaed925a59740916ad298569d548f9e25',
       'response_sha256':'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a'}
    _require(all(peer.get(k)==v for k,v in expected.items()) and
       all(type(peer.get(k)) is int and peer[k]==v for k,v in
         (('complete_input_fields',46292),('potential_alias_field_count',204),('enabled_alias_field_count',204),
          ('enabled_alias_count',4),('inherited_tokens_to_remove_count',4))) and
       peer.get('alias_use_counts')==[103,97,1,3] and
       all(peer.get(k) is True for k in ('actual_full_field_validation','actual_namespace_validation',
         'actual_cookie_collision_rejected','unapproved_framehandler_dynamiccast_unaliased',
         'qualified_UUID_negative_flags_preserved','third_own_source_bound')) and
       all(peer.get(k) is False for k in ('allow_native','allow_game_execution','runtime_ABI_approved')),
       'CRT consumer review evidence differs')


def _validate_crt_peer_bindings(peer,*input_maps):
    by_path={}
    for mapping in input_maps:
        _require(type(mapping) is dict,'bound peer input map required')
        for row in mapping.values():
            path,sha=row['path'],row['sha256']
            _require(path not in by_path or by_path[path]==sha,'conflicting peer path pins')
            by_path[path]=sha
    for key,prefix in (('sources',''),('inputs','build/rebuild/')):
        _require(type(peer[key]) is dict and peer[key], 'CRT peer bindings missing')
        for path,sha in peer[key].items():
            _require(by_path.get(prefix+path)==sha,'CRT peer source/input not bound')

if __name__=='__main__':main()
