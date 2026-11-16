"""Prepare an import-only successor of V10; no Game/native execution."""
import argparse,gzip,importlib,json
from pathlib import Path
import application_link_diagnostic as diagnostic
import application_wave10_diagnostic as predecessor
import application_import34_inputs as joins
import normal_import_archive as import_archive
ROOT=Path(__file__).resolve().parents[2]

def require(ok,message):
    if not ok:raise ValueError(message)

def response_tokens(text,old_out,out,replacement,prior_IAT,prior_CRT,allowed_IAT,new_IAT,new_CRT):
    lines=text.splitlines();require(all(len(t)>2 and t.startswith('"') and t.endswith('"') for t in lines),'quoted baseline response required');tokens=[t[1:-1] for t in lines]
    for old,new in [('/OUT:'+str(old_out/'diagnostic.exe'),'/OUT:'+str(out/'diagnostic.exe')),('/MAP:'+str(old_out/'diagnostic.map'),'/MAP:'+str(out/'diagnostic.map')),replacement]:
        require(tokens.count(old)==1 and new not in tokens,'exact selected old token and fresh replacement required');tokens[tokens.index(old)]=new
    require(len(prior_IAT)==31 and len(prior_CRT)==4 and len(set(prior_IAT+prior_CRT))==35 and len(allowed_IAT)==len(set(allowed_IAT))==34 and
        set(prior_IAT).issubset(allowed_IAT) and len(new_IAT)==len(set(new_IAT)) and set(new_IAT).issubset(allowed_IAT) and
        len(new_CRT)==len(set(new_CRT)) and set(new_CRT).issubset(prior_CRT),'only exact reviewed 34-cell and existingCRT subsets permitted')
    inherited=prior_IAT+prior_CRT;require(all(tokens.count(t)==1 for t in inherited),'complete inherited aliases required');tokens=[t for t in tokens if t not in inherited]
    require(not any(t.startswith('/ALTERNATENAME:') for t in tokens),'unreviewed inherited alias')
    aliases=new_IAT+new_CRT;require(all(t.startswith('/ALTERNATENAME:') and t.count('=')==1 for t in aliases) and len({t.split('=',1)[0] for t in aliases})==len(aliases),'conflicting successor aliases')
    tokens+=aliases;diagnostic.response_text(tokens);return tokens

