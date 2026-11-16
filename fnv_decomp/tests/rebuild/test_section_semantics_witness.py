"""Synthetic section witness adapter tests; no real objects or image reads."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import section_semantics_witness as adapter
import ordinary_initialized_data_omission as producer
from test_ordinary_initialized_data_omission import context

def fixture(**kwargs):
    raw,contract,base,sections=context(**kwargs)
    witness=producer.observe_omitted_initialized_data(raw,contract,base,sections)
    auth=dict(record_sha256='a'*64,receipt_sha256='b'*64,contract_sha256=adapter.digest(contract),
              certificate_sha256=adapter.digest(base),lane=1,ordinal=1)
    return raw,contract,base,sections,witness,auth

def qualify(f): return adapter.qualify(*f[:5],authority=f[5])

class SectionSemanticsWitnessTests(unittest.TestCase):
    def test_replayed_readonly_witness_preserves_negative(self):
        f=fixture(); before=copy.deepcopy(f); result=qualify(f)
        self.assertEqual(f,before); self.assertIs(f[2]['closure_observed'],False)
        self.assertEqual(len(result['qualified_occurrences']),1)
        self.assertEqual(result['original_blocker_occurrences'][0]['blocker'],f[2]['blockers'][0])
        self.assertEqual(result['unqualified_occurrences'],[])
        for key in adapter.FALSE:self.assertIs(result[key],False)
        self.assertTrue(result['authority_authentication_required'])

    def test_second_supported_alignment(self):
        self.assertEqual(len(qualify(fixture(flags=0x40101040,selection=1))['qualified_occurrences']),1)

    def test_unsupported_sections_remain_unqualified(self):
        for name,flags in [('.bss',0xc0100080),('.tls$',0xc0300040),('.xdata$x',0x40300040),('.CRT$XCU',0x40300040)]:
            with self.subTest(name=name,flags=flags):
                result=qualify(fixture(name=name,flags=flags))
                self.assertEqual(result['qualified_occurrences'],[])
                self.assertTrue(result['unqualified_occurrences'])
        # This authored variant does not trigger an original negative at all.
        with self.assertRaisesRegex(ValueError,'negative certificate'):qualify(fixture(name='.rdata',flags=0x40400040))

    def test_live_incoming_alias_and_outgoing_cannot_qualify(self):
        for kwargs in [dict(incoming=True,retained=True),dict(alias=True),dict(outgoing=True),dict(special=True),dict(flags=0x40101040,selection=2)]:
            with self.subTest(kwargs=kwargs):self.assertEqual(qualify(fixture(**kwargs))['qualified_occurrences'],[])

    def test_forged_or_cross_scope_witness_rejected(self):
        f=list(fixture());f[4]=copy.deepcopy(f[4]);f[4]['rows'][0]['approved']=False
        with self.assertRaisesRegex(ValueError,'replay mismatch'):qualify(f)
        f=list(fixture());f[5]=dict(f[5],certificate_sha256='c'*64)
        with self.assertRaisesRegex(ValueError,'authority scope'):qualify(f)

    def test_stale_raw_and_certificate_rejected(self):
        f=list(fixture());f[0]+=b'changed'
        with self.assertRaises(ValueError):qualify(f)

    def test_metadata_without_physical_replay_cannot_qualify(self):
        f=list(fixture());f[0]={'claimed_object_sha256':f[1]['provenance']['object_sha256']}
        with self.assertRaisesRegex(ValueError,'input types'):qualify(f)

    def test_producer_source_pin_drift_rejected(self):
        with patch.object(adapter,'WITNESS_PIN','0'*64):
            with self.assertRaisesRegex(ValueError,'producer drift'):qualify(fixture())

    def test_witness_scope_and_ordinal_are_not_borrowable(self):
        for mutate in [lambda w:w.update(contract_identity_sha256='0'*64),
                       lambda w:w.update(original_certificate_sha256='0'*64),
                       lambda w:w['rows'][0].update(section=5),
                       lambda w:w['rows'][0].update(flags=0xc0100080),
                       lambda w:w['rows'][0].update(discharge_blocker_ids=[]),
                       lambda w:w.update(witness_complete=False)]:
            f=list(fixture());f[4]=copy.deepcopy(f[4]);mutate(f[4])
            with self.subTest(mutate=mutate),self.assertRaisesRegex(ValueError,'replay mismatch'):qualify(f)

    def test_nonsection_blocker_does_not_get_qualified(self):
        f=list(fixture()); base=copy.deepcopy(f[2]); b={'code':'SPECIAL_RUNTIME_REFERENCE','evidence':[1,2,3,4]};b['blocker_id']=adapter.digest(b);base['blockers']=[b];f[2]=base;f[5]=dict(f[5],certificate_sha256=adapter.digest(base));w=copy.deepcopy(f[4]);w['original_certificate_sha256']=adapter.digest(base);w['rows'][0]['discharge_blocker_ids']=[b['blocker_id']];w['discharge_blocker_ids']=[b['blocker_id']];f[4]=w
        with patch.object(adapter.omission,'observe_omitted_initialized_data',return_value=w):
            with self.assertRaisesRegex(ValueError,'ambiguous section blocker'):qualify(f)
        f=list(fixture());f[2]=copy.deepcopy(f[2]);f[2]['blockers']=[];f[5]=dict(f[5],certificate_sha256=adapter.digest(f[2]))
        with self.assertRaises(ValueError):qualify(f)

    def test_strict_scope_types(self):
        for mutate in [lambda f:f.__setitem__(3,[True]),lambda f:f[5].update(lane=True),lambda f:f[5].update(ordinal=0)]:
            f=list(fixture());f[5]=copy.deepcopy(f[5]);mutate(f)
            with self.assertRaises(ValueError):qualify(f)

    def test_duplicate_equal_blocker_occurrences_cannot_be_collapsed(self):
        f=list(fixture());base=copy.deepcopy(f[2]);base['blockers'].append(copy.deepcopy(base['blockers'][0]));f[2]=base;f[5]=dict(f[5],certificate_sha256=adapter.digest(base))
        forged=copy.deepcopy(f[4]);f[4]=forged
        # Isolate the adapter's occurrence guard; a real producer would reject
        # this forged original certificate during its independent replay first.
        forged['original_certificate_sha256']=adapter.digest(base)
        with patch.object(adapter.omission,'observe_omitted_initialized_data',return_value=forged):
            with self.assertRaisesRegex(ValueError,'ambiguous section blocker'):qualify(f)

    def test_mixed_blockers_preserve_nonsection_occurrence(self):
        f=list(fixture());base=copy.deepcopy(f[2]);other={'code':'SPECIAL_RUNTIME_REFERENCE','evidence':[1,2,3,4]};other['blocker_id']=adapter.digest(other);base['blockers'].append(other);f[2]=base;f[5]=dict(f[5],certificate_sha256=adapter.digest(base));w=copy.deepcopy(f[4]);w['original_certificate_sha256']=adapter.digest(base);w['remaining_blockers']=[other];f[4]=w
        with patch.object(adapter.omission,'observe_omitted_initialized_data',return_value=w):
            out=qualify(f)
        self.assertEqual([x['blocker'] for x in out['unqualified_occurrences']],[other]);self.assertFalse(out['runtime_eligible'])

if __name__=='__main__':unittest.main()
