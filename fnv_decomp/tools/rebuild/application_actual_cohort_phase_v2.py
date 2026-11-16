"""V2 read-only fresh phase observation for a pinned operation manifest.

Actual operation authority, lease, publication and review are external. Never
invokes native tools, writes output, or reuses phase observations.
"""
import hashlib
import json
from pathlib import Path
import application_link_diagnostic as diagnostic
import exact_binding_stability as stability


def require(ok, message):
    if not ok: raise ValueError(message)


def observe(*, manifest_bytes, manifest_sha256, phase):
    require(type(manifest_bytes) is bytes and type(manifest_sha256) is str and
            hashlib.sha256(manifest_bytes).hexdigest() == manifest_sha256,
            'exact reviewed manifest bytes required')
    m = json.loads(manifest_bytes)
    require(type(m) is dict and set(m) == {'operation_id', 'resources'} and
            type(m['operation_id']) is str and m['operation_id'] and
            type(m['resources']) is list and m['resources'], 'exact operation resources required')
    require(phase in ('pre', 'post', 'publication') and type(phase) is str, 'phase required')
    resources = m['resources']
    require(all(type(x) is dict and set(x) == {'role','identity'} and type(x['role']) is str and x['role']
                for x in resources), 'exact role and physical identity required')
    roles = [x['role'] for x in resources]
    require(len(set(roles)) == len(roles), 'duplicate resource role')
    bindings = [x['identity'] for x in resources]
    # Freshly hash/stat every distinct full identity in this phase via unchanged
    # D.stable, preserving all ledger occurrences and never carrying a cache.
    unique, facts = stability.select_exact_bindings(bindings)
    diagnostic.stable(unique)
    require(all(stability.identity_key(x) == stability.identity_key(y)
                for x,y in zip(bindings,[r['identity'] for r in resources])), 'manifest ledger mutated')
    return dict(kind='fresh-physical-phase-observation-v2', operation_id=m['operation_id'], phase=phase,
                manifest_sha256=manifest_sha256, resource_roles=roles, full_ledger=bindings,
                ledger_facts=facts, identity_checked=True, approval=False)
