"""Prepare one typed COMDAT addition to the accepted V11 diagnostic cohort."""
import argparse
import gzip
import importlib
import json
from pathlib import Path

import application_link_diagnostic as diagnostic
import application_link_cohort as cohort

ROOT = Path(__file__).resolve().parents[2]
HELPER_PINS = {'build/rebuild/root-certificate-composer-v1/source-freeze-v1/root_certificate_composer.py': '0e2f3ec93515c6fbe5d7dcf0ae03f9668f8fd58da6930ac875214e5994e7c745', 'tools/rebuild/bulk_code_pool.py': '4e6d697c1881c56c4c3f6a84788df6e0e2617b284d8e0226805828829bce49ed', 'tools/rebuild/centralordinary_root_collect.py': '97c827795e46c6d1e6558f6e785266b4e908ddb4c5cf253ec61a71ef19d51409', 'tools/rebuild/coff_code_archive.py': '76244d2d4dca4c1f8aa72224be1ef5c92f68976b5cda7d31b5cfe23d3cc29e64', 'tools/rebuild/coff_inventory.py': '3518c044738046e7cd9c8be37a3b1077af750fb2e7a19db793b09999a07ee0d2', 'tools/rebuild/coff_rewrite.py': '48cea438b05a1c2de992eea4200b45a1eb14e49a27704a5c6fff98f941b1ae4c', 'tools/rebuild/comdat_any_code_omission.py': 'd9e283ee6b63c5d3913bd61ffaa92bb80e1618989da9899bb6a15f69953dea10', 'tools/rebuild/comdat_any_code_projection.py': 'be4fe7b811316630fd77649162d66912580d4516389fc42f50b5870b9ebf7fb7', 'tools/rebuild/comdat_any_frontier_contexts.py': '0b306c51c32626714b48058c42160c0efc9371b95c49bb80d8f908932b9bbda1', 'tools/rebuild/comdat_any_frontier_factory.py': 'fbe593a9d5a9125be130dd73d424202a2a6b15b77bebde079f4a8abe1ecf0734', 'tools/rebuild/comdat_any_frontier_observer.py': '744bf379942e960e2ec170dd325b54eb51713e873bc2e8bf5ba5799345ffc625', 'tools/rebuild/comdat_any_root_composer.py': '243559315e7d3a3799d3e5d8e582973406dcc0a481a80c9af74d7ac7ef8b3e5d', 'tools/rebuild/composed_relocation_factory.py': '34e9ad9ccfb10943c2fc4c10ea57e28dae8312dc442621ed8045cbeb2b649477', 'tools/rebuild/current_code_frontier.py': '34ad6b6aacf0a9c5b0cfd68cf26fdd57e18cec4f9b74e24b48296049703397bc', 'tools/rebuild/frontier_root_collect_v3.py': 'b03bb96c147ba4233832ad539bcc60bc7478fc1cc0038965c8c9f587cb688bce', 'tools/rebuild/ordinary_code_projection.py': 'e01437aed27549d8892035d3ea7f1500a5e15150bb14a8d56db95ff17c1dac8d', 'tools/rebuild/ordinary_relocation_factory.py': 'f431d8599d7e91e2c67ed5570ccd067bdf80fbd8a92ee4c6daa3473cc26c928b', 'tools/rebuild/ordinary_relocation_projection.py': '30e149e02e4ba514cf5bf4ad6dce41625a46df19c2585874c90e97305ee3c732', 'tools/rebuild/root_code_closure.py': '4bfdb5001380a3d7e5db7517033285d49ab211be68e2fcba15964f0ad5b03c53', 'tools/rebuild/runtime_code_inventory.py': 'c2fdbd52b4b7f4b7c68f9d80ad03708ba57d42b29e5938dfcf9769366a1ffd0b', 'tools/rebuild/runtime_code_pool.py': '729f189e2893c7f3a3e3cd97df7d7381ac115169e1d75cf664e6bbc1c587b277', 'tools/rebuild/scalableordinary_root_collect.py': 'e7e5b45df15af0a2bd5cb4a65b36d85ca21eb753656714c0a9a5d8dd919e58ad'}
PINS = {'tools/rebuild/application_frontier_inputs.py': '2f47fc9ec0893b1be1168c328f4418be8df340a6aec4c39354bf4fce32406cd2', 'tests/rebuild/test_application_frontier_inputs.py': 'fccd1ae08d51fb0969922552aa8d92afbe0dd872d305e0bfa1d4f321932f6514', 'tools/rebuild/import_kernel32_nine.py': '696903fd3d5affaf0158da5ccbed7278f05a3b1f3da775c331b72eab22cd3864', 'tools/rebuild/normal_import_archive.py': '42a0eff5852d89aaadb1f239baf3884e7a2dcd4216870407d7e8510a6d68bf28', 'tools/rebuild/application_link_diagnostic.py': '74cca67c3ec414931f4bfb26403338734f87da5eb28952e2327d008cbb79b379', 'tools/rebuild/iat_field_annotations.py': '5ce0b3ae5069cde206b334bddc94515b308e611ef1cc269783cbd386fd778ae6', 'tests/rebuild/test_iat_field_annotations.py': 'fb8efec99e6e72761e7969997ba3665896c4afcfdea8dbb4e1a205c831da091b', 'tools/rebuild/application_wave8_diagnostic.py': '5643730f3031086829286d14c102e7a374da10f16cec187532a6ab89c3e09669', 'tools/rebuild/application_wave9_inputs.py': '27aab788d3b2ab887a2ff3eca2ba2cba98894110d261a71b0868b40e5cc8f596', 'tests/rebuild/test_application_wave9_inputs.py': '751926e1d81a8b191a896f2a35340dc91fd0f635307606abb85ba82162646d44', 'tools/rebuild/import_projection.py': 'b13a2e805950ff4dc79fdaa1a8d12b00bb8a9c171853d77180ddb069857df865', 'tools/rebuild/import_kernel32_extension.py': '15177c10e9b6469e0abab5c54e0ec6ef18afb9829cc275bef831795e9f358307', 'tools/rebuild/runtime_code_pool.py': '729f189e2893c7f3a3e3cd97df7d7381ac115169e1d75cf664e6bbc1c587b277', 'tools/rebuild/application_wave9_diagnostic.py': 'd54916fcb1880eea03217cf5067684cd9ddc02af18bfaab6fc5b63a3b0e65cc7', 'tools/rebuild/iat_code68_annotations.py': '199e3d51b1ce2eb0e64cb1f780b81c2231cbd8b91a5fdc0460d196b07d7beed9', 'tests/rebuild/test_iat_code68_annotations.py': '4bc339bfa55ac5c1fc18cb3449ccdbdf1e37f8dcad7c54b1d241e5a0214254e0', 'tools/rebuild/application_link_wave10.py': '0370d085d4c2eb411a927abef1e149623859b077c907146a4106e24903893c68', 'tests/rebuild/test_application_link_wave10.py': 'b108ef03889fba6c2374570034537393ff97cdf552116f632a25c822a514a8d0', 'tools/rebuild/application_wave10_diagnostic.py': 'd3a4b5ac465ed38ce5bbbd6e2ef67f41a3c53847dade2bdc348201ce5e67d308', 'tools/rebuild/application_import34_inputs.py': '67a6b3940e7a0949492b30a7a7cc881a9b83eb61654cb90e4fce8951696efa87', 'tests/rebuild/test_application_import34_inputs.py': '75cb5fbb5f62f5d1b942f442d9fed92426c6d14be0815cddb570677b5efd6404', 'build/rebuild/application-import34-inputs-independent-review.json': '6dc1941a0523770937e6495505aa13f2629a50b926e6c129b36e490f05b6318c', 'docs/rebuild/APPLICATION-IMPORT34-DIAGNOSTIC.md': '04888b7031c7329620d0e4ce8b8e98520d889e15c88bbffb0c3ecd693590a739', 'build/rebuild/application-link-diagnostic-v10-wave/receipt.json': 'bd7f463f8bb14b2f113497db63b3d2eb2208b41d201bc7c2ca466fa69ff70823', 'build/rebuild/application-link-diagnostic-v10-wave/link.rsp': '5fbb75c7441f2c66cefbff126d39a3dc74f2bbfed474bcecca857c7dfcbb3004', 'build/rebuild/application-link-diagnostic-v10-wave/link-receipt.json.gz': 'c64903ba8610368a3447574f073729edb8d8614792066d6a052485e5691279b5', 'build/rebuild/application-link-diagnostic-v10-wave/independent-outcome-review.json': 'a05ada7d2b8c8f33362fbc9462cbf2dbbf986ae682decf1788a272100faedfe2', 'build/rebuild/application-link-diagnostic-v10-wave/crt-plan-independent-outcome-review.json': 'b5271bc734e8f4d73c7e2fbe72d23af08639eae78d27be9d2daa37d512bb09e1', 'build/rebuild/application-wave10-cohort-observation-v1/receipt.json': 'd002831408a68ca88fe6adfedeb7288c0092bf7b818ea0be7d63a032994d0351', 'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz': '03c64e17917dfdacefbea440431fe52442da2bc0ea93fc2c19f4526044d78978', 'build/rebuild/application-wave10-cohort-observation-v1/independent-outcome-review.json': '8f093e34ada6f7c9e22900987ffbbfbf5182b5129b44e5ec838952a33443040f', 'tools/rebuild/assess_v10_imports.py': 'fe148aafdcd4af8dca5b89b2815df8acebbbc7832fbacdde6aa68b63d48a2a68', 'build/rebuild/application-crt-v10-four-contract-v1.json': '443fdd1ee0033d13d28566a31a24bce508367e58b42e93eb5010c6edcc86200d', 'build/rebuild/application-crt-v10-four-contract-peer-v1.json': 'f0ac503075579624346a2d13a16ed4d591c6bf473685dbc975cba9178ca41423', 'build/rebuild/application-crt-v10-four-proposal-v1.rsp': 'aaec970cae1dcf32699bda75317afbbcd4551c67252fca0d508d47eec997024a', 'tools/rebuild/crt_v10_four_alias_contract.py': '09b0dfcdd59fb2834dd2b798a70dbddb88641630c6003b5ccf690fdd49f6570d', 'tests/rebuild/test_crt_v10_four_alias_contract.py': '6f64218efca7dc6cb27d771b911a8c90a158b45f36b6afcb82a52bc303222f0e', 'tools/rebuild/crt_v10_four_alias_plan.py': 'b14e30e5bc3922281fabb54589f38378928dc228b9098f0f8f60a1dfb55b6d81', 'tests/rebuild/test_crt_v10_four_alias_plan.py': 'ea52bccf6ed00d82a7162a22112fc106869362993f2d1920675f18980c17a94d', 'build/rebuild/crt-v10-four-consumer-peer-v1.json': '4ffdddd38e108fa11f3a80490c91548dcf997a04688208019208f1292ad0270c', 'tools/rebuild/import_kernel32_fifteen.py': '57828dc1894e3fe5001cc14ad1aafb0f99d4043d41ce63df05e9bf76edd81d1f', 'tests/rebuild/test_import_kernel32_fifteen.py': '2ea148ae4a2d4260bb283846c542da5f09053344e2ddcd1e7b8e1623d6c21f8c', 'build/rebuild/import-kernel32-fifteen-v1/preparation.json': 'b4bd7a2683c6f99469d52f86f181ce40388df68fe9c9cb41fc0f1b9ad00464dc', 'build/rebuild/import-kernel32-fifteen-v1/independent-source-input-review.json': 'c4e45d292e089f3194046a9b7bffb7154282ffdc28c6b7ff9c23cb4bf06a3ff2', 'build/rebuild/import-kernel32-fifteen-native-v1/collection.json': '6824931642112f42877c75e51a8a34f705738070b49618b635aad7fa2bee10c1', 'build/rebuild/import-kernel32-fifteen-native-v1/independent-outcome-review.json': 'd3283033752d0c8ad33ff8173c1196cd3f07d9d4649e615bb4eb3c328299654d', 'build/rebuild/import-kernel32-fifteen-native-v1/kernel32-fifteen.lib': '7485983d540767fad6c69366f7b89c7943654fdfd4ef501067fbb43ff073fe04', 'tools/rebuild/application_import34_diagnostic.py': '25a856c6417e073fc1b8f9681c112f45071bd3c20841b2e055823b6a4ec8bbe6', 'tests/rebuild/test_application_import34_diagnostic.py': '2eb90ed37d2f949acb7d79181be80373411bf56b5b7ae36cae6230917c6d7143', 'tools/rebuild/application_typed_comdat.py': '0d33d5e00eddd63c40ee397de000749044c1252567a3fc70c654ddb88d0e4323', 'tests/rebuild/test_application_typed_comdat.py': 'cb44a23a96f05a44c61b1794091daad47e9b5cb5ca496d0a8d8da1fa08ba39c5', 'docs/rebuild/APPLICATION-TYPED-COMDAT.md': '5618d5d6cbacc9c9296b431fd52c85da0584c2f1216f7e439d96493c3a4d5865', 'build/rebuild/application-typed-comdat-source-independent-review.json': 'cca323a330f252e29a5aebf04e622fe25a1d2495557ebda6d4394fd8d815e2f0', 'build/rebuild/application-link-diagnostic-v11-import34/receipt.json': '4c660cce0f2c6988c7943f8d51ef0f2fd7a6324467347bfc7222814e015d2a69', 'build/rebuild/application-link-diagnostic-v11-import34/link.rsp': '0cc9a1dc49d5858dcb73e628a2b0bab57d37b7c9fad7ab89fb4803bcd63b8e2a', 'build/rebuild/application-link-diagnostic-v11-import34/link-receipt.json.gz': '7a3c8eae91177fa51c1f059004581d44f7451ccf04e453e8cd06281ab99cf289', 'build/rebuild/application-link-diagnostic-v11-import34/independent-outcome-review.json': 'de771fc26eb350a0450a55a04aa8abc24f838a689eaec520df3ffc12781377e6', 'build/rebuild/application-link-diagnostic-v11-import34/crt-plan-independent-outcome-review.json': 'd4ec1ae66b6d16a2789877634e9a8d1f18b316acb5db7dc3f1507b4881659115', 'build/rebuild/comdat-any-v8-export-handoff-v1.json': '94ff62e56cc259b04fa2499016075ebaed4754293d581c0d35abc62d2302b24a', 'build/rebuild/comdat-any-v8-candidate-request-v1.json': 'dd723c2c1ad94ba2e7ece7ab8ac5322dc3efd73cd5119fa20269b75aa409e25a', 'build/rebuild/comdat-any-native-conformance-v1/receipt.json': '5ae9725428ad1d162cf0eb9da61bba1790762ddc6a366dcb1aef514da7fea0eb', 'build/rebuild/comdat-any-native-conformance-v1/independent-outcome-review.json': 'a4aad40f652a92d032120da454977650784a97b07eabc0be3b2413000c47ed10', 'build/rebuild/code-lane-02/comdat-projection-handoff-review-v1.json': 'f622f5cd885dfe823c20c7d9b200a7d584bc1c625338a6ef031f50945db3b05c', 'build/rebuild/comdat-any-v8-projection-v1/COMDAT-ANY-code.lib': '65770b6f8ca4d549ec4211103f97cc4b3fd59a9fc15344ddfc85de198fd32fa7', 'build/rebuild/code-lane05-synthetic-projection-v1/comdat-any-v8-projection-outcome-authority-review-v1.json': '5a8b91f19025fdc32b4cefec72051e53e3e8426c5aa096eaf7f59b394ce0ec78', 'build/rebuild/comdat-any-v8-projection-v1/field-proofs.jsonl.gz': '28f3cbb9a34626466ddfac20afe9b7887e039bff5cce8e55e616313062f19eda', 'build/rebuild/code-lane-02/comdat-projection-outcome-review-v1.json': 'f3dc0b4f87ac7971c337e0515e6b4e71e411f426ba34086ae159ec38477be489', 'build/rebuild/comdat-any-v8-projection-v1/members.json': 'ba5df752e2ff7c3d8306c11585fbc6f1ec5f3202128cb786c5cb32eba3b7fb33', 'build/rebuild/code-lane05-synthetic-projection-v1/comdat-any-v8-observation-authority-outcome-review-v1.json': 'd875f577c8d411f13c89ea365aa53140c3517ad1b76074f1a7b803c881b155ec', 'build/rebuild/comdat-any-v8-observation-v1/observations.jsonl.gz': '82d711379b74c21c89891ec840a84b470bfba4f9933dac5303cdf7a77629e43c', 'build/rebuild/code-lane-02/comdat9-observer-outcome-review-v1.json': '529a838d6d3377749f30e5836f5c830f39b02699a053763a7485d6ee213cc9fd', 'build/rebuild/comdat-any-v8-observation-v1/receipt.json': '6a52f19cb3aaed9a7827190772338f3c169b98accda4d3151580784aebaef33e', 'build/rebuild/comdat-any-v8-post-outcome-docs-v1.json': '69ced683228e05b20089a55ed2b720d75c20a268e6d08f5df77be52039a131d9', 'build/rebuild/comdat-any-v8-projection-v1/receipt.json': '35cc2e79a30823a3dcab0073b54c1e56e1a3c74e70d4f5433d440c5ff63ad3e1', 'build/rebuild/comdat-any-v8-upstream-exclusions-v1.json': '58804ef4d799868edb2230a5acbfed379f5091b914c54d2a558640cbf9723abf', 'docs/rebuild/APPLICATION-COMDAT-DIAGNOSTIC.md': '3125c8176f651a4d4557bbc36147d0712a3018066f446575f967410333edc8f4', 'build/rebuild/application-comdat-failed-preparation-source-v1.py': 'efde434c1b332ee7574423cd6390796af5c9c3b53fd758b722567457963bea68', 'build/rebuild/application-comdat-prepare-v1-control/receipt.json': 'f31c11a44ad7aa51194f2a05ab4dc99b5cd3c30617f4cc920d9aa9f72ed013d0', 'build/rebuild/application-comdat-prepare-v1-control/stderr.txt': 'a4bae0f2c04389c7f406831df232f172fc50f2aacfaa62657365a05574bbef2e', 'build/rebuild/application-comdat-prepare-v1-request.json': '1f6bca195418c5ac0ce4033277932dc3079d15298d05ec4a67314294901aac85', 'build/rebuild/application-comdat-prepare-v1-independent-review.json': 'a6a6d128a3941878959200caa1ea51585e2af0347bf9b84df4883f263e58baaa', 'build/rebuild/application-comdat-IAT-diagnosis-v1.py': '1a1708cd8950ae1a5a77244354ed27432317e39cf16863cd92baded501c2ea10', 'build/rebuild/application-comdat-IAT-diagnosis-v1-run.py': 'bfbc357ea599f6317f7dc0cefe68475d6f53210d17b23cf9abeec65310ecbd1d', 'build/rebuild/application-comdat-IAT-diagnosis-v1-request.json': '7e659688f7a2c0a9b38461e113a77fc0143663903b6d64f59cf17aef4f3462c4', 'build/rebuild/application-comdat-IAT-diagnosis-v1-control/receipt.json': 'dc53df152473062cf1a10cf60f741f3b67fb3486ff379eb468176d106a6bf7b8', 'build/rebuild/application-comdat-IAT-diagnosis-v1-control/stdout.txt': '47d5ce46f12203c0963ee9c348bc50a679fdd58233226db6bbb870c5904f3e7c'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source_pins(*groups):
    result={}
    for group in groups:
        for name,sha in group.items():
            require(name not in result or result[name]==sha, 'conflicting fixed dependency: '+name)
            result[name]=sha
    return result


def unchanged_aliases(fresh, saved):
    require(diagnostic.canonical(fresh)==diagnostic.canonical(saved) and len(fresh)==34 and
            sum(row['use_count'] for row in fresh)==239 and all(row['enabled'] for row in fresh),
            'unchanged IAT34/239 census differs')


def response_tokens(text, old_out, out, archive, IAT, CRT):
    lines = text.splitlines()
    require(all(len(t)>2 and t.startswith('"') and t.endswith('"') for t in lines), 'quoted prior response required')
    tokens = [t[1:-1] for t in lines]
    for key, filename in [('OUT', 'diagnostic.exe'), ('MAP', 'diagnostic.map')]:
        old='/'+key+':'+str(old_out/filename); new='/'+key+':'+str(out/filename)
        require(tokens.count(old)==1 and new not in tokens, 'exact prior destination required')
        tokens[tokens.index(old)] = new
    require(str(archive) not in tokens and len(IAT)==34 and len(CRT)==4 and len(set(IAT+CRT))==38 and
            all(tokens.count(t)==1 for t in IAT+CRT), 'exact inherited aliases/new archive required')
    require({t for t in tokens if t.startswith('/ALTERNATENAME:')}==set(IAT+CRT), 'unreviewed inherited alias')
    tokens.append(str(archive))
    diagnostic.response_text(tokens)
    return tokens


def native_scope(native, peer, archive_sha, producer_sha, receipt_sha):
    require(native.get('kind')=='comdat-any-native-conformance-v1' and type(native.get('schema_version')) is int and
            native['schema_version']==1 and native.get('status')=='pass' and native.get('input_stability_verified') is True and
            all(native.get(k) is False for k in ('ABI_verified','Game_execution','archive_generated','compiler_performed',
                'executable_linked','object_rewritten','provider_selected','runtime_eligible')), 'accepted typed native scope required')
    require(len(native['components'])==1, 'exact one typed native component required')
    c=native['components'][0]; facts=c['facts']
    require(c['label']=='comdat-any-code1' and c['kind']=='archive' and c['input_sha256']==archive_sha and
            c['receipt_sha256']==producer_sha and c['native_metadata_matches'] is True and
            facts['members']==facts['exports']==1 and facts['complete_native_linker_index'] is True and
            len(facts['objects'])==1 and facts['objects'][0]['all_native_metadata_matches'] is True,
            'typed native physical component differs')
    require(peer.get('kind')=='comdat-any-native-independent-review-v1' and peer.get('schema_version')==1 and
            peer.get('status')=='accepted' and peer['receipt_sha256']==receipt_sha and peer['archive_sha256']==archive_sha and
            peer['collection_sha256']==native['collection_sha256'] and
            type(peer.get('native_commands_replayed')) is int and peer['native_commands_replayed']==0 and
            all(peer.get(k) is False for k in
                ('ABI_verified','game_execution','link_performed','provider_selected','runtime_eligible')),
            'typed independent native ancestry differs')


def prepare(repository, out, source_sha, tests_sha):
    repository=Path(repository).resolve();out=Path(out).resolve()
    require(out==repository/'build/rebuild/application-link-diagnostic-v12-comdat-v2' and not out.exists(), 'exclusive V12 output required')
    bindings=[]
    def bind(relative, expected):
        path=repository/relative
        require(path.resolve().is_relative_to(repository) and diagnostic.file_hash(path)==expected, 'fixed input differs: '+relative)
        bindings.append(diagnostic.identity(path));return path
    for name, sha in source_pins(diagnostic.SOURCE_PINS, HELPER_PINS, PINS).items():bind(name,sha)
    bind('tools/rebuild/application_comdat_diagnostic.py',source_sha)
    bind('tests/rebuild/test_application_comdat_diagnostic.py',tests_sha)
    def load(relative):return json.loads((repository/relative).read_text())
    old_out=repository/'build/rebuild/application-link-diagnostic-v11-import34'
    report=load('build/rebuild/application-link-diagnostic-v11-import34/receipt.json')
    diagnostic.stable(report['input_bindings']);bindings.extend(report['input_bindings'])
    obs=load('build/rebuild/application-wave10-cohort-observation-v1/receipt.json')
    diagnostic.stable(obs['input_bindings']);bindings.extend(obs['input_bindings'])
    typed=importlib.import_module('application_typed_comdat')
    require(typed.factory.PINS=={k:v for k,v in HELPER_PINS.items() if k in typed.factory.PINS}, 'factory dependency inventory differs')
    with gzip.open(repository/'build/rebuild/comdat-any-v8-observation-v1/observations.jsonl.gz','rt',encoding='utf-8') as f:
        rows=[json.loads(line) for line in f]
    handoff=load('build/rebuild/comdat-any-v8-export-handoff-v1.json')
    for key,value in handoff.items():
        if isinstance(value,dict) and set(value)=={'path','sha256'}:
            path=Path(value['path']);require(path.resolve().is_relative_to(repository/'build/rebuild'), 'handoff descriptor outside private inputs')
            bind(path.relative_to(repository).as_posix(),value['sha256'])
    result=typed.consume(load('build/rebuild/comdat-any-v8-observation-v1/receipt.json'),rows,
        load('build/rebuild/comdat-any-v8-candidate-request-v1.json'),handoff,
        load('build/rebuild/comdat-any-v8-projection-v1/members.json'),
        (repository/'build/rebuild/comdat-any-v8-projection-v1/COMDAT-ANY-code.lib').read_bytes())
    require(len(result['observer_ledger'])==9 and sum(row['selected'] for row in result['observer_ledger'])==1 and result['fields']==[],
            'exact nine-accounted/one-selected zero-field typed scope required')
    native_scope(load('build/rebuild/comdat-any-native-conformance-v1/receipt.json'),
        load('build/rebuild/comdat-any-native-conformance-v1/independent-outcome-review.json'),handoff['archive']['sha256'],
        handoff['producer_receipt']['sha256'],PINS['build/rebuild/comdat-any-native-conformance-v1/receipt.json'])
    consumer_peer=load('build/rebuild/application-typed-comdat-source-independent-review.json')
    require(consumer_peer['source_sha256']==PINS['tools/rebuild/application_typed_comdat.py'] and
            consumer_peer['tests_sha256']==PINS['tests/rebuild/test_application_typed_comdat.py'] and
            consumer_peer['factory_sha256']==HELPER_PINS['tools/rebuild/comdat_any_frontier_factory.py'],
            'typed consumer source review identity differs')
    providers=[row for group in report['provenance'].values() for row in group if row.get('component')=='current-CODE-definition']
    require(len(providers)==12946, 'complete baseline current CODE providers required')
    providers+=report['selected_supplementary_providers']
    providers.append(dict(component='actual-entry',member='application-entry.lib',canonical=diagnostic.partial.CANONICAL,
        recipe_id=diagnostic.partial.IDENTITY['recipe_id'],object_sha256=diagnostic.partial.IDENTITY['object_sha256'],
        symbol_index=diagnostic.partial.IDENTITY['symbol_index'],original_address='0x0086a850'))
    other=[name for name,kind in obs['provider_namespace']['symbols'].items() if kind=='existing-noncode']
    require(len(providers)==14476 and cohort.disjoint_providers([],baseline_providers=providers,
        existing_noncode_definitions=other)==obs['provider_namespace'], 'complete unchanged V11 provider namespace differs')
    namespace=cohort.disjoint_providers([[result['provider']]],baseline_providers=providers,existing_noncode_definitions=other)
    require(namespace['physical_owners']==namespace['original_addresses']==14477, 'typed successor collision census differs')
    with gzip.open(repository/'build/rebuild/application-wave10-cohort-observation-v1/fields.json.gz','rt',encoding='utf-8') as f:fields=json.load(f)
    normative=[row for group in report['provenance'].values() for row in group if row.get('proof')]
    require(len(normative)==len(fields)==45947 and sorted(normative,key=diagnostic.canonical)==sorted(fields,key=diagnostic.canonical) and
        diagnostic.digest(diagnostic.canonical(sorted(fields,key=diagnostic.canonical)))==obs['fields_canonical_sha256'], 'unchanged complete normative field multiset differs')
    old=importlib.import_module('application_import34_diagnostic')
    contract=importlib.import_module('crt_v10_four_alias_contract')
    gate=contract.validate((repository/old.INPUT_PATHS['crt_plan']).read_bytes(),(repository/old.INPUT_PATHS['crt_review']).read_bytes(),
        (repository/old.INPUT_PATHS['crt_response']).read_bytes(),fields,namespace['symbols'])
    require(gate==report['CRT_diagnostic_bindings'] and gate['alias_field_count']==202 and len(gate['tokens'])==4, 'unchanged CRT202 gate differs')
    crt=load(old.INPUT_PATHS['crt_plan'])
    require(all(row['normal_provider']['archive_sha256']==report['default_libraries']['libcmt.lib']['sha256'] for row in crt['bindings']), 'selected normal CRT differs')
    producer=importlib.import_module('import_kernel32_fifteen');annotations=importlib.import_module('iat_code68_annotations')
    originals={}
    for key,relative in old.IMPORT_ANCESTRY.items():
        path=bind(relative,producer.PINS[key])
        if key!='fields':originals[key]=json.loads(path.read_text())
    request=load(old.INPUT_PATHS['import_request']);native=load(old.INPUT_PATHS['import_native'])
    expected_sources=dict(producer.HELPER_PINS,**{'tools/rebuild/import_kernel32_fifteen.py':PINS['tools/rebuild/import_kernel32_fifteen.py']})
    parsed=old.import_archive.read_archive(repository/old.INPUT_PATHS['kernel_library'])
    reconciled=old.native_evidence(native,request,PINS[old.INPUT_PATHS['import_request']],parsed,producer,originals,expected_sources)
    selected={'kernel32-fifteen.lib':old.INPUT_PATHS['kernel_library'],'user32-sixteen.lib':'build/rebuild/import-v8-four-native-v1/user32-sixteen.lib',
        'provider-000.lib':'build/rebuild/application-link-inputs-v2/provider-000.lib','provider-002.lib':'build/rebuild/application-link-inputs-v2/provider-002.lib'}
    baseline_text=(old_out/'link.rsp').read_text()
    libraries={}
    for row in [reconciled['library']]+reconciled['unchanged_libraries']:
        path=bind(selected[row['file']],row['sha256'])
        require(path.stat().st_size==row['bytes'] and baseline_text.splitlines().count('"'+str(path)+'"')==1 and
            any(b['requested_path']==str(path) and b['path']==str(path) and b['sha256']==row['sha256'] for b in report['input_bindings']),
            'selected library physical path/provenance differs')
        libraries[row['file']]=diagnostic.partial.native_archive(path.read_bytes())
    aliases=old.joins.import34_alias_census(reconciled['proposed_pointer_aliases'],annotations.census_view(fields,originals['catalog']),originals['catalog'],libraries)
    for row in aliases:
        row['evaluation_view_sha256']=diagnostic.digest(diagnostic.canonical(row['complete_actual_uses']))
        uses=[field for field in fields if field['canonical']==row['canonical']]
        require(len(uses)==row['use_count'], 'normative IAT use count differs')
        row['complete_actual_uses']=uses;row['compact_proofs_preserved']=True
    unchanged_aliases(aliases,report['aliases'])
    IAT=['/ALTERNATENAME:'+row['canonical']+'='+row['native_pointer'] for row in aliases]
    archive=repository/'build/rebuild/comdat-any-v8-projection-v1/COMDAT-ANY-code.lib'
    tokens=response_tokens(baseline_text,old_out,out,archive,IAT,gate['tokens'])
    require(len(tokens)==69, 'exact V12 token count differs')
    provider=result['provider'];report['provenance'].setdefault(provider['canonical'],[]).append(provider)
    report['selected_supplementary_providers'].append(provider)
    report.update(kind='fixed-V12-typed-COMDAT1-diagnostic',status='prepared-no-native-LINK',input_bindings=bindings,
        command=[report['command'][0],'@'+str(out/'link.rsp')],selected_game_function_provider_count=14477,ordinary_prepared_count=14472,
        typed_COMDAT_saved_evidence=result,typed_COMDAT_namespace=namespace,
        baseline_V11_prepared_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v11-import34/receipt.json'],
        baseline_V11_actual_receipt_sha256=PINS['build/rebuild/application-link-diagnostic-v11-import34/link-receipt.json.gz'],
        no_Game_inputs_added_or_removed=False,one_typed_Game_input_added=True,native_LINK_performed=False,
        executable_execution=False,runtime_eligible=False,provider_adopted=False,link_ready=False)
    diagnostic.stable(bindings)
    out.mkdir();(out/'link.rsp').write_text(diagnostic.response_text(tokens),encoding='utf-8')
    report['response_sha256']=diagnostic.file_hash(out/'link.rsp')
    with (out/'receipt.json').open('x',encoding='utf-8') as f:json.dump(report,f,separators=(',',':'))
    diagnostic.stable(bindings)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('source-sha256','tests-sha256','out'):p.add_argument('--'+key,required=True)
    a=p.parse_args();r=prepare(ROOT,a.out,a.source_sha256,a.tests_sha256)
    print(json.dumps(dict(status=r['status'],Game_providers=r['selected_game_function_provider_count'],Game_fields=r['full_included_field_count'],IAT_cells=34,CRT_uses=202,native_LINK_performed=False)))


if __name__=='__main__':main()
