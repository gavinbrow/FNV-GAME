"""V6 semantic join tests using authored COFF bytes only."""
import copy, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import application_actual_cohort_semantic_v6 as v2
from test_application_link_cohort import obj, mapped_args


def fixture():
    args=mapped_args(); name=v2.pool.unresolved('0x02000000','data'); raw=v2.cohort.coff.namespace(obj(),[(1,name)]); root=args['roots'][0]
    args['namespace'][1]['name']=name
    root.update(recipe_id='fixture', object_sha256='a'*64, recipe_index=1, symbol='root')
    full=dict(recipe_id='fixture', function_va=root['original_address'], physical_section=7,
              physical_offset=4, physical_field_overlap_count=1, classification='ORIGINAL_IMAGE_DATA_REQUIRES_CANONICAL_OWNER', code_owners=[], code_ownership_ambiguous=False, expected_original_target_va='0x02000000', exact_original_target_va='0x02000000', derived_source_symbol_base_va='0x02000000', source_resolution_basis='OWN_RECIPE_BINDING',
              proof_consistency='EXACT_OWN_SOURCE_RESOLUTION', function_symbol='root', recipe_index=1,
              source_field_offset=4, original_field_va='0x00401004', original_operand=0x02000000, coff_relocation=dict(offset=4, kind=6, symbol_index=11, addend=0, width=4, symbol_type=0))
    compact=dict(section=7,offset=4,symbol_index=11,kind=6,field_proof_sha256=v2.ledger.digest(full),
                 original_base='0x02000000',original_target='0x02000000', addend_bits=0,
                 role='data', canonical_name=name)
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
                expected_fields=fields,component='synthetic',selected_providers={})


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

    def test_target_proof_and_operand_must_match(self):
        for mode in ('target','operand','parent','base','exact_target'):
            f=copy.deepcopy(fixture()); full=f['wrappers'][0]['fields'][0]
            if mode=='target': full['expected_original_target_va']='0x99999999'
            elif mode=='operand': full['original_operand']=0x12345678
            elif mode=='base': full['derived_source_symbol_base_va']='0x99999999'
            elif mode=='exact_target': full['exact_original_target_va']='0x99999999'
            else: full['function_symbol']='other'
            compact=f['members'][0]['projection']['fields'][0]
            compact['field_proof_sha256']=v2.ledger.digest(full)
            wrapper=f['wrappers'][0]; wrapper['fields_sha256']=v2.ledger.digest(wrapper['fields'])
            record=f['handoff']['records'][0]; record['field_proof_record_sha256']=v2.ledger.digest(wrapper)
            record['original_fields_sha256']=wrapper['fields_sha256']
            with self.subTest(mode=mode), self.assertRaises(ValueError): v2.derive(**f)

    def test_overlapping_physical_relocation_rejected(self):
        f=copy.deepcopy(fixture()); wrapper=f['wrappers'][0]; full=copy.deepcopy(wrapper['fields'][0]);full['physical_offset']=5
        full['coff_relocation']['offset']=5; wrapper['fields'].append(full)
        compact=copy.deepcopy(f['members'][0]['projection']['fields'][0]);compact['offset']=5
        compact['field_proof_sha256']=v2.ledger.digest(full);f['members'][0]['projection']['fields'].append(compact)
        wrapper['fields_sha256']=v2.ledger.digest(wrapper['fields']);record=f['handoff']['records'][0]
        record['fields']=2;record['field_proof_record_sha256']=v2.ledger.digest(wrapper)
        record['original_fields_sha256']=wrapper['fields_sha256'];f['field_count']=2
        with self.assertRaisesRegex(ValueError, 'overlapping'):v2.derive(**f)

    def test_mismatched_role_classification_and_canonical_rejected(self):
        for mode in ('role','classification','canonical','ownership'):
            f=copy.deepcopy(fixture()); full=f['wrappers'][0]['fields'][0]; c=f['members'][0]['projection']['fields'][0]
            if mode=='role': c['role']='crt-contract'
            elif mode=='classification': full['classification']='EXPLICIT_NORMAL_CRT_CONTRACT_CANDIDATE'
            elif mode=='canonical': c['canonical_name']='wrong'
            else: full['code_owners']=[{'address':'0x02000000','offset':0}]
            c['field_proof_sha256']=v2.ledger.digest(full);w=f['wrappers'][0];w['fields_sha256']=v2.ledger.digest(w['fields'])
            r=f['handoff']['records'][0];r['field_proof_record_sha256']=v2.ledger.digest(w);r['original_fields_sha256']=w['fields_sha256']
            with self.subTest(mode=mode),self.assertRaises(ValueError):v2.derive(**f)


if __name__=='__main__': unittest.main()
