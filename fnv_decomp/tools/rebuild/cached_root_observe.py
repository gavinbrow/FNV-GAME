"""Fresh ordinary COFF observations over unchanged qualified cached contracts.

Metadata qualification creates no certificate. Fresh observations add evidence
outside those contracts and preserve every frozen ordinary outcome unchanged.
"""
from __future__ import annotations
from collections import Counter
import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import struct
import tempfile
import time

import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_inventory as inventory
import scalableordinary_root_collect as finite

POLICY='cached-context-root-observation-v1'
QUALIFIED_POLICY='cached-CODE-frontier-inventory-v1'
MAX_ROOTS=180
MAX_RECIPES=77
MAX_RECORDS=257
ROOT_KEYS=finite.ROOT_KEYS
NATIVE_KEYS=('original_address','symbol','symbol_index','section','value','size')
CONTRACT_KEYS={'recipe_id','roots','export_policy','verified_match','fields_complete','missing_fields_complete',
    'unit_proofs_complete','fields','missing_fields','parent_eh','omission_field_proofs','unit_verified_functions',
    'iat_import_observation','provenance'}
QUALIFIED_FALSE=('provider_selected','runtime_eligible','ABI_verified','native_tools_run','emission_performed',
    'closure_inferred','full_serialization_eligible','historical_certificate_contract_identity_equal_claimed','certificate_created')
QUALIFIED_KEYS={'schema_version','kind','policy_id','event','requested_roots','contract','contract_sha256',
    'new_metadata_contract_sha256','source_frame_verification','native_observation_required',*QUALIFIED_FALSE}
FALSE=dict(emission_performed=False,runtime_eligible=False,provider_selected=False,ABI_verified=False,
    link_ready=False,namespace_approved=False,full_serialization_eligible=False,typed_waiver_applied=False)
PINS={'coff_code_archive.py':'76244d2d4dca4c1f8aa72224be1ef5c92f68976b5cda7d31b5cfe23d3cc29e64',
    'root_code_closure.py':'4bfdb5001380a3d7e5db7517033285d49ab211be68e2fcba15964f0ad5b03c53',
    'runtime_code_inventory.py':'c2fdbd52b4b7f4b7c68f9d80ad03708ba57d42b29e5938dfcf9769366a1ffd0b',
    'scalableordinary_root_collect.py':'e7e5b45df15af0a2bd5cb4a65b36d85ca21eb753656714c0a9a5d8dd919e58ad',
    'runtime_gaps.py':'0399e0f91e94de781512a153ac598f4d5eb6210920bc58241542339c72904116',
    'data_plan.py':'e013ed5f217f9beeeaf571d089a36df22b645559063e826554179cea506f5bf8',
    'import_plan.py':'6b9237ab5951e7d4a2ac2f9b0c3435f0a667a9fdebac02a4534ba0e30ba98d9c',
    'coff_inventory.py':'3518c044738046e7cd9c8be37a3b1077af750fb2e7a19db793b09999a07ee0d2'}
require=coff.require
canonical=inventory.canonical
digest=inventory.digest


def typed_equal(a,b):return canonical(a)==canonical(b)


def validate_roots(unit,proof,requested):
    require(type(unit['recipe_index']) is int and type(proof['recipe_index']) is int and unit['recipe_index']>=0,
        'unit/proof recipe index must be exact integer')
    require(all(isinstance(unit[k],str) and re.fullmatch('[0-9a-f]{64}',unit[k]) for k in ('object_sha256','source_sha256')),
        'unit source/object digest format differs')
    inventory.check_unit(unit,proof)
    require(type(requested) is list and 0<len(requested)<=MAX_ROOTS,'finite exact requested roots required')
    require(all(all(type(f[k]) is int for k in ('section','value','size')) for f in proof['verified_functions']), 'retained physical integer types differ')
    result={}
    for r in requested:
        require(type(r) is dict and set(r)==ROOT_KEYS and all(type(r[k]) is int for k in ('recipe_index','symbol_index','section','value','size')),
            'exact typed physical root schema required')
        a=r['original_address'];require(isinstance(a,str) and re.fullmatch('0x[0-9a-f]{8}',a) and a not in result,'duplicate/invalid root address')
        require(r['recipe_index']==unit['recipe_index'] and r['recipe_id']==unit['recipe_id'] and
            r['object_sha256']==unit['object_sha256'] and r['source_sha256']==unit['source_sha256'] and
            r['section']>0 and r['value']>=0 and r['size']>0,'root source/object/recipe differs')
        matches=[f for f in proof['verified_functions'] if f['address']==a and f['symbol']==r['symbol'] and
            typed_equal([f[k] for k in ('section','value','size')],[r[k] for k in ('section','value','size')])]
        require(len(matches)==1 and r['symbol_index']>=0,'root lacks unique exact retained span')
        result[a]=r
    return result


