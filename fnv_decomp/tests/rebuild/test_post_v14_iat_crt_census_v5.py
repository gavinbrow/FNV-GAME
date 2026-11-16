import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'rebuild'))
import post_v14_iat_crt_census_v5 as census


class CensusTests(unittest.TestCase):
    def fixture(self, count):
        old = census.v14.old
        base, role, export, kind = old.BINDINGS[2]
        fields = [dict(component='new', member='m', root='0x00002000', caller='f', section=1, offset=i * 4,
            canonical=old.undefined(base, role), kind=kind, physical_symbol_index=2, undefined=True,
            proof=dict(original_base=base, original_target=base, role=role, kind=kind,
                       addend_bits=0, symbol_index=2, physical_section=1), unknown={'preserve': i}) for i in range(count)]
        bindings = []
        for b, r, e, k in old.BINDINGS:
            uses = old.census(fields, b, r, k)
            bindings.append(dict(original_base=b, role=r, canonical_undefined=old.undefined(b, r),
                normal_export=e, enabled=True, fields=uses, field_count=len(uses),
                field_census_sha256=old.digest(uses)))
        source = [dict(field_sha256=census.digest(f), review_record='synthetic') for f in fields]
        validated = census.crt.validate_bindings(bindings, fields, [])
        original = old.response([dict(canonical_undefined=old.undefined(b, r), normal_export=e)
            for b, r, e, k in old.BINDINGS]).replace('\n', '\r\n').encode('ascii')
        prior = original.decode('ascii').splitlines()[:2]
        evidence = dict(source_evidence=source, bindings=bindings, validated_bindings=validated,
            tokens=census.v14.response_bytes(bindings, original).decode('ascii').splitlines(),
            inherited_tokens_to_remove=prior, alias_field_count=count)
        peer = dict(kind='post-v14-current-crt-census-peer', status='independent-review-complete',
            reviewer='synthetic-reviewer', fields_sha256=census.digest(fields), baseline_sha256=census.digest([]),
            namespace_sha256=census.digest([]), evidence_sha256=census.digest(evidence),
            source_and_namespace_reviewed=True, provider_adopted=False, runtime_ABI_approved=False,
            runtime_eligible=False, native_operation_authorized=False)
        raw = json.dumps(peer).encode()
        return dict(baseline=[], fields=fields, namespace=[], bindings=bindings, source_evidence=source,
                    prior_crt=prior, peer_bytes=raw, peer_sha256=hashlib.sha256(raw).hexdigest())

    def test_current_crt_counts_are_dynamic(self):
        for count in (0, 1, 3):
            args = self.fixture(count)
            out = census.crt_census(**args)
            self.assertEqual(count, out['alias_field_count'])
            self.assertEqual(args['prior_crt'], out['inherited_tokens_to_remove'])

    def test_missing_source_or_strong_collision_rejected(self):
        args = self.fixture(1)
        args['source_evidence'] = []
        with self.assertRaises(ValueError): census.crt_census(**args)
        args = self.fixture(1)
        args['namespace'] = [args['bindings'][2]['canonical_undefined']]
        with self.assertRaises(ValueError): census.crt_census(**args)

    def test_changed_record_and_peer_rejected(self):
        args = self.fixture(1)
        args['fields'][0]['unknown']['preserve'] = 99
        with self.assertRaises(ValueError): census.crt_census(**args)
        args = self.fixture(0)
        args['peer_bytes'] += b' '
        with self.assertRaises(ValueError): census.crt_census(**args)

    def test_baseline_is_ordered_and_duplicate_records_fail(self):
        row = {'unknown': 1}
        with self.assertRaises(ValueError): census._current([row], [{'unknown': 2}], [])
        with self.assertRaises(ValueError): census._current([], [row, copy.deepcopy(row)], [])

    def test_iat_rejects_uncovered_new_full_proof_before_replay(self):
        row = {'component': 'new', 'member': 'm', 'section': 1, 'offset': 4,
               'proof': {'role': 'iat-cell', 'field_proof_sha256': 'abc'}}
        with self.assertRaises(ValueError):
            census.iat_census(baseline=[], fields=[row], namespace=[], full_proofs={},
                              peer_bytes=b'', peer_sha256='', replay={})

    def test_crt_same_physical_field_with_different_caller_fails(self):
        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        duplicate['caller'] = 'different-caller'
        duplicate['unknown'] = {'distinct': True}
        args['fields'].append(duplicate)
        # V14's role-specific census keys on caller, so it accepts these two
        # different rows as separate uses; V3 must reject their same geometry.
        old = census.v14.old
        b, r, _, k = old.BINDINGS[2]
        self.assertEqual(2, len(old.census(args['fields'], b, r, k)))
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.crt_census(**args)

        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        duplicate['root'] = '0x00003000'
        duplicate['caller'] = 'different-caller'
        args['fields'].append(duplicate)
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.crt_census(**args)


