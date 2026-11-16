"""Prepare V12 plus accepted CODE56; no native operation or Game execution."""
import argparse
import gzip
import importlib
import json
from pathlib import Path

import application_link_cohort as cohort
import application_link_diagnostic as diagnostic
import application_comdat_diagnostic as predecessor
import application_wave8_diagnostic as foundation

ROOT = Path(__file__).resolve().parents[2]
require = cohort.require
source_pins = predecessor.source_pins
CRT_PATHS = {
    'crt_plan': 'build/rebuild/application-crt-v13-four-contract-v1.json',
    'crt_review': 'build/rebuild/application-crt-v13-four-contract-peer-v1.json',
    'crt_response': 'build/rebuild/application-crt-v13-four-proposal-v1.rsp',
    'crt_consumer': 'tools/rebuild/crt_v13_four_alias_contract.py',
    'crt_consumer_tests': 'tests/rebuild/test_crt_v13_four_alias_contract.py',
    'crt_producer': 'tools/rebuild/crt_v13_four_alias_plan.py',
    'crt_producer_tests': 'tests/rebuild/test_crt_v13_four_alias_plan.py',
    'crt_consumer_peer': 'build/rebuild/crt-v13-four-consumer-peer-v1.json'}
# Frozen actual observation peer will be added before independent input review.
PINS = {'tools/rebuild/application_link_frontier.py': 'b371e8eab1c7928395b990a8a5507d9a68c630e68b02d23247ee73ef79439d7c', 'tools/rebuild/application_link_cohort.py': 'a5feab657f68e7e0e0243250128d477358311d36dc10c23c5d71c88e0959ee32', 'tools/rebuild/application_link_diagnostic.py': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379', 'tools/rebuild/coff_code_archive.py': '76244d2d4dca4c1f8aa72224be1ef5c92f68976b5cda7d31b5cfe23d3cc29e64', 'tools/rebuild/iat_field_annotations.py': '5ce0b3ae5069cde206b334bddc94515b308e611ef1cc269783cbd386fd778ae6', 'tests/rebuild/test_iat_field_annotations.py': 'fb8efec99e6e72761e7969997ba3665896c4afcfdea8dbb4e1a205c831da091b', 'tools/rebuild/iat_code68_annotations.py': '199e3d51b1ce2eb0e64cb1f780b81c2231cbd8b91a5fdc0460d196b07d7beed9', 'tests/rebuild/test_iat_code68_annotations.py': '4bc339bfa55ac5c1fc18cb3449ccdbdf1e37f8dcad7c54b1d241e5a0214254e0', 'build/rebuild/application-link-diagnostic-v12-comdat-v2/receipt.json': '9dd9b2d6a8627cbbc98eeabadf32a03244645634f852fbd341c85bf3cf30998e', 'build/rebuild/application-link-diagnostic-v12-comdat-v2/independent-outcome-review.json': '2da9a6e506ead22b7177c13b460f2190117759b91a686b5e5a1119b8c37cbc17', 'build/rebuild/application-link-diagnostic-v12-comdat-v2/crt-plan-independent-outcome-review.json': 'aa5298385ff38d88340b1906c58ab78d83e9454026175bba861edf86dc05854c', 'build/rebuild/cached-frontier-code-v12-v1/CACHED-code.lib': 'b17b46d322063f4e30a9508317421435a8137d5250f1e2ca3d4f5a707017427c', 'build/rebuild/cached-frontier-code-v12-v1/members.json': '5c39833286b1b37f3fcbf9f483daaa8f5852b3bfc1620b9bb2b0732d2fd2581d', 'build/rebuild/cached-frontier-code-v12-v1/field-proofs.jsonl.gz': '57b1ccf51a71eec09b8aae405fc1f4593f55c0cbb48de348431bab76b08a05b5', 'build/rebuild/cached-frontier-code-v12-export-handoff-v1.json': '5150b751ae74e19c7850ddcc8608f0935afea984d22b907d950154963a0debcb', 'build/rebuild/code-lane01-analysis-v1/cached-frontier-code-v12-handoff-review-v1.json': '4264c15143b65197aedc3997e0faa59cb4235f3ee5027c63031f47efbfd921c0', 'build/rebuild/application-wave13-verifier-independent-review.json': '6c997ce04f33dff74bece022e1e6a891b31a5d2345e4ce7a3da6e9412c7ebb36', 'tools/rebuild/application_link_wave13.py': 'b5a61acc14d39a0c16683572c30013c56a1427b6971fdb4ab57f843f8ccb91ac', 'tests/rebuild/test_application_link_wave13.py': '94d471553bb4ec76c86a423b88913c7bb5c7d00224eb60c256e786992af1eb72', 'tools/rebuild/iat_code56_annotations.py': '67109cc15e51801ff2a18c2f169abbbede77417eb43af79d6093b3ef0cb485e9', 'tests/rebuild/test_iat_code56_annotations.py': '1aad3cf4680fcd959ff08b6414c638108e8386c3a0f3ffe6fcab7630ee7b69d1', 'build/rebuild/application-wave10-cohort-observation-v1/receipt.json': 'd002831408a68ca88fe6adfedeb7288c0092bf7b818ea0be7d63a032994d0351', 'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz': '03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978', 'build/rebuild/application-wave10-cohort-observation-v1/independent-outcome-review.json': '8f093e34ada6f7c9e22900987ffbbfbf5182b5129b44e5ec838952a33443040f', 'build/rebuild/cached-code56-native-conformance-v1/receipt.json': '9fa1dfcaf007cc71fe388735f2cf54b63d0515ae0610bf60477a88d8840867ca', 'build/rebuild/cached-code56-native-conformance-v1/independent-outcome-review.json': '7756cbd8d280e0bbf92eb2e68c501f762f801b9a8a8a250ff676746ebffd12a9', 'build/rebuild/application-wave13-cohort-observation-v1/receipt.json': 'e19302008032c9bb733eeaa32e2db1f075aa420ef5067332cf0857eaab094c69', 'build/rebuild/application-wave13-cohort-observation-v1/fields.json.gz': 'b7823e8892a4a5051d42b6447078058f5d0be4d3db0dc3bfbf5630621b73f23a', 'build/rebuild/application-wave13-cohort-observation-v1/independent-outcome-review.json': 'aecffece805bad88152f80a340a2074349795b59164390d7376df687c3d008ce', 'build/rebuild/application-link-diagnostic-v12-comdat-v2/link.rsp': '92e498b799f16535cb11e472d25091182696072e1ee04cdb0b5f58712fb42fd9', 'build/rebuild/application-link-diagnostic-v12-comdat-v2/link-receipt.json.gz': '6700a779ddbbfc58fd122d7e731d5424920bfb9561ce81a7500ba21c8be19405', 'tools/rebuild/application_comdat_diagnostic.py': '117b1bbe952bc808accfe8ae406b7348fe71033e234c31c738ef0c01bd1c00b7', 'docs/rebuild/APPLICATION-WAVE13-DIAGNOSTIC.md': '804212de8ca862eac6fa9678be00d00dafc6327877e2b80df3d7a7bf9a409585'}


def response_tokens(text, old_out, out, archive, prior_IAT, prior_CRT, IAT, CRT):
    lines = text.splitlines()
    require(all(len(t)>2 and t.startswith('"') and t.endswith('"') for t in lines), 'quoted baseline required')
    tokens = [t[1:-1] for t in lines]
    for key, filename in [('OUT','diagnostic.exe'),('MAP','diagnostic.map')]:
        old = '/'+key+':'+str(old_out/filename)
        new = '/'+key+':'+str(out/filename)
        require(tokens.count(old)==1 and new not in tokens, 'exact old destination required')
        tokens[tokens.index(old)] = new
    require(len(prior_IAT)==34 and len(prior_CRT)==4 and len(set(prior_IAT+prior_CRT))==38 and
            set(IAT).issubset(prior_IAT) and len(set(IAT))==len(IAT) and
            set(CRT).issubset(prior_CRT) and len(set(CRT))==len(CRT), 'only reviewed alias subsets allowed')
    inherited = prior_IAT+prior_CRT
    require(all(tokens.count(t)==1 for t in inherited) and
            {t for t in tokens if t.startswith('/ALTERNATENAME:')}==set(inherited), 'exact inherited aliases required')
    require(str(archive) not in tokens, 'new archive already present')
    tokens = [t for t in tokens if t not in inherited]
    tokens += [str(archive)]+IAT+CRT
    diagnostic.response_text(tokens)
    return tokens


def prepare(repository, out, source_sha, tests_sha, input_path, input_sha):
    repository = Path(repository).resolve()
    out = Path(out).absolute()
    input_path = Path(input_path).absolute()
    require(out.resolve()==out and out==repository/'build/rebuild/application-link-diagnostic-v13-code56' and
            not out.exists(), 'exclusive V13 output required')
    require(input_path.resolve()==input_path and input_path.parent==repository/'build/rebuild', 'exact private request required')
    bindings = []
    def bind(relative, sha):
        path = repository/relative
        require(path.resolve().is_relative_to(repository) and diagnostic.file_hash(path)==sha, 'bound input differs: '+relative)
        bindings.append(diagnostic.identity(path))
        return path
    for relative, sha in source_pins(diagnostic.SOURCE_PINS, predecessor.PINS, PINS).items():
        bind(relative, sha)
    bind('tools/rebuild/application_wave13_diagnostic.py',source_sha)
    bind('tests/rebuild/test_application_wave13_diagnostic.py',tests_sha)
    request = json.loads(bind(input_path.relative_to(repository).as_posix(),input_sha).read_bytes())
    require(type(request.get('schema_version')) is int and request['schema_version']==1 and
            request.get('kind')=='fixed-wave13-existing-four-CRT-inputs' and set(request['inputs'])==set(CRT_PATHS),
            'fixed CRT input request required')
    paths = {}
    for key, relative in CRT_PATHS.items():
        ref=request['inputs'][key]
        require(set(ref)=={'path','sha256'} and ref['path']==relative, 'fixed CRT path differs')
        paths[key]=bind(relative,ref['sha256'])
    def load(relative): return json.loads((repository/relative).read_bytes())
    old_out=repository/'build/rebuild/application-link-diagnostic-v12-comdat-v2'
    report=load('build/rebuild/application-link-diagnostic-v12-comdat-v2/receipt.json')
    diagnostic.stable(report['input_bindings']);bindings.extend(report['input_bindings'])
    obs=load('build/rebuild/application-wave13-cohort-observation-v1/receipt.json')
    diagnostic.stable(obs['input_bindings']);bindings.extend(obs['input_bindings'])
    with gzip.open(repository/'build/rebuild/application-wave13-cohort-observation-v1/fields.json.gz','rt',encoding='utf-8') as f:
        fields=json.load(f)
    require(len(fields)==obs['complete_field_count']==46237 and obs['selected_Game_function_candidates']==14533 and
            obs['ordinary_prepared_count']==14528 and obs['extra_field_count']==290 and
            diagnostic.digest(diagnostic.canonical(sorted(fields,key=diagnostic.canonical)))==obs['fields_canonical_sha256'],
            'complete V13 field/provider scope differs')
    normative=[r for group in report['provenance'].values() for r in group if r.get('proof')]
    require(len(normative)==45947 and sorted(normative,key=diagnostic.canonical)==
            sorted(fields[:45947],key=diagnostic.canonical), 'all old fields must remain exact')
    providers=[r for group in report['provenance'].values() for r in group if r.get('component')=='current-CODE-definition']
    require(len(providers)==12946, 'complete baseline definitions required')
    providers+=report['selected_supplementary_providers']
    providers.append(dict(component='actual-entry',member='application-entry.lib',canonical=diagnostic.partial.CANONICAL,
        recipe_id=diagnostic.partial.IDENTITY['recipe_id'],object_sha256=diagnostic.partial.IDENTITY['object_sha256'],
        symbol_index=diagnostic.partial.IDENTITY['symbol_index'],original_address='0x0086a850'))
    other=[name for name,kind in obs['provider_namespace']['symbols'].items() if kind=='existing-noncode']
    added=obs['extra_providers']
    require(len(providers)==14477 and len(added)==56 and cohort.disjoint_providers([added],baseline_providers=providers,
        existing_noncode_definitions=other)==obs['provider_namespace'], 'fresh full namespace differs')
    foundation.native_scope(load('build/rebuild/cached-code56-native-conformance-v1/receipt.json'),
        'cached-code56','cached-code56-native-conformance-v1',
        'b17b46d322063f4e30a9508317421435a8137d5250f1e2ca3d4f5a707017427c',56,290)
    contract=importlib.import_module('crt_v13_four_alias_contract')
    gate=contract.validate(paths['crt_plan'].read_bytes(),paths['crt_review'].read_bytes(),
        paths['crt_response'].read_bytes(),fields,obs['provider_namespace']['symbols'])
    require(gate['alias_field_count']==202 and gate['inherited_tokens_to_remove']==report['CRT_diagnostic_bindings']['tokens'],
            'existing-four CRT scope differs')
    crt=json.loads(paths['crt_plan'].read_bytes())
    for relative,sha in crt['sources'].items():bind(relative,sha)
    for relative,sha in crt['inputs'].items():bind('build/rebuild/'+relative,sha)
    bind('build/units.json',crt['units_sha256'])
    require(type(crt.get('own_sources')) is dict and len(crt['own_sources'])==2, 'two own sources required')
    for relative,sha in crt['own_sources'].items():
        require((repository/relative).resolve().is_relative_to(repository/'src'),'own source outside source tree')
        bind(relative,sha)
    require(all(row['normal_provider']['archive_sha256']==report['default_libraries']['libcmt.lib']['sha256']
                for row in crt['bindings']), 'selected normal CRT library differs')
    old=importlib.import_module('application_import34_diagnostic')
    producer=importlib.import_module('import_kernel32_fifteen')
    annotations=importlib.import_module('iat_code56_annotations')
    originals={}
    for key,relative in old.IMPORT_ANCESTRY.items():
        path=bind(relative,producer.PINS[key])
        if key!='fields':originals[key]=json.loads(path.read_bytes())
    native_request=load(old.INPUT_PATHS['import_request']);native=load(old.INPUT_PATHS['import_native'])
    sources=source_pins(producer.HELPER_PINS,{'tools/rebuild/import_kernel32_fifteen.py':predecessor.PINS['tools/rebuild/import_kernel32_fifteen.py']})
    parsed=old.import_archive.read_archive(repository/old.INPUT_PATHS['kernel_library'])
    reconciled=old.native_evidence(native,native_request,predecessor.PINS[old.INPUT_PATHS['import_request']],parsed,producer,originals,sources)
    selected={'kernel32-fifteen.lib':old.INPUT_PATHS['kernel_library'],
        'user32-sixteen.lib':'build/rebuild/import-v8-four-native-v1/user32-sixteen.lib',
        'provider-000.lib':'build/rebuild/application-link-inputs-v2/provider-000.lib',
        'provider-002.lib':'build/rebuild/application-link-inputs-v2/provider-002.lib'}
    text=(old_out/'link.rsp').read_text()
    libraries={}
    for row in [reconciled['library']]+reconciled['unchanged_libraries']:
        path=bind(selected[row['file']],row['sha256'])
        require(path.stat().st_size==row['bytes'] and text.splitlines().count('"'+str(path)+'"')==1 and
            any(b['requested_path']==str(path) and b['path']==str(path) and b['sha256']==row['sha256']
                for b in report['input_bindings']), 'selected native library physical provenance differs')
        libraries[row['file']]=diagnostic.partial.native_archive(path.read_bytes())
    aliases=old.joins.import34_alias_census(reconciled['proposed_pointer_aliases'],
        annotations.census_view(fields,originals['catalog']),originals['catalog'],libraries)
    for row in aliases:
        row['evaluation_view_sha256']=diagnostic.digest(diagnostic.canonical(row['complete_actual_uses']))
        uses=[field for field in fields if field['canonical']==row['canonical']]
        require(len(uses)==row['use_count'],'normative IAT use count differs')
        row['complete_actual_uses']=uses;row['compact_proofs_preserved']=True
    require(len(aliases)==34 and sum(row['use_count'] for row in aliases)==240,'fresh IAT34/240 scope differs')
    prior_IAT=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in report['aliases'] if r['enabled']]
    allowed=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in aliases]
    require(set(prior_IAT)==set(allowed), 'no new or changed IAT alias permitted')
    IAT=['/ALTERNATENAME:'+r['canonical']+'='+r['native_pointer'] for r in aliases if r['enabled']]
    archive=repository/'build/rebuild/cached-frontier-code-v12-v1/CACHED-code.lib'
    tokens=response_tokens(text,old_out,out,archive,prior_IAT,gate['inherited_tokens_to_remove'],IAT,gate['tokens'])
    for provider in added:report['provenance'].setdefault(provider['canonical'],[]).append(provider)
    for field in fields[45947:]:report['provenance'].setdefault(field['canonical'],[]).append(field)
    report['selected_supplementary_providers'].extend(added)
    report.update(kind='fixed-V13-CODE56-diagnostic',status='prepared-no-native-LINK',input_bindings=bindings,
        command=[report['command'][0],'@'+str(out/'link.rsp')],aliases=aliases,CRT_diagnostic_bindings=gate,
        selected_game_function_provider_count=14533,ordinary_prepared_count=14528,
        full_included_field_count=46237,IAT_actual_fields=414,wave13_namespace=obs['provider_namespace'],
        wave13_observation_sha256=PINS['build/rebuild/application-wave13-cohort-observation-v1/receipt.json'],
        CODE56_native_conformance_sha256=PINS['build/rebuild/cached-code56-native-conformance-v1/receipt.json'],
        CODE56_final_handoff_sha256=PINS['build/rebuild/cached-frontier-code-v12-export-handoff-v1.json'],
        CODE56_fullproof_ledger_sha256=PINS['build/rebuild/cached-frontier-code-v12-v1/field-proofs.jsonl.gz'],
        baseline_V12_prepared_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v12-comdat-v2/receipt.json'],
        one_CODE56_archive_added=True,native_LINK_performed=False,executable_execution=False,runtime_eligible=False,
        provider_adopted=False,link_ready=False,Steam_remains_unaliased=True)
    diagnostic.stable(bindings)
    out.mkdir();(out/'link.rsp').write_text(diagnostic.response_text(tokens),encoding='utf-8')
    report['response_sha256']=diagnostic.file_hash(out/'link.rsp')
    with (out/'receipt.json').open('x',encoding='utf-8') as f:json.dump(report,f,separators=(',',':'))
    diagnostic.stable(bindings)
    return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-sha256',required=True);p.add_argument('--tests-sha256',required=True)
    p.add_argument('--inputs',required=True);p.add_argument('--inputs-sha256',required=True)
    a=p.parse_args();result=prepare(ROOT,ROOT/'build/rebuild/application-link-diagnostic-v13-code56',
        a.source_sha256,a.tests_sha256,a.inputs,a.inputs_sha256)
    print(json.dumps({'status':result['status'],'native_LINK_performed':False}))


if __name__=='__main__':main()
