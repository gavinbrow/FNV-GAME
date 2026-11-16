"""Fixed UUID2768 derived-artifact consumer; no I/O, original reads or adoption."""
import collections
import copy
import gzip
import hashlib
import io
import json
import re

import application_link_frontier as frontier
import coff_code_archive as coff

POLICY='application-uuid2768-derived-consumer-v1'
PINS={'receipt':'fdec31d202ebbed1e846c0c8198a384db995d05aab5433b75d475b4f820ba98c',
'object':'6fcd604987e08477566cbf9b6901f3200304eb557fdc8f7c356fedaf27d633b3',
'archive':'b921ee8a8d6baf9a751f1a488aa10a763627ede51b2b475668c97455a4e9eb53',
'proof':'4b7cb6ce64a9a84d461ef0ef536cd17c5952fe03b697e45e652e18c2f5e7cc31',
'base_review':'dc5553cc029f0821b01c645a4975a70bdabc1a959f95178919df534f51d6b89e',
'continuity':'e5bead380f35dbb91947ecf14d2f3d776e5b4cf7523cf8aa28348e8aaf09e8db',
'native_receipt':'12dae2e56d941949650dbc8c0d72a0660c4d8da5d4d14f2209db4f79e2c852f1',
'native_review':'f161af6ac5ce40e02088724ba156f7737484def6b5aafadc4f8bda104587b7f6',
'declaration':'2cf2f061f003d027213cbfa77e53f2a15be34de8db62fa32712148ff6dbb51ac',
'context':'8b044fe51ce0b455ea6baac1c88441d566ec1514e4def0866b7102382b1b784f',
'declaration_review':'9cce2a0d39394c9bf0b564a8f872a83b655f83bb22a6db036f306643f15c9dfd',
'declaration_audit':'32481c04d52919500766a9e10b1a0d2ffe801254a1d542721e49773c6daad1dd',
'handoff':'4ce4f515e43a04f622b1efaa70ac47753f16109111944f73ca0aefeb915b06a1',
'handoff_review':'7b879e3baa1bf55e81c9a9884f692b27feff025c0d5fe55a30d7c3d60135ab9d'}
CERT='7c4704d0c777585656272cd2a39a06437d124e34d4cea712236b982641cf9a26'
CONTRACT='4480150173b81b205a05fd92fff0f3707ef090ea2402217379bceb121cdad4df'
COMPOSITION='69076d817070c2411fbb8d3dbf9cf1ea0ca3409d6a438360c25dffc19aa7d238'
ROOT='0x00c5d4e0'
EXPECTED_SDK={'path':r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\PlatformSDK\Lib\Uuid.Lib',
'sha256':'6f363d2fbc78a5c17354bacfb481e615aeb4b0fd462581c02f9d6aca3e893969',
'device':11251121510599050284,'inode':1970324839389565,'size':2812980}
FALSE=('ABI_verified','provider_selected','runtime_eligible','link_ready','compiler_performed',
       'native_tools_run','executable_link_performed','game_execution_performed')

def require(ok,msg):
    if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def _json(b):
    require(type(b) is bytes and len(b)<=8*1024*1024,'invalid evidence bytes');return json.loads(b)

def _comparison(rows,symbol,fields):
    require(type(rows) is list and len(rows)==1,'singleton saved comparison required');r=rows[0]
    require(r.get('address')==ROOT and r.get('symbol')==symbol and type(r.get('size')) is int and r['size']==58 and
            type(r.get('compiled_extent')) is int and r['compiled_extent']==58 and r.get('verdict')=='match' and
            r.get('errors')==[] and not r.get('byte_differences',[]) and type(r.get('relocations')) is list and
            len(r['relocations'])==9 and all(type(x) is dict and x.get('match') is True for x in r['relocations']),
            'saved full span and nine relocation MATCH required')
    require([(x.get('offset'),x.get('kind'),x.get('expected'),x.get('observed')) for x in r['relocations']]==
            [(f['offset'],f['kind'],f['original_target'],f['original_target']) for f in fields],
            'saved comparison target/offset differs')