def verify_physical_fields(obj,rows,relocations):
    """Reject contradictory known physical evidence; do not infer target roles."""
    for e in rows:
        r=e['coff_relocation'];require(r is not None,'missing field in physical field list')
        section=obj['sections'].get(e['physical_section'])
        require(section is not None and typed_equal(r['offset'],e['physical_offset']),'field section/offset contradiction')
        key=canonical([r['offset'],r['symbol_index'],r['kind']])
        require(key in relocations[e['physical_section']],'field absent from exact native relocation table')
        target=obj['symbols'].get(r['symbol_index'])
        if target is not None:
            require(typed_equal([r[k] for k in ('symbol','symbol_section','symbol_value','symbol_type','symbol_storage')],
                [target[k] for k in ('name','section','value','type','storage')]), 'physical target metadata contradiction')
        if type(r['kind']) is int and r['kind'] in (6,20):
            off=r['offset'];require(type(off) is int and 0<=off<=len(section['payload'])-4,'known physical field extent contradiction')
            bits=int.from_bytes(section['payload'][off:off+4],'little')
            require(typed_equal(r['addend'],bits),'known physical addend contradiction')


def observe_recipe_contracts(raw,unit,proof,requested,qualified_views,observation_provenance):
    """Streaming pure seam: one parse, exact qualified contracts, no waivers.

    Qualified producer order is singletons followed by its recipe union. The
    caller must consume every result and finish the operation before publishing.
    Source-file freshness and whole-artifact authority belong to the driver.
    """
    requested_by_address=validate_roots(unit,proof,requested)
    require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==unit['object_sha256'],'raw original object hash differs')
    require(isinstance(observation_provenance,dict) and isinstance(observation_provenance.get('qualified_request_sha256'),str) and
        re.fullmatch('[0-9a-f]{64}',observation_provenance['qualified_request_sha256']),
        'qualified request lineage required')
    original_inputs=digest([unit,proof,requested,observation_provenance])
    try:obj=coff.parse(raw);parse_error=None
    except (ValueError,UnicodeError,struct.error) as error:obj=None;parse_error=inventory.public_metadata(str(error))
    if obj is not None:
        relocations={i:{canonical(list(x)) for x in s['relocs']} for i,s in obj['sections'].items()}
        for r in requested:
            s=obj['symbols'].get(r['symbol_index'])
            require(s is not None and typed_equal([s[k] for k in ('name','section','value')],
                [r[k] for k in ('symbol','section','value')]),'native selected physical owner contradiction')
    singles={};union_seen=False;common=None;frame=None;count=0
    for view in qualified_views:
        count+=1;require(count<=len(requested)+1,'extra qualified view')
        require(type(view) is dict and set(view)==QUALIFIED_KEYS and type(view.get('schema_version')) is int and view['schema_version']==1 and
            view.get('kind')=='new-cached-metadata-contract' and view.get('policy_id')==QUALIFIED_POLICY and
            all(view.get(k) is False for k in QUALIFIED_FALSE) and view.get('native_observation_required') is True,
            'qualified metadata authority/schema/promotion differs')
        before=digest(view);contract=view['contract'];roots=view['requested_roots']
        require(type(contract) is dict and set(contract)==CONTRACT_KEYS and contract['recipe_id']==unit['recipe_id'] and
            digest(contract)==view['contract_sha256']==view['new_metadata_contract_sha256'],'qualified contract identity/schema differs')
        require(type(roots) is list and roots and len({r['original_address'] for r in roots})==len(roots) and
            all(r['original_address'] in requested_by_address and typed_equal(r,requested_by_address[r['original_address']]) for r in roots), 'borrowed/duplicate qualified root')
        require(typed_equal(contract['roots'],[{k:r[k] for k in NATIVE_KEYS} for r in roots]),'qualified native root scope differs')
        require(contract['export_policy']==ordinary.EXPORT_POLICY and all(contract[k] is True for k in
            ('verified_match','fields_complete','missing_fields_complete','unit_proofs_complete')), 'incomplete qualified contract')
        require(typed_equal(contract['unit_verified_functions'],proof['verified_functions']) and
            typed_equal(contract['parent_eh'],[r for r in proof.get('eh_sections',[]) if r[3] in {v['original_address'] for v in roots}]),
            'qualified unit/EH proof changed')
        p=contract['provenance'];require(p['object_sha256']==unit['object_sha256'] and p['source_sha256']==unit['source_sha256'] and
            p['request_sha256']==observation_provenance['qualified_request_sha256'],'qualified source/request provenance differs')
        fingerprint=digest({k:v for k,v in contract.items() if k not in ('roots','fields','missing_fields','parent_eh','provenance')})
        shared_provenance=digest({k:v for k,v in p.items() if k!='binding_row_references'})
        current=(fingerprint,shared_provenance)
        require(common is None or common==current,'recipe-wide qualified proofs/provenance differ');common=current
        verification=view['source_frame_verification']
        require(type(verification['recipe_index']) is int and verification['recipe_index']==unit['recipe_index'] and
            type(verification['row_count']) is int and verification['row_count']>=0 and
            all(isinstance(verification[k],str) and re.fullmatch('[0-9a-f]{64}',verification[k]) for k in ('raw_sha256','compressed_sha256')) and
            verification.get('whole_data_hash_verified_this_read') is False and
            verification.get('unrequested_frames_verified') is False,'qualified frame identity/claims differ')
        require(frame is None or typed_equal(frame,verification),'qualified unit frame differs');frame=verification
        event=view['event']
        if event=='SINGLE_ROOT_METADATA_CONTRACT':
            require(not union_seen and len(roots)==1,'singleton after union or wrong scope');a=roots[0]['original_address']
            require(a not in singles,'duplicate qualified singleton')
            singles[a]=([digest(r) for r in contract['fields']],[digest(r) for r in contract['missing_fields']],
                        [digest(r) for r in p['binding_row_references']])
            output_event='SINGLE_ROOT_OBSERVATION'
        elif event=='RECIPE_UNION_METADATA_CONTRACT':
            require(not union_seen and set(singles)==set(requested_by_address) and len(roots)==len(requested), 'incomplete/duplicate qualified union')
            for i,values in enumerate((contract['fields'],contract['missing_fields'],p['binding_row_references'])):
                require([digest(r) for r in values]==[h for root in roots for h in singles[root['original_address']][i]], 'union field/missing/reference partition differs')
            union_seen=True;output_event='RECIPE_ROOT_UNION_OBSERVATION'
        else:raise ValueError('unknown qualified view event')
        if obj is not None:
            verify_physical_fields(obj,contract['fields'],relocations)
            if count==1:verify_physical_fields(obj,contract['omission_field_proofs'],relocations)
            certificate=ordinary.assess_object(obj,contract)
            require(certificate['contract_identity_sha256']==view['contract_sha256'] and certificate['full_serialization_eligible'] is False,
                'frozen observation identity/policy changed')
        else:certificate=None
        require(digest(view)==before and digest([unit,proof,requested,observation_provenance])==original_inputs,'observation mutated qualified evidence')
        record=dict(schema_version=1,policy_id=POLICY,kind='fresh-root-observation-from-qualified-contract',event=output_event,
            recipe_id=unit['recipe_id'],recipe_index=unit['recipe_index'],requested_roots=roots,contract=contract,
            contract_identity_sha256=view['contract_sha256'],qualified_metadata_row_sha256=before,
            qualified_metadata_identity={k:view[k] for k in ('schema_version','kind','policy_id','event','certificate_created',
                'native_observation_required','historical_certificate_contract_identity_equal_claimed','source_frame_verification')},
            observation_provenance=observation_provenance,native_object_sha256=unit['object_sha256'],native_parse_performed=obj is not None,
            qualified_contract_unchanged=True,fresh_certificate_created=certificate is not None,**FALSE)
        if certificate is None:
            record.update(closure_observed=False,graph_observation_complete=False,root_closure_candidate=False,
                blockers=[dict(code='UNSUPPORTED_ORIGINAL_COFF_FORMAT',evidence=parse_error)])
        else:
            record.update(certificate=certificate,certificate_sha256=digest(certificate),closure_observed=certificate['closure_observed'],
                graph_observation_complete=certificate['graph_observation_complete'],root_closure_candidate=certificate['root_closure_candidate'],
                blockers=certificate['blockers'])
        yield record
    require(count==len(requested)+1 and union_seen and set(singles)==set(requested_by_address),'partial qualified recipe batch')


