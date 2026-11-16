"""Authored COFF and qualified metadata; no saved/native Game input reads."""
import copy
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import cached_root_observe as c
from test_scalableordinary_root_collect import fixture as native_fixture


def fixture(field=True,safeseh=False):
    raw,unit,proof,requested,_,_,buckets=native_fixture(field=field,safeseh=safeseh)
    p=dict(object_sha256=unit['object_sha256'],source_sha256=unit['source_sha256'],request_sha256='a'*64,
           metadata_only=True,native_observation_performed=False)
    frame=dict(recipe_index=0,raw_sha256='b'*64,compressed_sha256='c'*64,row_count=int(field),
        first_ordinal=1 if field else None,last_ordinal=1 if field else None,
        whole_data_hash_verified_this_read=False,unrequested_frames_verified=False)
    views=[]
    imported=dict(import_id=175,dll='USER32.dll',function='GetActiveWindow',original_cell='0x00fdf2fc')
    for event,roots in [('SINGLE_ROOT_METADATA_CONTRACT',[r]) for r in requested]+[('RECIPE_UNION_METADATA_CONTRACT',requested)]:
        contract=c.finite.build_contract(unit,proof,roots,buckets,imported,copy.deepcopy(p))
        v=dict(schema_version=1,kind='new-cached-metadata-contract',policy_id=c.QUALIFIED_POLICY,event=event,
            requested_roots=copy.deepcopy(roots),contract=contract,contract_sha256=c.digest(contract),
            new_metadata_contract_sha256=c.digest(contract),source_frame_verification=copy.deepcopy(frame),native_observation_required=True)
        v.update({k:False for k in c.QUALIFIED_FALSE});views.append(v)
    return raw,unit,proof,requested,views,dict(qualified_request_sha256='a'*64,fresh_source_file_sha256=unit['source_sha256'])


def observe(args):return list(c.observe_recipe_contracts(*args))


def rehash(v):v['contract_sha256']=v['new_metadata_contract_sha256']=c.digest(v['contract'])


class CachedObservationTests(unittest.TestCase):
    def test_one_parse_exact_frozen_results_unchanged_qualified_contracts(self):
        args=fixture();before=copy.deepcopy(args);parse=c.coff.parse
        with patch.object(c.coff,'parse',wraps=parse) as parsing:records=observe(args)
        self.assertEqual(parsing.call_count,1);self.assertEqual(args,before);self.assertEqual(len(records),3)
        obj=parse(args[0])
        for source,r in zip(args[4],records):
            self.assertEqual(r['contract'],source['contract']);self.assertEqual(r['contract_identity_sha256'],source['contract_sha256'])
            self.assertEqual(r['certificate'],c.ordinary.assess_object(obj,source['contract']))
            self.assertFalse(r['qualified_metadata_identity']['certificate_created']);self.assertTrue(r['fresh_certificate_created'])
            self.assertFalse(r['contract']['provenance']['native_observation_performed']);self.assertTrue(r['native_parse_performed'])
            for flag in c.FALSE:self.assertIs(r[flag],False)

    def test_no_eh_inferred_from_empty_parent_or_zero_root_fields(self):
        args=fixture(field=False,safeseh=True);self.assertTrue(all(v['contract']['parent_eh']==[] for v in args[4]))
        records=observe(args)
        self.assertEqual([len(r['contract']['fields']) for r in records],[0,0,0])
        self.assertFalse(records[1]['closure_observed']);self.assertFalse(records[2]['closure_observed'])
        self.assertIn('LIVE_SAFESEH_HANDLER_REQUIRES_ADAPTER',{b['code'] for b in records[1]['blockers']})
        self.assertEqual(records[0]['contract']['iat_import_observation']['import_id'],175)
        self.assertEqual(records[0]['contract']['fields'],[])

    def test_unknown_fields_missing_and_ordinary_blockers_not_waived(self):
        args=list(fixture());args[2]['eh_sections']=[['authored',0,False,'0x00500000']]
        for v in args[4]:
            v['contract']['parent_eh']=[r for r in args[2]['eh_sections'] if r[3] in {x['original_address'] for x in v['requested_roots']}]
            rehash(v)
        records=observe(args)
        self.assertFalse(records[0]['closure_observed']);self.assertTrue(records[0]['contract']['parent_eh'])

    def test_source_raw_retained_and_native_physical_contradictions_are_fatal(self):
        for change in ('raw','proof','root','native-index','source'):
            args=list(fixture())
            if change=='raw':args[0]+=b'changed'
            elif change=='proof':args[2]['verified_functions'][0]['value']=1
            elif change=='root':args[3][0]['size']=True
            elif change=='native-index':
                args[3][0]['symbol_index']=5
                for v in args[4]:
                    for r in v['requested_roots']:
                        if r['original_address']=='0x00500000':r['symbol_index']=5
                    for r in v['contract']['roots']:
                        if r['original_address']=='0x00500000':r['symbol_index']=5
                    rehash(v)
            else:args[4][0]['contract']['provenance']['source_sha256']='f'*64;rehash(args[4][0])
            with self.subTest(change=change),self.assertRaises(ValueError):observe(args)

    def test_contract_schema_digest_scope_and_promotion_cannot_be_borrowed(self):
        changes=[lambda v:v.update(contract_sha256='f'*64),lambda v:v.update(runtime_eligible=True),
            lambda v:v.update(event='UNSUPPORTED_VIEW'),lambda v:v['requested_roots'][0].update(recipe_index=True),
            lambda v:v.update(certificate_created=True),lambda v:v['contract'].update(verified_match=False),
            lambda v:v.update(certificate={'closure_observed':True}),lambda v:v.update(certificate_sha256='f'*64)]
        for mutate in changes:
            args=list(fixture());mutate(args[4][0])
            with self.assertRaises(ValueError):observe(args)

    def test_partial_duplicate_extra_and_wrong_order_batches_are_fatal(self):
        for kind in ('partial','duplicate','extra','unionfirst'):
            args=list(fixture());views=args[4]
            if kind=='partial':views.pop()
            elif kind=='duplicate':views[1]=copy.deepcopy(views[0])
            elif kind=='extra':views.append(copy.deepcopy(views[0]))
            else:views[:]=[views[-1],*views[:-1]]
            with self.subTest(kind=kind),self.assertRaises(ValueError):observe(args)

    def test_union_field_or_reference_drop_fails_globally(self):
        for key in ('fields','missing_fields','refs'):
            args=list(fixture());v=args[4][-1]
            if key=='fields':v['contract']['fields']=[]
            elif key=='refs':v['contract']['provenance']['binding_row_references']=[]
            else:v['contract']['missing_fields']=[{'authored_missing':True}]
            rehash(v)
            with self.subTest(key=key),self.assertRaises(ValueError):observe(args)

    def test_shared_incoming_proof_and_import_changes_are_fatal(self):
        for key in ('omission_field_proofs','iat_import_observation'):
            args=list(fixture());args[4][1]['contract'][key]=[{'altered':True}] if key=='omission_field_proofs' else {}
            rehash(args[4][1])
            with self.subTest(key=key),self.assertRaises(ValueError):observe(args)

    def test_known_native_relocation_or_addend_contradiction_not_quarantined(self):
        for key,val in [('offset',8),('addend',1),('symbol','_wrong')]:
            args=list(fixture());v=args[4][0];v['contract']['fields'][0]['coff_relocation'][key]=val;rehash(v)
            with self.subTest(key=key),self.assertRaises(ValueError):observe(args)

    def test_only_parse_format_failure_gets_structured_negative(self):
        args=list(fixture());args[0]=b'authored unsupported COFF'
        h=hashlib.sha256(args[0]).hexdigest();args[1]['object_sha256']=args[2]['object_sha256']=h
        for r in args[3]:r['object_sha256']=h
        for v in args[4]:
            for r in v['requested_roots']:r['object_sha256']=h
            v['contract']['provenance']['object_sha256']=h;rehash(v)
        result=observe(args);self.assertEqual(len(result),3)
        for r in result:
            self.assertFalse(r['fresh_certificate_created']);self.assertFalse(r['closure_observed'])
            self.assertEqual(r['blockers'][0]['code'],'UNSUPPORTED_ORIGINAL_COFF_FORMAT')