def _consume_core(evidence):
    r=_json(evidence['receipt']);base=_json(evidence['base_review']);cont=_json(evidence['continuity'])
    nr=_json(evidence['native_receipt']);np=_json(evidence['native_review']);dec=_json(evidence['declaration'])
    ctx=_json(evidence['context']);dr=_json(evidence['declaration_review']);audit=_json(evidence['declaration_audit'])
    handoff=_json(evidence['handoff']);handoff_review=_json(evidence['handoff_review'])
    obj=evidence['object'];archive=evidence['archive'];coff.parse(obj);ar=coff.read_archive(archive)
    require(ar['members']==[('uuid2768.obj',obj)] and len(ar['index'])==1,'derived archive member/index differs')
    with gzip.GzipFile(fileobj=io.BytesIO(evidence['proof'])) as gz:content=gz.read(4*1024*1024+1)
    require(len(content)<=4*1024*1024 and content.endswith(b'\n') and len(content.splitlines())==1,'proof gzip scope')
    ledger=_json(content);v=r['result'];p=v['projection'];assessment=v['assessment'];root=p['requested_roots'][0]
    require(r.get('kind')=='finite-uuid2768-factory-outcome-v1' and r.get('emitted')==1 and r.get('fields')==9 and
       r.get('code_bytes')==58 and r.get('archive_sha256')==PINS['archive'] and r.get('field_proof_sha256')==PINS['proof'] and
       r.get('original_negative_certificate_preserved') is True and v.get('original_negative_unchanged') is True and
       ledger==v['field_ledger'] and ledger.get('original_negative_unchanged') is True and
       ledger.get('certificate_sha256')==CERT and ledger.get('contract_sha256')==CONTRACT and
       ledger.get('composition_sha256')==COMPOSITION and ledger.get('output_sha256')==PINS['object'], 'producer lineage differs')
    require(root['original_address']==ROOT and root['size']==58 and root['recipe_index']==2768 and
       ledger['root']==root and p['output_sha256']==PINS['object'] and p['original_negative_certificate_sha256']==CERT and
       p['contract_identity_sha256']==CONTRACT and p['composed_certificate_sha256']==COMPOSITION and
       p['base_closure_observed'] is False and p['full_serialization_eligible'] is False and
       p['original_negative_certificate_preserved'] is True and all(p.get(k) is False for k in FALSE) and
       assessment.get('eligible') is True and assessment.get('serialization_performed') is False and
       all(assessment.get(k) is False for k in FALSE), 'typed projection scope differs')
    require(type(ledger['fields']) is list and type(ledger['mapped_fields']) is list and
       len(ledger['fields'])==len(ledger['mapped_fields'])==len(p['fields'])==9 and
       digest(canonical(ledger['fields']))==ledger['fields_sha256'], 'full proof fields differ')
    require(collections.Counter(x['role'] for x in p['fields'])=={'code':7,'data':2},'unexpected role')
    for n,(orig,mapped,field) in enumerate(zip(ledger['fields'],ledger['mapped_fields'],p['fields']),1):
        cr=orig['coff_relocation'];require(mapped['ordinal']==n and digest(canonical(orig))==mapped['original_field_sha256']==field['field_proof_sha256'] and
          (orig['physical_section'],cr['offset'],cr['symbol_index'],cr['kind'])==
          (field['section'],field['offset'],field['symbol_index'],field['kind']) and
          mapped['original_section']==field['section'] and mapped['original_offset']==field['offset'] and
          mapped['original_symbol_index']==field['symbol_index'] and mapped['kind']==field['kind'] and
          all(mapped[k]==field[k] for k in ('role','canonical_name','original_base','original_target','addend_bits')) and
          mapped['serialized_section']==p['maps']['section_map'][str(field['section'])] and
          mapped['serialized_symbol_index']==p['maps']['symbol_map'][str(field['symbol_index'])], 'full field ancestry differs')
    _comparison(v['before_comparison'],root['symbol'],p['fields']);_comparison(v['after_comparison'],p['exports'][0],p['fields'])
    require(base.get('status')=='accepted-projected-pending-native-conformance' and base.get('receipt_sha256')==PINS['receipt'] and
       base.get('object_sha256')==PINS['object'] and base.get('archive_sha256')==PINS['archive'] and
       base.get('field_proofs_sha256')==PINS['proof'] and base.get('full58B_before_after_saved_MATCH') is True and
       base.get('original_negative_preserved') is True, 'base independent review differs')
    require(cont.get('status')=='accepted-derived-and-saved-only' and cont.get('base_review_sha256')==PINS['base_review'] and
       cont.get('declaration_sha256')==PINS['declaration'] and cont.get('dependency_context_sha256')==PINS['context'] and
       cont.get('exact_original93B_directive_retained') is True and cont.get('future_fullpath_UUID_response_obligation_unchanged') is True,
       'continuity review differs')
    require(np.get('status')=='accepted' and np.get('receipt_sha256')==PINS['native_receipt'] and
       np.get('object_sha256')==PINS['object'] and np.get('archive_sha256')==PINS['archive'] and
       np.get('UUID_selected_or_loaded') is False and nr.get('UUID_selected_or_loaded') is False and
       nr.get('kind')=='uuid2768-native-conformance-v1' and nr.get('status')=='pass' and
       nr.get('input_stability_verified') is True and len(nr['components'])==1 and
       nr['components'][0]['facts']['exports']==1 and nr['components'][0]['facts']['members']==1 and
       nr['typed_producer_evidence']['base_closure_observed'] is False and
       nr['typed_producer_evidence']['original_negative_preserved'] is True and
       nr['typed_producer_evidence']['nested_sha256']=={'assessment':digest(canonical(assessment)),
           'field_ledger':digest(canonical(ledger)),'projection':digest(canonical(p))} and
       all(nr.get(k) is False for k in ('ABI_verified','provider_selected','runtime_eligible','Game_execution','executable_linked')) and
       type(np.get('native_commands_replayed')) is int and np['native_commands_replayed']==0, 'native review differs')
    candidate=ctx['normal_sdk_search_candidate'];path=dec['absolute_path']
    require(dec.get('kind')=='explicit-normal-sdk-library-dependency-v1' and dec.get('library_name')=='uuid.lib' and
       dec['required_response_token']==path==r['future_uuid_response_token']==candidate['path'] and
       {k:candidate[k] for k in EXPECTED_SDK}==EXPECTED_SDK and candidate['sha256']==dec['sha256'] and dr.get('status')=='accepted' and
       dr.get('declaration_sha256')==digest(canonical(dec)) and audit.get('status')=='accepted' and
       audit.get('declaration_raw_sha256')==PINS['declaration'] and audit.get('context_sha256')==PINS['context'] and
       audit.get('review_file_sha256')==PINS['declaration_review'] and
       all(type(candidate[k]) is int for k in ('device','inode','size')) and
       all(audit['sdk_'+k]==candidate[k] for k in ('device','inode','size')) and audit['sdk_candidate_sha256']==dec['sha256'],
       'reviewed normal UUID dependency differs')
    require(handoff.get('kind')=='accepted-qualified-UUID-CODE-export-handoff' and handoff.get('sealed') is True and
       len(handoff['records'])==1 and handoff.get('future_uuid_response_token')==path and
       handoff.get('native_archive_conformance_verified') is False and
       all(handoff.get(k) is False for k in ('provider_selected','runtime_eligible','ABI_verified','library_selected','library_loaded')) and
       handoff_review.get('status')=='accepted-qualified-metadata-handoff' and
       handoff_review.get('handoff_sha256')==PINS['handoff'] and handoff_review.get('complete_fields')==9 and
       handoff_review.get('original_negative_occurrences')==3 and handoff_review.get('whole_payload_matches_independently_reviewed_draft') is True,
       'qualified typed handoff review differs')
    hr=handoff['records'][0];directive=handoff['directive'];parsed=coff.parse(obj)
    require(hr['root']==root and hr['canonical_export']==p['exports'][0] and hr['original_fields']==ledger['fields'] and
       hr['normalized_fields']==ledger['mapped_fields'] and hr['namespace_maps']==p['maps'] and
       hr['original_negative_occurrences']==p['discharged_blocker_occurrences'] and
       hr['original_negative_certificate_sha256']==CERT and hr['original_contract_sha256']==CONTRACT and
       hr['qualified_composition_sha256']==COMPOSITION and hr['projection_sha256']==digest(canonical(p)) and
       hr['qualified_assessment_sha256']==digest(canonical(assessment)) and
       hr['field_ledger_sha256']==digest(canonical(ledger)) and hr['namespace_maps_sha256']==digest(canonical(p['maps'])),
       'typed handoff proof ancestry differs')
    directive_payload=bytes.fromhex(directive['payload_hex']);directive_section=parsed['sections'][p['maps']['section_map']['1']]
    require(len(directive_payload)==93 and digest(directive_payload)==directive['payload_sha256'] and
       directive_section['name']=='.drectve' and directive_section['size']==93 and directive_section['flags']==0x100a00 and
       directive_section['payload']==directive_payload and not directive_section['relocs'] and
       directive['ordered_tokens']==['/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"uuid.lib"','/DEFAULTLIB:"LIBCMT"','/DEFAULTLIB:"OLDNAMES"'],
       'typed directive scope differs')
    require(ar['index']==[(p['exports'][0],'uuid2768.obj')], 'archive canonical export differs')
    providers,mapped=frontier.ordinary_member(obj,{'name':'uuid2768.obj','projection':p},component='uuid2768')
    require(len(providers)==1 and len(mapped)==9,'physical mapping count differs')
    for i,row in enumerate(mapped):row['original_field_proof']=copy.deepcopy(ledger['fields'][i]);row['normative_field']=copy.deepcopy(ledger['mapped_fields'][i])
    return {'kind':'qualified-uuid2768-consumer-evidence-v1','policy_id':POLICY,'providers':providers,'mapped_fields':mapped,
       'original_negative_certificate_sha256':CERT,'contract_sha256':CONTRACT,'qualified_composition_sha256':COMPOSITION,
       'base_closure_observed':False,'full_serialization_eligible':False,'dependency_identity':{k:candidate[k] for k in ('path','sha256','device','inode','size')},
       'future_uuid_response_token':path,'original_negative_occurrences':copy.deepcopy(p['discharged_blocker_occurrences']),
       'provider_selected':False,'runtime_eligible':False,'ABI_verified':False,'link_ready':False,
       'UUID_selected_or_loaded':False,'fresh_sdk_identity_verified':False,'response_checked':False}

