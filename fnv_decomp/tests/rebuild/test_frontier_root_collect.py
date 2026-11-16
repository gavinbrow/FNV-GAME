"""Synthetic new-epoch accounting; no original objects or global stream reads."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import frontier_root_collect as c
from test_scalableordinary_root_collect import fixture


def scope():
    fx=fixture(); request=dict(schema_version=1,kind='fnv-finite-ordinary-root-request',roots=fx[3])
    prior=dict(observations=[dict(event='SINGLE_ROOT_OBSERVATION',roots=['0x%08x'%(0x700000+i)]) for i in range(205)])
    context=dict(schema_version=1,kind='new-original-frontier-root-context',epoch='application-link-v5-original-selected',
        request_sha256='a'*64,frontier_join_sha256='b'*64,planned_map_sha256=c.MAP_PIN,prior_receipt_sha256=c.PRIOR_PIN,
        new_original_addresses=[r['original_address'] for r in request['roots']],provider_selected=False,runtime_eligible=False,emission_performed=False)
    return fx,context,request,prior


class FrontierTests(unittest.TestCase):
    def test_new_scope_and_exact_prior_epoch(self):
        _,context,request,prior=scope()
        self.assertEqual(c.validate_context(context,request,prior,'a'*64,'b'*64),context['epoch'])

    def test_cached_root_is_rejected_not_recomputed(self):
        _,context,request,prior=scope();prior['observations'][0]['roots']=[request['roots'][0]['original_address']]
        with self.assertRaises(ValueError):c.validate_context(context,request,prior,'a'*64,'b'*64)

    def test_context_pins_promotion_and_order_cannot_drift(self):
        for key,val in [('request_sha256','f'*64),('frontier_join_sha256','f'*64),('planned_map_sha256','f'*64),
                        ('prior_receipt_sha256','f'*64),('runtime_eligible',True),('provider_selected',True),
                        ('new_original_addresses',['0x00000001']),('epoch','')]:
            _,context,request,prior=scope();context[key]=val
            with self.subTest(key=key),self.assertRaises(ValueError):c.validate_context(context,request,prior,'a'*64,'b'*64)

    def test_duplicate_empty_oversized_and_unknown_schema_rejected(self):
        for kind in ('duplicate','empty','oversized','extra'):
            _,context,request,prior=scope()
            if kind=='duplicate':request['roots'].append(request['roots'][0]);context['new_original_addresses'].append(request['roots'][0]['original_address'])
            elif kind=='empty':request['roots']=[];context['new_original_addresses']=[]
            elif kind=='oversized':request['roots']*=c.MAX_ROOTS
            else:context['waive_unknowns']=True
            with self.subTest(kind=kind),self.assertRaises(ValueError):c.validate_context(context,request,prior,'a'*64,'b'*64)

    def test_exact_new_request_uses_unchanged_selected_proof_gate(self):
        fx,context,request,prior=scope();raw,u,p,rows,selections,providers,b=fx
        groups=c.finite.validate_request(request,selections,dict(units=[u]),dict(units=[p]),providers)
        self.assertEqual(groups,{0:rows})
        p['verified_functions'][0]['value']=4
        with self.assertRaises(ValueError):c.finite.validate_request(request,selections,dict(units=[u]),dict(units=[p]),providers)

    def test_shared_observer_one_parse_union_and_singletons(self):
        fx,_,_,_=scope();raw,u,p,rows,_,_,bucket=fx
        provenance=dict(object_sha256=u['object_sha256'],source_sha256=u['source_sha256'],observation_epoch='new-v5')
        original=c.central.coff.parse
        with patch.object(c.central.coff,'parse',wraps=original) as parse:
            records=list(c.central.observe_recipe(raw,u,p,rows,bucket,{},provenance))
        self.assertEqual(parse.call_count,1);self.assertEqual(len(records),3)
        self.assertEqual([r['event'] for r in records],['RECIPE_ROOT_UNION_OBSERVATION','SINGLE_ROOT_OBSERVATION','SINGLE_ROOT_OBSERVATION'])
        for row in records:
            self.assertEqual(row['contract']['provenance']['observation_epoch'],'new-v5')
            self.assertFalse(row['runtime_eligible']);self.assertFalse(row['full_serialization_eligible'])

    def test_stale_native_object_is_not_a_new_observation(self):
        fx,_,_,_=scope();raw,u,p,rows,_,_,bucket=fx
        with self.assertRaises(ValueError):list(c.central.observe_recipe(raw+b'changed',u,p,rows,bucket,{},{}))

    def test_summary_preserves_complete_graph_separately_from_closure(self):
        raw,u,p,rows,_,_,bucket=fixture(safeseh=True)
        record=next(c.central.observe_recipe(raw,u,p,rows,bucket,{},dict(object_sha256=u['object_sha256'],source_sha256=u['source_sha256'])))
        row=c.summary_row(record,1)
        self.assertEqual(row['graph_observation_complete'],record['graph_observation_complete'])
        self.assertFalse(row['closure_observed']);self.assertTrue(row['graph_observation_complete'])
        self.assertEqual(row['record_sha256'],c.digest(record))

    def test_map_scope_and_false_runtime_flags_are_required(self):
        fx,_,_,_=scope();selections=fx[4];providers={a:dict(i,section=selections[a]['section']) for a,i in fx[5].items()}
        planned=dict(policy_id='selected-physical-provider-map-v1',kind='typed-provider-map',census=dict(selected_owners=68657),
            materialized_exports=0,provider_identity_is_planned_namespace=True,input_stability=True,optional_function_index_present=False,
            materialization_approved=False,native_tools_run=False,providers=providers,**c.FALSE)
        self.assertEqual(c.map_identities(planned,selections),fx[5])
        for key,val in [('materialized_exports',1),('namespace_approved',True),('optional_function_index_present',True)]:
            bad=copy.deepcopy(planned);bad[key]=val
            with self.subTest(key=key),self.assertRaises(ValueError):c.map_identities(bad,selections)


if __name__=='__main__':unittest.main()
