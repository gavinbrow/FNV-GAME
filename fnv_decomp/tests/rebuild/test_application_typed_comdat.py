"""Authored COFF and saved-metadata negatives; no Game or native tools."""
import copy
import json
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/rebuild'), str(ROOT/'tests/rebuild')]
import application_typed_comdat as subject
import test_comdat_any_frontier_observer as fixture_owner
from test_comdat2_code_policy_independent import fixture as native_fixture, rewrite


def fixture():
    raw, contract, root = native_fixture()
    def directive(sections, symbols, obj):
        sections[1]['payload'] = subject.DIRECTIVES
        sections[1]['size'] = len(subject.DIRECTIVES)
        from test_coff_code_archive import symbol, aux
        symbols[2] = symbol('.drectve', 2, storage=3, auxiliary=aux(len(subject.DIRECTIVES), selection=0))
    raw, contract, root = rewrite(raw, contract, root, directive)
    with patch.object(fixture_owner, 'native_fixture', return_value=(raw, contract, root)):
        raw, row, candidate = fixture_owner.fixture()
    f = subject.factory
    evidence = f.observer.observe_member(raw, row, candidate)
    providers = {root['original_address']: f.observer.selector.root_identity(root)}
    output, p = f.core.project_member(raw, row['contract'], row['certificate'], evidence['witnesses'],
        evidence['composed'], [root], providers, existing_exports=[], policy_id=f.core.POLICY)
    p.update(authority=candidate['authority'], central_record_sha256=f.digest(row),
             observer_record_sha256=f.digest(evidence))
    for key, name in [('before_comparison', root['symbol']), ('after_comparison', p['exports'][0])]:
        p[key] = [dict(address=root['original_address'],symbol=name,size=root['size'],compiled_extent=root['size'],
                       verdict='match',errors=[],relocations=[])]
    return output, json.loads(json.dumps(p)), evidence


class TypedConsumerTests(unittest.TestCase):
    def test_accepted_authored_member_preserves_saved_metadata(self):
        data,p,e=fixture();before=copy.deepcopy((p,e))
        result=subject.verify_member(data,p,e)
        self.assertEqual(result['canonical'],p['exports'][0]);self.assertEqual((p,e),before)
        self.assertFalse(e['original_negative_certificate']['closure_observed'])

    def test_negative_certificate_cannot_be_promoted_or_borrowed(self):
        data,p,e=fixture();e['original_negative_certificate']['closure_observed']=True
        with self.assertRaises(ValueError):subject.verify_member(data,p,e)
        data,p,e=fixture();p['composed_certificate_sha256']='0'*64
        with self.assertRaises(ValueError):subject.verify_member(data,p,e)

    def test_aux_selection_or_checksum_changed_even_if_output_hash_rebound(self):
        for relative,value,fmt in [(14,1,'<B'),(8,1234,'<I')]:
            data,p,e=fixture();data=bytearray(data)
            symbol_table=struct.unpack_from('<I',data,8)[0]
            definition=e['witnesses'][0]['observation']['root_section_definition_symbol_index']
            aux=p['maps']['auxiliary_map'][str(definition+1)]
            struct.pack_into(fmt,data,symbol_table+aux*18+relative,value)
            p['output_sha256']=subject.sha(data)
            with self.assertRaises(ValueError):subject.verify_member(bytes(data),p,e)

    def test_hidden_directive_is_rejected_after_hash_rebinding(self):
        data,p,e=fixture();data=data.replace(b'OLDNAMES',b'OTHERLIB');p['output_sha256']=subject.sha(data)
        with self.assertRaises(ValueError):subject.verify_member(data,p,e)

    def test_wrong_original_aux_owner_rejected(self):
        data,p,e=fixture();p['maps']['auxiliary_map']={}
        with self.assertRaises(ValueError):subject.verify_member(data,p,e)

    def test_stale_payload_rejected_even_if_output_hash_rebound(self):
        data,p,e=fixture();data=data.replace(b'authored-code-01!',b'authored-code-02!');p['output_sha256']=subject.sha(data)
        with self.assertRaises(ValueError):subject.verify_member(data,p,e)

    def test_no_namespace_or_runtime_promotion(self):
        for key in subject.FALSE_FLAGS:
            data,p,e=fixture();p[key]=True
            with self.assertRaises(ValueError):subject.verify_member(data,p,e)


if __name__ == '__main__':
    unittest.main()