ROOT=Path(__file__).resolve().parents[2]
LIMITS=dict(seconds=900,peak_memory_bytes=1024**3,output_bytes=128*1024**2)
JOURNAL_LIMIT=1024**2
ARTIFACT_PINS=dict(selection=inventory.EXPECTED['selection'],manifest=inventory.EXPECTED['manifest'],
    retained=inventory.EXPECTED['retained'],recipes=inventory.EXPECTED['recipes'],
    planned_map='6cd5bf884bb28d460cfc92f63b765c15413904f58355844243ddd6b59b97001c',imports=finite.IMPORT_PIN,
    qualified_receipt='8515d988f83be331e5ce3e68f348f15de6600c6ce0fef173d3c7e16179ae08c7',
    qualified_request='41db05330f7983b353098628a67b6768123ff591a2b97a696c857210e95d930c',
    qualified_records='9d3a15f0feb2815418a68485c3cbb9fb63dc3b181e5a6d91ca60681b0fde4cbf',
    qualified_registry='5b013be46525c93620ffdcbeee06ce07c3ec3c205e54c53ddc443676175090d0',
    qualification_main_review='c35af56da70ffdd9cca665fd832d8df083976bc10c0d0c55c28dcf296346f6b8',
    qualification_authority_review='1c43600094a886fd38528d9b5c6d565dd2790c11182567355dd1d54bbb08954e',
    current_groups='d3677e25ec2b80d84a848765285899922c0e146b452c0e6dc69b7c65e71b3083',
    current_review='2da9a6e506ead22b7177c13b460f2190117759b91a686b5e5a1119b8c37cbc17')
