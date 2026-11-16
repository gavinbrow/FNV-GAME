"""Independent projection/publication attacks using authored fixtures only."""
from pathlib import Path
from types import SimpleNamespace
import struct
import tempfile
import unittest
from unittest.mock import patch

from test_parent_eh_adapter import valid_case
from test_parent_eh_extension_lane08 import descriptor_first
import parent_eh_adapter as adapter
import parent_eh_project as projector
import parent_eh_publish as publisher


def mixed_table(obj, *, alias=False):
    obj['symbols'][26] = dict(name='_another_omitted_handler', section=17,
        value=8, type=32, storage=2, aux_count=0, aux=b'')
    obj['sections'][16].update(size=12, payload=struct.pack('<III', 68, 19, 26))
    aux = bytearray(obj['symbols'][64]['aux'])
    struct.pack_into('<I', aux, 0, 12)
    obj['symbols'][64]['aux'] = bytes(aux)
    if alias:
        obj['symbols'][27] = dict(name='_authored_sx_alias', section=16,
            value=8, type=0, storage=3, aux_count=0, aux=b'')


class ParentEHProjectionAdversarialTests(unittest.TestCase):
    def test_table_trim_cannot_leave_static_symbol_outside_new_extent(self):
        inputs = valid_case(object_edit=lambda obj: mixed_table(obj, alias=True))
        expected = adapter.observe_parent(**inputs)
        self.assertTrue(expected['structural_projection_candidate'], expected)
        with self.assertRaises(ValueError):
            projector.project_parent(inputs, expected)

    def test_nonfirst_handler_and_six_state_descriptor_mapping_survive(self):
        def edit(obj):
            descriptor_first(obj, 6)
            mixed_table(obj)
        inputs = valid_case(object_edit=edit)
        expected = adapter.observe_parent(**inputs)
        self.assertTrue(expected['structural_projection_candidate'], expected)
        output, report = projector.project_parent(inputs, expected)
        final = projector.coff.parse(output)
        sx = report['safeseh']
        self.assertEqual([row['retain'] for row in sx['source_records']], [False, True, False])
        self.assertEqual(final['sections'][sx['output_section']]['payload'],
                         struct.pack('<I', sx['output_handler_index']))
        self.assertEqual(len(report['after']['fields']), 16)
        self.assertEqual(report['original_before']['semantic']['metadata_descriptors'],
                         dict(funcinfo=[0, 36], unwind=[36, 84]))
        self.assertFalse(report['runtime_eligible'])

    def test_oversized_envelopes_reject_before_read_or_JSON_allocation(self):
        for selected in ('input_request', 'observation', 'outcome_review'):
            with self.subTest(selected=selected), tempfile.TemporaryDirectory() as folder:
                args = SimpleNamespace(expected_tool=[name + '=' + 'a' * 64
                    for name in publisher.TOOLS], parent='0x10000000',
                    out_dir=Path(folder) / 'out')
                for name in ('input_request', 'observation', 'outcome_review'):
                    path = Path(folder) / (name + '.json')
                    if name == selected:
                        with path.open('wb') as stream:
                            stream.seek(8 * 1024**2)
                            stream.write(b'x')
                    else:
                        path.write_text('{}')
                    setattr(args, name, path)
                    setattr(args, name + '_sha256', 'a' * 64)
                with patch.object(publisher.collector, 'read_bound',
                    side_effect=AssertionError('envelope read reached before size guard')) as mocked:
                    with self.assertRaises(ValueError):
                        publisher.publish(args)
                mocked.assert_not_called()


if __name__ == '__main__':
    unittest.main()