def consume(evidence):
    """Authenticate each exact saved byte string before any parsing or mapping."""
    require(type(evidence) is dict and set(evidence)==set(PINS),'exact evidence set required')
    require(all(type(evidence[k]) is bytes and len(evidence[k])<=8*1024*1024 and digest(evidence[k])==v for k,v in PINS.items()),'fixed evidence pin differs')
    return _consume_core(evidence)

def guard_response(tokens,fresh_identity,qualified):
    """Pure gate on token list and caller-observed identity; does not read the SDK."""
    require(type(qualified) is dict and qualified.get('policy_id')==POLICY and
       qualified.get('kind')=='qualified-uuid2768-consumer-evidence-v1','qualified consumer evidence required')
    require(type(tokens) is list and all(type(x) is str and x for x in tokens),'parsed response tokens required')
    path=qualified['future_uuid_response_token'];identity=qualified['dependency_identity']
    require(identity==EXPECTED_SDK and path==EXPECTED_SDK['path'], 'qualified UUID authority differs')
    require(type(fresh_identity) is dict and set(fresh_identity)=={'path','sha256','device','inode','size'} and
       fresh_identity==identity and all(type(fresh_identity[x]) is int for x in ('device','inode','size')),
       'caller-observed physical UUID identity differs')
    hits=[x for x in tokens if re.search(r'(?i)(?<![a-z0-9_])uuid(?:\.lib)?(?![a-z0-9_])',x)]
    require(hits==[path],'exact full UUID path exactly once; no alternate UUID token')
    return {'status':'response-obligation-consistent','required_token':path,'caller_fresh_identity_required':True,
            'fresh_sdk_identity_verified':False,'library_selected':False,'library_loaded':False,'runtime_eligible':False}
