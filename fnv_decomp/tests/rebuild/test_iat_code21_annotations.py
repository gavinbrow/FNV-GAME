"""Additive CODE21 proof handling; no metadata archives or native processes."""
import copy
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]/'tools/rebuild'))
import iat_field_annotations as old
import iat_code21_annotations as new
from test_iat_field_annotations import fixture


def inputs():
    rows, proofs, catalog, expected = fixture()
    rows[0]['component'] = 'CODE21'
    return rows, proofs, catalog, [new.location(rows[0])]


class Code21Tests(unittest.TestCase):
    def test_additive_annotation_and_census_preserve_compact_full_other_rows(self):
        args = inputs(); before = copy.deepcopy(args)
        rows = new.annotate(*args); normative = copy.deepcopy(rows)
        view = new.census_view(rows, args[2])
        self.assertEqual(args, before); self.assertEqual(rows, normative)
        self.assertEqual(rows[0]['proof'], args[0][0]['proof'])
        self.assertEqual(new.digest(rows[0]['original_field_proof']), rows[0]['proof']['field_proof_sha256'])
        self.assertEqual(rows[1], args[0][1])
        self.assertEqual(view[0]['proof']['import_id'], 13)
        self.assertNotIn('import_id', rows[0]['proof'])

    def test_existing_CODE59_annotation_and_all_other_components_unchanged(self):
        original = fixture(); old_rows = old.annotate(*original)
        rows, proofs, catalog, expected = inputs()
        rows = old_rows+rows
        annotated = new.annotate(rows, proofs, catalog, expected)
        self.assertEqual(annotated[:2], old_rows)
        view = new.census_view(annotated, catalog)
        self.assertEqual(view[0]['proof']['import_id'], 13)
        self.assertEqual(view[2]['proof']['import_id'], 13)
        self.assertEqual(annotated[:2], old_rows)

    def test_missing_duplicate_extra_or_wrong_hash_rejected(self):
        for change in ('missing', 'duplicate', 'extra', 'hash'):
            rows, proofs, catalog, expected = inputs()
            if change == 'missing': rows.pop(0)
            if change == 'duplicate': rows.append(copy.deepcopy(rows[0]))
            if change == 'extra':
                row = copy.deepcopy(rows[0]); row['member'] = 'extra.obj'; rows.append(row)
            if change == 'hash': next(iter(proofs.values()))['changed'] = True
            with self.subTest(change=change), self.assertRaises(ValueError): new.annotate(rows, proofs, catalog, expected)

    def test_unsafe_even_rehashed_fullproof_is_not_normalized(self):
        rows, proofs, catalog, expected = inputs(); full = next(iter(proofs.values()))
        full['import_pointer_source_conflict'] = True
        h = new.digest(full); rows[0]['proof']['field_proof_sha256'] = h
        with self.assertRaisesRegex(ValueError, 'conflicting original IAT'):
            new.annotate(rows, {h:full}, catalog, [new.location(rows[0])])

    def test_unhydrated_CODE21_or_tampered_export_rejected_by_view(self):
        args = inputs()
        with self.assertRaisesRegex(ValueError, 'not hydrated'): new.census_view(args[0], args[2])
        rows = new.annotate(*args); rows[0]['IAT_annotation']['export'] = dict(kind='name', name='Wrong')
        with self.assertRaises(ValueError): new.census_view(rows, args[2])


if __name__ == '__main__': unittest.main()
