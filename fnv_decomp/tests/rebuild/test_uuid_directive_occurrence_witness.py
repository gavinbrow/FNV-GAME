"""Authored fixtures only: no original object, native read or selected library."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[2] / 'tools/rebuild/uuid_directive_occurrence_witness.py'
spec = importlib.util.spec_from_file_location('uuid_witness', PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture(address='0x0045b020'):
    root = dict(original_address=address, **{k:v for k,v in m.ROOTS[address].items() if k != 'certificate_sha256'})
    native = {k:root[k] for k in m.ROOT_FIELDS}
    contract = dict(recipe_id=root['recipe_id'], roots=[native], provenance={k:root[k] for k in
                    ('recipe_id','recipe_index','object_sha256','source_sha256')})
    blockers = [dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=m.UUID,blocker_id=m.UUID_ID),
                dict(code='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE',evidence=m.UUID,blocker_id=m.UUID_ID),
                dict(code='DIRECTIVE_CONTRACT_DIFFERS',evidence=copy.deepcopy(m.TOKENS),blocker_id=m.DIFF_ID)]
    base = dict(recipe_id=root['recipe_id'],roots=[native],contract_identity_sha256=m.digest(contract),
                closure_observed=False,graph_observation_complete=False,root_closure_candidate=False,blockers=blockers)
    payload = b' '.join(s.encode() for s in m.TOKENS)
    payload += b' ' * (93-len(payload))
    header = dict(index=1,name='.drectve',size=93,flags=0x100a00,virtual_size=0,virtual_address=0,object_size=10000,raw_data_offset=8000,section_count=150,optional_header_size=0,
                  relocation_count=0,relocation_pointer=0,line_number_count=0,line_number_pointer=0)
    binding = dict(kind='bound-normal-sdk-search-candidate',library_name='uuid.lib',path='fixture/uuid.lib',
                   sha256='1'*64,candidate_manifest_path='fixture/candidate.json',candidate_manifest_sha256='2'*64)
    args = [root,contract,base,payload,header,binding,{}]
    repin(args)
    return args


def repin(a):
    root, contract, base, raw, header, binding, _ = a
    a[6] = dict(root_sha256=m.digest(root),contract_sha256=m.digest(contract),certificate_sha256=m.digest(base),
                section_sha256=hashlib.sha256(raw).hexdigest(),header_sha256=m.digest(header),binding_sha256=m.digest(binding),
                candidate_manifest_path=binding['candidate_manifest_path'],
                candidate_manifest_sha256=binding['candidate_manifest_sha256'])


def call(a, fixture_certificate=None):
    # Patch only the immutable real-certificate pin for synthetic certificates.
    # Never patches the two actual root identities and never reads actual inputs.
    address = a[0]['original_address']
    fake = dict(m.ROOTS[address],certificate_sha256=fixture_certificate or m.digest(a[2]))
    with patch.dict(m.ROOTS,{address:fake}):
        return m.assess(*a)


class WitnessTests(unittest.TestCase):
    def test_both_roots_and_exact_occurrences(self):
        for addr in m.ROOTS:
            a=fixture(addr); before=copy.deepcopy(a); w=call(a)
            self.assertEqual(a,before)
            self.assertEqual([x['ordinal'] for x in w['proposed_blocker_occurrences']],[1,2,3])
            self.assertEqual([x['blocker_id'] for x in w['proposed_blocker_occurrences']],[m.UUID_ID,m.UUID_ID,m.DIFF_ID])
            self.assertEqual([x['directive_ordinals'] for x in w['proposed_blocker_occurrences']],[[1],[2],[1,2,3,4]])
            self.assertLessEqual(w['directive_occurrences'][0]['end'],w['directive_occurrences'][1]['start'])
            self.assertEqual(bytes.fromhex(w['raw_section_hex']),a[3])
            for k in ('provider_selected','runtime_eligible','ABI_verified','admission_approved','ordinary_graph_closure',
                      'native_tools_run','certificate_rewritten','object_write_performed','duplicate_linker_semantics_proved',
                      'library_request_proved','library_selection_proved','library_loaded_proved'):
                self.assertIs(w[k],False)

    def rejected(self, change, *, rebind=True):
        a=fixture(); change(a)
        if rebind: repin(a)
        with self.assertRaises((ValueError,TypeError,KeyError)): call(a)

    def test_missing_duplicate_occurrence(self):
        self.rejected(lambda a:a[2]['blockers'].pop(1))
    def test_extra_duplicate_occurrence(self):
        self.rejected(lambda a:a[2]['blockers'].insert(1,copy.deepcopy(a[2]['blockers'][0])))
    def test_non_uuid_occurrence_or_reordered(self):
        self.rejected(lambda a:a[2]['blockers'].reverse())
        self.rejected(lambda a:a[2]['blockers'][1].__setitem__('evidence','other'))
    def test_unsupported_directives_and_literal_variations(self):
        variants=[b'/INCLUDE:x',b'/FORCE',b'/NODEFAULTLIB',b'/alternatename:a=b',b'/TLS',b'/defaultlib:"uuid.lib"',b'\0',b'\xff']
        for bad in variants:
            def change(a):
                p=bad+b' '+b' '.join(x.encode() for x in m.TOKENS)
                a[3]=(p+b' '*93)[:93]
            self.rejected(change)
    def test_duplicate_missing_extra_reordered_or_changed_raw(self):
        for seq in ([m.UUID,m.TOKENS[2],m.TOKENS[3]], [m.UUID]*3+m.TOKENS[2:],
                    [m.UUID,m.TOKENS[2],m.UUID,m.TOKENS[3]], [m.UUID,m.UUID,m.TOKENS[2],'/DEFAULTLIB:"oldnames"']):
            def change(a):
                p=b' '.join(x.encode() for x in seq); a[3]=(p+b' '*93)[:93]
            self.rejected(change)
    def test_header_and_type_rejections(self):
        for key,value in [('size',92),('index',True),('flags',0),('virtual_size',1),('virtual_address',1),('object_size',300),('section_count',0),('section_count',31),('section_count',65536),('section_count',201),('optional_header_size',1),('relocation_count',1),('relocation_pointer',5),
                          ('line_number_count',1),('line_number_pointer',4),('raw_data_offset',1),('name','.tls')]:
            self.rejected(lambda a,k=key,v=value:a[4].__setitem__(k,v))
    def test_binding_constraints(self):
        for key,value in [('kind','dll'),('kind','already-selected-normal-static-library'),('library_name','UUID.LIB'),('path',''),('path','x/uuid.dll'),('path','x/other.lib'),('path','x/uuid.lib\0'),('candidate_manifest_path','a\nb'),('sha256','fake')]:
            self.rejected(lambda a,k=key,v=value:a[5].__setitem__(k,v))
    def test_each_pinned_fact_drift(self):
        for index,key in [(0,'source_sha256'),(1,'recipe_id'),(2,'recipe_id'),(4,'raw_data_offset'),(5,'path')]:
            a=fixture(); trusted=m.digest(a[2]); a[index][key]='drift'
            with self.assertRaises((ValueError,TypeError,KeyError)): call(a,trusted)
        a=fixture(); a[3]=b'\t'+a[3][1:]
        with self.assertRaises(ValueError):call(a)
    def test_manifest_path_or_hash_drift(self):
        for key in ('candidate_manifest_path','candidate_manifest_sha256','binding_sha256'):
            a=fixture(); a[6][key]='3'*64
            with self.assertRaises(ValueError):call(a)
    def test_certificate_and_contract_mismatch(self):
        a=fixture(); old=m.digest(a[2]); a[2]['other']='drift'; repin(a)
        with self.assertRaises(ValueError):call(a,old)
        self.rejected(lambda a:a[2].__setitem__('contract_identity_sha256','0'*64))
    def test_false_approvals_and_bool_counts(self):
        for key in ('closure_observed','graph_observation_complete','root_closure_candidate'):
            self.rejected(lambda a,k=key:a[2].__setitem__(k,True))
        self.rejected(lambda a:a[4].__setitem__('relocation_count',False))
        self.rejected(lambda a:a[0].__setitem__('recipe_index',True))


if __name__ == '__main__': unittest.main()
