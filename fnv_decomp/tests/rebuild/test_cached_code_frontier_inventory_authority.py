"""Original metadata authority cases; copied authority literals are not real evidence."""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_code_frontier_inventory as inventory


def universe(count=578):
    providers={};units={};roots=[];groups=[]
    special=['0x0086beb0','0x004e6620','0x0086ff70']
    for i in range(count):
        address=special[i]if i<3 else '0x%08x'%(0x02000000+i*32)
        p=dict(recipe_id='authored-inventory-%d'%i,object_sha256='%064x'%(i+1),source_sha256='f'*64,
            symbol='_authored_%d'%i,symbol_index=i+4,section=1,value=0,size=17)
        identity={k:p[k]for k in ('recipe_id','object_sha256','symbol_index')}
        p['planned_canonical_name']=inventory.base.pool.canonical(identity);providers[address]=p
        units[p['recipe_id']]=dict(recipe_index=i,object_sha256=p['object_sha256'],source_sha256=p['source_sha256'])
        r=inventory.planner.root_record(address,p,units);roots.append(r)
        groups.append(dict(symbol=p['planned_canonical_name'],classification='CODE',observed_roles=['code'],
            original_bases=[address],original_targets=[address],included_provenance_is_extraction_proof=False))
    report=dict(kind='actual-unresolved-LNK-target-groups',groups=groups,classifications=dict(CODE=count),executable_execution=False,runtime_eligible=False)
    return providers,units,roots,report


def routing_fixture():
    providers,units,roots,groups=universe();records={};offset=0
    for kind,receipt,request,count in inventory.AUTHORITY_PINS:
        for ordinal,root in enumerate(roots[offset:offset+count],1):
            i=root['recipe_index'];positive=i<3 or i==4
            s=dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],roots=[root['original_address']],
                closure_observed=positive,graph_observation_complete=True,blocker_codes={}if positive else{'AUTHORED_BLOCKER':1},
                record_sha256='%064x'%(1000+i),certificate_sha256='%064x'%(2000+i))
            a=dict(kind=kind,receipt_sha256=receipt,request_sha256=request,record_sha256=s['record_sha256'],certificate_sha256=s['certificate_sha256'],
                contract_identity_sha256=None,contract_identity_is_bound_through_record_hash=True,ordinal=ordinal)
            if kind=='cached-central':s.update(lane=1,lane_record_ordinal=ordinal);a['lane']=1
            else:s['ordinal']=ordinal
            records[root['original_address']]=dict(root=root,summary=s,authority=a)
        offset+=count
    registry=dict(schema_version=1,kind='distinct-authority-original-root-registry',roots=528,records=records,
        authorities=[dict(kind=k,receipt_sha256=r,request_sha256=q,roots=n)for k,r,q,n in inventory.AUTHORITY_PINS],
        contract_digest_loaded_only_from_authenticated_body=True)
    quarantine=[dict(root=r,fresh_body_compared=False,blockers=[dict(code='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2')])for r in roots[:3]]
    return groups,providers,units,registry,{groups['groups'][3]['symbol']},quarantine


def epoch_fixture():
    providers,units,roots,_=universe(4);root=roots[3]
    old=[]
    for i in range(2):
        identity=dict(recipe_id='authored-parent-%d'%i,object_sha256='a'*64,symbol_index=i)
        old.append(dict(canonical=inventory.base.pool.canonical(identity),namespace_identity=identity,
                        category='ordinary'if i==0 else'application-candidate',authored_nested_marker=dict(preserved=i)))
    parent=dict(kind='prepared-CODE-collision-exclusions',ordinary_prepared_count=1,collision_exclusion_count=2,records=old,
        ordinary_names=[old[0]['canonical']],exclusion_names=sorted(r['canonical']for r in old),
        application_selection_inferred_from_counts=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False)
    name=inventory.base.pool.canonical({k:root[k]for k in ('recipe_id','object_sha256','symbol_index')})
    entry=dict(root=root,canonical=name,original_object_sha256=root['object_sha256'],original_negative_certificate_preserved=True,
        selection2_auxiliary_preserved=True,selection_rewritten=False,original_negative_certificate_sha256='b'*64,
        composed_certificate_sha256='c'*64,observer_record_sha256='d'*64,definition_census_sha256='e'*64,
        member='authored-typed.obj',member_sha256='9'*64,serialized_symbol_index=0)
    handoff=dict(kind='accepted-typed-COMDAT-CODE-export-handoff',records=[entry],new_distinct_exports=1,
        upstream_ordinary_prepared_count=1,upstream_collision_exclusion_count=2,successor_ordinary_prepared_count=2,successor_collision_exclusion_count=3,
        original_negative_certificates_preserved=True,selection2_auxiliaries_preserved=True,requires_successor_exclusion_epoch=True,
        selection_rewritten=False,provider_selected=False,runtime_eligible=False,application_manifest_adopted=False,native_tools_run=False)
    return parent,handoff,providers,units