ARTIFACT_KEYS=set(ARTIFACT_PINS)|{'qualified_inventory'}


def budget(start):
    from coff_inventory import peak_memory_bytes
    require(time.monotonic()-start<=LIMITS['seconds'],'observation time bound')
    peak=peak_memory_bytes();require(type(peak) is int and 0<peak<=LIMITS['peak_memory_bytes'],'observation memory bound/counter unavailable')
    return peak


def read_bound_json(path,expected):
    require(isinstance(expected,str) and re.fullmatch('[0-9a-f]{64}',expected),'explicit input SHA required')
    with Path(path).open('rb') as source:raw=source.read(LIMITS['output_bytes']+1)
    require(len(raw)<=LIMITS['output_bytes'] and hashlib.sha256(raw).hexdigest()==expected,'bounded JSON hash differs')
    return json.loads(raw.decode('utf-8-sig'))


def validate_saved_context(receipt,request,qualified_inventory,registry,current_groups,planned,manifest,proof,selection,imports):
    """Pure complete saved-authority gate; no source/object/cache data reads."""
    require(receipt['policy_id']==QUALIFIED_POLICY and receipt['status']=='metadata-only' and
        all(type(receipt[k]) is int for k in ('qualified_metadata_roots','qualified_recipes','generated_contract_records','code_demands','registry_roots')) and
        (receipt['qualified_metadata_roots'],receipt['qualified_recipes'],receipt['generated_contract_records'],receipt['code_demands'],receipt['registry_roots'])==(180,77,257,578,528) and
        receipt['certificate_created'] is False and receipt['native_observation_required'] is True and
        all(receipt[k] is False for k in ('provider_selected','runtime_eligible','native_tools_run','original_objects_read','source_bodies_read','code_emission_performed')),
        'qualified receipt scope/promotion differs')
    require(set(request)=={'schema_version','kind','roots'} and type(request['schema_version']) is int and request['schema_version']==1 and
        request['kind']=='fnv-finite-ordinary-root-request' and len(request['roots'])==MAX_ROOTS,'whole exact180 request required')
    require(typed_equal(qualified_inventory['metadata_requests'],request['roots']) and len(qualified_inventory['records'])==578,
        'qualified inventory request/demand scope differs')
    require(registry['roots']==528 and len(registry['records'])==528 and
        not ({r['original_address'] for r in request['roots']}&set(registry['records'])),'borrowed historical root context')
    require(set(planned['providers'])==set(selection['selections']) and len(selection['selections'])==68657 and
        planned['materialized_exports']==0 and planned['provider_selected'] is False and planned['runtime_eligible'] is False,'planned physical namespace scope differs')
    providers={a:{k:p[k] for k in ('recipe_id','object_sha256','symbol_index')} for a,p in planned['providers'].items()}
    groups=finite.validate_request(request,selection['selections'],manifest,proof,providers)
    require(len(groups)==MAX_RECIPES,'whole exact77 recipe scope required')
    require(current_groups['kind']=='actual-unresolved-LNK-target-groups' and current_groups['executable_execution'] is False and
        current_groups['runtime_eligible'] is False,'current nonexecuted link authority required')
    code_rows=[g for g in current_groups['groups'] if g['classification']=='CODE']
    code={g['symbol']:g for g in code_rows};require(len(code_rows)==len(code)==577,'duplicate/extra current CODE demand')
    old={r['symbol'] for r in qualified_inventory['records']};require(len(old)==578 and len(code)==577,'V11/V12 CODE census differs')
    prepared=planned['providers']['0x008d8520'];removed='_fnv_code_'+digest({k:prepared[k] for k in ('recipe_id','object_sha256','symbol_index')})
    require(not set(code)-old and old-set(code)=={removed},'current authority has additions or wrong prepared removal')
    for r in request['roots']:
        name='_fnv_code_'+digest(providers[r['original_address']]);g=code.get(name)
        require(g is not None and g['observed_roles']==['code'] and g['included_provenance_is_extraction_proof'] is False and
            r['original_address'] in g['original_bases'],'new requested physical root absent from current CODE demand')
    require(all(type(r['recipe_index']) is int and type(r['requested_roots']) is int and r['requested_roots']>0 and
        type(r['verification']['recipe_index']) is int and r['verification']['recipe_index']==r['recipe_index']
        for r in receipt['recipe_frame_verifications']),'qualified frame receipt integer identity differs')
    frames={r['recipe_index']:r for r in receipt['recipe_frame_verifications']}
    require(len(frames)==len(receipt['recipe_frame_verifications'])==MAX_RECIPES and set(frames)==set(groups) and
        all(frames[i]['requested_roots']==len(roots) for i,roots in groups.items()),'qualified complete frame verification scope differs')
    singles={};expected_roots={r['original_address']:r for r in request['roots']}
    for item in qualified_inventory['records']:
        if item.get('inventory_action')!='REQUEST_CACHED_METADATA':continue
        root=item['root'];a=root['original_address'];entry=item['new_metadata']
        require(a not in singles and a in expected_roots and typed_equal(root,expected_roots[a]),'duplicate/borrowed qualified singleton index')
        require(type(entry['contract_record_ordinal']) is int and 1<=entry['contract_record_ordinal']<=MAX_RECORDS and
            all(isinstance(entry[k],str) and re.fullmatch('[0-9a-f]{64}',entry[k]) for k in ('generated_record_sha256','new_metadata_contract_sha256')),
            'qualified singleton ordinal/hash schema differs')
        singles[a]=entry
    require(set(singles)=={r['original_address'] for r in request['roots']},'qualified singleton index coverage differs')
    require(imports['inputs']['manifest']==ARTIFACT_PINS['manifest'] and imports['inputs']['retained']==ARTIFACT_PINS['retained'] and
        imports['inputs']['reference']==proof['inputs']['image_sha256'],'import/reference authority differs')
    imported=[r for r in imports['imports'] if r['import_id']==175];require(len(imported)==1,'exact unit import175 metadata required')
    return dict(groups=groups,singleton_index=singles,frames=frames,imported=imported[0],
        units={u['recipe_index']:u for u in manifest['units']},proofs={p['recipe_index']:p for p in proof['units']})


