"""Authored dictionary-only UUID handoff attacks; no saved input or native I/O."""
import copy,importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]/'build/rebuild/uuid2768-typed-handoff-source-v1/test_prepare.py'
s=importlib.util.spec_from_file_location('uuid_handoff_author_fixture_lane08',P);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);m=h.m
class IndependentHandoffTests(unittest.TestCase):
 def call(self,v,c,k):
  with patch.object(m,'CERT',c),patch.object(m,'CONTRACT',k),patch.object(m,'DECL_CANONICAL',m.digest(v['declaration'])):return m.draft(**v)
 def test_contract_fields_cannot_be_replaced_with_self_consistent_ledger(self):
  v,c,k=h.fixture();l=v['ledger'];l['fields']=copy.deepcopy(l['fields']);l['fields'][0]['unproved']='alternate'
  l['fields_sha256']=m.digest(l['fields']);l['mapped_fields'][0]['original_field_sha256']=m.digest(l['fields'][0]);v['receipt']['result']['projection']['fields'][0]['field_proof_sha256']=m.digest(l['fields'][0])
  with self.assertRaises(ValueError):self.call(v,c,k)
 def test_ledger_identity_digests_are_required(self):
  for key in ('output_sha256','contract_sha256','fields_sha256'):
   v,c,k=h.fixture();v['ledger'][key]='0'*64
   with self.subTest(key=key),self.assertRaises(ValueError):self.call(v,c,k)
 def test_serialized_indices_are_strict_positive_typed(self):
  for section,index in ((2,True),(True,10),(2,-1)):
   v,c,k=h.fixture();p=v['receipt']['result']['projection'];v['ledger']['mapped_fields'][0].update(serialized_section=section,serialized_symbol_index=index);p['maps']['section_map']['131']=section;p['maps']['symbol_map']['100']=index
   with self.subTest(section=section,index=index),self.assertRaises(ValueError):self.call(v,c,k)
 def test_duplicate_occurrence_ordinal_not_set_membership(self):
  v,c,k=h.fixture();p=v['receipt']['result']['projection'];p['discharged_blocker_occurrences'][1]['ordinal']=1
  with self.assertRaises(ValueError):self.call(v,c,k)
 def test_more_directive_material_not_ignored(self):
  v,c,k=h.fixture();raw=bytes.fromhex(v['facts']['raw_section_hex']);raw=raw.rstrip()+b'X';raw+=b' '*(93-len(raw));v['facts'].update(raw_section_hex=raw.hex(),raw_section_sha256=__import__('hashlib').sha256(raw).hexdigest())
  with self.assertRaises(ValueError):self.call(v,c,k)
 def test_success_is_copy_and_no_adoption(self):
  v,c,k=h.fixture();before=copy.deepcopy(v);r=self.call(v,c,k);self.assertEqual(v,before);self.assertFalse(r['sealed']);self.assertFalse(r['namespace_approved']);self.assertFalse(r['native_archive_conformance_verified'])
if __name__=='__main__':unittest.main()
