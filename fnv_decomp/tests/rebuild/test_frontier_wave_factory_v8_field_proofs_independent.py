"""Original full-field evidence binding tests; authored COFF only."""
import copy
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import frontier_wave_factory_v8 as factory
import scalableordinary_root_collect as collector
import root_code_closure as ordinary
import coff_code_archive as coff
from test_scalableordinary_root_collect import fixture


def authored(field=True):
    raw,unit,proof,roots,_,_,bindings=fixture(field=field);root=roots[0]
    contract=collector.build_contract(unit,proof,[root],bindings,{},
        {k:root[k]for k in ('recipe_id','recipe_index','object_sha256','source_sha256')})
    certificate=ordinary.assess_object(coff.parse(raw),contract)
    assert certificate['closure_observed'] is True
    row=dict(event='SINGLE_ROOT_OBSERVATION',recipe_id=root['recipe_id'],requested_roots=[root],
        closure_observed=True,graph_observation_complete=True,contract=contract,certificate=certificate,
        certificate_sha256=factory.digest(certificate),contract_identity_sha256=factory.digest(contract),provenance=contract['provenance'])
    authority=dict(kind='new-frontier-v3',receipt_sha256='a'*64,ordinal=1,record_sha256=factory.digest(row),certificate_sha256=factory.digest(certificate))
    selection=dict(root=root,authority=authority)
    projection=dict(requested_roots=[root],authority=authority,central_record_sha256=factory.digest(row),
        original_object_sha256=root['object_sha256'],contract_identity_sha256=factory.digest(contract),
        certificate_sha256=factory.digest(certificate),output_sha256=coff.digest(raw),
        fields=[dict(field_proof_sha256=factory.digest(f))for f in contract['fields']])
    return row,selection,projection,raw


class IndependentFieldProofTests(unittest.TestCase):
    def test_full_original_rows_are_preserved_without_enrichment(self):
        for has_fields in (False,True):
            values=authored(has_fields);before=copy.deepcopy(values)
            result=factory.field_proof_record('authored.obj',*values)
            self.assertEqual(result['fields'],values[0]['contract']['fields'])
            self.assertEqual(result['fields_sha256'],factory.digest(result['fields']))
            self.assertEqual(result['contract_identity_sha256'],values[2]['contract_identity_sha256'])
            self.assertEqual(result['output_object_sha256'],values[2]['output_sha256'])
            self.assertFalse(result['source_evidence_enriched']);self.assertEqual(values,before)

    def test_mutated_missing_extra_or_duplicate_original_rows_are_refused(self):
        for mutation in ('source','missing','extra','duplicate'):
            values=list(authored())
            if mutation=='source':values[0]['contract']['fields'][0]['classification']='FORGED'
            elif mutation=='missing':values[2]['fields']=[]
            elif mutation=='extra':values[2]['fields'].append(dict(field_proof_sha256='e'*64))
            else:
                fields=values[0]['contract']['fields'];fields.append(copy.deepcopy(fields[0]))
                values[0]['contract_identity_sha256']=factory.digest(values[0]['contract'])
                values[0]['certificate']['contract_identity_sha256']=values[0]['contract_identity_sha256']
                values[0]['certificate_sha256']=factory.digest(values[0]['certificate'])
                values[1]['authority'].update(record_sha256=factory.digest(values[0]),certificate_sha256=values[0]['certificate_sha256'])
                values[2].update(central_record_sha256=factory.digest(values[0]),certificate_sha256=values[0]['certificate_sha256'],
                    contract_identity_sha256=values[0]['contract_identity_sha256'])
                values[2]['fields'].append(copy.deepcopy(values[2]['fields'][0]))
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):factory.field_proof_record('authored.obj',*values)

    def test_borrowed_zero_field_projection_bindings_are_refused(self):
        for field in ('contract_identity_sha256','certificate_sha256','original_object_sha256','central_record_sha256','authority'):
            values=list(authored(False))
            if field=='authority':values[2][field]=dict(values[2][field],receipt_sha256='e'*64)
            else:values[2][field]='e'*64
            with self.subTest(field=field),self.assertRaises(ValueError):factory.field_proof_record('authored.obj',*values)

    def test_certificate_cannot_bind_another_contract_even_after_outer_rehash(self):
        values=list(authored(False));values[0]['certificate']['contract_identity_sha256']='e'*64
        values[0]['certificate_sha256']=factory.digest(values[0]['certificate'])
        values[1]['authority'].update(record_sha256=factory.digest(values[0]),certificate_sha256=values[0]['certificate_sha256'])
        values[2].update(central_record_sha256=factory.digest(values[0]),certificate_sha256=values[0]['certificate_sha256'])
        with self.assertRaises(ValueError):factory.field_proof_record('authored.obj',*values)

    def test_actual_output_bytes_must_match_the_recorded_projection_hash(self):
        values=list(authored());values[3]+=b'changed'
        with self.assertRaises(ValueError):factory.field_proof_record('authored.obj',*values)


if __name__=='__main__':unittest.main()
