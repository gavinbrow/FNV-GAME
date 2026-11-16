import importlib.util
import math
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module);return module
e=load('encoder','tools/rebuild/successor_tagged_evidence_encoder_v1.py')
d=load('decoder','tools/rebuild/successor_tagged_evidence_decoder_v1.py')
w=load('old_wrapper','tools/rebuild/application_successor_fixed_v6.py')

class Tests(unittest.TestCase):
    def test_exact_old_canonical_bytes_and_roundtrip(self):
        data={'literal':{'$bytes_base64':'aGk='},'bytes':b'hi','unknown':[True,0,None,-0.0,'é 😀',b'x'*13000]}
        expected=w.canonical({'kind':'successor-semantic-composition-v12','encoding':'tagged-tree-v1',
                              'evidence':w._encode_evidence(data)})+b'\n'
        actual=e.encode_document(data)
        self.assertEqual(actual,expected);self.assertEqual(d.decode_document(actual),data)
    def test_chunk_boundaries_and_unicode_escaping(self):
        for x in ('\\"\n'*5000,'😀'*5000,'\ud800x'*3000):
            expected=w.canonical({'kind':'successor-semantic-composition-v12','encoding':'tagged-tree-v1',
                                  'evidence':w._encode_evidence(x)})+b'\n'
            self.assertEqual(e.encode_document(x),expected)
    def test_enforces_depth_nodes_decoded_bytes_and_document_cap(self):
        for name,limit,value in [('MAX_DEPTH',1,[[1]]),('MAX_NODES',2,[1,2]),
                                 ('MAX_DECODED_BYTES',1,[b'a',b'b']),('MAX_DOCUMENT_BYTES',100,'x'*5000)]:
            with self.subTest(name=name),patch.object(e,name,limit):
                with self.assertRaises(ValueError):e.encode_document(value)
    def test_rejects_nonfinite_and_foreign_types(self):
        for x in (float('nan'),float('inf'),bytearray(b'x'),{1:'bad'},(1,2)):
            with self.subTest(x=x),self.assertRaises(ValueError):e.encode_document(x)
    def test_exact_128_depth_boundary(self):
        value=1
        for _ in range(128):value=[value]
        self.assertEqual(d.decode_document(e.encode_document(value)),value)
        with self.assertRaises(ValueError):e.encode_document([value])

if __name__=='__main__':unittest.main()
