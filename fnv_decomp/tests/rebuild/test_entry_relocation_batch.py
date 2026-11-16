"""Nineteen fixed source transforms and synthetic metadata; no native compiler."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import entry_relocation_batch as batch
from coff_inventory import Coff


def recipe(owner):
    selected = owner['original_selected_owner']
    return dict(functions=[dict(address=owner['function_va'],symbol=selected['symbol'],size=selected['size'])]+[
        f['target_function'] for f in owner['fields'] if 'target_function' in f],
        symbols={f['proposed_target_symbol']:f['target_va'] for f in owner['fields'] if 'target_function' not in f})


def fixture(owner, overlay=False, *, changed_byte=False, wrong_addend=False, wrong_kind=False,
            wrong_target=False, duplicate=False, data_defined=False, code_undefined=False, old_reference_changed=False,
            extra_relocation=False, wrong_code_section=False):
    selected = owner['original_selected_owner']; section = selected['section']; size = selected['size']
    targets = {f['proposed_target_symbol']:f for f in owner['fields']}
    definitions = {name:f for name,f in targets.items() if 'target_function' in f}
    code_sections = {name:section+i+1 for i,name in enumerate(definitions)}
    count = section+len(code_sections)
    code = bytearray(b'\x90'*size); struct.pack_into('<I',code,1,0)
    names = [selected['symbol'],'_unchanged_base']+list(targets)
    if duplicate:names.append(names[-1])
    relocs = [(1,1,6 if old_reference_changed else 20)]
    for f in owner['fields']:
        off = f['function_offset']; struct.pack_into('<I',code,off,4 if overlay and wrong_addend else 0 if overlay else int(f['target_va'],16))
        if overlay: relocs.append((off,names.index(f['proposed_target_symbol']),20 if wrong_kind else 6))
    if changed_byte:code[-1] ^= 1
    if extra_relocation:relocs.append((6,1,20))
    records=bytearray(); strings=bytearray(struct.pack('<I',4))
    for idx,name in enumerate(names):
        symbol_section = section if idx == 0 else code_sections.get(name,0)
        if data_defined and name in targets and name not in definitions:symbol_section=section
        if code_undefined and name in definitions:symbol_section=0
        if wrong_code_section and name in definitions:symbol_section=section
        encoded = ('_wrong_'+name if wrong_target and name in targets else name).encode()
        offset=len(strings); strings.extend(encoded+b'\0')
        typ=32 if idx == 0 or name in definitions else 0
        records.extend(struct.pack('<IIIhHBB',0,offset,0,symbol_section,typ,2,0))
    struct.pack_into('<I',strings,0,len(strings))
    pointer=20+count*40; headers=[]; payload=bytearray()
    for idx in range(1,count+1):
        data=code if idx == section else b'\x90'*next((f['target_function']['size'] for n,f in definitions.items() if code_sections[n]==idx),0)
        refs=relocs if idx == section else []
        raw=pointer+len(payload); payload.extend(data)
        relptr=pointer+len(payload); payload.extend(b''.join(struct.pack('<IIH',*r) for r in refs))
        headers.append(struct.pack('<8sIIIIIIHHI',b'.text',0,0,len(data),raw,relptr,0,len(refs),0,0x60000020))
    return struct.pack('<HHIIIHH',0x14c,count,0,pointer+len(payload),len(names),0,0)+b''.join(headers)+payload+records+strings


class BatchTests(unittest.TestCase):
    def setUp(self):self.policy=batch.policy();self.units=self.policy['units']

    def test_fixed_census_and_exact_declaration_source_reversal(self):
        self.assertEqual(len(self.units),6)
        self.assertEqual(sum(len(u['owners']) for u in self.units),10)
        self.assertEqual(sum(len(o['fields']) for u in self.units for o in u['owners']),19)
        self.assertEqual(sum(u['expected_complete_function_rows'] for u in self.units),619)
        for u in self.units:
            raw=(batch.ROOT/u['source']).read_bytes(); new=batch.transform(raw,u)
            self.assertEqual(new.count(b'\n'),raw.count(b'\n'))
            self.assertEqual(new.count(b'\r\n'),raw.count(b'\r\n'))
            # Reverse each edit using the known cumulative byte displacement.
            shift=0; spans=[]
            for e in sorted(u['edits'],key=lambda e:e['byte_offset']):
                spans.append((e['byte_offset']+shift,e));shift+=len(e['new'].encode())-len(e['old'].encode())
            for start,e in reversed(spans):new=new[:start]+e['old'].encode()+new[start+len(e['new'].encode()):]
            self.assertEqual(new,raw)

    def test_unauthorized_declaration_namespace_cast_or_header_scope_rejected(self):
        for path in ('declaration','cast','namespace','header'):
            u=copy.deepcopy(self.units[0]); raw=(batch.ROOT/u['source']).read_bytes()
            if path=='header':u['headers'].append(dict(path='invented.h'))
            elif path=='declaration':u['edits'][0]['new']=u['edits'][0]['new'].replace('__cdecl','__stdcall')
            elif path=='namespace':u['edits'][0]['new']='namespace invented {}\r\n'
            else:u['edits'][-1]['new']='unsigned int invented=0;\r\n'
            with self.assertRaisesRegex(ValueError,'unauthorized'):batch.transform(raw,u)

    def test_stale_comment_only_or_duplicate_source_rejected(self):
        for u in self.units:
            raw=(batch.ROOT/u['source']).read_bytes()
            old=u['edits'][-1]['old'].encode()
            for changed in (raw+b'\r\n',raw.replace(old,b'// '+old,1),raw+old):
                with self.assertRaises(ValueError):batch.transform(changed,u)

    def test_all_nineteen_dir32_and_ten_nonfield_spans(self):
        with tempfile.TemporaryDirectory() as td:
            before,after=Path(td)/'before.obj',Path(td)/'after.obj'
            for u in self.units:
                for o in u['owners']:
                    before.write_bytes(fixture(o));after.write_bytes(fixture(o,True))
                    proof=batch.verify_owner(Coff(before),Coff(after),o,recipe(o))
                    self.assertEqual(len(proof['migrations']),len(o['fields']))
                    self.assertTrue(proof['non_field_bytes_equal'])

    def test_wrong_kind_addend_target_and_other_behavior_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            before,after=Path(td)/'before.obj',Path(td)/'after.obj'
            for u in self.units:
                for o in u['owners']:
                    before.write_bytes(fixture(o))
                    for kwargs in [dict(wrong_kind=True),dict(wrong_addend=True),dict(wrong_target=True),dict(changed_byte=True),dict(old_reference_changed=True),dict(duplicate=True),dict(extra_relocation=True)]:
                        after.write_bytes(fixture(o,True,**kwargs))
                        with self.assertRaises(ValueError):batch.verify_owner(Coff(before),Coff(after),o,recipe(o))

    def test_data_cannot_be_defined_and_code_cannot_be_undefined(self):
        with tempfile.TemporaryDirectory() as td:
            before,after=Path(td)/'before.obj',Path(td)/'after.obj'
            for u in self.units:
                for o in u['owners']:
                    before.write_bytes(fixture(o));kind='code_undefined' if 'target_function' in o['fields'][0] else 'data_defined'
                    after.write_bytes(fixture(o,True,**{kind:True}))
                    with self.assertRaises(ValueError):batch.verify_owner(Coff(before),Coff(after),o,recipe(o))
                    if kind=='code_undefined':
                        after.write_bytes(fixture(o,True,wrong_code_section=True))
                        with self.assertRaises(ValueError):batch.verify_owner(Coff(before),Coff(after),o,recipe(o))

    def test_complete_rows_and_all_ten_owner_extents(self):
        recipes=json.loads((batch.ROOT/'build/units.json').read_text())['units']
        total=0
        for u in self.units:
            r=recipes[u['recipe_index']]
            rows=[dict(f,verdict='match',compiled_extent=f['size']) for f in r['functions']]
            total+=len(rows)
            batch.complete_matches(rows,r,u['owners'])
            target=u['owners'][0]['original_selected_owner']['symbol']
            for bad in (rows[:-1],rows+rows[:1],[dict(f,verdict='mismatch') if i==0 else f for i,f in enumerate(rows)],
                        [dict(f,compiled_extent=f['size']+1) if f['symbol']==target else f for f in rows]):
                with self.assertRaises(ValueError):batch.complete_matches(bad,r,u['owners'])
        self.assertEqual(total,619)

    def test_missing_migrations_preserve_unrepaired_fields_and_fresh_binding(self):
        for u in self.units:
            old=[];new=[]
            for o in u['owners']:
                for f in o['fields']:
                    common=dict(function_va=o['function_va'],source_field_offset=f['function_offset'])
                    old.append(dict(common,event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER'))
                    new.append(dict(common,event='SELECTED_FUNCTION_COFF_RELOCATION',coff_relocation=dict(kind=6,symbol=f['proposed_target_symbol']),exact_original_target_va=f['target_va'],proof_consistency='EXACT_OWN_SOURCE_RESOLUTION'))
            unresolved=dict(function_va=u['owners'][0]['function_va'],source_field_offset=99999,event='MISSING_ORIGINAL_HIGHLOW_SOURCE_MIGRATION_BLOCKER')
            old.append(unresolved);new.append(unresolved)
            self.assertEqual(batch.migrations_match(old,new,u)['overlay_missing_count'],1)
            for changed in (new[:-1],new[1:], [dict(x,exact_original_target_va='0x00000000') if i==0 else x for i,x in enumerate(new)]):
                with self.assertRaises(ValueError):batch.migrations_match(old,changed,u)


if __name__=='__main__':unittest.main()
