import json
import os
import pathlib
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import splice
import m3secs

CL = pathlib.Path(r'C:\path\to\Decompilation\FNV\tools\vc2008\VC\bin\cl.exe')


@unittest.skipUnless(CL.is_file(), 'VC2008 compiler unavailable')
class ObjectBackingTests(unittest.TestCase):
    def test_relocation_cells_must_fit_symbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            source = p / 'reloc.cpp'
            source.write_text('extern "C" { extern int M3D_00002000; int *ptr = &M3D_00002000; }', encoding='utf-8')
            obj = p / 'reloc.obj'
            env = os.environ.copy()
            env['PATH'] = str(CL.parent) + os.pathsep + env['PATH']
            subprocess.run([str(CL), '/nologo', '/c', '/Fo' + str(obj), str(source)],
                           cwd=tmp, env=env, capture_output=True, check=True)
            e = {'sym': '_ptr', 'name': 'ptr', 'va': 4096, 'section': '.data',
                 'size': 4, 'fields': [[0]]}
            manifest = p / 'manifest.json'
            def load(path):
                manifest.write_text(json.dumps({'entries': [e]}), encoding='utf-8')
                return splice.load(str(manifest), str(path))
            self.assertEqual(len(load(obj)[0]['relocs']), 1)
            e['size'] = 2
            with self.assertRaisesRegex(ValueError, 'crosses end'):
                load(obj)
            c = splice.Coff(str(obj))
            raw = bytearray(obj.read_bytes())
            symptr = struct.unpack_from('<I', raw, 8)[0]
            ix = next(i for i, symbol in c.symbols.items() if symbol['name'] == '_ptr')
            struct.pack_into('<I', raw, symptr + 18 * ix + 8, 1)
            shifted = p / 'shifted.obj'
            shifted.write_bytes(raw)
            e.update(size=3, align=1, fields=[])
            with self.assertRaisesRegex(ValueError, 'crosses start'):
                load(shifted)

    def test_cross_source_range_claims(self):
        records = [{'va': 0x1000, 'data': bytes(8)},
                   {'va': 0x1008, 'data': bytes(8)}]
        splice.validate_records(records)
        records[1]['va'] = 0x1004
        with self.assertRaisesRegex(ValueError, 'overlapping overlay'):
            splice.validate_records(records)
        claims = splice.RangeClaims()
        claims.add(0x1008, 8)
        with self.assertRaisesRegex(ValueError, 'overlapping overlay'):
            claims.add(0x1004, 8)

    def test_overlapping_relocation_cells(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            src = p / 'reloc.cpp'
            src.write_text('extern "C" { extern int M3D_00002000; int *ptr[2] = {&M3D_00002000, &M3D_00002000}; }', encoding='utf-8')
            obj = p / 'reloc.obj'
            env = os.environ.copy()
            env['PATH'] = str(CL.parent) + os.pathsep + env['PATH']
            subprocess.run([str(CL), '/nologo', '/c', '/Fo' + str(obj), str(src)],
                           cwd=tmp, env=env, capture_output=True, check=True)
            e = {'sym': '_ptr', 'name': 'ptr', 'va': 4096, 'section': '.data',
                 'size': 8, 'fields': [[0], [4]]}
            manifest = p / 'manifest.json'
            def load(path):
                manifest.write_text(json.dumps({'entries': [e]}), encoding='utf-8')
                return splice.load(str(manifest), str(path))
            self.assertEqual(len(load(obj)[0]['relocs']), 2)
            c = splice.Coff(str(obj))
            section = c.named('_ptr')['section']
            raw = bytearray(obj.read_bytes())
            relptr = struct.unpack_from('<I', raw, 20 + (section - 1) * 40 + 24)[0]
            struct.pack_into('<I', raw, relptr + 10, 1)
            modified = p / 'overlap.obj'
            modified.write_bytes(raw)
            e['fields'] = [[0], [1]]
            with self.assertRaisesRegex(ValueError, 'overlapping DIR32'):
                load(modified)

    def test_backed_sections_and_rawless_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pathlib.Path(tmp)
            source = p / 'fixture.cpp'
            source.write_text('''#pragma section(".data", read, write)
#pragma section(".rdata", read)
extern "C" {
__declspec(allocate(".data")) __declspec(align(4)) unsigned char rw_zero[16] = {0};
extern __declspec(allocate(".rdata")) __declspec(align(4)) const unsigned char ro_zero[16] = {0};
__declspec(align(4)) unsigned char bss_zero[16] = {0};
}
''', encoding='utf-8')
            obj = p / 'fixture.obj'
            env = os.environ.copy()
            env['PATH'] = str(CL.parent) + os.pathsep + env['PATH']
            subprocess.run([str(CL), '/nologo', '/c', '/Fo' + str(obj), str(source)],
                           cwd=tmp, env=env, capture_output=True, check=True)
            def load(symbol, section, path):
                entry = {'sym': symbol, 'name': symbol, 'va': 4096, 'section': section,
                         'size': 16, 'align': 4, 'fields': []}
                manifest = p / 'manifest.json'
                manifest.write_text(json.dumps({'entries': [entry]}), encoding='utf-8')
                return splice.load(str(manifest), str(path))
            for sym, section in [('_rw_zero', '.data'), ('_ro_zero', '.rdata')]:
                self.assertEqual(load(sym, section, obj)[0]['data'], bytes(16))
            with self.assertRaisesRegex(ValueError, 'not backed by object file bytes'):
                load('_bss_zero', '.bss', obj)
            # Exercise the public placement-record adapter against the same real object.
            entries = [
                {'sym': '_rw_zero', 'name': 'rw_zero', 'va': 4096, 'section': '.data',
                 'size': 16, 'align': 4, 'fields': []},
                {'sym': '_ro_zero', 'name': 'ro_zero', 'va': 4112, 'section': '.rdata',
                 'size': 16, 'align': 4, 'fields': []},
            ]
            manifest = p / 'placement.json'
            manifest.write_text(json.dumps({'entries': entries}), encoding='utf-8')
            with mock.patch.object(splice, 'MANIFEST', str(manifest)), mock.patch.object(splice, 'OBJ', str(obj)):
                units = m3secs.m3_units()
                self.assertEqual(units, {m3secs.UID: {'idx': m3secs.UID, 'err': None, 'secs': [
                    {'u': m3secs.UID, 'k': i, 'name': e['section'],
                     'flags': m3secs.FLAGS[e['section']] | m3secs.ALIGN[4],
                     'data': bytes(16), 'size': 16, 'relocs': [],
                     'defs': [('m3$' + e['name'], 0, 2)],
                     'hints': [(e['va'], 'm3-name', 'm3$' + e['name'])],
                     'forced': e['va'], 'kind0': 'm3-global'}
                    for i, e in enumerate(entries)]}})
                manifest.write_text(json.dumps({'entries': [dict(entries[0], sym='_bss_zero', section='.bss')]}), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'not backed by object file bytes'):
                    m3secs.m3_units()
            with self.assertRaisesRegex(ValueError, 'invalid M3 destination alignment'):
                e = {'sym': '_rw_zero', 'name': 'unaligned', 'va': 4097, 'section': '.data',
                     'size': 16, 'align': 4, 'fields': []}
                bad_manifest = p / 'unaligned.json'
                bad_manifest.write_text(json.dumps({'entries': [e]}), encoding='utf-8')
                splice.load(str(bad_manifest), str(obj))
            entry = {'sym': '_rw_zero', 'name': 'one', 'va': 4096, 'section': '.data',
                     'size': 16, 'align': 4, 'fields': []}
            duplicate = dict(entry, name='two', va=4100)
            manifest = p / 'overlap.json'
            manifest.write_text(json.dumps({'entries': [entry, duplicate]}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'overlapping M3 ranges'):
                splice.load(str(manifest), str(obj))
            c = splice.Coff(str(obj))
            header = 20 + (c.named('_bss_zero')['section'] - 1) * 40
            raw = bytearray(obj.read_bytes())
            raw[header:header + 8] = b'.data\0\0\0'
            forged = p / 'rawless.obj'
            forged.write_bytes(raw)
            with self.assertRaisesRegex(ValueError, 'not backed by object file bytes'):
                load('_bss_zero', '.data', forged)
            # Even an initialized flag cannot substitute for a raw-data pointer.
            flags = struct.unpack_from('<I', raw, header + 36)[0]
            struct.pack_into('<I', raw, header + 36, (flags & ~0x80) | 0x40)
            forged.write_bytes(raw)
            with self.assertRaisesRegex(ValueError, 'not backed by object file bytes'):
                load('_bss_zero', '.data', forged)


if __name__ == '__main__':
    unittest.main()
