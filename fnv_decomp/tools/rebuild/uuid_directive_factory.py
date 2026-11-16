"""Finite UUID2768 factory draft; exact input review and lease are required."""
import hashlib
import gzip
import json
import os
from pathlib import Path
import sys
import time

OPTIONAL_INDEX = Path(__file__).resolve().parents[2]/'build/function_index.json'
ROOT = {'original_address':'0x00c5d4e0','recipe_id':'2768-7a8853c4310f459f',
        'recipe_index':2768,'section':131,'size':58,'symbol':'?FUN_00c5d4e0@@YAXXZ',
        'symbol_index':553,'value':0,
        'object_sha256':'a7280d36e8d796a5689c8b61adac4be327eb17d55e12d734600b0ede46cafb88',
        'source_sha256':'376782096fdbabae4c10fb175023317d58fcbd8930596abea1008d8628bffe02'}
CERT = '7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26'
CONTRACT = '4480150173b81b205a05fd92fff0f3707ef090ea2402217379bceb121cdad4df'
RECORD = 'b25d2047794244d0649b4c22b3029621f37c50660aeee45f7c42ba1305bb9e7d'
UUID_ID = '500b64d35a879017b6e729c7264954dafd1722389e78fe47ff618916fb537d35'
DIFF_ID = '771cd50e84e5996d8fda1470742f71fe7d99f887e03ad7338a4dd10d753ef094'
FACTS = '9d8a7197bf12ac5cc842336b0b9e184e33a5b2be664f7830d4a4665733f6c631'
SIX = 'e475b8e3a687bc5394088fb5c6df70a1fa2e794ebd4d1bf05fcd382ecef56314'
PEER = 'aa05bf0a00cfb84e5655c810ee3b89d7cfbfd32e524ba53d5b29bf769aa7ed17'
SIX_PEER = 'bf641453a0fbd1b29896039936f7cef357f5dc1af167f6e0e6e40d98a3d1b038'
IMAGE = 'c03da09d39b8fd22283792c3dc1fbb6ac1e526d8afadd832fabc4071f1720cb1'
RETAINED = '04d44b73e81982f846bfe8d81806db72ea669586b579ff22007dfd6f7d831297'
DECLARATION = '26e13ca4ee534ef4dd7df52b5b31b388dfd49ba79a4099561ffe2bf9fa8c73d9'
DECL_REVIEW = '8f6af441694e3c11157b6b1ac56538f5da3f8aa0ae9209dad88b84c95906df80'
UUID_LIB = '6f363d2fbc78a5c17354bacfb481e615aeb4b0fd462581c02f9d6aca3e893969'
DEPENDENCY_CONTEXT = '8b044fe51ce0b455ea6baac1c88441d566ec1514e4def0866b7102382b1b784f'
ARTIFACT_PINS = {
    'raw_facts':FACTS, 'raw_peer':PEER, 'saved_rows':SIX, 'saved_rows_peer':SIX_PEER,
    'declaration':'2cf2f061f003d027213cbfa77e53f2a15be34de8db62fa32712148ff6dbb51ac',
    'declaration_context':DEPENDENCY_CONTEXT,
    'declaration_review':'9cce2a0d39394c9bf0b564a8f872a83b655f83bb22a6db036f306643f15c9dfd',
    'declaration_audit':'32481c04d52919500766a9e10b1a0d2ffe801254a1d542721e49773c6daad1dd',
    'composer_review':'71770d7db4242bddfba9b66a2f4c8d2791d94fadef08cc6a7254b46c164ac342',
    'prepared_epoch':'250c9cf8be4cd98e805eb81ed89daae989bab6d262cab5cf0f3e8040120693af',
    'prepared_epoch_receipt':'3f4fceadfacee79edfc2032eccdfbfd6d7b553952b2aee1416be305cc0f85e7b',
    'prepared_epoch_peer':'e72d05c46ae0211579ba88e58477249d4f85a04129f448db1f70ce96e0f771ef',
    'provider_map':'6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c',
    'provider_review':'ac44b36431da8b070c2dcd95452a6e3faed57efd8758e4b95aa275d8fa8c1baf',
    'manifest':'bc62a5fb2553431b1e0547d11f366e52efb73096ea8ceb206c556ae5740a53eb',
    'retained':RETAINED,'image_check':IMAGE,'source':ROOT['source_sha256'],
    'object':ROOT['object_sha256'],'uuid_library':UUID_LIB,
    'selection':'48ae62cdc5b1754b9c4af674ef4716d53afb554882e174a93acf860eaf1c6cb1',
    'owners':'fac1496a2675e9a6b697d604c8d5b35a2e4b8bb6194e2ec823e5a37d1092f2e8',
    'recipes':'62f2c8da5f0daa912abdf4576328706711c6561eef7f01c93a89cb71ad46fb6c',
    'raw_request':'b23441461ba1528d95fa69b998fe5942b57dd442c1d03145990d19fba305ffa3',
    'raw_collector':'2b2ac76b14b50811d43b21e97a01d332ec2cca96222ed7b8d3b73c90096cf558',
    'raw_input_review':'694668046dc1ba0484717a3a7f2fa6ca54ba6292131ce81e64f1c661273762c7',
    'raw_control_receipt':'daa48d34eded3a9b5f9b2b439bd50c3e02ad4609e2797966adbecf15f460ecc9'}
