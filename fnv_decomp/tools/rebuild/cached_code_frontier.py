"""Opt-in lossless binding-cache contract qualification; no native admission."""
from __future__ import annotations
import copy
import hashlib
import json

import binding_context_cache as cache_module
import scalableordinary_root_collect as finite

POLICY = 'cached-CODE-frontier-contract-qualification-v1'
require = cache_module.require
digest = cache_module.digest
canonical = cache_module.canonical
FALSE = dict(provider_selected=False, runtime_eligible=False, ABI_verified=False,
             native_tools_run=False, emission_performed=False,
             closure_inferred=False, full_serialization_eligible=False)
ROOT_KEYS = {'original_address','recipe_id','recipe_index','object_sha256',
             'source_sha256','symbol','symbol_index','section','value','size'}


def build_recipe_contexts(cache, recipe_index, selections, unit, proof,
                          requested, imported, provenance):
    """Read one full recipe frame and build frozen singleton AND union contracts.

    Provenance is supplied unchanged to the frozen constructor. Frame identity
    is separate evidence, never inserted into or substituted for original rows.
    No object bytes, native parser or closure assessor are used here.
    """
    require(type(recipe_index) is int and type(unit['recipe_index']) is int and
            type(proof['recipe_index']) is int and recipe_index == unit['recipe_index'],
            'recipe index differs')
    require(all(all(type(row[k]) is int for k in ('section','value','size'))
                for row in proof['verified_functions']), 'retained native integer types differ')
    cache_module.frozen.check_unit(unit, proof)
    require(isinstance(requested, list) and requested, 'nonempty finite recipe roots required')
    seen = set()
    verified = {r['original_address']: r for r in
                cache_module.frozen.selected_rows(unit, proof, selections)}
    for root in requested:
        require(set(root) == ROOT_KEYS, 'exact physical root schema required')
        require(all(type(root[k]) is int for k in
                    ('recipe_index','symbol_index','section','value','size')),
                'physical root integer types differ')
        address = root['original_address']
        require(address not in seen and address in verified, 'duplicate/unselected physical root')
        seen.add(address)
        selected = verified[address]
        require(type(selected['recipe_index']) is int and
                selected['runtime_eligible'] is False and selected['link_ready'] is False and
                canonical([root[k] for k in ('symbol','section','value','size')]) ==
                canonical([selected[k] for k in ('symbol','section','value','size')]),
                'typed retained physical selection differs')
        require(root['recipe_id'] == unit['recipe_id'] and
                root['recipe_index'] == recipe_index and
                root['object_sha256'] == unit['object_sha256'] and
                root['source_sha256'] == unit['source_sha256'] and
                all(root[k] == selected[k] for k in ('symbol','section','value','size')),
                'physical/source root differs from retained selection')
    original_inputs = canonical([unit, proof, requested, imported, provenance])
    buckets, verification = cache.read_recipe(recipe_index, selections, unit, proof)
    # read_recipe authenticates this entry against the receipt-bound loaded
    # index before parsing. Native symbol slots are absent from selected_rows.
    roster = {row[0]: row for row in cache.index['frames'][recipe_index]['roster']}
    for root in requested:
        row = roster[root['original_address']]
        require(canonical(row[:6]) == canonical([root[k] for k in
                ('original_address','symbol','section','value','size','symbol_index')]),
                'requested native symbol differs from authenticated frame roster')
    # The full recipe bucket intentionally includes unrequested owners. Frozen
    # omission checks depend on these incoming uses and missing-field records.
    rows = []
    scopes = [('SINGLE_ROOT_METADATA_CONTRACT', [root]) for root in requested]
    scopes.append(('RECIPE_UNION_METADATA_CONTRACT', requested))
    for event, roots in scopes:
        contract = finite.build_contract(unit, proof, roots, buckets, imported,
                                         copy.deepcopy(provenance))
        rows.append(dict(event=event, requested_roots=copy.deepcopy(roots),
                         contract=contract, contract_sha256=digest(contract),
                         source_frame_verification=copy.deepcopy(verification), **FALSE))
    require(canonical([unit, proof, requested, imported, provenance]) == original_inputs,
            'contract qualification mutated caller evidence')
    return dict(schema_version=1, policy_id=POLICY,
                kind='cached-recipe-metadata-contracts', recipe_index=recipe_index,
                requested_roots=len(requested), records=rows,
                certificate_created=False, native_observation_required=True, **FALSE)


def read_bound_json(path, expected_sha256, *, limit=128*1024**2):
    """Hash and parse exactly the same bounded bytes."""
    with open(path, 'rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit and hashlib.sha256(raw).hexdigest() == expected_sha256,
            'bounded JSON hash/size differs')
    return json.loads(raw)
