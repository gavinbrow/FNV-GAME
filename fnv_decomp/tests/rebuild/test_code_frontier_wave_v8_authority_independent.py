"""Authored three-epoch269 registry/467 routing; no original inputs."""
import copy
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import code_frontier_wave_v8 as wave
from test_code_frontier_wave_authority_independent import authored


def fixture():
    _,providers,units,groups=authored(467)
    roots=[wave.prior.planner.root_record(a,p,units)for a,p in providers.items()]
    sources=[]
    for kind,chosen,epoch in [('cached-central',roots[:205],'a'),('cached-frontier',roots[205:215],'b'),
                              ('cached-frontier',roots[215:269],'c')]:
        summaries=[]
        for ordinal,root in enumerate(chosen,1):
            positive=ordinal==1
            summary=dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],roots=[root['original_address']],
                closure_observed=positive,graph_observation_complete=True,blocker_codes={}if positive else{'ROOT_CONJUNCT':1},
                record_sha256='%064x'%(root['symbol_index']+1000),certificate_sha256='%064x'%(root['symbol_index']+2000))
            if kind=='cached-central':summary.update(lane=1,lane_record_ordinal=ordinal)
            else:summary['ordinal']=ordinal
            summaries.append(summary)
        sources.append(dict(kind=kind,receipt_sha256=epoch*64,request_sha256=epoch*64,requests=chosen,
            receipt=dict(status='metadata-only',input_stability=True,optional_function_index_present=False,
                         request_sha256=epoch*64,observations=summaries)))
    return sources,providers,units,groups


def registry(values):return wave.old.cache_registry(*values[:3],expected_total=269)
def reconcile(values,registered,exclusions=set()):
    root=registered['records']['0x0086beb0']['root']
    quarantine=[dict(root=root,blockers=[dict(code='CANONICAL_REFERENCE_GROUP_REQUIRES_REVIEWED_V2')])]
    return wave.reconcile_v8(values[3],values[1],values[2],registered,exclusions,quarantine)


class IndependentThreeAuthorityTests(unittest.TestCase):
    def test_third_epoch_keeps_same_local_locator_separate_and_contract_hash_deferred(self):
        values=fixture();before=copy.deepcopy(values);result=registry(values)
        self.assertEqual(result['roots'],269);self.assertEqual([a['roots']for a in result['authorities']],[205,10,54])
        records=list(result['records'].values());second=records[205]['authority'];third=records[215]['authority']
        self.assertEqual(second['kind'],third['kind']);self.assertEqual(second['ordinal'],third['ordinal'])
        self.assertNotEqual(second['receipt_sha256'],third['receipt_sha256'])
        self.assertNotEqual(second['request_sha256'],third['request_sha256'])
        self.assertIsNone(third['contract_identity_sha256']);self.assertTrue(third['contract_identity_is_bound_through_record_hash'])
        self.assertEqual(values,before)

    def test_third_epoch_borrowed_request_root_or_original_source_fails(self):
        for mutation in ('request','duplicate-root','source'):
            values=fixture();third=values[0][2]
            if mutation=='request':third['request_sha256']=values[0][1]['request_sha256']
            elif mutation=='duplicate-root':
                root=copy.deepcopy(values[0][0]['requests'][0]);third['requests'][0]=root
                third['receipt']['observations'][0].update(recipe_id=root['recipe_id'],roots=[root['original_address']])
            else:third['requests'][0]['source_sha256']='e'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):registry(values)

    def test_missing_or_duplicated_third_epoch_view_cannot_look_complete(self):
        for mutation in ('missing','duplicate','locator'):
            values=fixture();summaries=values[0][2]['receipt']['observations']
            if mutation=='missing':summaries.pop()
            elif mutation=='duplicate':summaries.append(copy.deepcopy(summaries[0]))
            else:summaries[1]['ordinal']=summaries[0]['ordinal']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):registry(values)

    def test_COMDAT_annotations_do_not_promote_third_epoch_original_negative(self):
        values=fixture();summary=values[0][2]['receipt']['observations'][1]
        summary.update(comdat_candidate=True,witness_complete=True,composed_omission_complete=True)
        registered=registry(values);result=reconcile(values,registered)
        row=next(r for r in result['records']if r.get('root',{}).get('original_address')==summary['roots'][0])
        self.assertEqual(row['state'],'CACHED_ORIGINAL_OMISSION_BLOCKED')
        self.assertEqual(row['cached_observation'],summary)
        self.assertEqual(row['cache_authority']['receipt_sha256'],'c'*64)
        self.assertNotIn(row['root'],result['cached_positive_roots'])

    def test_exact467_partition_keeps_quarantine_and_all_new_roots_disjoint(self):
        values=fixture();registered=registry(values);result=reconcile(values,registered)
        self.assertEqual(len(result['records']),467)
        self.assertEqual(result['counts'],dict(PRESERVED_REFERENCE_GROUP_QUARANTINE=1,
            CACHED_ORIGINAL_OMISSION_BLOCKED=266,CACHED_BARE_POSITIVE_REQUIRES_FRESH_CLASSIFICATION=2,
            NEW_SELECTED_ROOT_REQUIRES_OBSERVATION=198))
        self.assertEqual(len(result['new_roots']),198)
        self.assertFalse(set(r['original_address']for r in result['new_roots'])&set(registered['records']))
        for row in result['records']:
            if row.get('root',{}).get('original_address')in registered['records']:
                self.assertEqual(row['cache_authority'],registered['records'][row['root']['original_address']]['authority'])
        self.assertFalse(result['code_emission_performed'])

    def test_prepared_historical_negative_skips_without_changing_its_original_observation(self):
        values=fixture();registered=registry(values);summary=values[0][2]['receipt']['observations'][1]
        name=next(g['symbol']for g in values[3]['groups']if g['original_bases']==summary['roots'])
        result=reconcile(values,registered,{name})
        row=next(r for r in result['records']if r['symbol']==name)
        self.assertEqual(row['state'],'PREPARED_SKIP')
        self.assertFalse(registered['records'][summary['roots'][0]]['summary']['closure_observed'])
        self.assertEqual(registered['records'][summary['roots'][0]]['summary']['blocker_codes'],{'ROOT_CONJUNCT':1})

    def test_prepared_name_cannot_erase_preserved_quarantine(self):
        values=fixture();registered=registry(values)
        name=next(g['symbol']for g in values[3]['groups']if g['original_bases']==['0x0086beb0'])
        with self.assertRaises(ValueError):reconcile(values,registered,{name})


if __name__=='__main__':unittest.main()