EXTRA_ARTIFACTS = {'reference'}
PRODUCER_NAMES = frozenset(('bulk_code_pool','centralordinary_root_collect','coff_code_archive','coff_inventory',
    'coff_rewrite','comdat_any_code_omission','comdat_any_code_projection','comdat_any_frontier_contexts',
    'comdat_any_frontier_factory','comdat_any_frontier_observer','comdat_any_root_composer','composed_relocation_factory',
    'composed_relocation_projection','current_code_frontier','data_plan','frontier_root_collect_v3','import_plan',
    'local_label_projection','ordinary_code_projection','ordinary_initialized_data_omission','ordinary_relocation_factory',
    'ordinary_relocation_projection','prepared_code_exclusions','root_certificate_composer','root_code_closure',
    'runtime_code_inventory','runtime_code_pool','runtime_gaps','scalableordinary_root_collect',
    'uuid_directive_occurrence_witness','uuid_directive_projection','uuid_directive_root_composer'))
OWNED = frozenset(('tools/rebuild/uuid_directive_factory.py','tests/rebuild/test_uuid_directive_factory.py',
                   'docs/rebuild/UUID-DIRECTIVE-FACTORY.md'))
FIXED_PRODUCERS = {
    'uuid_directive_root_composer':'64128957fb51bdc6af96a886fcfc0c03ae1c04673ea38de267ef3d622732ed56',
    'uuid_directive_projection':'b11c69e28bdef6e432de0cdd1004c00684ea36860583c136b7ca0cdbf49d4170',
    'uuid_directive_occurrence_witness':'905d1eb9f0dfdc0e808f344eb8c8784ca60f97a1b26020b7af40d47b34cfaf4e',
    'comdat_any_frontier_factory':'fbe593a9d5a9125be130dd73d424202a2a6b15b77bebde079f4a8abe1ecf0734',
    'composed_relocation_factory':'34e9ad9ccfb10943c2fc4c10ea57e28dae8312dc442621ed8045cbeb2b649477'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def require(test, message):
    if not test: raise ValueError(message)


def exact(a,b):
    return a == b and digest(a) == digest(b)


def validate_operation(operation, review):
    """Validate externally authenticated, exact source/input review before imports.

    This purely validates records; an eventual executor must authenticate every
    referenced file and source dependency before using a producer module.
    """
    require(type(operation) is dict and set(operation)=={'schema_version','kind','roots','artifacts','producer_sha256',
            'output_relative','resource_limits'} and type(operation['schema_version']) is int and
            operation['schema_version']==1 and operation['kind']=='finite-uuid2768-factory-operation-v1' and
            exact(operation['roots'],[ROOT]) and type(operation['artifacts']) is dict and
            set(operation['artifacts'])==set(ARTIFACT_PINS)|EXTRA_ARTIFACTS, 'finite operation schema differs')
    for name,ref in operation['artifacts'].items():
        require(type(ref) is dict and set(ref)=={'path','sha256'} and type(ref['path']) is str and bool(ref['path']) and
                type(ref['sha256']) is str and len(ref['sha256'])==64 and
                all(c in '0123456789abcdef' for c in ref['sha256']) and
                (name not in ARTIFACT_PINS or ref['sha256']==ARTIFACT_PINS[name]), 'artifact reference differs: '+name)
    producers=operation['producer_sha256']
    require(type(producers) is dict and set(producers)==PRODUCER_NAMES and
            all(type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h) for h in producers.values()) and
            all(producers[k]==v for k,v in FIXED_PRODUCERS.items()) and
            type(operation['output_relative']) is str and operation['output_relative'].startswith('build/rebuild/') and
            exact(operation['resource_limits'],{'seconds':900,'peak_memory_bytes':1073741824,'output_bytes':134217728}),
            'source/output/resource scope differs')
    require(type(review) is dict and set(review)=={'schema_version','kind','reviewer','approved','root_authorized',
            'independent_source_schema_review_pass','artifact_input_review_pass','operation_sha256','source_sha256',
            'producer_sha256','allow_original_objects_read','allow_source_hashing','allow_reference_image_read',
            'allow_code_emission','allow_native_tools','allow_executable_link','allow_game_execution'} and
            type(review['schema_version']) is int and review['schema_version']==1 and
            review['kind']=='finite-uuid2768-factory-input-review-v1' and type(review['reviewer']) is str and
            bool(review['reviewer'].strip()) and review['operation_sha256']==digest(operation) and
            exact(review['producer_sha256'],operation['producer_sha256']) and type(review['source_sha256']) is dict and
            set(review['source_sha256'])==OWNED and
            all(type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h) for h in review['source_sha256'].values()) and
            all(review[k] is True for k in ('approved','root_authorized','independent_source_schema_review_pass',
                'artifact_input_review_pass','allow_original_objects_read','allow_source_hashing','allow_reference_image_read','allow_code_emission')) and
            all(review[k] is False for k in ('allow_native_tools','allow_executable_link','allow_game_execution')),
            'independent exact-operation authorization required')
    return True


def _sha_file(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda:stream.read(1024*1024),b''):h.update(part)
    return h.hexdigest()


def _snapshot(path, expected, snapshots):
    """Record content and physical identity; fail if the file changes mid-read."""
    path=Path(path).resolve(strict=True);before=path.stat()
    require(path.is_file() and _sha_file(path)==expected, 'input hash differs')
    after=path.stat()
    identity=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    require(identity(before)==identity(after), 'input changed during snapshot')
    value=(expected,identity(after));require(path not in snapshots or snapshots[path]==value,'input identity changed')
    snapshots[path]=value
    return path


def _stable(snapshots):
    require(not os.path.lexists(OPTIONAL_INDEX),'optional function index unexpectedly present')
    for path,(expected,identity) in snapshots.items():
        stat=path.stat()
        require((stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns)==identity and
                _sha_file(path)==expected, 'protected input changed')


