"""Prepare the fixed broader diagnostic cohort; no native tool invocation."""
import argparse
import gzip
import importlib
import json
from pathlib import Path

import application_link_diagnostic as diagnostic
import application_frontier_inputs as joins
import normal_import_archive as import_archive

ROOT = Path(__file__).resolve().parents[2]
PINS = {
 'docs/rebuild/APPLICATION-FRONTIER-DIAGNOSTIC.md':'84947d0d852d0f8098c7bf67c9cbabc3b30b488e90d4082e4150b4291fb387a4',
 'tools/rebuild/application_frontier_inputs.py':'2f47fc9ec0893b1be1168c328f4418be8df340a6aec4c39354bf4fce32406cd2',
 'tests/rebuild/test_application_frontier_inputs.py':'fccd1ae08d51fb0969922552aa8d92afbe0dd872d305e0bfa1d4f321932f6514',
 'tools/rebuild/import_kernel32_nine.py':'696903fd3d5affaf0158da5ccbed7278f05a3b1f3da775c331b72eab22cd3864',
 'tools/rebuild/normal_import_archive.py':'42a0eff5852d89aaadb1f239baf3884e7a2dcd4216870407d7e8510a6d68bf28',
 'tools/rebuild/application_link_diagnostic.py':'74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379',
 'build/rebuild/application-frontier-cohort-observation-v2/receipt.json':'284185702ca7db04e5447d14db74d2a230cd56cb84e6b56886cde90b46b81d83',
 'build/rebuild/application-frontier-cohort-observation-v2/independent-outcome-review.json':'c9e30fb9f5fb5c971516bf1a8df8fa504189fc13adef4aba9491fe98dab8ddc2',
 'build/rebuild/application-frontier-cohort-observation-v2/fields.json.gz':'02274272cb24b3de74079944fd50e1df05c0dc645e73a56b807fe44d62f1dd0b',
 'build/rebuild/application-link-diagnostic-v6-crt/receipt.json':'54165d0899e493556487e1406867d71de33cd7e1961d11a7e9d5ae5806299940',
 'build/rebuild/application-link-diagnostic-v6-crt/link.rsp':'b5852f6a9770ac296d01fa70d39915fb5b77208e618c9ac0398c236edb9a34ee',
 'build/rebuild/application-link-diagnostic-v6-crt/link-receipt.json':'50d56dbed059f38c075350eb3852f68b246878bd66632cc4ab32d8b95dba7fdd',
 'build/rebuild/application-link-diagnostic-v6-crt/independent-outcome-review.json':'80b00f8bab2c7f629adabc6c85be2a4c68dbb1593b4a8fa841403d6739d908dd',
 'build/rebuild/application-additional-code-native-conformance-v1/receipt.json':'b4be887d8363df90c53d00dbb9e9ef4be4a3273e60c92d6cf13571ceaf874c59',
 'build/rebuild/application-additional-code-native-conformance-v1/independent-outcome-review.json':'72b1ac690f7bc0db89c7055eb246062db7fe5488a9f9648e8e08bbfec300c3d6',
 'build/rebuild/import-kernel32-nine-v1/preparation.json':'92a5dc7185a95e1afac5856fba651322e48086ef20df11beca0e68afbf09d176',
 'build/rebuild/import-kernel32-nine-native-v1/collection.json':'a80e16739a2393a068d0da8ed5d9e4a1d165ccbfc5495e9e41830add98d35e0b',
 'build/rebuild/import-kernel32-nine-native-v1/kernel32-nine.lib':'fe222155feda5664e45f41014ecc9f5e08b91f436b7f2114293b72d457a7043e',
 'build/rebuild/import-kernel32-nine-native-v1/independent-outcome-review.json':'59f5cda6743dcffaa643a95e0d04b03cdf28fa771cfa75ccc526d8b65050e605',
}
CRT_PATHS = {
 'crt_plan':'build/rebuild/application-crt-frontier-contract-v2.json',
 'crt_review':'build/rebuild/application-crt-frontier-contract-peer-v2.json',
 'crt_response':'build/rebuild/application-crt-frontier-proposal-v2.rsp',
 'crt_consumer':'tools/rebuild/crt_frontier_adoption_contract.py',
 'crt_consumer_tests':'tests/rebuild/test_crt_frontier_adoption_contract.py',
 'crt_producer':'tools/rebuild/crt_frontier_adoption_plan.py',
 'crt_producer_tests':'tests/rebuild/test_crt_frontier_adoption_plan.py',
 'crt_consumer_peer':'build/rebuild/crt-frontier-consumer-peer-v1.json',
}