class IATReplayTests(unittest.TestCase):
    def fixture(self, count=2, baseline_count=0):
        import application_import34_inputs as joins
        import iat_code21_annotations as annotations
        f = census.iat
        imports, proposals, libraries = [], [], {}
        for lib_no in range(4):
            libraries['lib%d' % lib_no] = dict(imports=[], index=[])
        for i in range(34):
            va = '0x%08x' % (0x1000 + 4 * i)
            export = dict(kind='name', name='Func%d' % i)
            dll = 'KERNEL32.dll'
            name = f.imports.unresolved(va, 'iat-cell')
            lib = 'lib%d' % (i % 4)
            symbol = '_Func%d' % i
            native = dict(member_offset=i, dll=dll, export=export, machine=0x14c,
                          import_type=0, name_type=2, symbol=symbol, pointer_symbol='__imp_'+symbol)
            libraries[lib]['imports'].append(native)
            libraries[lib]['index'].extend([dict(member_offset=i, symbol=symbol),
                                             dict(member_offset=i, symbol='__imp_'+symbol)])
            imports.append(dict(original_IAT_va=va, import_id=i, representation=f.CLASSIFICATION,
                dll=dll, export=export, required_provider_contract=dict(dll=dll, export=export,
                runtime_provider_selected=False)))
            proposals.append(dict(canonical_IAT_symbol=name, original_IAT_va=va, dll=dll, export=export,
                library=lib, member_offset=i, proposed_pointer_symbol='__imp_'+symbol,
                pointer_indirection_preserved=True, alias_applied=False, runtime_provider_adopted=False,
                source_ABI_approved=False))
        catalog = dict(kind='fnv-static-import-plan', schema_version=1, runtime_closure_verified=False,
                       game_fixups_approved=0, imports=imports, summary=dict(imports=34))
        fields, full_proofs = [], {}
        for i in range(count):
            va = imports[0]['original_IAT_va']; root = '0x%08x' % (0x2000 + i * 0x100)
            full = dict(coff_relocation=dict(kind=6, addend=0, width=4, symbol_index=3, offset=4),
                physical_field_overlap_count=1, physical_section=1, physical_offset=4,
                function_va=root, recipe_id='recipe', event='SELECTED_FUNCTION_COFF_RELOCATION',
                original_field_va='0x%08x' % (int(root, 16)+4), source_field_offset=4,
                classification=f.CLASSIFICATION, proof_consistency='EXACT_OWN_SOURCE_RESOLUTION',
                source_resolution_basis='OWN_RECIPE_BINDING', derived_source_symbol_base_va=va,
                exact_original_target_va=va, expected_original_target_va=va, original_operand=int(va,16),
                representation=dict(addend=0, representation='ABSOLUTE_VA_DIR32', target=int(va,16)), import_id=0)
            sha = f.digest(full); name = f.imports.unresolved(va, 'iat-cell')
            proof = dict(physical_section=1, section=1, symbol_index=3, offset=4, field_offset=4,
                kind=6, field_proof_sha256=sha, original_base=va, original_target=va,
                canonical_name=name, role='iat-cell', addend_bits=0)
            fields.append(dict(component='new', member='m%d' % i, root=root, recipe_id='recipe',
                               section=1, offset=4, kind=6, physical_symbol_index=3, canonical=name,
                               undefined=True, proof=proof, unknown='preserve'))
            full_proofs[sha] = full
        refs = {name: dict(sha256=('%064x' % (i+1)), bytes=i+1)
                for i,name in enumerate(libraries)}
        native_rows = [dict(file=name, **ref) for name,ref in refs.items()]
        reconciled = dict(library=native_rows[0], unchanged_libraries=native_rows[1:],
                          proposed_pointer_aliases=proposals)
        old = SimpleNamespace(native_evidence=lambda *args: reconciled, joins=joins)
        prior = ['/ALTERNATENAME:'+p['canonical_IAT_symbol']+'='+p['proposed_pointer_symbol'] for p in proposals]
        replay = dict(old=old, producer=None, annotations=annotations, native=None, request=None,
                      request_sha256='', parsed=None, originals=None, expected_sources=None,
                      catalog=catalog, libraries=libraries, library_refs=refs, prior_iat=prior)
        baseline = copy.deepcopy(fields[:baseline_count])
        for row in baseline:
            row['component'] = 'actual-entry'
            row['proof']['classification'] = f.CLASSIFICATION
            del full_proofs[row['proof']['field_proof_sha256']]
        fields[:baseline_count] = copy.deepcopy(baseline)
        args = dict(baseline=baseline, fields=fields, namespace=[], full_proofs=full_proofs,
                    peer_bytes=b'', peer_sha256='', replay=replay)
        # Capture computed evidence only for authoring the synthetic review; the
        # tested call below uses the real peer parser and hash-bound validation.
        with patch.object(census, '_peer') as captured:
            census.iat_census(**args)
            evidence = captured.call_args.args[-1]
        peer = dict(kind='post-v14-current-iat-census-peer', status='independent-review-complete',
            reviewer='synthetic-reviewer', fields_sha256=census.digest(fields), baseline_sha256=census.digest(baseline),
            namespace_sha256=census.digest([]), evidence_sha256=census.digest(evidence),
            source_and_namespace_reviewed=True, provider_adopted=False, runtime_ABI_approved=False,
            runtime_eligible=False, native_operation_authorized=False)
        args['peer_bytes'] = json.dumps(peer).encode()
        args['peer_sha256'] = hashlib.sha256(args['peer_bytes']).hexdigest()
        return args

    def test_positive_whole_cohort_and_dynamic_counts(self):
        for count in (0, 1, 2):
            args = self.fixture(count); before = copy.deepcopy(args['fields'])
            result = census.iat_census(**args)
            self.assertEqual(count, result['total_iat_fields'])
            self.assertEqual(count, result['rows'][0]['use_count'])
            self.assertEqual(bool(count), result['rows'][0]['enabled'])
            self.assertEqual(int(bool(count)), len(result['tokens']))
            self.assertEqual(before, args['fields'])
            self.assertEqual(before, result['rows'][0]['complete_actual_uses'])

    def test_tampered_proof_and_catalog_are_rejected(self):
        args = self.fixture(1)
        next(iter(args['full_proofs'].values()))['original_operand'] += 4
        with self.assertRaises(ValueError): census.iat_census(**args)

    def test_complete_census_includes_baseline_and_new_fields(self):
        args = self.fixture(2, baseline_count=1)
        result = census.iat_census(**args)
        self.assertEqual(2, result['rows'][0]['use_count'])
        self.assertEqual(args['fields'], result['rows'][0]['complete_actual_uses'])
        args['fields'][0]['unknown'] = 'changed'
        with self.assertRaises(ValueError): census.iat_census(**args)
        args = self.fixture(1)
        args['replay']['catalog']['imports'][0]['import_id'] = 99
        with self.assertRaises(ValueError): census.iat_census(**args)

    def test_native_pointer_identity_and_namespace_are_fail_closed(self):
        args = self.fixture(1)
        args['replay']['libraries']['lib0']['imports'][0]['pointer_symbol'] = '__imp_bad'
        with self.assertRaises(ValueError): census.iat_census(**args)  # peer-bound outcome changed
        args = self.fixture(1)
        args['namespace'] = [args['fields'][0]['canonical']]
        with self.assertRaises(ValueError): census.iat_census(**args)

    def test_evidence_omission_and_unknown_mutation_fail(self):
        args = self.fixture(2)
        args['full_proofs'].pop(next(iter(args['full_proofs'])))
        with self.assertRaises(ValueError): census.iat_census(**args)

    def test_overlapping_ranges_rejected_within_and_across_families(self):
        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        full = copy.deepcopy(next(iter(args['full_proofs'].values())))
        duplicate['offset'] = duplicate['proof']['offset'] = duplicate['proof']['field_offset'] = 5
        full['physical_offset'] = full['coff_relocation']['offset'] = 5
        full['source_field_offset'] = 5
        full['original_field_va'] = '0x00002005'
        sha = census.iat.digest(full)
        duplicate['proof']['field_proof_sha256'] = sha
        census.iat.validate_full(duplicate, full)
        args['fields'].append(duplicate)
        args['full_proofs'][sha] = full
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.iat_census(**args)

        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        base, role, _, kind = census.v14.old.BINDINGS[2]
        duplicate.update(offset=5, kind=kind, canonical=census.v14.old.undefined(base, role))
        duplicate['proof'].update(original_base=base, original_target=base, role=role, kind=kind,
                                  offset=5, field_offset=5)
        args['fields'].append(duplicate)
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.iat_census(**args)
        # Shared gate also runs when the CRT entry point is called.
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.crt_census(baseline=[], fields=args['fields'], namespace=[], bindings=[],
                              source_evidence=[], prior_crt=[], peer_bytes=b'', peer_sha256='')

        # Adjacent four-byte ranges are allowed; the separate peer gate still
        # protects against changing a previously reviewed cohort.
        duplicate['offset'] = 8
        census._disjoint_alias_ranges(args['fields'])
        args = self.fixture(1)
        args['fields'][0]['unknown'] = 'changed'
        with self.assertRaises(ValueError): census.iat_census(**args)

    def test_same_physical_iat_field_with_distinct_valid_witnesses_fails(self):
        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        full = copy.deepcopy(next(iter(args['full_proofs'].values())))
        full['extra_unknown_evidence'] = 'second witness'
        sha = census.iat.digest(full)
        duplicate['proof']['field_proof_sha256'] = sha
        args['fields'].append(duplicate)
        args['full_proofs'][sha] = full
        census.iat.validate_full(duplicate, full)
        self.assertNotEqual(census.iat.location(args['fields'][0]), census.iat.location(duplicate))
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.iat_census(**args)

        # Another source root and matching full proof cannot create a new slot
        # inside the same serialized member and section.
        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        full = copy.deepcopy(next(iter(args['full_proofs'].values())))
        duplicate['root'] = full['function_va'] = '0x00003000'
        full['original_field_va'] = '0x00003004'
        sha = census.iat.digest(full)
        duplicate['proof']['field_proof_sha256'] = sha
        args['fields'].append(duplicate)
        args['full_proofs'][sha] = full
        census.iat.validate_full(duplicate, full)
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.iat_census(**args)

        # A changed symbol index also cannot turn one physical slot into two.
        args = self.fixture(1)
        duplicate = copy.deepcopy(args['fields'][0])
        full = copy.deepcopy(next(iter(args['full_proofs'].values())))
        full['coff_relocation']['symbol_index'] = 4
        duplicate['physical_symbol_index'] = duplicate['proof']['symbol_index'] = 4
        sha = census.iat.digest(full)
        duplicate['proof']['field_proof_sha256'] = sha
        args['fields'].append(duplicate)
        args['full_proofs'][sha] = full
        census.iat.validate_full(duplicate, full)
        with self.assertRaisesRegex(ValueError, 'overlapping IAT/CRT physical fields'):
            census.iat_census(**args)


if __name__ == '__main__': unittest.main()
