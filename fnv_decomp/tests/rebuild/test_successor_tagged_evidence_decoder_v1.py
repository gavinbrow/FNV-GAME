import base64
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
d=load('decoder_fixture','tools/rebuild/successor_tagged_evidence_decoder_v1.py')
w=load('encoder_fixture','tools/rebuild/application_successor_fixed_v6.py')
def wrap(node):
    return json.dumps({'kind':'successor-semantic-composition-v12','encoding':'tagged-tree-v1','evidence':node},
                      separators=(',',':')).encode()

class Tests(unittest.TestCase):
    def test_roundtrip_preserves_unknowns_and_bytes(self):
        original={'literal':{'$bytes_base64':'aGk='},'bytes':b'hi','empty':b'',
                  'nested':[None,True,False,0,1,1.25,-0.0,'',{'type':'bytes','base64':'aGk='}],
                  'unicode':'\u00e9'}
        actual=d.decode_document(wrap(w._encode_evidence(original)))
        self.assertEqual(actual,original);self.assertIs(type(actual['bytes']),bytes)
        self.assertIs(type(actual['literal']),dict);self.assertIs(type(actual['nested'][1]),bool)
        self.assertIs(type(actual['nested'][3]),int)
    def test_duplicate_json_and_tagged_map_keys_rejected(self):
        with self.assertRaises(ValueError):d.decode_document(b'{"kind":"x","kind":"y"}')
        x={'type':'map','items':[['x',{'type':'scalar','value':1}],['x',{'type':'scalar','value':2}]]}
        with self.assertRaises(ValueError):d.decode_document(wrap(x))
    def test_base64_is_canonical_and_strict(self):
        for value in ('aGk','aGk=\n','aGk===','aGk_','AB==','é'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                d.decode_document(wrap({'type':'bytes','base64':value}))
        self.assertEqual(d.decode_document(wrap({'type':'bytes','base64':base64.b64encode(b'hi').decode()})),b'hi')
    def test_schema_and_types_rejected(self):
        bad=[{'type':'bytes','base64':'','extra':1},{'type':'list','items':{}},
             {'type':'map','items':[['x']]},{'type':'scalar','value':[]},
             {'type':'scalar','value':{}},{'type':'unknown'},[],{'type':True},
             {'type':'scalar','value':float('inf')}]
        for node in bad:
            with self.subTest(node=node),self.assertRaises(ValueError):d.decode_document(wrap(node))
        with self.assertRaises(ValueError):d.decode_document(b'\xff')
        with self.assertRaises(ValueError):d.decode_document(wrap({'type':'scalar','value':1}).replace(b'tagged-tree-v1',b'wrong'))
    def test_bounds(self):
        with patch.object(d,'MAX_DOCUMENT_BYTES',5):
            with self.assertRaises(ValueError):d.decode_document(wrap({'type':'scalar','value':1}))
        with patch.object(d,'MAX_NODES',2):
            with self.assertRaises(ValueError):d.decode_document(wrap(w._encode_evidence([1,2])))
        with patch.object(d,'MAX_DEPTH',1):
            with self.assertRaises(ValueError):d.decode_document(wrap(w._encode_evidence([[1]])))
        with patch.object(d,'MAX_DECODED_BYTES',1):
            with self.assertRaises(ValueError):d.decode_document(wrap(w._encode_evidence([b'a',b'b'])))

if __name__=='__main__':unittest.main()
