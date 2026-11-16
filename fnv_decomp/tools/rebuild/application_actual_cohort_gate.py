"""Pure, fail-closed post-V14 cohort integration evidence gate.

No file access, native operation, approval, or provider selection. A coordinator
must authenticate every supplied input and independently review this source, its
inputs and outcomes. Hash bindings are integrity checks, not authentication.
"""
import re
import application_link_actual_cohort as proof
import application_uuid2768 as uuid
import application_link_cohort as cohort

EPOCH = '2e8a762f851eae7cf133cc5228efdd145ab4b32e70a2872ab527a3f32e6e318c'
BASE_FIELDS_SHA256 = '08106a9552e9fe8fbe43a5bd224a212409b00228c26654432b715223eb0d6da4'
BASE_FIELDS = 46292
BASE_PROVIDERS = 14555
PHASES = ('pre', 'post', 'publication')
REVIEWS = ('source', 'inputs', 'outcome', 'native_conformance', 'namespace', 'iat', 'crt')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(value):
    return proof.digest(value)


def hexsha(value):
    return type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def validate(bundle):
    """Return an evidence-only result; never returns link or execution approval.

    The independent reviews bind the complete evidence payload. The caller must
    authenticate their origin and the accepted V14 anchor; this pure gate cannot.
    """
    require(type(bundle) is dict and set(bundle) == {'evidence', 'reviews'}, 'exact bundle required')
    e = bundle['evidence']
    required = {'baseline', 'successor', 'producer', 'proof', 'namespace', 'response', 'phases'}
    require(type(e) is dict and set(e) == required, 'exact evidence sections required')
    b, s, producer = e['baseline'], e['successor'], e['producer']
    require(b['epoch_sha256'] == EPOCH, 'V14 prepared epoch differs')
    require(len(b['fields']) == BASE_FIELDS and len(b['providers']) == BASE_PROVIDERS,
            'V14 complete baseline census differs')
    require(sha(sorted(b['fields'], key=proof.diagnostic.canonical)) == BASE_FIELDS_SHA256,
            'accepted V14 canonical field identity differs')
    require(type(b['unknowns']) is list and type(b['quarantines']) is list and len(b['quarantines']) == 6,
            'baseline unknowns/six quarantines required')
    require(type(b['uuid_negative_rows']) is list and len(b['uuid_negative_rows']) == 9,
            'nine UUID negative rows required')
    for key in ('fields', 'providers', 'unknowns', 'quarantines', 'uuid_negative_rows', 'noncode_definitions'):
        require(type(s[key]) is list and len(s[key]) >= len(b[key]) and
                all(sha(x) == sha(y) for x, y in zip(b[key], s[key])),
                'baseline ordered ' + key + ' differs')
    for key in ('unknowns', 'quarantines', 'uuid_negative_rows', 'noncode_definitions'):
        require(len(s[key]) == len(b[key]), 'baseline ' + key + ' must remain exact')
    require(type(producer['member_count']) is int and producer['member_count'] > 0 and
            type(producer['field_count']) is int and producer['field_count'] >= 0 and
            all(hexsha(producer[k]) for k in ('observation_sha256', 'factory_sha256', 'handoff_sha256', 'handoff_peer_sha256')),
            'actual accepted producer identities/counts required')
    p = e['proof']
    verified = proof.verify_proof_ledger(p['wrappers'], p['member_ledger'], p['handoff'],
        member_count=producer['member_count'], field_count=producer['field_count'])
    require(sha(p['handoff']) == producer['handoff_sha256'], 'actual handoff differs')
    require(len(s['fields']) == BASE_FIELDS + producer['field_count'], 'successor field census differs')
    require(len(s['providers']) == BASE_PROVIDERS + producer['member_count'], 'successor provider census differs')
    ns = e['namespace']
    require(type(ns) is list and len(ns) == producer['member_count'], 'complete namespace join required')
    require([r['member'] for r in ns] == verified['members'], 'namespace member order differs')
    require(len({r['member'] for r in ns}) == len(ns), 'duplicate namespace member')
    new_providers = s['providers'][BASE_PROVIDERS:]
    cohort.disjoint_providers([new_providers], baseline_providers=b['providers'],
                              existing_noncode_definitions=b['noncode_definitions'])
    require([r['provider_sha256'] for r in ns] == [sha(x) for x in new_providers], 'namespace provider join differs')
    field_rows = s['fields'][BASE_FIELDS:]
    joins = [j for r in ns for j in r['fields']]
    require(len(joins) == producer['field_count'] and
            [j['serialized_sha256'] for j in joins] == [sha(x) for x in field_rows] and
            len({j['proof_sha256'] for j in joins}) == len(joins) and
            set(j['proof_sha256'] for j in joins) == set(verified['fullproofs']),
            'complete fullproof to serialized field join differs')
    for row in ns:
        require(row['member_sha256'] == next(x['member_sha256'] for x in p['handoff']['records'] if x['member'] == row['member']),
                'namespace member hash differs')
        owned = {f['field_proof_sha256'] for f in next(x['projection']['fields'] for x in p['member_ledger'] if x['name'] == row['member'])}
        require({j['proof_sha256'] for j in row['fields']} == owned, 'namespace field owner differs')
    response = e['response']
    uuid.guard_response(response['tokens'], response['fresh_uuid_identity'], response['qualified_uuid'])
    require(response['uuid_provider_count'] == 1 and type(response['uuid_provider_count']) is int,
            'one existing UUID provider required')
    phases = e['phases']
    require(type(phases) is list and [x['phase'] for x in phases] == list(PHASES), 'fresh phase sequence required')
    for phase in phases:
        require(type(phase['observation_id']) is str and phase['observation_id'] and
                type(phase['identities']) is dict and phase['identities'] and
                all(hexsha(v) for v in phase['identities'].values()) and
                hexsha(phase['stable_sha256']), 'full fresh identity observation required')
    require(len({x['observation_id'] for x in phases}) == 3 and
            all(x['identities'] == phases[0]['identities'] and x['stable_sha256'] == phases[0]['stable_sha256'] for x in phases),
            'fresh phase identity drift or reused observation')
    reviews = bundle['reviews']
    require(type(reviews) is list and len(reviews) == len(REVIEWS), 'independent review census required')
    require([x['kind'] for x in reviews] == list(REVIEWS) and
            all(x['evidence_sha256'] == sha(e) and x['verdict'] == 'accept' and
                type(x['reviewer']) is str and x['reviewer'] for x in reviews), 'review binding or verdict differs')
    require(all(x['reviewer'] != producer['owner'] for x in reviews), 'producer cannot independently review')
    return {'status': 'evidence-consistent-external-authentication-required', 'evidence_sha256': sha(e),
            'admission_approved': False, 'link_approved': False, 'execution_approved': False}