def extend(values):return inventory.extend_epoch(*values,expected_parent=(1,2),expected_new=1)


def cache_receipt_fixture():
    """Only the consumed descriptor schema; not an authenticated production index."""
    cm=inventory.seam.cache_module
    receipt=dict(schema_version=1,policy_id=cm.POLICY,status='metadata-cache-only',lossless_cache_complete=True,
        input_stability=True,optional_function_index_present=False,units=2988,selected_functions=68657,rows=490801,
        producer_sha256=inventory.PINS['tools/rebuild/binding_context_cache.py'],inputs=copy.deepcopy(cm.PINS),
        data_sha256=inventory.DATA_SHA,index_sha256=inventory.KNOWN['cache_index'],original_raw_sha256='a'*64,
        row_sequence_sha256=cm.SEQUENCE,index_bytes=40,data_bytes=80,**cm.FALSE)
    index={k:copy.deepcopy(receipt[k])for k in ('inputs','data_sha256','data_bytes','row_sequence_sha256','units','selected_functions','rows','original_raw_sha256')}
    index['data_file']='authored-cache.bin'
    return receipt,index


def validate_cache(values):return inventory.validate_cache_receipt(*values,data_name='authored-cache.bin',index_bytes=40,data_bytes=80)


def range_fixture(folder):
    first=b'authored-unrequested-frame';second=b'authored-selected-frame'
    path=folder/'cache.bin';path.write_bytes(first+second)
    index=dict(data_bytes=len(first+second),frames=[])
    for i,payload,offset in [(0,first,0),(1,second,len(first))]:
        index['frames'].append(dict(recipe_index=i,offset=offset,compressed_bytes=len(payload),
            compressed_sha256=hashlib.sha256(payload).hexdigest(),raw_sha256=str(i+1)*64,row_sequence_sha256=str(i+3)*64))
    return path,index,len(first)


