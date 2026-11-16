"""Authored records only; patched small baseline census, no filesystem/native use."""
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/rebuild'))
import application_actual_cohort_gate as gate
from test_application_link_actual_cohort import sample


def provider(n):
    return dict(canonical='symbol%d' % n, component='test', recipe_id='recipe%d' % n,
                object_sha256='object%d' % n, symbol_index=n, original_address='address%d' % n)


def fixture():
    w, m, h = sample()
    baseline = dict(epoch_sha256=gate.EPOCH, fields=[{'old': 1}, {'old': 2}],
                    providers=[provider(100), provider(101)], unknowns=[{'unknown': True}],
                    quarantines=list(range(6)), uuid_negative_rows=list(range(9)), noncode_definitions=['other'])
    providers = [provider(n) for n in range(9)]
    fields, namespace = [], []
    for row in m:
        n = int(row['name'][6:-4]); joins=[]
        for item in row['projection']['fields']:
            field={'serialized': item['field_proof_sha256']}; fields.append(field)
            joins.append(dict(proof_sha256=item['field_proof_sha256'], serialized_sha256=gate.sha(field)))
        namespace.append(dict(member=row['name'], member_sha256=row['projection']['output_sha256'],
                              provider_sha256=gate.sha(providers[n]), fields=joins))
    successor = copy.deepcopy(baseline)
    successor['fields'] += fields; successor['providers'] += providers
    sdk = copy.deepcopy(gate.uuid.EXPECTED_SDK)
    response=dict(tokens=[sdk['path']], fresh_uuid_identity=sdk, uuid_provider_count=1,
                  qualified_uuid=dict(policy_id=gate.uuid.POLICY, kind='qualified-uuid2768-consumer-evidence-v1',
                                      future_uuid_response_token=sdk['path'], dependency_identity=copy.deepcopy(sdk)))
    producer=dict(owner='producer', member_count=9, field_count=8, observation_sha256='a'*64,
                  factory_sha256='b'*64, handoff_sha256=gate.sha(h), handoff_peer_sha256='c'*64)
    phases=[dict(phase=x, observation_id=x, identities={'input':'d'*64}, stable_sha256='e'*64) for x in gate.PHASES]
    evidence=dict(baseline=baseline, successor=successor, producer=producer,
                  proof=dict(wrappers=w, member_ledger=m, handoff=h), namespace=namespace,
                  response=response, phases=phases)
    bundle=dict(evidence=evidence, reviews=[])
    review(bundle)
    return bundle


def review(bundle):
    bundle['reviews']=[dict(kind=k, evidence_sha256=gate.sha(bundle['evidence']), verdict='accept', reviewer='peer') for k in gate.REVIEWS]


def check(bundle):
    with patch.object(gate, 'BASE_FIELDS', 2), patch.object(gate, 'BASE_PROVIDERS', 2), \
         patch.object(gate, 'BASE_FIELDS_SHA256', gate.sha([{'old': 1}, {'old': 2}])):
        return gate.validate(bundle)


class GateTests(unittest.TestCase):
    def test_consistent_evidence_grants_no_approval(self):
        result=check(fixture())
        self.assertFalse(result['admission_approved']); self.assertFalse(result['link_approved'])
        self.assertFalse(result['execution_approved'])

    def test_missing_gate_or_review_is_rejected(self):
        for mode in ('section', 'review', 'self_review', 'binding'):
            b=fixture()
            if mode=='section': del b['evidence']['namespace']
            elif mode=='review': b['reviews'].pop()
            elif mode=='self_review': b['reviews'][0]['reviewer']='producer'
            else: b['reviews'][0]['evidence_sha256']='f'*64
            with self.subTest(mode=mode), self.assertRaises((ValueError, KeyError)): check(b)

    def test_baseline_and_unknowns_are_preserved(self):
        for key in ('fields', 'providers', 'unknowns', 'quarantines', 'uuid_negative_rows'):
            b=fixture(); b['evidence']['successor'][key][0]={'tampered': True}; review(b)
            with self.subTest(key=key), self.assertRaises(ValueError): check(b)

    def test_namespace_covers_zero_fields_and_fullproofs(self):
        for mode in ('zero_member', 'proof', 'serialized', 'member_hash'):
            b=fixture(); ns=b['evidence']['namespace']
            if mode=='zero_member': ns.pop(0)
            elif mode=='proof': ns[7]['fields'][0]['proof_sha256']='f'*64
            elif mode=='serialized': ns[7]['fields'][0]['serialized_sha256']='f'*64
            else: ns[0]['member_sha256']='f'*64
            review(b)
            with self.subTest(mode=mode), self.assertRaises(ValueError): check(b)

    def test_uuid_duplicate_and_provider_conflict(self):
        for mode in ('uuid', 'duplicate_provider'):
            b=fixture(); e=b['evidence']
            if mode=='uuid': e['response']['tokens'].append(e['response']['tokens'][0])
            else:
                e['successor']['providers'][2]['canonical']=e['baseline']['providers'][0]['canonical']
                e['namespace'][0]['provider_sha256']=gate.sha(e['successor']['providers'][2])
            review(b)
            with self.subTest(mode=mode), self.assertRaises(ValueError): check(b)

    def test_phase_reuse_or_drift_rejected(self):
        for mode in ('reuse', 'drift', 'stable'):
            b=fixture(); phases=b['evidence']['phases']
            if mode=='reuse': phases[1]['observation_id']=phases[0]['observation_id']
            elif mode=='drift': phases[1]['identities']['input']='f'*64
            else: phases[2]['stable_sha256']='f'*64
            review(b)
            with self.subTest(mode=mode), self.assertRaises(ValueError): check(b)

    def test_forecast_or_changed_handoff_rejected(self):
        for mode in ('count', 'handoff'):
            b=fixture()
            if mode=='count': b['evidence']['producer']['member_count']=55
            else: b['evidence']['producer']['handoff_sha256']='f'*64
            review(b)
            with self.subTest(mode=mode), self.assertRaises(ValueError): check(b)


if __name__=='__main__': unittest.main()