class DigestingSource:
    """The exact compressed bytes consumed by gzip are also hashed."""
    def __init__(self,source):self.source=source;self.hash=hashlib.sha256();self.bytes=0
    def read(self,size=-1):
        require(size>=0,'unbounded qualified compressed read')
        raw=self.source.read(size);self.bytes+=len(raw);require(self.bytes<=LIMITS['output_bytes'],'qualified compressed input bound')
        self.hash.update(raw);return raw
    def finish(self,expected,size):
        require(not self.read(1) and self.bytes==size and self.hash.hexdigest()==expected,'consumed qualified compressed hash/EOF differs')


class QualifiedReader:
    def __init__(self,stream,prepared,request_sha256):
        self.stream=stream;self.prepared=prepared;self.request_sha256=request_sha256;self.ordinal=0;self.last_index=-1
        self.next=None;self.singletons=set();self.unions=set();self.sequence=hashlib.sha256();self._advance()
    def _advance(self):
        raw=self.stream.readline(LIMITS['output_bytes']+1)
        if not raw:self.next=None;return
        require(len(raw)<=LIMITS['output_bytes'],'qualified metadata row size bound')
        self.ordinal+=1;require(self.ordinal<=MAX_RECORDS,'extra qualified metadata record')
        row=json.loads(raw);roots=row['requested_roots'];require(roots and type(roots[0]['recipe_index']) is int,'qualified root recipe type')
        index=roots[0]['recipe_index'];require(index in self.prepared['groups'] and index>=self.last_index,'foreign/unsorted qualified recipe')
        self.last_index=index;expected={r['original_address']:r for r in self.prepared['groups'][index]}
        require(all(r['original_address'] in expected and typed_equal(r,expected[r['original_address']]) for r in roots),'borrowed qualified physical root')
        require(row['contract_sha256']==row['new_metadata_contract_sha256']==digest(row['contract']) and
            row['contract']['provenance']['request_sha256']==self.request_sha256,'qualified row contract/request identity differs')
        require(typed_equal(row['source_frame_verification'],self.prepared['frames'][index]['verification']),'qualified frame receipt differs')
        if row['event']=='SINGLE_ROOT_METADATA_CONTRACT':
            require(len(roots)==1,'singleton metadata scope differs');a=roots[0]['original_address'];entry=self.prepared['singleton_index'][a]
            require(a not in self.singletons and entry['contract_record_ordinal']==self.ordinal and
                entry['generated_record_sha256']==digest(row) and entry['new_metadata_contract_sha256']==row['contract_sha256'] and
                typed_equal(entry['source_frame_verification'],row['source_frame_verification']),'qualified singleton ordinal/row identity differs')
            self.singletons.add(a)
        elif row['event']=='RECIPE_UNION_METADATA_CONTRACT':
            require(index not in self.unions and len(roots)==len(expected) and {r['original_address'] for r in roots}==set(expected),'qualified union scope differs')
            self.unions.add(index)
        else:raise ValueError('unknown qualified event')
        self.sequence.update(canonical([self.ordinal,digest(row)]));self.next=(self.ordinal,row)
    def take(self,index):
        require(self.next is None or self.next[1]['requested_roots'][0]['recipe_index']>=index,'unconsumed qualified recipe')
        while self.next is not None and self.next[1]['requested_roots'][0]['recipe_index']==index:
            value=self.next;yield value;self._advance()
    def finish(self):
        require(self.next is None and self.ordinal==MAX_RECORDS and len(self.singletons)==MAX_ROOTS and
            self.unions==set(self.prepared['groups']),'partial qualified global batch')
        return dict(records=self.ordinal,singletons=len(self.singletons),unions=len(self.unions),row_sequence_sha256=self.sequence.hexdigest())