class OperationAndPublicationTests(unittest.TestCase):
    def operation(self):
        refs={name:dict(path='build/rebuild/authored/'+name+'.json',sha256=c.ARTIFACT_PINS.get(name,'1'*64)) for name in c.ARTIFACT_KEYS}
        return dict(schema_version=1,kind='whole-qualified-contract-native-observation',policy_id=c.POLICY,epoch='authored-v12',
            roots=180,recipes=77,records=257,limits=dict(c.LIMITS),artifacts=refs,source_sha256='2'*64)

    def test_exact_operation_scope_and_paths(self):
        c.validate_operation(self.operation())
        for kind in ('bool','cap','foreign','pin','extra','duplicate'):
            op=self.operation()
            if kind=='bool':op['roots']=True
            elif kind=='cap':op['limits']['seconds']+=1
            elif kind=='foreign':op['artifacts']['manifest']['path']='../outside.json'
            elif kind=='pin':op['artifacts']['manifest']['sha256']='0'*64
            elif kind=='extra':op['artifacts']['extra']={}
            else:op['artifacts']['manifest']['path']=op['artifacts']['selection']['path']
            with self.subTest(kind=kind),self.assertRaises(ValueError):c.validate_operation(op)

    def test_unavailable_memory_counter_fails_closed(self):
        with patch('coff_inventory.peak_memory_bytes',return_value=None),self.assertRaises(ValueError):c.budget(time.monotonic())

    def test_exclusive_race_preserves_file_not_created_by_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);out,details,index=base/'out',base/'details',base/'index'
            details.write_bytes(b'other process');published=[]
            with patch.object(c.finite,'stable'),patch.object(c,'budget',return_value=1),self.assertRaises(FileExistsError):
                c.publish_outputs(out,details,io.BytesIO(b'new'),{'details_sha256':hashlib.sha256(b'new').hexdigest()}, {},index,published,time.monotonic())
            self.assertEqual(details.read_bytes(),b'other process');self.assertEqual(published,[])

    def test_after_publication_drift_removes_only_created_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);out,details,index=base/'out',base/'details',base/'index';published=[]
            result={'details_sha256':hashlib.sha256(b'new').hexdigest()}
            with patch.object(c.finite,'stable',side_effect=[None,ValueError('drift')]),patch.object(c,'budget',return_value=1),self.assertRaises(ValueError):
                c.publish_outputs(out,details,io.BytesIO(b'new'),result,{},index,published,time.monotonic())
            self.assertFalse(out.exists());self.assertFalse(details.exists())


if __name__=='__main__':unittest.main()
