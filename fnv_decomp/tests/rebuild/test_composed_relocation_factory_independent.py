"""Independent typed LABEL factory boundaries with authored COFF and oracle."""
import copy
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools/rebuild'), str(ROOT / 'tests/rebuild'), str(ROOT / 'tools')]
import coff_code_archive as coff
import composed_relocation_projection as core
import composed_relocation_factory as factory
from test_composed_relocation_projection_independent import typed_label_context


def authored_reference(values):
    root = values[5][0]
    source = bytearray(coff.parse(values[0])['sections'][root['section']]['payload'])
    for field in values[1]['fields']:
        struct.pack_into('<I', source, field['source_field_offset'], field['original_operand'])
    return SimpleNamespace(read=lambda address, size: bytes(source) if
        (address, size) == (int(root['original_address'], 16), root['size']) else b'')


def authored_operand_reference(executable=True):
    rows = [dict(coff_relocation=dict(kind=6), original_field_va='0x00500000',
                 original_operand=0x00600004, exact_original_target_va='0x00600004'),
            dict(coff_relocation=dict(kind=20), original_field_va='0x00500004',
                 original_operand=0xfffffff8, exact_original_target_va='0x00500000')]
    operands = {0x00100000: struct.pack('<I', rows[0]['original_operand']),
                0x00100004: struct.pack('<I', rows[1]['original_operand'])}
    pe = SimpleNamespace(base=0x00400000,
        section=lambda rva, size, required: dict(executable=executable and size == 4 and rva in operands),
        read_rva=lambda rva, size, allow_code: operands[rva])
    return pe, {0x00500000}, rows


class IndependentComposedFactoryTests(unittest.TestCase):
    def test_actual_label6_stage_and_real_ordinary_oracle_before_after(self):
        values = typed_label_context(addend=4)
        untouched = copy.deepcopy(values)
        with tempfile.TemporaryDirectory() as td:
            original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
            original.write_bytes(values[0])
            output, receipt = factory.verify_member(*values, set(), original, stage, authored_reference(values), {})
            self.assertEqual(values, untouched)
            self.assertFalse(values[2]['closure_observed'])
            self.assertEqual(stage.read_bytes(), output)
            self.assertTrue(any(s['storage'] == 6 for s in coff.parse(output)['symbols'].values()))
            self.assertEqual(struct.unpack_from('<I', coff.parse(output)['sections'][1]['payload'], 0)[0], 4)
            self.assertEqual([r['verdict'] for r in receipt['before_comparison'] + receipt['after_comparison']], ['match', 'match'])
            self.assertFalse(receipt['class6_disguised'])
            self.assertFalse(receipt['runtime_eligible'])
            recovered = coff.read_archive(coff.archive([('authored.obj', output)]))
            self.assertEqual(recovered['members'], [('authored.obj', output)])
            recovered_path = Path(td) / 'recovered.obj'
            recovered_path.write_bytes(recovered['members'][0][1])
            factory.base.bulk.strict_reparse(recovered_path, output)

    def test_comparison_failure_is_fatal_before_or_after_selection(self):
        values = typed_label_context()
        for fail_at in (1, 2):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as td:
                original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
                original.write_bytes(values[0]); calls = []
                def compare(*args, **kwargs):
                    calls.append(1)
                    if len(calls) == fail_at: raise ValueError('typed original comparison refused')
                    return [dict(authored='match')]
                with patch.object(factory.base.bulk, 'compare_functions', side_effect=compare):
                    with self.assertRaisesRegex(ValueError, 'typed original comparison refused'):
                        factory.verify_member(*values, set(), original, stage, object(), {})
                self.assertEqual(stage.exists(), fail_at == 2)
                self.assertEqual(len(calls), fail_at)
                self.assertFalse((Path(td) / 'receipt.json').exists())

    def test_fresh_typed_core_refusal_cannot_use_cached_eligibility(self):
        values = typed_label_context()
        with tempfile.TemporaryDirectory() as td:
            original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
            original.write_bytes(values[0])
            with patch.object(core, 'project_member', side_effect=ValueError('typed replay refused')), \
                 patch.object(factory.base.bulk, 'compare_functions', return_value=[dict(authored='match')]):
                with self.assertRaisesRegex(ValueError, 'typed replay refused'):
                    factory.verify_member(*values, set(), original, stage, object(), {})
            self.assertFalse(stage.exists())

    def test_independent_reader_failure_is_not_a_policy_quarantine(self):
        values = typed_label_context()
        with tempfile.TemporaryDirectory() as td:
            original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
            original.write_bytes(values[0])
            with patch.object(factory.base.bulk, 'strict_reparse', side_effect=ValueError('typed second reader refused')), \
                 patch.object(factory.base.bulk, 'compare_functions', return_value=[dict(authored='match')]):
                with self.assertRaisesRegex(ValueError, 'typed second reader refused'):
                    factory.verify_member(*values, set(), original, stage, object(), {})
            self.assertTrue(stage.exists())
            self.assertFalse((Path(td) / 'receipt.json').exists())

    def test_existing_stage_is_preserved(self):
        values = typed_label_context()
        with tempfile.TemporaryDirectory() as td:
            original, stage = Path(td) / 'original.obj', Path(td) / 'stage.obj'
            original.write_bytes(values[0]); stage.write_bytes(b'authored-preexisting-evidence')
            with patch.object(factory.base.bulk, 'compare_functions', return_value=[dict(authored='match')]):
                with self.assertRaises(FileExistsError):
                    factory.verify_member(*values, set(), original, stage, object(), {})
            self.assertEqual(stage.read_bytes(), b'authored-preexisting-evidence')

    def test_fresh_operand_audit_keeps_highlow_dir32_and_signed_rel32_distinct(self):
        pe, highlow, rows = authored_operand_reference()
        facts = factory.audit_original_fields(pe, highlow, rows + [copy.deepcopy(rows[0])])
        self.assertEqual(len(facts), 2)
        self.assertEqual(facts[0x00500000], (6, 0x00600004, 0x00600004))
        self.assertEqual(facts[0x00500004], (20, 0xfffffff8, 0x00500000))

    def test_cached_operand_target_or_wrong_highlow_membership_cannot_pass(self):
        for change in ('operand', 'target', 'missing-DIR32', 'extra-REL32'):
            pe, highlow, rows = authored_operand_reference()
            if change == 'operand': rows[0]['original_operand'] += 4
            elif change == 'target': rows[1]['exact_original_target_va'] = '0x00500004'
            elif change == 'missing-DIR32': highlow.clear()
            else: highlow.add(0x00500004)
            with self.subTest(change=change), self.assertRaises(ValueError):
                factory.audit_original_fields(pe, highlow, rows)

    def test_original_operand_audit_rejects_non_code_section_and_bool_operand(self):
        pe, highlow, rows = authored_operand_reference(executable=False)
        with self.assertRaises(ValueError): factory.audit_original_fields(pe, highlow, rows)
        pe, highlow, rows = authored_operand_reference()
        rows[0]['original_operand'] = True
        with self.assertRaises(ValueError): factory.audit_original_fields(pe, highlow, rows)


if __name__ == '__main__':
    unittest.main()