def require(ok, message):
    if not ok: raise ValueError(message)

def source_pins(*groups):
    result={}
    for group in groups:
        for name,sha in group.items():
            require(name not in result or result[name]==sha,'conflicting reviewed source pin: '+name)
            result[name]=sha
    return result

def response_tokens(text, old_out, out, old_kernel, new_kernel, additions, prior_IAT, prior_CRT, new_IAT, new_CRT):
    lines=text.splitlines()
    require(all(len(line)>2 and line.startswith('"') and line.endswith('"') for line in lines),'malformed baseline response')
    tokens=[line[1:-1] for line in lines]
    for old,new in [(str(old_kernel),str(new_kernel)),('/OUT:'+str(old_out/'diagnostic.exe'),'/OUT:'+str(out/'diagnostic.exe')),
                    ('/MAP:'+str(old_out/'diagnostic.map'),'/MAP:'+str(out/'diagnostic.map'))]:
        require(tokens.count(old)==1,'one exact baseline library/output token required')
        tokens[tokens.index(old)]=new
    require(len(prior_IAT)==26 and len(prior_CRT)==4 and len(new_CRT)<=4 and set(new_CRT).issubset(prior_CRT),'fixed previous CRT/import scope and enabled CRT subset required')
    removed=prior_IAT+prior_CRT
    require(len(set(removed))==30 and all(tokens.count(token)==1 for token in removed),'previous alias response differs')
    tokens=[token for token in tokens if token not in removed]
    require(not any(token.startswith('/ALTERNATENAME:') for token in tokens),'unreviewed baseline alias')
    require(len(additions)==3 and len(set(additions))==3 and not set(additions).intersection(tokens),'additional component duplicate')
    aliases=new_IAT+new_CRT
    require(len({token.split('=',1)[0] for token in aliases})==len(aliases) and all(token.startswith('/ALTERNATENAME:') and '=' in token for token in aliases),'duplicate/conflicting successor alias')
    tokens += additions + aliases
    diagnostic.response_text(tokens)
    return tokens

