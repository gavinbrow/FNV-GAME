"""Synthetic strict Kernel15/Steam-exclusion preparation; no native inputs or calls."""
import copy
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parents[1]/'tools/rebuild'))
import import_kernel32_fifteen as p
from test_assess_v10_imports import fixture as source_fixture


def fixture():
    catalog,fields,groups,native,inventory=source_fixture()
    cells=p.imports.catalog(catalog)
    for i,alias in enumerate(native['proposed_pointer_aliases']):
        alias.update(canonical_IAT_symbol=cells[alias['original_IAT_va']]['canonical_IAT_symbol'],
            member_offset=1000+100*i,pointer_indirection_preserved=True,alias_applied=False,
            source_ABI_approved=False,runtime_provider_adopted=False,
            library='kernel32-twelve.lib' if alias['dll']=='KERNEL32.dll' else 'old.lib')
    native.update(kind='fnv-v8-four-import-successor-native-collection',schema_version=1,**p.FALSE_FLAGS)
    for row in native['libraries']:
        if row['file']=='user32-sixteen.lib':row.update(sha256=p.UNCHANGED[0][1],bytes=p.UNCHANGED[0][2])
    for row in native['unchanged_libraries']:
        for name,h,size in p.UNCHANGED:
            if row['library']==name:row['sha256']=h
    assessment,definition=p.assessment_tool.assess(catalog,fields,groups,native,inventory)
    review=dict(kind='v10-import-assessment-independent-outcome-review',schema_version=1,
        status='accepted_metadata_only',assessment_sha256=p.PINS['assessment'])
    return catalog,assessment,review,native,fields,groups


def request_parse():
    data=fixture();request,definition=p.prepare(*data[:4]);request.update(inputs=dict(assessment_sha256='a'*64),source_sha256=dict(tool='b'*64))
    parsed=dict(both_indexes_agree=True,ordinary_members=[{}]*3,archive_sha256='c'*64,archive_bytes=4096,
        imports=[dict(dll=c['dll'],export=c['export'],machine=0x14c,import_type=0,symbol='_'+c['export']['name'],
            pointer_symbol='__imp__'+c['export']['name'],member_offset=1000+120*i) for i,c in enumerate(request['cells'])])
    return request,parsed


class Kernel15Tests(unittest.TestCase):
    def test_strict_win32_superset_preserves_old31_and_steam_blockers(self):
        data=fixture();before=copy.deepcopy(data[:4]);request,definition=p.prepare(*data[:4])
        self.assertEqual(data[:4],before)
        self.assertEqual(len(request['cells']),15);self.assertEqual(len(request['prior_pointer_aliases']),31)
        self.assertEqual(len(request['unchanged_libraries']),3)
        self.assertNotIn(b'Steam',definition);self.assertTrue(request['Steam_remains_unaliased'])
        self.assertFalse(request['Steam_native_library_proposed'])
        self.assertEqual(len(request['Steam_inventory_context']['provider_blockers']),3)
        self.assertEqual(sum(r['complete_V10_use_count'] for r in request['new_kernel32_all_use_censuses']),22)

    def test_full45947_evidence_replay_and_tamper_rejection(self):
        catalog,assessment,review,native,fields,groups=fixture()
        result=p.validate_fields(assessment,fields,groups,catalog,native)
        self.assertIn(b'    EnterCriticalSection\n',result)
        fields[0]['proof']['addend_bits']=4
        with self.assertRaisesRegex(ValueError,'replay differs'):p.validate_fields(assessment,fields,groups,catalog,native)

    def test_partial_kernel_eligibility_or_steam_promotion_rejected(self):
        data=fixture();data[1]['eligible_kernel32_cells'].pop()
        with self.assertRaises(ValueError):p.prepare(*data[:4])
        data=fixture();next(r for r in data[1]['per_cell_censuses'] if r['original_IAT_va']==p.assessment_tool.STEAM_CELL)['native_library_proposed']=True
        with self.assertRaisesRegex(ValueError,'Steam'):p.prepare(*data[:4])

    def test_native_join34_has_no_steam_and_all_flags_false(self):
        request,parsed=request_parse();result=p.reconcile(request,parsed,'d'*64)
        self.assertEqual(len(result['proposed_pointer_aliases']),34)
        self.assertTrue(result['old_31_pointer_identities_preserved'])
        self.assertTrue(result['replacement_identity_verified'])
        self.assertFalse(any(a['dll']=='steam_api.dll' for a in result['proposed_pointer_aliases']))
        for flag in p.FALSE_FLAGS:self.assertIs(result[flag],False)

    def test_old_pointer_change_bad_archive_or_steam_substitution_rejected(self):
        for change in ('pointer','machine','missing','steam','promotion'):
            request,parsed=request_parse();item=parsed['imports'][0]
            if change=='pointer':item.update(symbol='_Wrong',pointer_symbol='__imp__Wrong')
            if change=='machine':item['machine']=0x8664
            if change=='missing':parsed['imports'].pop()
            if change=='steam':request['cells'][0]['dll']='steam_api.dll'
            if change=='promotion':request['prior_pointer_aliases'][15]['runtime_provider_adopted']=True
            with self.subTest(change=change),self.assertRaises(ValueError):p.reconcile(request,parsed,'d'*64)

    def test_private_output_gate_precedes_reads(self):
        args=type('Args',(),dict(out=p.ROOT/'src'/'wrong-output'))()
        with self.assertRaisesRegex(ValueError,'private output'):p.run(args)


if __name__=='__main__':unittest.main()
