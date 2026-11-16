"""Pure composition wiring tests with synthetic consumers, no native actions."""
import hashlib,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import application_successor_compose_v12 as v

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
            out=v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',response_inputs={'new_archive':'archive.lib'},archive_bytes=b'a',archive_sha256=hashlib.sha256(b'a').hexdigest(), archive_identity=dict(requested_path='archive.lib',path='archive.lib',sha256=hashlib.sha256(b'a').hexdigest(),size=1,device=1,inode=1),factory_inputs={},qualified_selected_providers={})
        self.assertFalse(out['link_approved']);self.assertFalse(out['admission_approved'])

    def test_consumer_failure_stops_composition(self):
        built={'fields':[],'baseline_observation':{'complete_field_count':0},
               'report':{'successor_namespace':{'symbols':{}}}}
        with patch.object(v.assembly,'assemble',return_value=built), \
             patch.object(v.census,'iat_census',side_effect=ValueError('bad census')), \
             patch.object(v.response,'transform') as transform:
            with self.assertRaises(ValueError):
                v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',response_inputs={'new_archive':'archive.lib'},archive_bytes=b'a',archive_sha256=hashlib.sha256(b'a').hexdigest(), archive_identity=dict(requested_path='archive.lib',path='archive.lib',sha256=hashlib.sha256(b'a').hexdigest(),size=1,device=1,inode=1),factory_inputs={},qualified_selected_providers={})
            transform.assert_not_called()

    def test_unrelated_response_path_or_archive_hash_rejected(self):
        for path,sha in [('other.lib',hashlib.sha256(b'a').hexdigest()),('archive.lib','b'*64)]:
            with self.subTest(path=path,sha=sha), self.assertRaises(ValueError):
                v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',
                    response_inputs={'new_archive':'archive.lib'},archive_bytes=b'a',archive_sha256=hashlib.sha256(b'a').hexdigest(),
                    archive_identity=dict(requested_path=path,path=path,sha256=sha,size=1,device=1,inode=1),
                    factory_inputs={},qualified_selected_providers={})

    def test_declared_size_matches_actual_archive_bytes(self):
        digest=hashlib.sha256(b'a').hexdigest()
        with self.assertRaises(ValueError):
            v.compose(baseline_bytes={},semantic_inputs={},iat_inputs={},crt_inputs={},response_bytes=b'x',
                response_inputs={'new_archive':'archive.lib'},archive_bytes=b'a',archive_sha256=digest,
                archive_identity=dict(requested_path='archive.lib',path='archive.lib',sha256=digest,size=999,device=1,inode=1),
                factory_inputs={},qualified_selected_providers={})

if __name__=='__main__':unittest.main()