PINS={'tools/rebuild/application_frontier_inputs.py': '2f47fc9ec0893b1be1168c328f4418be8df340a6aec4c39354bf4fce32406cd2', 'tests/rebuild/test_application_frontier_inputs.py': 'fccd1ae08d51fb0969922552aa8d92afbe0dd872d305e0bfa1d4f321932f6514', 'tools/rebuild/import_kernel32_nine.py': '696903fd3d5affaf0158da5ccbed7278f05a3b1f3da775c331b72eab22cd3864', 'tools/rebuild/normal_import_archive.py': '42a0eff5852d89aaadb1f239baf3884e7a2dcd4216870407d7e8510a6d68bf28', 'tools/rebuild/application_link_diagnostic.py': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379', 'tools/rebuild/iat_field_annotations.py': '5ce0b3ae5069cde206b334bddc94515b308e611ef1cc269783cbd386fd778ae6', 'tests/rebuild/test_iat_field_annotations.py': 'fb8efec99e6e72761e7969997ba3665896c4afcfdea8dbb4e1a205c831da091b', 'tools/rebuild/application_wave8_diagnostic.py': '5643730f3031086829286d14c102e7a374da10f16cec187532a6ab89c3e09669', 'tools/rebuild/application_wave9_inputs.py': '27aab788d3b2ab887a2ff3eca2ba2cba98894110d261a71b0868b40e5cc8f596', 'tests/rebuild/test_application_wave9_inputs.py': '751926e1d81a8b191a896f2a35340dc91fd0f635307606abb85ba82162646d44', 'tools/rebuild/import_projection.py': 'b13a2e805950ff4dc79fdaa1a8d12b00bb8a9c171853d77180ddb069857df865', 'tools/rebuild/import_kernel32_extension.py': '15177c10e9b6469e0abab5c54e0ec6ef18afb9829cc275bef831795e9f358307', 'tools/rebuild/runtime_code_pool.py': '729f189e2893c7f3a3e3cd97df7d7381ac115169e1d75cf664e6bbc1c587b277', 'tools/rebuild/application_wave9_diagnostic.py': 'd54916fcb1880eea03217cf5067684cd9ddc02af18bfaab6fc5b63a3b0e65cc7', 'tools/rebuild/iat_code68_annotations.py': '199e3d51b1ce2eb0e64cb1f780b81c2231cbd8b91a5fdc0460d196b07d7beed9', 'tests/rebuild/test_iat_code68_annotations.py': '4bc339bfa55ac5c1fc18cb3449ccdbdf1e37f8dcad7c54b1d241e5a0214254e0', 'tools/rebuild/application_link_wave10.py': '0370d085d4c2eb411a927abef1e149623859b077c907146a4106e24903893c68', 'tests/rebuild/test_application_link_wave10.py': 'b108ef03889fba6c2374570034537393ff97cdf552116f632a25c822a514a8d0', 'tools/rebuild/application_wave10_diagnostic.py': 'd3a4b5ac465ed38ce5bbbd6e2ef67f41a3c53847dade2bdc348201ce5e67d308', 'tools/rebuild/application_import34_inputs.py': '67a6b3940e7a0949492b30a7a7cc881a9b83eb61654cb90e4fce8951696efa87', 'tests/rebuild/test_application_import34_inputs.py': '75cb5fbb5f62f5d1b942f442d9fed92426c6d14be0815cddb570677b5efd6404', 'build/rebuild/application-import34-inputs-independent-review.json': '6dc1941a0523770937e6495505aa13f2629a50b926e6c129b36e490f05b6318c', 'docs/rebuild/APPLICATION-IMPORT34-DIAGNOSTIC.md': '04888b7031c7329620d0e4ce8b8e98520d889e15c88bbffb0c3ecd693590a739', 'build/rebuild/application-link-diagnostic-v10-wave/receipt.json': 'bd7f463f8bb14b2f113497db63b3d2eb2208b41d201bc7c2ca466fa69ff70823', 'build/rebuild/application-link-diagnostic-v10-wave/link.rsp': '5fbb75c7441f2c66cefbff126d39a3dc74f2bbfed474bcecca857c7dfcbb3004', 'build/rebuild/application-link-diagnostic-v10-wave/link-receipt.json.gz': 'c64903ba8610368a3447574f073729edb8d8614792066d6a052485e5691279b5', 'build/rebuild/application-link-diagnostic-v10-wave/independent-outcome-review.json': 'a05ada7d2b8c8f33362fbc9462cbf2dbbf986ae682decf1788a272100faedfe2', 'build/rebuild/application-link-diagnostic-v10-wave/crt-plan-independent-outcome-review.json': 'b5271bc734e8f4d73c7e2fbe72d23af08639eae78d27be9d2daa37d512bb09e1', 'build/rebuild/application-wave10-cohort-observation-v1/receipt.json': 'd002831408a68ca88fe6adfedeb7288c0092bf7b818ea0be7d63a032994d0351', 'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz': '03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978', 'build/rebuild/application-wave10-cohort-observation-v1/independent-outcome-review.json': '8f093e34ada6f7c9e22900987ffbbfbf5182b5129b44e5ec838952a33443040f', 'tools/rebuild/assess_v10_imports.py': 'fe148aafdcd4af8dca5b89b2815df8acebbbc7832fbacdde6aa68b63d48a2a68'}
INPUT_PATHS={'crt_plan': 'build/rebuild/application-crt-v10-four-contract-v1.json', 'crt_review': 'build/rebuild/application-crt-v10-four-contract-peer-v1.json', 'crt_response': 'build/rebuild/application-crt-v10-four-proposal-v1.rsp', 'crt_consumer': 'tools/rebuild/crt_v10_four_alias_contract.py', 'crt_consumer_tests': 'tests/rebuild/test_crt_v10_four_alias_contract.py', 'crt_producer': 'tools/rebuild/crt_v10_four_alias_plan.py', 'crt_producer_tests': 'tests/rebuild/test_crt_v10_four_alias_plan.py', 'crt_consumer_peer': 'build/rebuild/crt-v10-four-consumer-peer-v1.json', 'import_producer': 'tools/rebuild/import_kernel32_fifteen.py', 'import_producer_tests': 'tests/rebuild/test_import_kernel32_fifteen.py', 'import_request': 'build/rebuild/import-kernel32-fifteen-v1/preparation.json', 'import_request_peer': 'build/rebuild/import-kernel32-fifteen-v1/independent-source-input-review.json', 'import_native': 'build/rebuild/import-kernel32-fifteen-native-v1/collection.json', 'import_native_peer': 'build/rebuild/import-kernel32-fifteen-native-v1/independent-outcome-review.json', 'kernel_library': 'build/rebuild/import-kernel32-fifteen-native-v1/kernel32-fifteen.lib'}
IMPORT_ANCESTRY={'catalog': 'build/rebuild/import-plan-native-v3.json', 'assessment': 'build/rebuild/v10-import-assessment-v1/assessment.json', 'assessment_review': 'build/rebuild/v10-import-assessment-v1/independent-outcome-review.json', 'fields': 'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz', 'groups': 'build/rebuild/application-link-diagnostic-v10-wave/unresolved-groups.json', 'prior_native': 'build/rebuild/import-v8-four-native-v1/collection.json', 'prior_review': 'build/rebuild/import-v8-four-native-v1/independent-outcome-review.json'}

def native_evidence(receipt,request,request_sha256,parsed,producer,originals,expected_sources):
    core,definition=producer.prepare(originals['catalog'],originals['assessment'],originals['assessment_review'],originals['prior_native'])
    expected_request=dict(core,inputs={key+'_sha256':value for key,value in producer.PINS.items()},source_sha256=expected_sources)
    require(request==expected_request,'complete Kernel15 source/request evidence replay differs')
    expected=producer.reconcile(request,parsed,request_sha256)
    require(all(key in receipt and receipt[key]==value for key,value in expected.items()) and receipt.get('all_inputs_tools_sources_stable') is True,'actual Kernel15 native evidence/stability differs')
    return expected

def selected_kernel_replacement(repository,paths,request,baseline_text,baseline_bindings):
    old=repository/'build/rebuild/import-v8-four-native-v1/kernel32-twelve.lib'
    require(request['replacement']['old_library']=='kernel32-twelve.lib' and request['replacement']['new_library']=='kernel32-fifteen.lib' and old.resolve()==old and
        baseline_text.splitlines().count('"'+str(old)+'"')==1,'exact old selected Kernel12 token required')
    require(any(row.get('requested_path')==str(old) and row.get('path')==str(old) and row.get('sha256')==request['replacement']['old_library_sha256'] for row in baseline_bindings) and
        diagnostic.file_hash(old)==request['replacement']['old_library_sha256'],'old Kernel12 selected physical ancestry differs')
    return str(old),str(paths['kernel_library'])

def inherited_identity_coverage(observed,inherited):
    checked={diagnostic.canonical(row) for row in inherited}
    require(all(diagnostic.canonical(row) in checked for row in observed),'sealed full-cohort identities not all present in inherited checked inputs')

def prepare(repository,out,source_sha256,tests_sha256,input_path,input_sha256):
    repository=Path(repository).resolve();out=Path(out).absolute();input_path=Path(input_path).absolute()
    require(out.resolve()==out and out.parent==repository/'build/rebuild' and not out.exists(),'exclusive private output required')
    require(input_path.resolve()==input_path and input_path.parent==repository/'build/rebuild' and diagnostic.file_hash(input_path)==input_sha256,'exact reviewed private request required')
    bindings=[]
    def bind(path,expected):
        path=Path(path);require(diagnostic.file_hash(path)==expected,'bound source/input differs: '+str(path));bindings.append(diagnostic.identity(path));return path
    pins=predecessor.foundation.source_pins(diagnostic.SOURCE_PINS,PINS)
    pins.update({'tools/rebuild/application_import34_diagnostic.py':source_sha256,'tests/rebuild/test_application_import34_diagnostic.py':tests_sha256})
    for name,sha in pins.items():bind(repository/name,sha)
    request=json.loads(bind(input_path,input_sha256).read_text());require(request.get('kind')=='fixed-import34-diagnostic-inputs' and request.get('schema_version')==1 and set(request.get('inputs',{}))==set(INPUT_PATHS),'fixed import-only input request required')
    paths={}
    for key,relative in INPUT_PATHS.items():
        row=request['inputs'][key];require(set(row)=={'path','sha256'} and row['path']==relative,'fixed successor path required');paths[key]=bind(repository/relative,row['sha256'])
    old_out=repository/'build/rebuild/application-link-diagnostic-v10-wave';report=json.loads((old_out/'receipt.json').read_text())
    diagnostic.stable(report['input_bindings']);bindings.extend(report['input_bindings'])
    obs=json.loads((repository/'build/rebuild/application-wave10-cohort-observation-v1/receipt.json').read_text())
    inherited_identity_coverage(obs['input_bindings'],report['input_bindings'])
    producer=importlib.import_module('import_kernel32_fifteen');annotations=importlib.import_module('iat_code68_annotations');contract=importlib.import_module('crt_v10_four_alias_contract')
    with gzip.open(repository/'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz','rt',encoding='utf-8') as stream:fields=json.load(stream)
    require(len(fields)==obs['complete_field_count']==report['full_included_field_count']==45947 and report['selected_game_function_provider_count']==obs['selected_Game_function_candidates']==14476 and
        report['ordinary_prepared_count']==14471 and diagnostic.digest(diagnostic.canonical(sorted(fields,key=diagnostic.canonical)))==obs['fields_canonical_sha256'],'unchanged V10 field/provider snapshot differs')
    gate=contract.validate(paths['crt_plan'].read_bytes(),paths['crt_review'].read_bytes(),paths['crt_response'].read_bytes(),fields,obs['provider_namespace']['symbols'])
    require(gate==report['CRT_diagnostic_bindings'] and gate['alias_field_count']==202 and len(gate['tokens'])==4,'immutable V10 CRT contract differs')
    crt=json.loads(paths['crt_plan'].read_text())
    require(all(row['normal_provider']['archive_sha256']==report['default_libraries']['libcmt.lib']['sha256'] for row in crt['bindings']),'normal CRT provider differs')
    for name,sha in crt['inputs'].items():
        path=repository/'build/rebuild'/name;require(path.resolve().is_relative_to(repository/'build/rebuild'),'CRT ancestry outside private directory');bind(path,sha)
    for name,sha in crt['sources'].items():bind(repository/name,sha)
    bind(repository/'build/units.json',crt['units_sha256'])
    require(isinstance(crt.get('own_sources'),dict) and len(crt['own_sources'])==2,'two own source identities required')
    for name,sha in crt['own_sources'].items():
        path=repository/name;require(path.resolve().is_relative_to(repository/'src'),'own source outside source tree');bind(path,sha)
    originals={}
    for key,relative in IMPORT_ANCESTRY.items():
        path=bind(repository/relative,producer.PINS[key])
        if key!='fields':originals[key]=json.loads(path.read_text())
    for relative,sha in producer.HELPER_PINS.items():bind(repository/relative,sha)
    native_request=json.loads(paths['import_request'].read_text());receipt=json.loads(paths['import_native'].read_text())
    expected_sources=dict(producer.HELPER_PINS,**{'tools/rebuild/import_kernel32_fifteen.py':request['inputs']['import_producer']['sha256']})
    require(native_request['definition']['file']=='kernel32-fifteen.def','exact new DEF name required');bind(paths['import_request'].parent/'kernel32-fifteen.def',native_request['definition']['sha256'])
    parsed=import_archive.read_archive(paths['kernel_library'])
    native=native_evidence(receipt,native_request,request['inputs']['import_request']['sha256'],parsed,producer,originals,expected_sources)
    source_peer=json.loads(paths['import_request_peer'].read_text());native_peer=json.loads(paths['import_native_peer'].read_text())
    require(source_peer.get('kind')=='fnv-kernel32-fifteen-source-input-review' and type(source_peer.get('schema_version')) is int and source_peer['schema_version']==1 and source_peer.get('status')=='accepted_source_and_prepared_inputs_only' and
        source_peer.get('request_sha256')==request['inputs']['import_request']['sha256'] and source_peer.get('source_sha256')==native_request['source_sha256'],'Kernel15 source peer ancestry differs')
    require(native_peer.get('kind')=='fnv-kernel32-fifteen-independent-outcome-review' and type(native_peer.get('schema_version')) is int and native_peer['schema_version']==1 and native_peer.get('status')=='accepted_metadata_conformance_only' and
        native_peer.get('request_sha256')==request['inputs']['import_request']['sha256'] and native_peer.get('collection_sha256')==request['inputs']['import_native']['sha256'] and native_peer.get('library')==native['library'],'Kernel15 native peer ancestry differs')
    libraries={'kernel32-fifteen.lib':diagnostic.partial.native_archive(paths['kernel_library'].read_bytes())}
    selected_paths={'user32-sixteen.lib':'build/rebuild/import-v8-four-native-v1/user32-sixteen.lib','provider-000.lib':'build/rebuild/application-link-inputs-v2/provider-000.lib','provider-002.lib':'build/rebuild/application-link-inputs-v2/provider-002.lib'}
    baseline_text=(old_out/'link.rsp').read_text()
    require(len(native['unchanged_libraries'])==3 and {row['file'] for row in native['unchanged_libraries']}==set(selected_paths),'exact unchanged three native inputs required')
    for row in native['unchanged_libraries']:
        path=bind(repository/selected_paths[row['file']],row['sha256']);require(path.stat().st_size==row['bytes'] and baseline_text.splitlines().count('"'+str(path)+'"')==1 and
            any(b['requested_path']==str(path) and b['path']==str(path) and b['sha256']==row['sha256'] for b in report['input_bindings']),'unchanged selected library path/size/physical provenance differs')
        libraries[row['file']]=diagnostic.partial.native_archive(path.read_bytes())
    aliases=joins.import34_alias_census(native['proposed_pointer_aliases'],annotations.census_view(fields,originals['catalog']),originals['catalog'],libraries)
    require(len(aliases)==34 and all(row['original_IAT_va']!='0x00fdf488' for row in aliases),'exact Win32-only34 scope required; Steam remains unaliased')
    for row in aliases:
        row['evaluation_view_sha256']=diagnostic.digest(diagnostic.canonical(row['complete_actual_uses']))
        uses=[field for field in fields if field['canonical']==row['canonical']];require(len(uses)==row['use_count'],'normative/evaluation per-cell use count differs');row['complete_actual_uses']=uses;row['compact_proofs_preserved']=True
    prior_IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in report['aliases'] if row['enabled']]
    allowed_IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in aliases];new_IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in aliases if row['enabled']]
    replacement=selected_kernel_replacement(repository,paths,native_request,baseline_text,report['input_bindings']);bind(replacement[0],native_request['replacement']['old_library_sha256'])
    tokens=response_tokens(baseline_text,old_out,out,replacement,prior_IAT,report['CRT_diagnostic_bindings']['tokens'],allowed_IAT,new_IAT,gate['tokens'])
    mapped={row['canonical'] for row in aliases};unmapped={}
    for field in fields:
        if field['proof'].get('role')=='iat-cell' and field['canonical'] not in mapped:unmapped.setdefault(field['canonical'],[]).append(field)
    report.update(kind='fixed-V11-Win32-import34-diagnostic',status='prepared-no-native-LINK',input_bindings=bindings,command=[report['command'][0],'@'+str(out/'link.rsp')],aliases=aliases,
        CRT_diagnostic_bindings=gate,unmapped_IAT_cells=[dict(canonical=name,use_count=len(rows),original_bases=sorted({r['proof']['original_base'] for r in rows})) for name,rows in sorted(unmapped.items())],
        import_native_receipt_sha256=request['inputs']['import_native']['sha256'],import_preparation_sha256=request['inputs']['import_request']['sha256'],
        baseline_V10_actual_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v10-wave/link-receipt.json.gz'],input_request_sha256=input_sha256,
        native_LINK_performed=False,executable_execution=False,runtime_eligible=False,provider_adopted=False,link_ready=False,whole_DATA_included=False,unreviewed_CRT_aliases=[],
        no_Game_inputs_added_or_removed=True,Steam_remains_unaliased=True,Steam_provider_adopted=False)
    diagnostic.stable(bindings);out.mkdir();(out/'link.rsp').write_text(diagnostic.response_text(tokens),encoding='utf-8');report['response_sha256']=diagnostic.file_hash(out/'link.rsp')
    with (out/'receipt.json').open('x',encoding='utf-8') as stream:json.dump(report,stream,separators=(',',':'))
    diagnostic.stable(bindings);return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('source-sha256','tests-sha256','inputs','inputs-sha256','out'):parser.add_argument('--'+key,required=True)
    args=parser.parse_args();r=prepare(ROOT,args.out,args.source_sha256,args.tests_sha256,args.inputs,args.inputs_sha256)
    print(json.dumps(dict(status=r['status'],IAT_aliases=sum(row['enabled'] for row in r['aliases']),CRT_tokens=len(r['CRT_diagnostic_bindings']['tokens']),Game_providers=14476,Game_fields=45947,Steam_unaliased=True,native_LINK_performed=False)))
if __name__=='__main__':main()