def validate_operation(operation):
    """Fixed finite operation envelope; no files are opened by this function."""
    require(type(operation) is dict and set(operation)=={'schema_version','kind','policy_id','epoch','roots','recipes','records',
        'limits','artifacts','source_sha256'},'unknown operation envelope')
    require(type(operation['schema_version']) is int and operation['schema_version']==1 and
        operation['kind']=='whole-qualified-contract-native-observation' and operation['policy_id']==POLICY,'unknown operation policy')
    require(type(operation['epoch']) is str and 0<len(operation['epoch'])<=100 and operation['epoch'].isascii(),'explicit epoch required')
    require(all(type(operation[k]) is int for k in ('roots','recipes','records')) and
        (operation['roots'],operation['recipes'],operation['records'])==(MAX_ROOTS,MAX_RECIPES,MAX_RECORDS) and
        typed_equal(operation['limits'],LIMITS),'whole finite census/resource limits required')
    require(isinstance(operation['source_sha256'],str) and re.fullmatch('[0-9a-f]{64}',operation['source_sha256']),'explicit observer digest required')
    require(type(operation['artifacts']) is dict and set(operation['artifacts'])==ARTIFACT_KEYS,'exact saved authority set required')
    paths=[]
    for name,ref in operation['artifacts'].items():
        require(type(ref) is dict and set(ref)=={'path','sha256'} and isinstance(ref['path'],str) and ref['path'] and
            isinstance(ref['sha256'],str) and re.fullmatch('[0-9a-f]{64}',ref['sha256']),'malformed artifact reference')
        path=(ROOT/ref['path']).resolve()
        require(not Path(ref['path']).is_absolute() and path.is_relative_to(ROOT),'foreign artifact path')
        paths.append(path)
        if name in ARTIFACT_PINS:require(ref['sha256']==ARTIFACT_PINS[name],'saved authority pin differs')
    require(len(set(paths))==len(paths),'artifact path collision')
    return operation


def prepare_operation(operation,observations,started=None):
    def check():
        if started is not None:budget(started)
    check()
    validate_operation(operation)
    paths={name:(ROOT/ref['path']).resolve() for name,ref in operation['artifacts'].items()}
    refs=operation['artifacts'];loaded={}
    for name,path in paths.items():
        if name=='qualified_records':continue
        loaded[name]=read_bound_json(path,refs[name]['sha256']);observations[path]=refs[name]['sha256'];check()
    receipt=loaded['qualified_receipt']
    for key,filename in (('qualified_inventory','inventory.json'),('qualified_request','metadata-request.json'),
                         ('qualified_registry','cache-registry.json'),('qualified_records','metadata-contracts.jsonl.gz')):
        require(receipt['output_sha256'][filename]==refs[key]['sha256'],'qualified receipt/output hash differs')
    observations[paths['qualified_records']]=refs['qualified_records']['sha256']
    prepared=validate_saved_context(receipt,loaded['qualified_request'],loaded['qualified_inventory'],loaded['qualified_registry'],
        loaded['current_groups'],loaded['planned_map'],loaded['manifest'],loaded['retained'],loaded['selection'],loaded['imports'])
    check()
    require(finite.reconcile_recipes(loaded['manifest'],paths['recipes'])['verified'],'authoritative recipe epoch differs')
    check()
    for name,expected in PINS.items():
        path=ROOT/'tools/rebuild'/name;finite.pin(path,expected,observations);check()
    for module,name in ((coff,'coff_code_archive.py'),(ordinary,'root_code_closure.py'),(inventory,'runtime_code_inventory.py'),(finite,'scalableordinary_root_collect.py')):
        require(Path(module.__file__).resolve()==ROOT/'tools/rebuild'/name,'foreign imported observer dependency')
    finite.pin(Path(__file__),operation['source_sha256'],observations)
    for name,expected in loaded['retained']['inputs']['tools_sha256'].items():
        path=(ROOT/name).resolve();require(path.is_relative_to(ROOT),'foreign retained proof dependency');finite.pin(path,expected,observations);check()
    prepared.update(loaded=loaded,paths=paths)
    return prepared


