"""Pure post-V14 IAT/CRT census; caller must authenticate every input and source.

No IO, admission, provider change, or operation authority. The peer byte pins
are supplied by a future fixed wrapper and must themselves be independently
established. This module is not a substitute for that wrapper or review.
"""
import copy
import hashlib
import json

import application_wave14_diagnostic as wave14
import crt_frontier_adoption_contract as crt
import crt_v14_four_alias_plan as v14
import iat_field_annotations as iat


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate peer key')
        result[key] = value
    return result


def _peer(raw, pin, kind, fields, baseline, namespace, evidence):
    require(type(raw) is bytes and len(raw) <= 8 * 1024 * 1024 and type(pin) is str and
            len(pin) == 64 and all(c in '0123456789abcdef' for c in pin) and
            hashlib.sha256(raw).hexdigest() == pin, 'peer bytes or independent pin differs')
    peer = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('invalid JSON constant')))
    require(type(peer) is dict and peer.get('kind') == kind and peer.get('status') == 'independent-review-complete' and
            type(peer.get('reviewer')) is str and bool(peer['reviewer'].strip()) and
            peer.get('fields_sha256') == digest(fields) and peer.get('baseline_sha256') == digest(baseline) and
            peer.get('namespace_sha256') == digest(namespace) and peer.get('evidence_sha256') == digest(evidence) and
            peer.get('source_and_namespace_reviewed') is True and
            all(peer.get(k) is False for k in ('provider_adopted', 'runtime_ABI_approved', 'runtime_eligible', 'native_operation_authorized')),
            'current census peer does not bind full evidence and negative scope')
    return peer


def _current(baseline, fields, namespace):
    require(type(baseline) is list and type(fields) is list and type(namespace) is list and
            all(type(x) is str and x for x in namespace) and len(set(namespace)) == len(namespace),
            'complete fields and unique explicit strong namespace required')
    require(len(fields) >= len(baseline) and canonical(fields[:len(baseline)]) == canonical(baseline),
            'ordered baseline fields or unknowns changed')
    records = [canonical(row) for row in fields]
    require(len(records) == len(set(records)), 'duplicate complete field record')
    return fields[len(baseline):]


def _physical_identity(row):
    """Identify the field independently of witness hash, role, or addend."""
    # section is the observed serialized-object section for every component,
    # including actual-entry, whose compact proof need not name the source section.
    # Root and relocation symbol are evidence about a slot, not its location.
    # Namespace qualification must separately prove component/member ownership.
    return (row['component'], row['member'], row['section'], row['offset'])


def _unique_physical(rows, label):
    identities = [_physical_identity(row) for row in rows]
    require(len(identities) == len(set(identities)), 'duplicate ' + label + ' physical field')


