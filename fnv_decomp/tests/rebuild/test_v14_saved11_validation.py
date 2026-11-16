import copy
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'rebuild'))
import v14_saved11_validation as subject


class ScopeTests(unittest.TestCase):
    def fixture(self):
        forbidden=sorted(subject.FORBIDDEN)
        roots=[{'original_address':'0x%08x'%i,'size':i+1} for i in range(11)]+[{'original_address':a,'size':2} for a in forbidden]
        prior=[{'address':r['original_address'],'name':'CACHED-CODE-%03d-%s.obj'%(i,r['original_address'][2:]),'sha256':'a'*64,'bytes':2} for i,r in enumerate(roots[:11])]
        op={'kind':'v14-saved11-fresh-validation-proposal','status':'owner-authorized-finite-work-awaiting-reviewed-gates-and-fresh-lease',
            'in_memory_reconstruction_authorized':True,'new_object_emission':False,'prior_batch_replay':False,
            'prior_match_inferred':False,'provider_selected':False,'runtime_eligible':False,
            'members':[{'root':copy.deepcopy(r),'saved_member':{k:p[k] for k in ('name','sha256','bytes')}} for r,p in zip(roots,prior)],
            'exclusions':{'quarantined':['0x0048e140'],'inflight_unknown':['0x00484da0'],'unstarted':['0x00484d60','0x0076b610']}}
        return op,{'verified_members':prior},{'roots':roots}

    def test_exact_scope(self):
        self.assertTrue(subject.validate_scope(*self.fixture()))

    def test_rejects_borrowed_member_and_excluded_or_duplicate_root(self):
        for change in ('hash','root','excluded'):
            op,evidence,positive=self.fixture()
            if change=='hash':op['members'][0]['saved_member']['sha256']='b'*64
            if change=='root':op['members'][0]['root']['size']=99
            if change=='excluded':op['members'][0]['root']=positive['roots'][11]
            with self.subTest(change=change),self.assertRaises(ValueError):subject.validate_scope(op,evidence,positive)

    def test_prior_proof_and_emission_claims_rejected(self):
        op,evidence,positive=self.fixture();op['prior_match_inferred']=True
        with self.assertRaises(ValueError):subject.validate_scope(op,evidence,positive)


