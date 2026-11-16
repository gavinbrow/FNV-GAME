"""Synthetic-only variable cohort proof tests."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import application_link_actual_cohort as actual
from test_application_link_wave14 import fixture


def sample():
    wrappers, members, handoff = fixture()
    # Recreate a distinct actual subset with original contiguous proof ordinals.
    return wrappers[:9], members[:9], {'records': handoff['records'][:9]}


def verify(args, members=9, fields=8):
    return actual.verify_proof_ledger(*args, member_count=members, field_count=fields)


class ActualCohortTests(unittest.TestCase):
    def test_actual_scope_keeps_zero_field_members(self):
        result = verify(sample())
        self.assertEqual(len(result['fullproofs']), 8)
        self.assertEqual(result['members'], ['member%d.obj' % n for n in range(9)])

    def test_counts_are_actual_not_forecast(self):
        for members, fields in [(55, 8), (9, 46), (True, 8), (9, True), (0, 8)]:
            with self.subTest(members=members, fields=fields), self.assertRaises(ValueError):
                verify(sample(), members, fields)

    def test_missing_or_duplicate_member_and_ordinal(self):
        for mode in ('missing', 'member', 'ordinal'):
            args = copy.deepcopy(sample())
            if mode == 'missing': args[1].pop()
            elif mode == 'member': args[2]['records'][1]['member'] = args[2]['records'][0]['member']
            else: args[2]['records'][1]['field_proof_ordinal'] = 1
            with self.subTest(mode=mode), self.assertRaises(ValueError): verify(args)

    def test_tampered_wrapper_ancestry_and_compact(self):
        for mode in ('wrapper', 'ancestry', 'compact'):
            args = copy.deepcopy(sample())
            if mode == 'wrapper': args[0][7]['fields'][0]['physical_offset'] = 9
            elif mode == 'ancestry': args[1][0]['projection']['authority'] = {}
            else: args[1][7]['projection']['fields'][0]['symbol_index'] = 999
            with self.subTest(mode=mode), self.assertRaises(ValueError): verify(args)

    def test_zero_fields_still_require_member_ancestry(self):
        args = copy.deepcopy(sample())
        args[1][0]['projection']['output_sha256'] = 'different'
        with self.assertRaises(ValueError): verify(args)

    def test_duplicate_root_rejected_even_with_valid_ancestry(self):
        args = copy.deepcopy(sample())
        root = args[2]['records'][0]['root']
        w, p, r = args[0][1], args[1][1]['projection'], args[2]['records'][1]
        w['requested_root'] = root
        p['requested_roots'] = [root]
        r['root'] = root
        r['field_proof_record_sha256'] = actual.digest(w)
        with self.assertRaisesRegex(ValueError, 'duplicate root'): verify(args)

    def test_boolean_coordinate_rejected(self):
        args = copy.deepcopy(sample())
        args[1][7]['projection']['fields'][0]['offset'] = False
        with self.assertRaisesRegex(ValueError, 'integer physical coordinates'): verify(args)

    def test_reordered_handoff_rejected(self):
        args = copy.deepcopy(sample())
        args[2]['records'][0], args[2]['records'][1] = args[2]['records'][1], args[2]['records'][0]
        with self.assertRaisesRegex(ValueError, 'ordinals'): verify(args)

    def test_same_address_with_extra_root_key_rejected(self):
        args = copy.deepcopy(sample())
        root = dict(args[2]['records'][0]['root'], extra='different')
        w, p, r = args[0][1], args[1][1]['projection'], args[2]['records'][1]
        w['requested_root'] = root
        p['requested_roots'] = [root]
        r['root'] = root
        r['field_proof_record_sha256'] = actual.digest(w)
        with self.assertRaisesRegex(ValueError, 'duplicate root'): verify(args)


if __name__ == '__main__': unittest.main()