def iat_census(*, baseline, fields, namespace, full_proofs, peer_bytes, peer_sha256, replay):
    """Replay V14 native/identity gate over all fields with new full proofs.

    replay contains exactly the arguments to wave14._iat_gate except fields;
    its fixed-wrapper caller must authenticate the native evidence and libraries.
    The published original fields are not mutated. The peer binds both proof
    bundle and replay output and must independently inspect actual source joins.
    """
    added = _current(baseline, fields, namespace)
    selected = [r for r in added if r['proof'].get('role') == 'iat-cell']
    require(type(full_proofs) is dict and set(full_proofs) ==
            {r['proof']['field_proof_sha256'] for r in selected}, 'new IAT full-proof coverage differs')
    _unique_physical([r for r in fields if r['proof'].get('role') == 'iat-cell'], 'IAT')
    view = copy.deepcopy(fields)
    catalog = iat.imports.catalog(replay['catalog'])
    for row in view[len(baseline):]:
        if row['proof'].get('role') != 'iat-cell':
            continue
        full = full_proofs[row['proof']['field_proof_sha256']]
        iat.validate_full(row, full)
        cell = catalog.get(row['proof']['original_base'])
        require(cell is not None and full['import_id'] == cell['import_id'], 'new IAT catalog identity differs')
        annotation = dict(schema_version=1, kind='exact-original-IAT-field-annotation',
            catalog_sha256=iat.CATALOG_SHA256, original_IAT_va=row['proof']['original_base'],
            import_id=full['import_id'], classification=iat.CLASSIFICATION, dll=cell['dll'], export=cell['export'],
            field_proof_sha256=row['proof']['field_proof_sha256'], provider_selected=False, ABI_verified=False)
        for key, value in dict(original_field_proof=full, IAT_annotation=annotation,
                               import_id=full['import_id'], classification=iat.CLASSIFICATION).items():
            require(key not in row or row[key] == value, 'new IAT annotation conflicts with existing evidence')
            row[key] = copy.deepcopy(value)
    rows, tokens = wave14._iat_gate(fields=view, **replay)
    for row in rows:
        row['complete_actual_uses'] = copy.deepcopy([f for f in fields if f['canonical'] == row['canonical']])
    require(all(not row['enabled'] or row['canonical'] not in namespace for row in rows),
            'strong definition supersedes enabled IAT alias')
    evidence = dict(full_proofs=full_proofs, rows=rows, tokens=tokens,
                    total_iat_fields=sum(f['proof'].get('role') == 'iat-cell' for f in fields))
    _peer(peer_bytes, peer_sha256, 'post-v14-current-iat-census-peer', fields, baseline, namespace, evidence)
    return evidence


def crt_census(*, baseline, fields, namespace, bindings, source_evidence, prior_crt, peer_bytes, peer_sha256):
    """Validate the existing four CRT bindings against the actual whole cohort.

    New CRT source qualification is an independent review requirement, bound to
    every added field and its supplied source evidence, not inferred by counts.
    """
    added = _current(baseline, fields, namespace)
    names = {v14.old.undefined(base, role) for base, role, _, _ in v14.old.BINDINGS}
    relevant = [f for f in added if f['canonical'] in names or
                (f['proof']['original_base'], f['proof']['role']) in
                {(b, r) for b, r, _, _ in v14.old.BINDINGS}]
    _unique_physical([f for f in fields if f['canonical'] in names or
                      (f['proof']['original_base'], f['proof']['role']) in
                      {(b, r) for b, r, _, _ in v14.old.BINDINGS}], 'CRT')
    require(all(f['canonical'] == v14.old.undefined(f['proof']['original_base'], f['proof']['role'])
                and (f['proof']['original_base'], f['proof']['role']) in
                {(b, r) for b, r, _, _ in v14.old.BINDINGS} for f in relevant),
            'new CRT canonical role/base collision')
    require(type(source_evidence) is list and len(source_evidence) == len(relevant) and
            [x['field_sha256'] for x in source_evidence] == [digest(f) for f in relevant],
            'new CRT source evidence does not cover actual fields in order')
    validated = crt.validate_bindings(bindings, fields, namespace)
    original = v14.old.response([dict(canonical_undefined=v14.old.undefined(b, r), normal_export=e)
        for b, r, e, _ in v14.old.BINDINGS]).replace('\n', '\r\n').encode('ascii')
    response = v14.response_bytes(bindings, original)
    require(type(prior_crt) is list and len(set(prior_crt)) == len(prior_crt) and
            set(prior_crt).issubset(set(original.decode('ascii').splitlines())),
            'inherited CRT aliases differ')
    evidence = dict(source_evidence=source_evidence, bindings=bindings, validated_bindings=validated,
                    tokens=response.decode('ascii').splitlines(), inherited_tokens_to_remove=copy.deepcopy(prior_crt),
                    alias_field_count=sum(b['field_count'] for b in validated))
    _peer(peer_bytes, peer_sha256, 'post-v14-current-crt-census-peer', fields, baseline, namespace, evidence)
    return evidence
