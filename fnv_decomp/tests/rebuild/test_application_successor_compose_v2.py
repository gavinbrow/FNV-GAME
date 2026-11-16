"""Pure composition wiring tests with synthetic consumers, no native actions."""
import sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_successor_compose_v2 as v

class Tests(unittest.TestCase):
    def test_uses_full_assembled_fields_and_current_aliases(self):
        built={'fields':[{'old':1},{'new':2}],'baseline_observation':{'complete_field_count':1},
               'report':{'successor_namespace':{'symbols':{'base':'c','new':'c'}}}}
        def check(**args):
            self.assertEqual(args['baseline'],[{'old':1}]);self.assertEqual(args['fields'],built['fields'])
            self.assertEqual(args['namespace'],['base','new']);return {'tokens':['iat']}
        def crt(**args):
            self.assertEqual(args['fields'],built['fields']);return {'tokens':['crt']}
        def response(data,**args):
            self.assertEqual(args['current_aliases'],['iat','crt']);return {'response_sha256':'synthetic'}
        with patch.object(v.assembly,'assemble',return_value=built),patch.object(v.census,'iat_census',side_effect=check), \
             patch.object(v.census,'crt_census',side_effect=crt),patch.object(v.response,'transform',side_effect=response):
            out=v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',response_inputs={})
        self.assertFalse(out['link_approved']);self.assertFalse(out['admission_approved'])

    def test_consumer_failure_stops_composition(self):
        built={'fields':[],'baseline_observation':{'complete_field_count':0},
               'report':{'successor_namespace':{'symbols':{}}}}
        with patch.object(v.assembly,'assemble',return_value=built), \
             patch.object(v.census,'iat_census',side_effect=ValueError('bad census')), \
             patch.object(v.response,'transform') as transform:
            with self.assertRaises(ValueError):
                v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',response_inputs={})
            transform.assert_not_called()

if __name__=='__main__':unittest.main()
