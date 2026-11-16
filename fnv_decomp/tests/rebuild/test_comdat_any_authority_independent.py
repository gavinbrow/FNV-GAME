"""Original COMDAT wrapper/composition authority negatives; no private inputs."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import comdat_any_root_composer as composer
import comdat_any_code_projection as consumer
from test_comdat_any_code_omission import authored


def fixture(**kwargs):
    values=authored(fields=False,**kwargs)
    raw,contract,base,root,census=values
    observation=composer.policy.observe_comdat_any_code_policy(*values,policy_id=composer.policy.POLICY)
    wrappers=[dict(kind=composer.WITNESS_KIND,definition_census=census,observation=observation)]
    composed=composer.compose(raw,contract,base,wrappers,policy_id=composer.POLICY)
    providers={root['original_address']:{k:root[k]for k in ('recipe_id','object_sha256','symbol_index')}}
    return raw,contract,base,wrappers,composed,[root],providers


def assess(values):return consumer.assess_member(*values,existing_exports=set(),policy_id=consumer.POLICY)


class IndependentComdatAuthorityTests(unittest.TestCase):
    def test_complete_candidate_preserves_original_negative_and_false_global_claims(self):
        values=fixture();before=copy.deepcopy(values);result=assess(values)
        self.assertTrue(result['eligible']);self.assertFalse(result['serialization_performed'])
        self.assertFalse(values[2]['closure_observed']);self.assertTrue(values[4]['composed_omission_complete'])
        self.assertEqual(len(values[4]['discharged_blockers']),1)
        for flag in composer.FALSE:self.assertIs(values[4][flag],False)
        self.assertEqual(values,before)

    def test_duplicate_or_unknown_witness_wrapper_is_refused(self):
        for mutation in ('duplicate','unknown-key','wrong-kind'):
            values=list(fixture())
            if mutation=='duplicate':values[3].append(copy.deepcopy(values[3][0]))
            elif mutation=='unknown-key':values[3][0]['borrowed_authority']=True
            else:values[3][0]['kind']='typed-data-witness'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):assess(values)

    def test_borrowed_or_partial_observation_cannot_discharge_root(self):
        for mutation in ('root','census-hash','source','complete','discharge','boolean'):
            values=list(fixture());obs=values[3][0]['observation']
            if mutation=='root':obs['requested_root']['original_address']='0x00700000'
            elif mutation=='census-hash':obs['definition_census_sha256']='e'*64
            elif mutation=='source':obs['source_sha256']='e'*64
            elif mutation=='complete':obs['witness_complete']=False
            elif mutation=='discharge':obs['discharge_blocker_ids'].append(obs['discharge_blocker_ids'][0])
            else:obs['schema_version']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):assess(values)

    def test_unrelated_census_entries_cannot_be_laundered_by_fresh_candidate_replay(self):
        values=list(fixture());wrapper=values[3][0];extra=copy.deepcopy(wrapper['definition_census']['entries'][0])
        extra['root'].update(original_address='0x00700000',recipe_id='other',object_sha256='e'*64)
        extra['planned_canonical_name']=composer.policy.pool.canonical({k:extra['root'][k]for k in ('recipe_id','object_sha256','symbol_index')})
        wrapper['definition_census']['entries'].append(extra)
        wrapper['observation']=composer.policy.observe_comdat_any_code_policy(values[0],values[1],values[2],values[5][0],
            wrapper['definition_census'],policy_id=composer.policy.POLICY)
        self.assertTrue(wrapper['observation']['witness_complete'])
        with self.assertRaises(ValueError):composer.compose(values[0],values[1],values[2],values[3],policy_id=composer.POLICY)

    def test_fake_positive_or_numeric_alias_original_base_is_refused(self):
        for field,value in [('closure_observed',True),('provider_selected',0),('schema_version',True)]:
            values=list(fixture());values[2][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):assess(values)

    def test_independent_repeated_directives_stay_incomplete_with_exact_occurrences(self):
        values=fixture(directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib"')
        before=copy.deepcopy(values[2]);result=assess(values)
        self.assertFalse(result['eligible']);self.assertFalse(values[4]['composed_omission_complete'])
        self.assertEqual(values[4]['discharged_blockers'],[])
        self.assertEqual(values[4]['remaining_blockers'],before['blockers'])
        repeated=[b for b in before['blockers']if b['code']=='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE']
        self.assertEqual(len(repeated),2);self.assertEqual(repeated[0]['blocker_id'],repeated[1]['blocker_id'])
        self.assertEqual([r['base_blocker_ordinal']for r in values[4]['remaining_blocker_occurrences']],list(range(1,len(before['blockers'])+1)))
        with patch.object(consumer.coff,'namespace',side_effect=AssertionError('incomplete emission forbidden')):
            with self.assertRaises(ValueError):consumer.project_member(*values,existing_exports=set(),policy_id=consumer.POLICY)
        self.assertEqual(values[2],before)

    def test_observation_or_composition_promotion_and_unknown_composed_key_are_refused(self):
        for mutation in ('observation','composition','extra'):
            values=list(fixture())
            if mutation=='observation':values[3][0]['observation']['planned_definition_census_authenticated']=True
            elif mutation=='composition':values[4]['namespace_approved']=True
            else:values[4]['pretend_complete']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):assess(values)

    def test_borrowed_requested_root_provider_or_existing_export_is_refused(self):
        for mutation in ('requested','provider','existing'):
            values=list(fixture());exports=set()
            if mutation=='requested':values[5][0]=dict(values[5][0],source_sha256='e'*64)
            elif mutation=='provider':values[6][values[5][0]['original_address']]['object_sha256']='e'*64
            else:exports.add(composer.policy.pool.canonical(values[6][values[5][0]['original_address']]))
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                consumer.assess_member(*values,existing_exports=exports,policy_id=consumer.POLICY)

    def test_missing_explicit_policy_optin_never_reaches_serializer(self):
        values=fixture()
        with patch.object(consumer.coff,'namespace',side_effect=AssertionError('implicit emission forbidden')):
            with self.assertRaises(ValueError):consumer.project_member(*values,existing_exports=set(),policy_id='ordinary')

    def test_native_qualification_is_census_only_and_keeps_independent_policy_blockers(self):
        values=fixture(directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib"')
        before=copy.deepcopy(values)
        result=composer.assess_native_definition(values[0],values[1],values[2],values[5][0],policy_id=composer.POLICY)
        self.assertTrue(result['eligible']);self.assertFalse(result['candidate_policy_evaluated'])
        self.assertFalse(result['serialization_performed']);self.assertFalse(result['full_serialization_eligible'])
        self.assertEqual(result['original_blocker_ids'],[b['blocker_id']for b in values[2]['blockers']])
        self.assertFalse(values[4]['composed_omission_complete']);self.assertEqual(values,before)

    def test_native_preflight_integrity_errors_are_fatal_not_unsupported_forms(self):
        for mutation in ('raw','base-type','source'):
            values=list(fixture())
            if mutation=='raw':values[0]=values[0][:-1]
            elif mutation=='base-type':values[2]['provider_selected']=0
            else:values[5][0]['source_sha256']='e'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                composer.assess_native_definition(values[0],values[1],values[2],values[5][0],policy_id=composer.POLICY)

    def test_unsupported_summary_fresh_replay_preserves_repeated_ids_and_occurrence_order(self):
        values=fixture(directives=b' /DEFAULTLIB:"LIBCMT" /DEFAULTLIB:"OLDNAMES" /DEFAULTLIB:"uuid.lib" /DEFAULTLIB:"uuid.lib"')
        summary=composer.summarize_unsupported(*values[:5],policy_id=composer.POLICY)
        ids=[b['blocker_id']for b in values[2]['blockers']]
        self.assertEqual(summary['original_blocker_ids'],ids);self.assertEqual(summary['remaining_blocker_ids'],ids)
        self.assertEqual(summary['original_occurrences'],len(ids));self.assertEqual(summary['remaining_occurrences'],len(ids))
        self.assertFalse(summary['root_conjunct_discharge_proved']);self.assertFalse(summary['serialization_approved'])
        values[4]['unsupported_summary']['remaining_blocker_ids'].pop()
        with self.assertRaises(ValueError):composer.summarize_unsupported(*values[:5],policy_id=composer.POLICY)


if __name__=='__main__':unittest.main()
