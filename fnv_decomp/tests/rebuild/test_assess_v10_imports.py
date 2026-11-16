"""Synthetic V10 field assessment and Steam source inventory; no binaries/native IO."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/rebuild'))
import assess_v10_imports as a


def fixture():
    records=[];aliases=[]
    for i in range(31):
        dll='KERNEL32.dll' if i<12 else 'USER32.dll' if i<28 else 'GDI32.dll' if i==28 else 'SHELL32.dll'
        identity=dict(kind='name',name='OldImport%d'%i);base='0x%08x'%(0x00402000+4*i)
        records.append(dict(import_id=1000+i,original_IAT_va=base,dll=dll,export=identity,
            representation='IAT_POINTER_CELL_NOT_FUNCTION_BODY',required_provider_contract=dict(dll=dll,export=identity,runtime_provider_selected=False)))
        aliases.append(dict(original_IAT_va=base,dll=dll,export=identity,proposed_pointer_symbol='__imp__'+identity['name']))
    fields=[];groups=[]
    for base,(iid,dll,name,count) in a.SPECS.items():
        identity=dict(kind='name',name=name);canonical=a.imports.unresolved(base,'iat-cell')
        records.append(dict(import_id=iid,original_IAT_va=base,dll=dll,export=dict(identity,hint=7),
            representation='IAT_POINTER_CELL_NOT_FUNCTION_BODY',required_provider_contract=dict(dll=dll,export=identity,runtime_provider_selected=False)))
        uses=[]
        for i in range(count):
            ordinal=len(fields)+1
            row=dict(component='synthetic',member='use-%d.obj'%ordinal,root='0x00401000',section=1,offset=4*ordinal,
                symbol_index=ordinal,kind=6,canonical=canonical,undefined=True,proof=dict(role='iat-cell',original_base=base,
                    original_target=base,addend_bits=0,classification='IAT_POINTER_CELL_NOT_FUNCTION_BODY',import_id=iid))
            fields.append(row);uses.append(copy.deepcopy(row))
        groups.append(dict(symbol=canonical,classification='IAT',original_bases=[base],included_input_provenance=uses))
    fields += [dict(component='padding',canonical='_padding',proof=dict(role='code'))]*(45947-len(fields))
    catalog=dict(kind='fnv-static-import-plan',schema_version=1,summary=dict(imports=35),imports=records,
                 runtime_closure_verified=False,game_fixups_approved=0)
    native=dict(proposed_pointer_aliases=aliases,native_library_generated=True,all_inputs_tools_sources_stable=True,
        libraries=[dict(file='kernel32-twelve.lib',sha256=a.OLD_KERNEL_SHA256,bytes=1),
                   dict(file='user32-sixteen.lib',sha256='a'*64,bytes=1)],
        unchanged_libraries=[dict(library='provider-000.lib',sha256='b'*64),dict(library='provider-002.lib',sha256='c'*64)])
    inventory=dict(source_declared_signature=dict(return_type='void',calling_convention='__cdecl',arguments=[]),
                   owned_DLL_export_verified=False,SDK_header_or_binary_ABI_verified=False)
    return catalog,fields,dict(groups=groups),native,inventory


class V10Tests(unittest.TestCase):
    def test_full_scope_all23uses_kernel15_only_and_steam_unadopted(self):
        data=fixture();before=a.digest(data[1]);result,definition=a.assess(*data)
        self.assertEqual(a.digest(data[1]),before)
        self.assertEqual([r['complete_V10_use_count'] for r in result['per_cell_censuses']],[8,13,1,1])
        self.assertTrue(result['kernel32_source_use_gate_pass'])
        self.assertEqual(result['proposed_kernel32_replacement']['new_import_count'],15)
        self.assertIn(b'    EnterCriticalSection\n',definition)
        self.assertNotIn(b'Steam',definition)
        steam=next(r for r in result['per_cell_censuses'] if r['original_IAT_va']==a.STEAM_CELL)
        self.assertFalse(steam['native_library_proposed']);self.assertEqual(len(steam['provider_blockers']),3)
        self.assertIsNone(steam['native_pointer_symbol']);self.assertTrue(result['steam_remains_unaliased'])

    def test_unsafe_kernel_use_preserved_blocks_superset_not_unrelated_cells(self):
        data=fixture();data[1][0]['proof']['addend_bits']=4
        result,definition=a.assess(*data)
        self.assertIsNotNone(definition);self.assertEqual(result['proposed_kernel32_replacement']['new_import_count'],14)
        self.assertNotIn(b'    EnterCriticalSection\n',definition)
        self.assertIn(b'    LeaveCriticalSection\n',definition)
        self.assertFalse(result['kernel32_source_use_gate_pass'])
        self.assertEqual(len(result['per_cell_censuses'][0]['source_use_blockers']),1)
        self.assertTrue(result['per_cell_censuses'][1]['all_current_source_use_proofs_pass'])
        self.assertEqual(result['per_cell_censuses'][0]['complete_use_records'][0]['census_view_row']['proof']['addend_bits'],4)

    def test_missing_full_scope_or_diagnostic_use_rejected(self):
        data=fixture();data[1].pop()
        with self.assertRaisesRegex(ValueError,'complete V10'):a.assess(*data)
        data=fixture();data[2]['groups'][0]['included_input_provenance'].pop()
        result,definition=a.assess(*data)
        self.assertFalse(result['per_cell_censuses'][0]['all_current_source_use_proofs_pass'])
        self.assertTrue(result['per_cell_censuses'][1]['all_current_source_use_proofs_pass'])
        self.assertEqual(result['proposed_kernel32_replacement']['new_import_count'],14)

    def test_canonical_base_target_union_catches_hidden_domain_use(self):
        data=fixture();base=next(iter(a.SPECS))
        extra=copy.deepcopy(data[1][0]);extra.update(component='extra',canonical='_other')
        extra['proof']['role']='data';data[1][-1]=extra
        result,definition=a.assess(*data)
        self.assertEqual(result['per_cell_censuses'][0]['complete_V10_use_count'],9)
        self.assertEqual(result['per_cell_censuses'][0]['samebase_or_target_other_canonical_uses'],1)
        self.assertFalse(result['per_cell_censuses'][0]['all_current_source_use_proofs_pass'])
        self.assertEqual(result['proposed_kernel32_replacement']['new_import_count'],14)

    def test_source_inventory_is_declaration_only_not_vendor_binary_approval(self):
        text='// synthetic\nextern "C" __declspec(dllimport) void __cdecl SteamAPI_RunCallbacks();\n'
        recipe=dict(source='src/staging/blk_006e0000_od.cpp',compiler='sp1',flags=['/Od'])
        inventory=a.typed_source_inventory(text,recipe)
        self.assertEqual(inventory['declaration_line'],2)
        self.assertEqual(inventory['source_declared_signature']['arguments'],[])
        self.assertFalse(inventory['owned_DLL_export_verified'])
        self.assertFalse(inventory['SDK_header_or_binary_ABI_verified'])
        with self.assertRaises(ValueError):a.typed_source_inventory(text+text,recipe)
        with self.assertRaises(ValueError):a.typed_source_inventory(text.replace('__cdecl','__stdcall'),recipe)

    def test_private_output_gate_precedes_input_reads(self):
        args=type('Args',(),dict(out=a.ROOT/'src'/'private-assessment'))()
        with self.assertRaisesRegex(ValueError,'private output'):a.run(args)


if __name__=='__main__':unittest.main()