class MemberTests(unittest.TestCase):
    class Highlow:
        def __len__(self):return 351931

    def fixture(self):
        raw=b'original synthetic';saved=b'saved synthetic'
        root={'original_address':'0x00000001','recipe_id':'unit','object_sha256':hashlib.sha256(raw).hexdigest(),
              'symbol_index':1,'symbol':'old','section':1,'value':0,'size':3}
        member={'name':'candidate.obj','sha256':hashlib.sha256(saved).hexdigest(),'bytes':len(saved)}
        record={'contract':{'fields':[],'unit_verified_functions':[],'provenance':{'recipe_unit_sha256':'proof'}},'certificate':{},'qualified_metadata_row_sha256':'a'}
        selection={'root':root,'authority':{}}
        identity={k:root[k] for k in ('recipe_id','object_sha256','symbol_index')}
        projection={'output_sha256':member['sha256'],'exports':['new'],'namespace_bindings':[(1,'new')]}
        return raw,saved,root,member,record,selection,identity,projection

    def test_reconstruction_mismatch_stops_before_comparison(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        raw,saved,root,member,record,selection,identity,projection=self.fixture()
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'),patch.object(driver,'_require_absent_index'),patch.object(v13.audit,'audit_original_fields',return_value={}), \
             patch.object(v13.base,'project_member',return_value=(b'different',projection)), \
             patch.object(v13.base.bulk,'compare_functions') as compare:
            with self.assertRaisesRegex(ValueError,'fresh in-memory reconstruction'):
                subject.verify_saved_member({'root':root,'saved_member':member},record,selection,raw,saved,
                    {root['original_address']:identity},set(),'original.obj','candidate.obj',None,{'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())
            compare.assert_not_called()

    def test_success_uses_saved_path_and_never_writes_member(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        raw,saved,root,member,record,selection,identity,projection=self.fixture()
        def report(symbol):return [{'verdict':'match','address':root['original_address'],'symbol':symbol,'size':3,
                                    'compiled_extent':3,'errors':[],'relocations':[]}]
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'),patch.object(driver,'_require_absent_index'),patch.object(v13.audit,'audit_original_fields',return_value={}), \
             patch.object(v13.base,'project_member',return_value=(saved,projection)),patch.object(v13.base.bulk,'strict_reparse'), \
             patch.object(v13.base.bulk,'compare_functions',side_effect=[report('old'),report('new')]) as compare, \
             patch.object(driver,'field_proof_record',return_value={'fields':[]}), \
             patch.object(Path,'open',side_effect=AssertionError('unexpected write/open')):
            result=subject.verify_saved_member({'root':root,'saved_member':member},record,selection,raw,saved,
                {root['original_address']:identity},set(),'original.obj','candidate.obj',None,{'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())
            self.assertEqual(compare.call_args_list[1].args[0],'candidate.obj')
            self.assertFalse(result['new_object_emission']);self.assertFalse(result['prior_match_inferred'])

    def test_unbound_run_rejects(self):
        with self.assertRaises(ValueError):subject.run()


class FieldPolicyTests(MemberTests):
    def test_unsupported_field_assessment_cannot_be_promoted(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        raw,saved,root,member,record,selection,identity,projection=self.fixture()
        record['contract']['fields']=[{}]
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'), \
             patch.object(driver,'_require_absent_index'),patch.object(v13.audit,'audit_original_fields',return_value={}), \
             patch.object(v13.frozen.fields.core,'assess_member',return_value={'eligible':False,'blockers':['unsupported']}), \
             patch.object(v13.base.bulk,'compare_functions') as compare:
            with self.assertRaisesRegex(ValueError,'supported field policy'):
                subject.verify_saved_member({'root':root,'saved_member':member},record,selection,raw,saved,
                    {root['original_address']:identity},set(),'original.obj','candidate.obj',None,
                    {'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())
            compare.assert_not_called()


class FieldComparisonTests(MemberTests):
    def test_nonempty_field_full_proof_and_failed_relocation(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        raw,saved,root,member,record,selection,identity,projection=self.fixture()
        record['contract']['fields']=[{'source':'synthetic'}]
        projection.update(fields=[{'field_proof_sha256':'x'}],comparison_base_view={})
        assessment={'eligible':True,'fields':copy.deepcopy(projection['fields']),'exports':['new']}
        def report(symbol,match=True):
            return [{'verdict':'match','address':root['original_address'],'symbol':symbol,'size':3,
                'compiled_extent':3,'errors':[],'relocations':[{'match':match,'expected':7,'observed':7}]}]
        args=({'root':root,'saved_member':member},record,selection,raw,saved,
            {root['original_address']:identity},set(),'original.obj','candidate.obj',None,
            {'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'), \
             patch.object(driver,'_require_absent_index'),patch.object(v13.audit,'audit_original_fields',return_value={5:('fact',)}), \
             patch.object(v13.frozen.fields.core,'assess_member',return_value=assessment), \
             patch.object(v13.frozen.fields.core,'project_member',return_value=(saved,projection)), \
             patch.object(v13.base.bulk,'strict_reparse'),patch.object(driver,'field_proof_record',return_value={'fields':[{'source':'synthetic'}]}), \
             patch.object(v13.base.bulk,'compare_functions',side_effect=[report('old'),report('new')]):
            result=subject.verify_saved_member(*args)
            self.assertEqual(len(result['full_field_proof']['fields']),1)
            self.assertEqual(result['field_facts'],{5:('fact',)})
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'), \
             patch.object(driver,'_require_absent_index'),patch.object(v13.audit,'audit_original_fields',return_value={}), \
             patch.object(v13.frozen.fields.core,'assess_member',return_value=assessment), \
             patch.object(v13.frozen.fields.core,'project_member',return_value=(saved,projection)), \
             patch.object(v13.base.bulk,'strict_reparse'), \
             patch.object(v13.base.bulk,'compare_functions',side_effect=[report('old'),report('new',False)]):
            with self.assertRaisesRegex(ValueError,'full original/staged comparison'):
                subject.verify_saved_member(*args)

    def test_index_appearance_after_comparison_is_rejected(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        raw,saved,root,member,record,selection,identity,projection=self.fixture()
        def report(symbol):return [{'verdict':'match','address':root['original_address'],'symbol':symbol,'size':3,'compiled_extent':3,'errors':[],'relocations':[]}]
        with patch.object(selector,'validate_selected'),patch.object(native,'validate_roots'), \
             patch.object(driver,'_require_absent_index',side_effect=[None,ValueError('index appeared')]), \
             patch.object(v13.audit,'audit_original_fields',return_value={}),patch.object(v13.base,'project_member',return_value=(saved,projection)), \
             patch.object(v13.base.bulk,'strict_reparse'),patch.object(driver,'field_proof_record',return_value={'fields':[]}), \
             patch.object(v13.base.bulk,'compare_functions',side_effect=[report('old'),report('new')]):
            with self.assertRaisesRegex(ValueError,'index appeared'):
                subject.verify_saved_member({'root':root,'saved_member':member},record,selection,raw,saved,
                    {root['original_address']:identity},set(),'original.obj','candidate.obj',None,
                    {'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())


class ComparisonCorruptionTests(MemberTests):
    def test_compiled_extent_and_byte_difference_reject(self):
        import cached_frontier_code_factory_v14 as selector
        import cached_frontier_code_factory_v13 as v13
        import cached_frontier_code_factory_v14_driver as driver
        import cached_root_observe_v14 as native
        for corruption in ('extent','bytes'):
            raw,saved,root,member,record,selection,identity,projection=self.fixture()
            def report(symbol):return [{'verdict':'match','address':root['original_address'],'symbol':symbol,
                'size':3,'compiled_extent':3,'errors':[],'relocations':[]}]
            after=report('new')
            if corruption=='extent':after[0]['compiled_extent']=2
            else:after[0]['byte_differences']=[{'offset':1}]
            with self.subTest(corruption=corruption),patch.object(selector,'validate_selected'), \
                 patch.object(native,'validate_roots'),patch.object(driver,'_require_absent_index'), \
                 patch.object(v13.audit,'audit_original_fields',return_value={}),patch.object(v13.base,'project_member',return_value=(saved,projection)), \
                 patch.object(v13.base.bulk,'strict_reparse'),patch.object(v13.base.bulk,'compare_functions',side_effect=[report('old'),after]):
                with self.assertRaisesRegex(ValueError,'full original/staged comparison'):
                    subject.verify_saved_member({'root':root,'saved_member':member},record,selection,raw,saved,
                        {root['original_address']:identity},set(),'original.obj','candidate.obj',None,
                        {'recipe':{}},{'verified_functions':[],'recipe_unit_sha256':'proof'},None,self.Highlow())

if __name__=='__main__':unittest.main()
