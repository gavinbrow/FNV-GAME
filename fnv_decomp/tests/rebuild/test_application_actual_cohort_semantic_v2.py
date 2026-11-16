"""V2 semantic join tests using authored COFF bytes only."""
import copy, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import application_actual_cohort_semantic_v2 as v2
from test_application_link_cohort import obj, mapped_args


def fixture():
    args=mapped_args(); raw=obj(); root=args['roots'][0]
    root.update(recipe_id='fixture', object_sha256='a'*64)
    full=dict(recipe_id='fixture', function_va=root['original_address'], physical_section=7,
              physical_offset=4, coff_relocation=dict(offset=4, kind=6, symbol_index=11, addend=0))
    compact=dict(section=7,offset=4,symbol_index=11,kind=6,field_proof_sha256=v2.ledger.digest(full),
                 original_base='0x02000000',original_target='0x02000000', addend_bits=0,
                 role='data', canonical_name='target')
    authority={'record_sha256':'auth'}
    common=dict(authority=authority,certificate_sha256='cert',contract_identity_sha256='contract',central_record_sha256='central')
    p=dict(requested_roots=[root], original_object_sha256=root['object_sha256'], output_sha256=v2.cohort.digest(raw),
           fields=[compact], maps=args['maps'], exports=['root'], **common)
    wrapper=dict(schema_version=1,source_evidence_enriched=False,member='original.obj',requested_root=root,
                 output_object_sha256=p['output_sha256'],fields=[full],fields_sha256=v2.ledger.digest([full]),**common)
    record=dict(member='original.obj',root=root,member_sha256=p['output_sha256'],field_proof_ordinal=1,
                field_proof_record_sha256=v2.ledger.digest(wrapper),original_fields_sha256=wrapper['fields_sha256'],fields=1,**common)
    args['obligations']=[dict(compact,physical_section=7,field_offset=4)]
    providers,fields=v2.cohort.mapped_member(raw,**args)
    return dict(wrappers=[wrapper],members=[dict(name='original.obj',projection=p)],handoff={'records':[record]},
                member_count=1,field_count=1,member_bytes={'original.obj':raw},
                namespace_by_member={'original.obj':args['namespace']},expected_providers=providers,
                expected_fields=fields,component='synthetic')


class Tests(unittest.TestCase):
    def test_authored_coff_derives_exact_records(self):
        result=v2.derive(**fixture()); self.assertFalse(result['link_approved'])

    def test_unrelated_provider_and_field_rejected(self):
        for which in ('provider','field'):
            f=copy.deepcopy(fixture())
            if which=='provider': f['expected_providers'][0]['object_sha256']='unrelated'
            else: f['expected_fields'][0]['canonical']='unrelated'
            with self.subTest(which=which), self.assertRaises(ValueError): v2.derive(**f)

    def test_physical_bytes_namespace_and_target_must_match(self):
        for which in ('bytes','namespace','proof'):
            f=copy.deepcopy(fixture())
            if which=='bytes': f['member_bytes']['original.obj']+=b'changed'
            elif which=='namespace': f['namespace_by_member']['original.obj'][1]['name']='wrong'
            else: f['members'][0]['projection']['fields'][0]['addend_bits']=99
            with self.subTest(which=which), self.assertRaises(ValueError): v2.derive(**f)

    def test_missing_member_even_without_fields_rejected(self):
        f=fixture(); del f['member_bytes']['original.obj']
        with self.assertRaises(ValueError): v2.derive(**f)


if __name__=='__main__': unittest.main()