def prepare(repository,out,source_sha256,tests_sha256,input_path,input_sha256):
    repository=Path(repository).resolve();out=Path(out).absolute();input_path=Path(input_path).absolute()
    require(out.resolve()==out and out.parent==repository/'build/rebuild' and not out.exists(),'exclusive direct private output required')
    require(input_path.resolve()==input_path and input_path.parent==repository/'build/rebuild' and diagnostic.file_hash(input_path)==input_sha256,'exact private input request required')
    bindings=[]
    def bind(path,expected):
        path=Path(path)
        require(diagnostic.file_hash(path)==expected,'bound source/input differs: '+str(path))
        bindings.append(diagnostic.identity(path));return path
    pins=source_pins(diagnostic.SOURCE_PINS,PINS,joins.nine.HELPER_PINS)
    pins.update({'tools/rebuild/application_frontier_diagnostic.py':source_sha256,'tests/rebuild/test_application_frontier_diagnostic.py':tests_sha256})
    for name,sha in pins.items():bind(repository/name,sha)
    bind(input_path,input_sha256);request=json.loads(input_path.read_text())
    require(request.get('kind')=='fixed-frontier-diagnostic-CRT-inputs' and request.get('schema_version')==1 and set(request.get('inputs',{}))==set(CRT_PATHS),'fixed reviewed CRT input request required')
    paths={}
    for key,relative in CRT_PATHS.items():
        row=request['inputs'][key]
        require(set(row)=={'path','sha256'} and row['path']==relative,'fixed CRT input path required')
        paths[key]=bind(repository/relative,row['sha256'])
    # Both newly imported CRT modules are bound before import, including the
    # producer imported by its pure consumer. They never invoke native tools.
    contract=importlib.import_module('crt_frontier_adoption_contract')
    obs=json.loads((repository/'build/rebuild/application-frontier-cohort-observation-v2/receipt.json').read_text())
    diagnostic.stable(obs['input_bindings']);bindings.extend(obs['input_bindings'])
    with gzip.open(repository/'build/rebuild/application-frontier-cohort-observation-v2/fields.json.gz','rt') as stream:fields=json.load(stream)
    require(len(fields)==obs['complete_field_count']==44540 and obs['selected_Game_function_candidates']==14345 and obs['ordinary_prepared_count']==14341,'exact broader field/provider census required')
    require(diagnostic.digest(diagnostic.canonical(sorted(fields,key=diagnostic.canonical)))==obs['fields_canonical_sha256'],'full field fingerprint differs')
    gate=contract.validate(paths['crt_plan'].read_bytes(),paths['crt_review'].read_bytes(),paths['crt_response'].read_bytes(),fields,obs['provider_namespace']['symbols'])
    require(len(gate['tokens'])<=4 and gate['alias_field_count']==198,'reviewed broader CRT alias scope required')
    crt_plan=json.loads(paths['crt_plan'].read_text())
    for name,sha in crt_plan['inputs'].items():
        path=repository/'build/rebuild'/name
        require(path.resolve().is_relative_to(repository/'build/rebuild'),'CRT ancestry outside exact private metadata')
        bind(path,sha)
    for name,sha in crt_plan['sources'].items():bind(repository/name,sha)
    bind(repository/'build/units.json',crt_plan['units_sha256'])
    bind(repository/crt_plan['own_source']['path'],crt_plan['own_source']['sha256'])
    conformance=json.loads((repository/'build/rebuild/application-additional-code-native-conformance-v1/receipt.json').read_text());joins.native_component_scope(conformance)
    nine_request=json.loads((repository/'build/rebuild/import-kernel32-nine-v1/preparation.json').read_text())
    nine_receipt=json.loads((repository/'build/rebuild/import-kernel32-nine-native-v1/collection.json').read_text())
    library=repository/'build/rebuild/import-kernel32-nine-native-v1/kernel32-nine.lib'
    parsed=import_archive.read_archive(library)
    native=joins.native_nine_evidence(nine_receipt,nine_request,PINS['build/rebuild/import-kernel32-nine-v1/preparation.json'],parsed)
    catalog=json.loads((repository/'build/rebuild'/diagnostic.PINS['imports'][0]).read_text())
    require(diagnostic.file_hash(repository/'build/rebuild'/diagnostic.PINS['imports'][0])==diagnostic.PINS['imports'][1],'original import catalog differs')
    bind(repository/'build/rebuild'/diagnostic.PINS['imports'][0],diagnostic.PINS['imports'][1])
    native_libraries={'kernel32-nine.lib':diagnostic.partial.native_archive(library.read_bytes())}
    for row in native['unchanged_libraries']:
        path=repository/'build/rebuild/import-native-main-v2'/row['library'];bind(path,row['sha256'])
        native_libraries[row['library']]=diagnostic.partial.native_archive(path.read_bytes())
    aliases=joins.frontier_alias_census(native['proposed_pointer_aliases'],fields,catalog,native_libraries)
    require(len(aliases)==27 and sum(row['proof'].get('role')=='iat-cell' for row in fields)==399,'complete IAT candidate/cohort scope differs')
    old_out=repository/'build/rebuild/application-link-diagnostic-v6-crt';report=json.loads((old_out/'receipt.json').read_text())
    diagnostic.stable(report['input_bindings']);bindings.extend(report['input_bindings'])
    require(gate['inherited_tokens_to_remove']==report['CRT_diagnostic_bindings']['tokens'],'CRT inherited-token removal scope differs')
    require(all(binding['normal_provider']['archive_sha256']==report['default_libraries']['libcmt.lib']['sha256']
        for binding in crt_plan['bindings']),'broader CRT provider differs from selected normal LIBCMT')
    prior_IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in report['aliases'] if row['enabled']]
    new_IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in aliases if row['enabled']]
    added=[repository/'build/rebuild/ordinary-relocation-first3-v1/ordinary-relocation.lib',repository/'build/rebuild/composed-relocation-first12-v1/typed-composed.lib',repository/'build/rebuild/parent-eh-file-projection-v1/component.obj']
    tokens=response_tokens((old_out/'link.rsp').read_text(),old_out,out,repository/'build/rebuild/import-kernel32-extension-native-v1/kernel32-eight.lib',library,list(map(str,added)),prior_IAT,report['CRT_diagnostic_bindings']['tokens'],new_IAT,gate['tokens'])
    provenance={name:[row for row in group if not row.get('proof')] for name,group in report['provenance'].items()}
    for provider in obs['extra_providers']:provenance.setdefault(provider['canonical'],[]).append(provider)
    for field in fields:provenance.setdefault(field['canonical'],[]).append(field)
    report.update(kind='fixed-broader-frontier-link-diagnostic',status='prepared-no-native-LINK',input_bindings=bindings,
        command=[report['command'][0],'@'+str(out/'link.rsp')],provenance=provenance,aliases=aliases,
        selected_supplementary_providers=report['selected_supplementary_providers']+obs['extra_providers'],
        selected_game_function_provider_count=14345,ordinary_prepared_count=14341,full_included_field_count=44540,
        CRT_diagnostic_bindings=gate,native_LINK_performed=False,executable_execution=False,runtime_eligible=False,
        provider_adopted=False,link_ready=False,whole_DATA_included=False,unreviewed_CRT_aliases=[],
        namespace_only=True,logical_CODE_address_only_aliases=[],IOTask_included=False,
        additional_native_conformance_sha256=PINS['build/rebuild/application-additional-code-native-conformance-v1/receipt.json'],
        kernel32_native_receipt_sha256=PINS['build/rebuild/import-kernel32-nine-native-v1/collection.json'],
        kernel32_preparation_sha256=PINS['build/rebuild/import-kernel32-nine-v1/preparation.json'],
        observation_sha256=PINS['build/rebuild/application-frontier-cohort-observation-v2/receipt.json'],
        baseline_V6_actual_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v6-crt/link-receipt.json'],
        input_request_sha256=input_sha256,
        deferred_components=[dict(component='IOTask-EH',selected=False,reason='outside fixed cohort')])
    diagnostic.stable(bindings);out.mkdir();(out/'link.rsp').write_text(diagnostic.response_text(tokens),encoding='utf-8')
    report['response_sha256']=diagnostic.file_hash(out/'link.rsp')
    with (out/'receipt.json').open('x') as stream:json.dump(report,stream,separators=(',',':'))
    diagnostic.stable(bindings);return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source-sha256','tests-sha256','inputs','inputs-sha256','out'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args();r=prepare(ROOT,args.out,args.source_sha256,args.tests_sha256,args.inputs,args.inputs_sha256)
    print(json.dumps(dict(status=r['status'],native_LINK_performed=False,eligible_IAT_cells=sum(row['enabled'] for row in r['aliases']),CRT_bindings=len(r['CRT_diagnostic_bindings']['tokens']),fields=44540)))

if __name__=='__main__':main()