def stream_observations(prepared,reader,read_native,observation_provenance):
    """Read one named raw object per recipe; exhaust all views before success."""
    for index,roots in sorted(prepared['groups'].items()):
        unit,proof=prepared['units'][index],prepared['proofs'][index]
        raw=read_native(unit)
        ordinals=[]
        def views():
            for ordinal,row in reader.take(index):
                ordinals.append(ordinal);yield row
        for record in observe_recipe_contracts(raw,unit,proof,roots,views(),observation_provenance):
            record['qualified_record_ordinal']=ordinals[-1]
            yield record
        del raw
    reader.finish()


def summary_row(record,ordinal):
    return dict(ordinal=ordinal,event=record['event'],recipe_id=record['recipe_id'],recipe_index=record['recipe_index'],
        roots=[r['original_address'] for r in record['requested_roots']],record_sha256=digest(record),
        qualified_record_ordinal=record['qualified_record_ordinal'],qualified_metadata_row_sha256=record['qualified_metadata_row_sha256'],
        contract_identity_sha256=record['contract_identity_sha256'],certificate_sha256=record.get('certificate_sha256'),
        closure_observed=record['closure_observed'],graph_observation_complete=record['graph_observation_complete'],
        blocker_codes=dict(Counter(b['code'] for b in record['blockers'])))


def owned_identity(path):
    stat=path.lstat();return stat.st_dev,stat.st_ino


def retract_outputs(published):
    for item in published:
        try:
            if owned_identity(item['path'])==item['identity']:item['path'].unlink()
        except FileNotFoundError:pass


def verify_outputs(published):
    for item in published:
        require(owned_identity(item['path'])==item['identity'] and finite.file_hash(item['path'])==item['sha256'],
            'published artifact identity/hash changed')


def created_output(path,target,published,sha256):
    stat=os.fstat(target.fileno())
    published.append(dict(path=path,identity=(stat.st_dev,stat.st_ino),sha256=sha256))


def publish_outputs(out,details,stage,result,observations,index,published,started):
    """Only remove files successfully created by this attempt, including drift."""
    try:
        finite.stable(observations);require(not index.exists(),'optional index appeared before publication');budget(started)
        details.parent.mkdir(parents=True,exist_ok=True);stage.seek(0)
        with details.open('xb') as target:
            created_output(details,target,published,result['details_sha256'])
            while block:=stage.read(1048576):target.write(block)
            target.flush();os.fsync(target.fileno())
        require(finite.file_hash(details)==result['details_sha256'],'published detail differs from staged bytes')
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('xb') as target:
            created_output(out,target,published,hashlib.sha256(canonical(result)+b'\n').hexdigest())
            target.write(canonical(result)+b'\n');target.flush();os.fsync(target.fileno())
        require(finite.file_hash(out)==hashlib.sha256(canonical(result)+b'\n').hexdigest(),'published summary differs')
        finite.stable(observations);require(not index.exists(),'optional index appeared after publication');budget(started);verify_outputs(published)
    except BaseException:
        retract_outputs(published)
        raise