class IndependentInventoryAuthorityTests(unittest.TestCase):
    def test_typed_append_preserves_parent_and_original_negative_identity_without_admission(self):
        values=epoch_fixture();before=copy.deepcopy(values);result=extend(values)
        old={r['canonical']:r for r in values[0]['records']};new={r['canonical']:r for r in result['records']}
        self.assertEqual({k:new[k]for k in old},old);self.assertEqual(values,before)
        added=next(r for r in result['records']if r['canonical']not in old)
        self.assertEqual(added['identity_mode'],'original-selected-physical-typed-COMDAT')
        self.assertEqual(added['serialized_symbol_index'],0);self.assertEqual(added['original_negative_certificate_sha256'],'b'*64)
        self.assertTrue(added['selection2_auxiliary_preserved']);self.assertFalse(added['selection_rewritten'])
        for flag in inventory.FALSE:self.assertIs(result[flag],False)

    def test_typed_physical_boolean_aliases_and_serialized_index_are_rejected(self):
        for key,value in [('value',False),('section',True),('serialized_symbol_index',False),('serialized_symbol_index',-1)]:
            values=epoch_fixture();entry=values[1]['records'][0]
            (entry if key=='serialized_symbol_index'else entry['root'])[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):extend(values)

    def test_all_typed_and_member_hashes_require_lowercase_hex(self):
        for key in ('original_negative_certificate_sha256','composed_certificate_sha256','observer_record_sha256','definition_census_sha256','member_sha256'):
            values=epoch_fixture();values[1]['records'][0][key]='g'*64
            with self.subTest(key=key),self.assertRaises(ValueError):extend(values)

    def test_parent_ordinary_category_must_match_its_names_before_append(self):
        values=epoch_fixture();values[0]['records'][0]['category']='application-candidate'
        with self.assertRaises(ValueError):extend(values)

    def test_578_partition_preserves_528_authorities_and_prioritizes_typed_prepared_and_quarantines(self):
        values=routing_fixture();before=copy.deepcopy(values);result=inventory.classify_demands(*values)
        self.assertEqual(result['code_demands'],578);self.assertEqual(result['registry_roots'],528)
        self.assertEqual(len(result['metadata_requests']),51)
        self.assertEqual(result['counts'],dict(PRESERVED_REFERENCE_GROUP_QUARANTINE=3,PREPARED_SKIP=1,
            CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION=1,CACHED_ORIGINAL_OMISSION_BLOCKED=523,
            NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=50))
        for row in result['records']:
            if row['state']in('PRESERVED_REFERENCE_GROUP_QUARANTINE','PREPARED_SKIP','CACHED_ORIGINAL_OMISSION_BLOCKED'):
                self.assertEqual(row['inventory_action'],'LEDGER_ONLY')
        self.assertEqual(values,before)
        for flag in inventory.FALSE:self.assertIs(result[flag],False)

    def test_registry_receipt_record_certificate_and_typed_locator_cannot_be_borrowed(self):
        for key in ('receipt_sha256','request_sha256','record_sha256','certificate_sha256','ordinal','lane'):
            values=routing_fixture();row=next(iter(values[3]['records'].values()))
            row['authority'][key]=True if key in('ordinal','lane')else'e'*64
            with self.subTest(key=key),self.assertRaises(ValueError):inventory.classify_demands(*values)

    def test_unknown_negative_certificate_is_preserved_without_metadata_hydration(self):
        values=routing_fixture();row=list(values[3]['records'].values())[5]
        row['summary']['certificate_sha256']=row['authority']['certificate_sha256']=None
        result=inventory.classify_demands(*values)
        record=next(r for r in result['records']if r.get('root',{}).get('original_address')==row['root']['original_address'])
        self.assertEqual(record['state'],'CACHED_ORIGINAL_OMISSION_BLOCKED');self.assertEqual(record['inventory_action'],'LEDGER_ONLY')
        self.assertIsNone(record['cached_observation']['certificate_sha256'])

    def test_prepared_namespace_cannot_silently_remove_quarantine_or_source_identity(self):
        for mutation in ('prepared','source','fresh-compare','boolean-value'):
            values=routing_fixture()
            if mutation=='prepared':values[4].add(values[0]['groups'][0]['symbol'])
            elif mutation=='source':values[5][0]['root']=dict(values[5][0]['root'],source_sha256='e'*64)
            elif mutation=='fresh-compare':values[5][0]['fresh_body_compared']=True
            else:values[5][0]['root']=dict(values[5][0]['root'],value=False)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):inventory.classify_demands(*values)

    def test_cache_receipt_index_identity_is_typed_and_nonpromoting(self):
        validate_cache(cache_receipt_fixture())
        for mutation in ('schema','index','data','name','promoted','raw-index'):
            values=cache_receipt_fixture();receipt,index=values
            if mutation=='schema':receipt['schema_version']=True
            elif mutation=='index':receipt['index_sha256']='e'*64
            elif mutation=='data':receipt['data_sha256']='e'*64
            elif mutation=='name':index['data_file']='borrowed.bin'
            elif mutation=='promoted':receipt['provider_selected']=True
            else:index['original_raw_sha256']='e'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_cache(values)

    def test_selected_range_hash_detects_changes_even_when_stat_identity_is_unchanged(self):
        with tempfile.TemporaryDirectory()as td:
            path,index,offset=range_fixture(Path(td));guard=inventory.SelectedRangeGuard(path,index,[1]);guard.verify()
            data=bytearray(path.read_bytes());data[offset]^=1;path.write_bytes(data)
            with patch.object(inventory,'data_identity',return_value=guard.initial):
                with self.assertRaises(ValueError):guard.verify()

    def test_range_guard_does_not_claim_or_verify_the_unrequested_data_hash(self):
        with tempfile.TemporaryDirectory()as td:
            path,index,offset=range_fixture(Path(td));guard=inventory.SelectedRangeGuard(path,index,[1])
            data=bytearray(path.read_bytes());data[0]^=1;path.write_bytes(data)
            with patch.object(inventory,'data_identity',return_value=guard.initial):guard.verify()
            result=guard.descriptor()
            self.assertFalse(result['whole_data_hash_verified_this_run']);self.assertFalse(result['unrequested_frames_verified'])
            self.assertEqual(result['receipt_expected_whole_data_sha256'],inventory.DATA_SHA)
            self.assertEqual(len(result['selected_ranges']),1);self.assertEqual(result['selected_ranges'][0]['recipe_index'],1)
            self.assertNotEqual(result['selected_ranges'][0]['compressed_sha256'],result['selected_ranges'][0]['raw_sha256'])

    def test_range_guard_copies_authenticated_entries_and_rejects_duplicate_or_boolean_indices(self):
        with tempfile.TemporaryDirectory()as td:
            path,index,offset=range_fixture(Path(td));guard=inventory.SelectedRangeGuard(path,index,[1])
            data=bytearray(path.read_bytes());data[offset]^=1;path.write_bytes(data)
            index['frames'][1]['compressed_sha256']=hashlib.sha256(data[offset:]).hexdigest()
            with patch.object(inventory,'data_identity',return_value=guard.initial):
                with self.assertRaises(ValueError):guard.verify()
            for indices in ([1,1],[True],[2]):
                with self.subTest(indices=indices),self.assertRaises(ValueError):inventory.SelectedRangeGuard(path,index,indices)


if __name__=='__main__':unittest.main()
