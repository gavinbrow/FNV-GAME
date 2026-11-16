"""Authored frontier identity/census and historical omission distinctions."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import current_code_frontier as f


def fixture():
    providers={};units={};roots=[];observations=[];groups=[]
    for i,positive in enumerate([True,False,True],1):
        a='0x%08x'%(0x400000+i*16);rid='authored%d'%i
        p=dict(recipe_id=rid,object_sha256=str(i)*64,symbol_index=i,source_sha256='f'*64,section=3,value=0,size=17,symbol='_root%d'%i)
        p['planned_canonical_name']=f.base.pool.canonical({k:p[k] for k in ('recipe_id','object_sha256','symbol_index')})
        providers[a]=p;units[rid]=dict(recipe_index=i,object_sha256=p['object_sha256'],source_sha256=p['source_sha256'])
        root=f.root_record(a,p,units);roots.append(root)
        if i!=3:observations.append(dict(event='SINGLE_ROOT_OBSERVATION',roots=[a],closure_observed=positive,graph_observation_complete=True,
            blocker_codes={} if positive else {'EH_BLOCKED':1},record_sha256=str(i)*64))
        groups.append(dict(symbol=p['planned_canonical_name'],classification='CODE',observed_roles=['code'],original_bases=[a],
            original_targets=[a],included_provenance_is_extraction_proof=False))
    unknown=dict(groups[0],symbol=f.base.pool.unresolved('0x00ec0000','code'),original_bases=['0x00ec0000'],original_targets=['0x00ec0000'])
    groups.append(unknown)
    report=dict(kind='actual-unresolved-LNK-target-groups',groups=groups,classifications={'CODE':4},executable_execution=False,runtime_eligible=False)
    return report,providers,units,dict(observations=observations),roots[:2],set()


class FrontierTests(unittest.TestCase):
    def test_all_current_demands_accounted_without_promoting_closure(self):
        values=fixture();result=f.reconcile(*values,expected_code_count=4)
        self.assertEqual(result['counts'],dict(CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION=1,CACHED_ORIGINAL_OMISSION_BLOCKED=1,
            NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=1,UNSELECTED_OR_NAMESPACE_UNPROVED=1))
        self.assertEqual(len(result['new_roots']),1);self.assertTrue(result['eligibility_not_inferred_from_closure'])
        self.assertFalse(result['provider_selected']);self.assertFalse(result['code_emission_performed'])

    def test_prepared_namespace_skips_even_historical_negative(self):
        values=list(fixture());values[-1]={values[0]['groups'][1]['symbol']}
        result=f.reconcile(*values,expected_code_count=4)
        self.assertEqual(result['counts']['PREPARED_SKIP'],1)
        self.assertNotIn('CACHED_ORIGINAL_OMISSION_BLOCKED',result['counts'])

    def test_no_guessed_address_alias_for_unselected_namespace(self):
        values=fixture();values[0]['groups'][-1]['original_bases']=[values[4][0]['original_address']]
        result=f.reconcile(*values,expected_code_count=4)
        self.assertEqual(result['records'][-1]['state'],'UNSELECTED_OR_NAMESPACE_UNPROVED')
        self.assertNotIn('root',result['records'][-1])

    def test_stale_physical_source_root_and_conflicting_demand_are_fatal(self):
        for mutate in [lambda v:v[4][0].update(symbol_index=99),lambda v:v[0]['groups'][0].update(original_bases=['0x00400000']),
                       lambda v:v[0]['groups'][0].update(observed_roles=['code','data']),lambda v:v[1][next(iter(v[1]))].update(source_sha256='a'*64)]:
            values=copy.deepcopy(fixture());mutate(values)
            with self.assertRaises(ValueError):f.reconcile(*values,expected_code_count=4)

    def test_duplicate_demand_cached_root_or_missing_census_is_fatal(self):
        values=fixture();values[0]['groups'].append(copy.deepcopy(values[0]['groups'][0]))
        with self.assertRaises(ValueError):f.reconcile(*values,expected_code_count=4)
        values=fixture();values[3]['observations'].append(copy.deepcopy(values[3]['observations'][0]))
        with self.assertRaises(ValueError):f.reconcile(*values,expected_code_count=4)
        with self.assertRaises(ValueError):f.reconcile(*fixture(),expected_code_count=5)

    def test_bad_metadata_review_fails_before_input_or_output(self):
        class Args:review=Path('authored.json');review_sha256='0'*64
        with patch.object(f.base,'observe',return_value=Args.review),patch.object(f.base,'load_json',return_value={}):
            with self.assertRaises(ValueError):f.run(Args())


if __name__=='__main__':unittest.main()