def _load_json(path, cap):
    require(path.stat().st_size<=cap,'JSON input size exceeds bound')
    with path.open('r',encoding='utf-8') as source:return json.load(source)


def _source_graph(source_dir, pins, snapshots, retained_tools):
    """Hash/scan both project import directories before any producer import."""
    import ast
    paths={}
    for name in sorted(PRODUCER_NAMES):
        p=_snapshot(source_dir/(name+'.py'),pins[name],snapshots)
        require(p.parent==source_dir.resolve(), 'producer escaped source directory')
        paths[name]=p
    tools_dir=source_dir.parent
    for name in ('compare','build_and_match','function_spans'):
        rel='tools/'+name+'.py'
        require(rel in retained_tools, 'comparison source lacks retained pin')
        p=_snapshot(tools_dir/(name+'.py'),retained_tools[rel],snapshots)
        require(p.parent==tools_dir.resolve() and name not in paths, 'comparison source path conflict')
        paths[name]=p
    for name,p in paths.items():
        tree=ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        for node in ast.walk(tree):
            imported=([a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else
                      [node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [])
            for child in imported:
                possible=[directory/(child+'.py') for directory in (source_dir,tools_dir) if (directory/(child+'.py')).is_file()]
                if possible:
                    require(len(possible)==1 and child in paths and possible[0].resolve()==paths[child],
                            'unreviewed or ambiguous local transitive import: '+child)
    return paths


def _write_owned(path,data,owned):
    """Exclusive creation and inode registration before the first write."""
    path=Path(path)
    with path.open('xb') as target:
        stat=os.fstat(target.fileno());owned[path]=(stat.st_dev,stat.st_ino)
        target.write(data);target.flush();os.fsync(target.fileno())


def _check_owned(owned,expected):
    require(set(owned)==set(expected),'owned output census differs')
    for path,identity in owned.items():
        require(not path.is_symlink(),'owned output became a symlink')
        stat=path.stat();require((stat.st_dev,stat.st_ino)==identity and _sha_file(path)==expected[path],
                                 'owned output identity or content changed')


def _remove_owned(owned):
    """Never unlink a path replaced since our exclusive creation."""
    unresolved=[]
    for path,identity in list(owned.items()):
        try:
            if not path.is_symlink():
                stat=path.stat()
                if (stat.st_dev,stat.st_ino)==identity:path.unlink()
                else:unresolved.append(path.name)
            else:unresolved.append(path.name)
        except FileNotFoundError:pass
        except OSError:unresolved.append(path.name)
    return unresolved


def saved_context(facts, facts_peer, six, six_peer):
    """Validate already authenticated metadata; never reads any path itself."""
    require(type(facts) is dict and facts.get('kind') == 'exact-object-raw-directive-facts' and
            exact(facts.get('root'),ROOT) and facts.get('rsp_contains_uuid_token') is False and
            all(facts.get(k) is False for k in ('dependency_selection_proved','provider_selected','ABI_verified',
                'runtime_eligible','admission_approved','emission_performed','certificate_created','link_ready','native_tools_run')),
            'raw facts scope/negative flags differ')
    require(facts.get('collector_sha256') == '2b2ac76b14b50811d43b21e97a01d332ec2cca96222ed7b8d3b73c90096cf558' and
            facts.get('review_sha256') == '694668046dc1ba0484717a3a7f2fa6ca54ba6292131ce81e64f1c661273762c7' and
            facts.get('request_sha256') == 'b23441461ba1528d95fa69b998fe5942b57dd442c1d03145990d19fba305ffa3',
            'raw collection request/source/review differs')
    require(type(facts_peer) is dict and facts_peer.get('status') == 'accepted_raw_metadata_only' and
            facts_peer.get('facts_sha256') == FACTS and facts_peer.get('object_reread') is False and
            facts_peer.get('dependency_selection_proved') is False and facts_peer.get('admission_approved') is False,
            'accepted raw-facts peer review required')
    require(type(six) is dict and six.get('kind') == 'six-row-saved-negative-assay' and
            type(six.get('rows')) is list and len(six['rows'])==6 and
            all(six.get(k) is False for k in ('blockers_discharged','emission_performed','original_objects_read',
                                              'provider_selected','runtime_eligible','witness_created')),
            'six-row negative assay required')
    require(type(six_peer) is dict and six_peer.get('status') == 'accepted' and
            six_peer.get('UUID_ordered_duplicate_occurrences_preserved') is True and
            six_peer.get('rows_verified') == 6 and six_peer.get('blockers_discharged') is False,
            'independently accepted six-row review required')
    candidates=[r for r in six['rows'] if r.get('fact',{}).get('address') == ROOT['original_address']]
    require(len(candidates)==1, 'one exact UUID2768 saved row required')
    item=candidates[0];fact=item['fact'];row=item['row'];contract=row['contract'];negative=row['certificate']
    require(exact(fact.get('root'),ROOT) and fact.get('record_sha256')==RECORD==digest(row) and
            fact.get('certificate_sha256')==CERT==digest(negative) and
            fact.get('contract_sha256')==CONTRACT==digest(contract) and
            row.get('contract_identity_sha256')==CONTRACT and row.get('certificate_sha256')==CERT and
            exact(row.get('requested_roots'),[ROOT]), 'borrowed negative record/contract/root')
    require(row.get('closure_observed') is False and row.get('graph_observation_complete') is False and
            row.get('root_closure_candidate') is False and negative.get('closure_observed') is False and
            type(contract.get('fields')) is list and len(contract['fields'])==9 and
            contract.get('fields_complete') is True and contract.get('missing_fields_complete') is True and
            contract.get('missing_fields')==[] and contract.get('parent_eh')==[], 'negative/fields scope differs')
    blockers=negative.get('blockers');require(type(blockers) is list and len(blockers)==3 and
        [b.get('blocker_id') for b in blockers]==[UUID_ID,UUID_ID,DIFF_ID] and
        exact(row.get('blockers'),blockers) and exact(fact.get('blockers'),blockers), 'ordered blocker occurrences differ')
    return dict(root=ROOT.copy(),contract=contract,negative=negative,record_sha256=RECORD,
                facts=facts,original_negative_unchanged=True,admission_approved=False)


def validate_epoch(epoch, providers, canonical_name):
    """Check the complete pinned collision epoch against the complete provider map."""
    require(type(epoch) is dict and type(epoch.get('schema_version')) is int and epoch['schema_version'] == 7 and
            epoch.get('kind') == 'prepared-CODE-collision-exclusions' and
            epoch.get('policy_id')=='prepared-CODE56-successor-v1' and
            epoch.get('parent_manifest_sha256')=='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e' and
            epoch.get('historical_records_preserved') is True and
            type(epoch.get('successor_export_count')) is int and epoch['successor_export_count']==56 and
            type(epoch.get('successor_field_count')) is int and epoch['successor_field_count']==290 and
            type(epoch.get('ordinary_prepared_count')) is int and epoch['ordinary_prepared_count']==14528 and
            type(epoch.get('collision_exclusion_count')) is int and epoch['collision_exclusion_count']==14534 and
            epoch.get('application_selected_code_count') is None and
            'application_manifest_adopted' not in epoch and epoch.get('application_selection_inferred_from_counts') is False and
            all(epoch.get(k) is False for k in ('provider_selected','runtime_eligible','ABI_verified',
                'admission_decision_created','emission_performed','namespace_approved','link_ready')), 'prepared epoch differs')
    records=epoch.get('records');names=epoch.get('exclusion_names');ordinary=epoch.get('ordinary_names')
    require(type(records) is list and type(names) is list and type(ordinary) is list and
            len(records)==len(names)==len(set(names))==14534 and len(ordinary)==len(set(ordinary))==14528,
            'complete collision census required')
    require(type(providers) is dict and len(providers)==68657 and
            {r.get('canonical') for r in records}==set(names) and set(ordinary)<=set(names), 'provider/collision universe differs')
    for r in records:
        identity=r.get('namespace_identity')
        require(type(identity) is dict and canonical_name(identity)==r['canonical'] and
                r.get('category') in ('ordinary','application-candidate'), 'collision namespace identity differs')
    require(sum(r['category']=='ordinary' for r in records)==14528 and
            {r['canonical'] for r in records if r['category']=='ordinary'}==set(ordinary), 'ordinary census differs')
    identity={k:ROOT[k] for k in ('recipe_id','object_sha256','symbol_index')}
    require(providers.get(ROOT['original_address'])==identity and canonical_name(identity) not in set(names),
            'requested identity missing or already prepared')
    return frozenset(names)


def validate_epoch_authority(epoch, receipt, peer):
    """Bind the reviewed successor output and predecessor lineage."""
    require(type(receipt) is dict and receipt.get('kind')=='prepared-code56-successor-collector-receipt-v1' and
            receipt.get('epoch_sha256')==ARTIFACT_PINS['prepared_epoch'] and
            receipt.get('input_sha256',{}).get('parent')=='934aa32fd6945ab28a364beba623e347c6c9311120e057e36e126a7d67a3ea7e' and
            receipt.get('input_sha256',{}).get('handoff')==epoch.get('successor_handoff_sha256') and
            receipt.get('input_sha256',{}).get('members')==epoch.get('successor_member_ledger_sha256') and
            type(receipt.get('exports_added')) is int and receipt['exports_added']==56 and
            type(receipt.get('field_rows')) is int and receipt['field_rows']==290 and
            receipt.get('provider_selected') is False and receipt.get('runtime_eligible') is False and
            receipt.get('application_selection_inferred') is False, 'successor receipt differs')
    require(type(peer) is dict and peer.get('kind')=='independent-prepared-code56-successor-outcome-review' and
            peer.get('status')=='accepted-derived-metadata-only' and peer.get('epoch_sha256')==ARTIFACT_PINS['prepared_epoch'] and
            peer.get('receipt_sha256')==ARTIFACT_PINS['prepared_epoch_receipt'], 'successor independent review differs')


def validate_output_scope(repo, manifest_path, manifest, unit, out, source_path, object_path):
    """Distinguish the manifest's resolution base from its object store."""
    repo=Path(repo).resolve();manifest_path=Path(manifest_path).resolve();out=Path(out).resolve()
    require(manifest_path==repo/'build/rebuild/objects-20261103T030230Z-7cfc935c.json' and
            'object_root_relative' not in manifest, 'manifest resolution schema differs')
    relative='objects/20261103T030230Z-7cfc935c/2768-7a8853c4310f459f/unit.obj'
    require(unit.get('recipe_id')==ROOT['recipe_id'] and type(unit.get('recipe_index')) is int and
            unit['recipe_index']==2768 and unit.get('object')==relative and
            unit.get('source')=='src/staging/blk_00c40000_od.cpp' and
            unit.get('object_sha256')==ROOT['object_sha256'] and unit.get('source_sha256')==ROOT['source_sha256'],
            'selected unit source/object association differs')
    resolution_base=manifest_path.parent;native_store=(resolution_base/'objects').resolve();source_root=(repo/'src').resolve()
    require((resolution_base/relative).resolve()==Path(object_path).resolve() and
            (repo/unit['source']).resolve()==Path(source_path).resolve(), 'manifest physical source/object differs')
    require(not out.is_relative_to(native_store) and not native_store.is_relative_to(out) and
            not out.is_relative_to(source_root) and not source_root.is_relative_to(out),
            'output overlaps native-object store or source root')
    return native_store


def comparison_rows(rows, symbol):
    """Demand an ordinary full-span MATCH, including all nine relocation checks."""
    require(type(rows) is list and len(rows)==1, 'singleton ordinary comparison required')
    row=rows[0]
    require(row.get('address')==ROOT['original_address'] and row.get('symbol')==symbol and
            type(row.get('size')) is int and row['size']==ROOT['size'] and
            type(row.get('compiled_extent')) is int and row['compiled_extent']==ROOT['size'] and
            row.get('verdict')=='match' and row.get('errors')==[] and not row.get('byte_differences',[]) and
            type(row.get('relocations')) is list and len(row['relocations'])==9 and
            all(type(x) is dict and x.get('match') is True for x in row['relocations']), 'ordinary full MATCH required')
    return True


def validate_dependency(facts, declaration, context, review, audit):
    """Bind the independently reviewed *future* dependency, not a selected provider."""
    require(digest(declaration)==DECLARATION and digest(review)==DECL_REVIEW and
            declaration.get('kind')=='explicit-normal-sdk-library-dependency-v1' and
            declaration.get('library_name')=='uuid.lib' and declaration.get('sha256')==UUID_LIB and
            declaration.get('absolute_path')==declaration.get('required_response_token') and
            review.get('kind')=='independent-normal-dependency-declaration-review-v1' and
            review.get('status')=='accepted' and review.get('declaration_sha256')==DECLARATION,
            'reviewed dependency declaration differs')
    candidate=facts['uuid_search_candidate']
    require(context.get('kind')=='finite-UUID-dependency-declaration-context' and
            context.get('root_scope')==[ROOT['original_address']] and context.get('declaration_canonical_sha256')==DECLARATION and
            exact(context.get('normal_sdk_search_candidate'),candidate) and
            context.get('baseline_response',{}).get('contains_UUID_token') is False and
            candidate.get('path')==declaration['absolute_path'] and candidate.get('sha256')==UUID_LIB and
            type(candidate.get('size')) is int and candidate['size']==2812980 and
            type(candidate.get('device')) is int and type(candidate.get('inode')) is int and
            all(context.get(k) is False for k in ('dependency_selected','dependency_loaded','provider_adopted','runtime_eligible')),
            'SDK candidate or scope differs')
    require(audit.get('status')=='accepted' and audit.get('root')==ROOT['original_address'] and
            type(audit.get('recipe_index')) is int and audit['recipe_index']==2768 and
            audit.get('context_sha256')==DEPENDENCY_CONTEXT and audit.get('rawfacts_sha256')==FACTS and
            audit.get('declaration_canonical_sha256')==DECLARATION and audit.get('review_canonical_sha256')==DECL_REVIEW and
            audit.get('sdk_candidate_sha256')==UUID_LIB and audit.get('sdk_size')==candidate['size'] and
            audit.get('sdk_device')==candidate['device'] and audit.get('sdk_inode')==candidate['inode'] and
            audit.get('candidate_hash_and_identity_stable_during_review') is True and
            audit.get('requested_and_declared_path_same_physical_file') is True and
            audit.get('baseline_response_uuid_present') is False and
            all(audit.get(k) is False for k in ('dependency_selected','dependency_loaded','provider_adopted','runtime_eligible',
                                                 'duplicate_semantics_proved','new_link_performed')),
            'independent SDK candidate review differs')
    return dict(path=declaration['absolute_path'],sha256=UUID_LIB,device=candidate['device'],inode=candidate['inode'],
                size=candidate['size'],future_response_token=declaration['required_response_token'],
                library_selection_proved=False,library_loaded_proved=False,duplicate_semantics_proved=False)


def field_ledger(contract, projection, negative, composed, output_sha256):
    """Produce complete immutable field evidence, not a certificate or admission."""
    fields=contract['fields']; rows=projection['fields']; hashes=[digest(f) for f in fields]
    require(len(fields)==len(rows)==9 and len(set(hashes))==9 and
            hashes==[r.get('field_proof_sha256') for r in rows], 'full original field coverage differs')
    require(projection.get('original_negative_certificate_sha256')==digest(negative)==CERT and
            projection.get('contract_identity_sha256')==digest(contract)==CONTRACT and
            projection.get('composed_certificate_sha256')==digest(composed) and
            projection.get('output_sha256')==output_sha256 and
            projection.get('original_negative_certificate_preserved') is True, 'field ledger proof identity differs')
    maps=projection['maps'];section_map=maps['section_map'];symbol_map=maps['symbol_map'];mapped=[]
    for ordinal,(field,row) in enumerate(zip(fields,rows),1):
        section=row['section'];symbol=row['symbol_index']
        require(type(section) is int and type(symbol) is int and section in section_map and symbol in symbol_map and
                type(row.get('offset')) is int and type(row.get('kind')) is int and
                field.get('physical_section')==section and field.get('coff_relocation',{}).get('offset')==row['offset'] and
                field['coff_relocation'].get('symbol_index')==symbol and field['coff_relocation'].get('kind')==row['kind'] and
                type(section_map[section]) is int and section_map[section]>0 and
                type(symbol_map[symbol]) is int and symbol_map[symbol]>=0 and
                type(row.get('role')) is str and type(row.get('canonical_name')) is str and bool(row['canonical_name']),
                'serialized field mapping or role missing')
        mapped.append(dict(ordinal=ordinal,original_field_sha256=digest(field),original_section=section,
            original_offset=row['offset'],original_symbol_index=symbol,kind=row['kind'],role=row['role'],
            canonical_name=row['canonical_name'],serialized_section=section_map[section],
            serialized_symbol_index=symbol_map[symbol],original_base=row['original_base'],original_target=row['original_target'],
            addend_bits=row['addend_bits']))
    require(len({(x['original_section'],x['original_offset'],x['original_symbol_index'],x['kind']) for x in mapped})==9,
            'physical fields duplicated')
    return dict(kind='uuid2768-original-negative-full-field-proof',root=ROOT.copy(),fields=fields,mapped_fields=mapped,
                fields_sha256=digest(fields),certificate_sha256=CERT,contract_sha256=CONTRACT,
                composition_sha256=digest(composed),output_sha256=output_sha256,
                original_negative_unchanged=True,provider_selected=False,runtime_eligible=False)


def _produce_member_after_gates(raw, context, witness, providers, exports, original_path, stage_path, pe, recipe,
                                composer, projector, bulk, owned):
    """Unwired producer step; callable only by a future authenticated executor.

    Modules must be real pinned public wrappers, not injectable production
    seams. No entrypoint currently calls this function.
    """
    contract=context['contract'];negative=context['negative']
    require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==ROOT['object_sha256'], 'original object hash differs')
    require(type(witness) is dict and set(witness)=={'header','binding','witness_authority','declaration','review','declaration_authority'},
            'exact UUID witness input required')
    before_inputs=digest(dict(contract=contract,negative=negative,witness=witness,providers=providers,exports=sorted(exports)))
    composition=composer.compose(raw,contract,negative,ROOT,witness['header'],witness['binding'],witness['witness_authority'],
        witness['declaration'],witness['review'],witness['declaration_authority'],policy_id=composer.POLICY)
    require(composition.get('base_certificate_sha256')==CERT and composition.get('base_certificate')==negative and
        composition.get('structural_composition_complete') is True and
        [b.get('ordinal') for b in composition.get('discharged_blocker_occurrences',[])]==[1,2,3] and
        [b.get('blocker_id') for b in composition['discharged_blocker_occurrences']]==[UUID_ID,UUID_ID,DIFF_ID] and
        composition.get('remaining_blocker_occurrences')==[] and composition.get('original_negative_unchanged') is True,
        'composition replay or occurrence mapping differs')
    assessment=projector.assess_member(raw,contract,negative,[witness],composition,[ROOT],providers,
                                       existing_exports=exports,policy_id=projector.POLICY)
    require(type(assessment.get('eligible')) is bool, 'assessment must be explicit')
    if not assessment['eligible']:
        require(type(assessment.get('blockers')) is list and assessment['blockers'] and
                assessment.get('serialization_performed') is False, 'unsupported outcome not terminal')
        require(digest(dict(contract=contract,negative=negative,witness=witness,providers=providers,exports=sorted(exports)))==before_inputs,
                'authenticated producer inputs changed')
        return dict(status='unsupported',assessment=assessment,original_negative_unchanged=True,
                    emitted=False,provider_selected=False,runtime_eligible=False)
    specs=[dict(selected={k:ROOT[k] for k in ('original_address','symbol','symbol_index','section','value','size')})]
    before=bulk.compare_functions(original_path,pe,specs,recipe)
    comparison_rows(before,ROOT['symbol'])
    output,projection=projector.project_member(raw,contract,negative,[witness],composition,[ROOT],providers,
                                                existing_exports=exports,policy_id=projector.POLICY)
    require(projection['fields']==assessment['fields'] and projection['exports']==assessment['exports'] and
            projection['comparison_base_view']==assessment['comparison_base_view'] and len(projection['exports'])==1,
            'projector differs from assessed plan')
    _write_owned(stage_path,output,owned);bulk.strict_reparse(stage_path,output)
    after=bulk.compare_functions(stage_path,pe,specs,recipe,
        dict(bindings=projection['namespace_bindings'],comparison_base_view=projection['comparison_base_view']))
    comparison_rows(after,projection['exports'][0])
    output_sha256=hashlib.sha256(output).hexdigest()
    ledger=field_ledger(contract,projection,negative,composition,output_sha256)
    require(digest(dict(contract=contract,negative=negative,witness=witness,providers=providers,exports=sorted(exports)))==before_inputs,
            'authenticated producer inputs changed')
    return dict(status='projected-pending-native-conformance',assessment=assessment,projection=projection,
                before_comparison=before,after_comparison=after,field_ledger=ledger,output=output,
                original_negative_unchanged=True,emitted=True,provider_selected=False,runtime_eligible=False)


def _prepare(operation_path,operation_sha256,review_path,review_sha256):
    """Authenticate all requested inputs and metadata before importing producers."""
    repo=Path(__file__).resolve().parents[2];snapshots={}
    operation_path=_snapshot(operation_path,operation_sha256,snapshots)
    review_path=_snapshot(review_path,review_sha256,snapshots)
    operation=_load_json(operation_path,4*1024*1024);review=_load_json(review_path,4*1024*1024)
    validate_operation(operation,review)
    for rel,h in review['source_sha256'].items():
        path=_snapshot(repo/rel,h,snapshots);require(path==repo/rel,'source path redirected')
    refs=operation['artifacts'];paths={}
    # Protected inputs are hashed only after all saved evidence, peer reviews,
    # source graph and complete provider metadata have passed their gates.
    sensitive={'reference','object','source','uuid_library'}
    for name,ref in refs.items():
        paths[name]=(Path(ref['path']).resolve(strict=True) if name in sensitive else
                     _snapshot(ref['path'],ref['sha256'],snapshots))
    for name in ('raw_facts','raw_peer','saved_rows','saved_rows_peer','declaration','declaration_context',
                 'declaration_review','declaration_audit','composer_review','prepared_epoch','prepared_epoch_receipt','prepared_epoch_peer','provider_map',
                 'provider_review','manifest','retained','selection','owners','raw_request','raw_input_review','raw_control_receipt'):
        require(paths[name].is_relative_to(repo/'build/rebuild'),'private evidence path escaped workspace')
    require(paths['image_check']==repo/'build/image_check.json' and paths['recipes']==repo/'build/units.json',
            'original image-check/recipe authority path differs')
    data={name:_load_json(paths[name],128*1024*1024) for name in ('raw_facts','raw_peer','saved_rows','saved_rows_peer',
        'declaration','declaration_context','declaration_review','declaration_audit','composer_review','prepared_epoch',
        'prepared_epoch_receipt','prepared_epoch_peer','provider_map','provider_review','manifest','retained','selection','owners','raw_request','raw_input_review','raw_control_receipt')}
    context=saved_context(data['raw_facts'],data['raw_peer'],data['saved_rows'],data['saved_rows_peer'])
    dependency=validate_dependency(data['raw_facts'],data['declaration'],data['declaration_context'],
                                   data['declaration_review'],data['declaration_audit'])
    validate_epoch_authority(data['prepared_epoch'],data['prepared_epoch_receipt'],data['prepared_epoch_peer'])
    require(paths['object']==Path(data['raw_facts']['object_identity']['path']).resolve() and
            paths['source']==(repo/context['contract']['provenance']['source_relative']).resolve() and
            paths['uuid_library']==Path(dependency['path']).resolve(), 'original source/object/SDK physical paths differ')
    require(data['retained']['inputs']['image_check_sha256']==IMAGE, 'original image-check lineage differs')
    for rel,h in data['retained']['inputs']['tools_sha256'].items():
        p=_snapshot(repo/rel,h,snapshots);require(p.is_relative_to(repo/'tools'),'retained tool path escaped')
    source_dir=(repo/'tools/rebuild').resolve()
    producer_paths=_source_graph(source_dir,operation['producer_sha256'],snapshots,data['retained']['inputs']['tools_sha256'])
    out=(repo/operation['output_relative']).resolve()
    require(out.is_relative_to(repo/'build/rebuild') and out!=repo/'build/rebuild' and not out.exists() and
            all(not p.is_relative_to(out) for p in list(snapshots)+list(paths.values())), 'exclusive private output required')
    _stable(snapshots)
    return repo,operation,review,paths,data,context,dependency,producer_paths,out,snapshots


def run(operation_path,operation_sha256,review_path,review_sha256):
    """Draft bounded executor; do not run before independent review and lease."""
    import importlib
    start=time.monotonic()
    repo,operation,review,paths,data,context,dependency,producer_paths,out,snapshots = _prepare(
        operation_path,operation_sha256,review_path,review_sha256)
    require(not any(name in sys.modules for name in producer_paths),'project module already imported before authentication')
    sys.dont_write_bytecode=True
    sys.path.insert(0,str(repo/'tools'));sys.path.insert(0,str(repo/'tools/rebuild'))
    prior=importlib.import_module('comdat_any_frontier_factory')
    audit=importlib.import_module('composed_relocation_factory')
    composer=importlib.import_module('uuid_directive_root_composer')
    projector=importlib.import_module('uuid_directive_projection')
    witness_module=importlib.import_module('uuid_directive_occurrence_witness')
    base=prior.base
    for name in set(producer_paths) & set(sys.modules):
        require(Path(sys.modules[name].__file__).resolve()==producer_paths[name], 'producer import identity differs')
    _stable(snapshots)
    prior.input_budget(start)
    require(operation['artifacts']['reference']['sha256']==base.pool.PINS['reference'],'reference authority differs')
    require(data['composer_review'].get('status')=='accepted-synthetic-only' and
            data['composer_review'].get('composer_sha256')==FIXED_PRODUCERS['uuid_directive_root_composer'] and
            data['composer_review'].get('projection_sha256')==FIXED_PRODUCERS['uuid_directive_projection'] and
            data['composer_review'].get('witness_sha256')==FIXED_PRODUCERS['uuid_directive_occurrence_witness'],
            'independent composer review required')
    units,proofs,providers=prior.validate_original_basis({k:data[k] for k in ('manifest','retained','selection','owners')},
                                                         data['provider_map'],paths['recipes'])
    exports=validate_epoch(data['prepared_epoch'],providers,base.pool.canonical)
    base.collector.validate_request(dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=[ROOT]),
        data['selection']['selections'],data['manifest'],data['retained'],providers)
    unit=units[ROOT['recipe_id']];proof=proofs[ROOT['recipe_id']]
    require(context['contract']['unit_verified_functions']==proof['verified_functions'] and
            context['contract']['provenance']['recipe_unit_sha256']==proof['recipe_unit_sha256'], 'retained source proof differs')
    for rel,h in context['contract']['provenance']['dependency_tools_sha256'].items():
        p=_snapshot(repo/rel,h,snapshots);require(p.is_relative_to(repo/'tools'),'foreign observation dependency')
    validate_output_scope(repo,paths['manifest'],data['manifest'],unit,out,paths['source'],paths['object'])
    for name in ('source','object','uuid_library','reference'):
        _snapshot(paths[name],operation['artifacts'][name]['sha256'],snapshots)
    sdk=paths['uuid_library'].stat()
    require((sdk.st_dev,sdk.st_ino,sdk.st_size)==(dependency['device'],dependency['inode'],dependency['size']),
            'SDK physical identity differs from accepted audit')
    _stable(snapshots)
    prior.input_budget(start)
    out.mkdir(parents=True,exist_ok=False)
    metadata=None;owned={};output_hashes={}
    try:
        import compare as oracle
        from build_and_match import image_ok
        for mod in (oracle,sys.modules['build_and_match']):
            require(Path(mod.__file__).resolve() in snapshots,'unreviewed comparison module')
        pe=base.checked_reference(paths['reference'],oracle,image_ok)
        metadata=audit.SnapshotPe(paths['reference'],pe)
        highlow={metadata.base+rva for rva in metadata.relocations()}
        require(len(highlow)==351931,'original relocation census differs')
        actual_fields=audit.audit_original_fields(metadata,highlow,context['contract']['fields'])
        require(len(actual_fields)==9,'complete original nine-field audit required')
        header=data['raw_facts']['header'];candidate=data['raw_facts']['uuid_search_candidate']
        binding=dict(kind='bound-normal-sdk-search-candidate',library_name='uuid.lib',path=candidate['path'],sha256=candidate['sha256'],
                     candidate_manifest_path=str(paths['declaration_context']),
                     candidate_manifest_sha256=DEPENDENCY_CONTEXT)
        witness_authority=dict(root_sha256=digest(ROOT),contract_sha256=CONTRACT,certificate_sha256=CERT,
            section_sha256=data['raw_facts']['raw_section_sha256'],header_sha256=digest(header),binding_sha256=digest(binding),
            candidate_manifest_path=binding['candidate_manifest_path'],candidate_manifest_sha256=DEPENDENCY_CONTEXT)
        declaration_authority=dict(declaration_sha256=DECLARATION,review_sha256=DECL_REVIEW)
        witness=dict(header=header,binding=binding,witness_authority=witness_authority,
                     declaration=data['declaration'],review=data['declaration_review'],declaration_authority=declaration_authority)
        raw=paths['object'].read_bytes()
        result=_produce_member_after_gates(raw,context,witness,providers,exports,paths['object'],out/'uuid2768.obj',pe,
                                           unit['recipe'],composer,projector,base.bulk,owned)
        member=result.pop('output',None);archive_sha=None
        if member is not None:
            archive=base.coff.archive([('uuid2768.obj',member)]);recovered=base.coff.read_archive(archive)
            require(recovered['members']==[('uuid2768.obj',member)] and
                    recovered['index']==[(result['projection']['exports'][0],'uuid2768.obj')], 'archive index differs')
            _write_owned(out/'uuid2768.lib',archive,owned);archive_sha=hashlib.sha256(archive).hexdigest()
            base.bulk.strict_reparse(out/'uuid2768.obj',member)
            stream=gzip.compress(canonical(result['field_ledger'])+b'\n',mtime=0)
            _write_owned(out/'field-proofs.jsonl.gz',stream,owned)
            field_proof_sha=hashlib.sha256(stream).hexdigest()
            output_hashes.update({out/'uuid2768.obj':hashlib.sha256(member).hexdigest(),out/'uuid2768.lib':archive_sha,
                                  out/'field-proofs.jsonl.gz':field_proof_sha})
        else:
            field_proof_sha=None
        metadata.close();metadata=None
        _stable(snapshots)
        usage=base.budget(start,out)
        receipt=dict(schema_version=1,kind='finite-uuid2768-factory-outcome-v1',status=result['status'],
            operation_sha256=operation_sha256,review_sha256=review_sha256,requested=1,emitted=int(member is not None),
            blocked=int(member is None),original_negative_certificate_preserved=True,code_bytes=58 if member else 0,
            fields=9 if member else 0,archive_sha256=archive_sha,field_proof_sha256=field_proof_sha,
            actual_field_audit_count=len(actual_fields),resource_observations=usage,
            future_uuid_response_token=dependency['future_response_token'],input_stability=True,
            optional_function_index_present=False,
            native_archive_conformance_verified=False,provider_selected=False,runtime_eligible=False,ABI_verified=False,
            application_manifest_adopted=False,library_selection_proved=False,library_loaded_proved=False,
            duplicate_semantics_proved=False,native_tools_run=False,executable_link_performed=False,game_execution_performed=False,
            result=result)
        receipt_bytes=canonical(receipt)+b'\n'
        _write_owned(out/'receipt.json',receipt_bytes,owned)
        output_hashes[out/'receipt.json']=hashlib.sha256(receipt_bytes).hexdigest()
        _stable(snapshots)
        base.budget(start,out)
        _check_owned(owned,output_hashes)
        return receipt
    except BaseException as error:
        unresolved=_remove_owned(owned)
        try:base.save_json(out/'abort.json',dict(status='aborted-no-retry',error_type=type(error).__name__,
            error_message=str(error)[:1000],successful_projection=False,owned_cleanup_unresolved=unresolved,
            provider_selected=False,runtime_eligible=False))
        except BaseException:pass
        raise
    finally:
        if metadata is not None:metadata.close()


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','review'):parser.add_argument('--'+name,required=True,type=Path)
    for name in ('operation','review'):parser.add_argument('--'+name+'-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=run(args.operation,args.operation_sha256,args.review,args.review_sha256)
    except (ValueError,OSError,KeyError,TypeError) as error:
        parser.exit(2,'UUID2768 factory rejected: '+str(error)+'\n')
    print(json.dumps(dict(requested=result['requested'],emitted=result['emitted'],blocked=result['blocked'])))
    return 0 if result['emitted']==1 else 3


if __name__=='__main__':raise SystemExit(main())