def _run(args,published,state):
    started=time.monotonic();operation_path=Path(args.operation).resolve()
    state['started']=started
    budget(started)
    operation=read_bound_json(operation_path,args.operation_sha256);validate_operation(operation)
    budget(started)
    observations={operation_path:args.operation_sha256};prepared=prepare_operation(operation,observations,started)
    state['observations']=observations
    reserved=set(observations)
    for unit in prepared['loaded']['manifest']['units']:
        obj=(prepared['paths']['manifest'].parent/prepared['loaded']['manifest'].get('object_root_relative','.')/unit['object']).resolve()
        src=(ROOT/unit['source']).resolve();reserved.update((src,obj))
    budget(started)
    out,details,progress=finite.output_paths(args.out,args.details,reserved)
    require(all(path.is_relative_to(ROOT/'build/rebuild') for path in (out,details,progress)),'private rebuild output paths required')
    index=ROOT/'build/function_index.json';require(not index.exists(),'optional index appeared')
    progress.parent.mkdir(parents=True,exist_ok=True)
    with progress.open('x',encoding='utf-8') as journal:
        def note(value):
            journal.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-started,3),**value))+'\n');journal.flush();os.fsync(journal.fileno())
            require(os.fstat(journal.fileno()).st_size<=JOURNAL_LIMIT,'progress journal byte bound')
        note(dict(state='started',pid=os.getpid(),epoch=operation['epoch'],roots=MAX_ROOTS,recipes=MAX_RECIPES))
        try:
            peak=budget(started);summaries=[];native_reads=0
            def read_native(unit):
                nonlocal native_reads,peak
                peak=max(peak,budget(started));src=(ROOT/unit['source']).resolve();require(src.is_relative_to(ROOT),'foreign selected source')
                finite.pin(src,unit['source_sha256'],observations)
                obj=(prepared['paths']['manifest'].parent/prepared['loaded']['manifest'].get('object_root_relative','.')/unit['object']).resolve()
                require(obj.is_relative_to(ROOT),'foreign selected object')
                with obj.open('rb') as source:raw=source.read(LIMITS['output_bytes']+1)
                require(len(raw)<=LIMITS['output_bytes'],'named original object byte bound')
                peak=max(peak,budget(started))
                require(hashlib.sha256(raw).hexdigest()==unit['object_sha256'],'fresh named object hash differs')
                observations[obj]=unit['object_sha256'];native_reads+=1
                note(dict(state='read_named_recipe_once',recipe_index=unit['recipe_index'],recipe_id=unit['recipe_id']))
                return raw
            provenance=dict(qualified_request_sha256=operation['artifacts']['qualified_request']['sha256'],
                observation_epoch=operation['epoch'],operation_sha256=args.operation_sha256,collector_sha256=operation['source_sha256'],
                saved_authorities={name:ref['sha256'] for name,ref in operation['artifacts'].items()},
                dependency_tools_sha256={p.relative_to(ROOT).as_posix():h for p,h in observations.items() if p.is_relative_to(ROOT/'tools')},
                optional_function_index_present=False,qualified_contract_provenance_restamped=False)
            with tempfile.TemporaryFile() as stage:
                path=prepared['paths']['qualified_records'];size=path.stat().st_size
                with path.open('rb') as source:
                    compressed=DigestingSource(source)
                    with gzip.GzipFile(fileobj=compressed,mode='rb') as incoming,gzip.GzipFile(fileobj=stage,mode='wb',mtime=0) as writer:
                        reader=QualifiedReader(incoming,prepared,operation['artifacts']['qualified_request']['sha256'])
                        for record in stream_observations(prepared,reader,read_native,provenance):
                            writer.write(canonical(record)+b'\n');summaries.append(summary_row(record,len(summaries)+1))
                            require(stage.tell()<=LIMITS['output_bytes'],'staged output bound');peak=max(peak,budget(started))
                        census=reader.finish()
                    compressed.finish(operation['artifacts']['qualified_records']['sha256'],size)
                require(len(summaries)==MAX_RECORDS and native_reads==MAX_RECIPES,'incomplete native observation batch')
                detail_size=stage.seek(0,2);require(detail_size<=LIMITS['output_bytes'],'closed staged output bound')
                stage.seek(0);hasher=hashlib.sha256()
                while block:=stage.read(1048576):hasher.update(block)
                summary=dict(roots=MAX_ROOTS,recipes=MAX_RECIPES,records=len(summaries),
                    singleton_closure=sum(r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'),
                    singleton_blocked=sum(not r['closure_observed'] for r in summaries if r['event']=='SINGLE_ROOT_OBSERVATION'),
                    union_closure=sum(r['closure_observed'] for r in summaries if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'),
                    union_blocked=sum(not r['closure_observed'] for r in summaries if r['event']=='RECIPE_ROOT_UNION_OBSERVATION'))
                result=dict(schema_version=1,policy_id=POLICY,status='metadata-only',epoch=operation['epoch'],operation_sha256=args.operation_sha256,
                    source_sha256=operation['source_sha256'],inputs=operation['artifacts'],details_sha256=hasher.hexdigest(),details_bytes=detail_size,
                    summary=summary,observations=summaries,qualified_census=census,native_object_observation_reads=native_reads,
                    native_object_parse_attempts=MAX_RECIPES,original_binding_stream_traversals=0,owner_stream_traversals=0,cache_frame_reads=0,
                    additional_source_and_object_stability_rehash_reads=True,
                    historical_roots_reobserved=0,qualified_contracts_preserved=True,input_stability=True,optional_function_index_present=False,
                    observed_input_bindings=[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sorted(observations.items())],
                    peak_memory_bytes=peak,elapsed_seconds=round(time.monotonic()-started,3),**FALSE)
                require(len(canonical(result))+1+detail_size+JOURNAL_LIMIT<=LIMITS['output_bytes'],'complete output including journal reserve bound')
                publish_outputs(out,details,stage,result,observations,index,published,started)
            note(dict(state='complete',receipt_sha256=finite.file_hash(out),details_sha256=result['details_sha256'],summary=summary))
            return result
        except BaseException as error:
            retract_outputs(published)
            note(dict(state='failed',error_type=type(error).__name__));raise


def run(args):
    published=[];state={}
    try:
        result=_run(args,published,state)
        # The journal has durably closed before the final successful return.
        finite.stable(state['observations']);require(not (ROOT/'build/function_index.json').exists(),'optional index appeared at final gate')
        budget(state['started']);verify_outputs(published)
        return result
    except BaseException:
        retract_outputs(published);raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('operation','out','details'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--operation-sha256',required=True);args=parser.parse_args(argv)
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'cached root observation rejected: '+str(error)+'\n')
    print(json.dumps(result['summary']));return 0


if __name__=='__main__':raise SystemExit(main())
