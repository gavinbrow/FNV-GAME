"""Opt-in, phase-local exact identity deduplication for caller stability checks.

No filesystem operations, global cache, native calls or receipt-ledger rewrite.
Production callers authenticate the unchanged stable delegate and its closure.
"""
from __future__ import annotations
import hashlib
import json
import re

IDENTITY_FIELDS=('requested_path','path','sha256','size','device','inode')
MAX_ROWS=1_000_000


def require(condition,message):
    if not condition:raise ValueError(message)


def identity_key(row):
    require(type(row) is dict and set(row)==set(IDENTITY_FIELDS),'exact complete identity dictionary required')
    require(all(type(row[name]) is str and row[name] for name in IDENTITY_FIELDS[:3]),'exact identity strings required')
    require(re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'exact lowercase file SHA-256 required')
    require(all(type(row[name]) is int and row[name]>=0 for name in IDENTITY_FIELDS[3:]),'typed identity size/device/inode required')
    return tuple(row[name] for name in IDENTITY_FIELDS)


def sequence_digest(keys):
    h=hashlib.sha256()
    for chunk in json.JSONEncoder(ensure_ascii=True,separators=(',',':'),allow_nan=False).iterencode(keys):h.update(chunk.encode('ascii'))
    return h.hexdigest()


def _selection(bindings):
    require(type(bindings) is list and len(bindings)<=MAX_ROWS,'bounded complete identity ledger list required')
    keys=[];unique=[];first_indices=[];seen=set();requested={};resolved={}
    for index,row in enumerate(bindings):
        key=identity_key(row);keys.append(key)
        request,path,sha,size,device,inode=key
        require(request not in requested or requested[request]==key,'conflicting requested-path identity')
        physical=(sha,size,device,inode)
        require(path not in resolved or resolved[path]==physical,'conflicting resolved-path identity')
        requested[request]=key;resolved[path]=physical
        if key not in seen:
            seen.add(key);first_indices.append(index)
            unique.append(dict(zip(IDENTITY_FIELDS,key)))
    facts=dict(identity_fields=list(IDENTITY_FIELDS),input_rows=len(keys),unique_rows=len(unique),
        exact_duplicate_rows=len(keys)-len(unique),first_occurrence_indices=first_indices,
        ledger_identity_sequence_sha256=sequence_digest(keys),
        unique_identity_sequence_sha256=sequence_digest([identity_key(row) for row in unique]),
        original_ledger_rewritten=False,cross_phase_cache_used=False,
        delegate_source_authentication_owned_by_caller=True)
    return unique,facts,keys


def select_exact_bindings(bindings):
    """Pure selection, suitable for saved-only equivalence qualification.

    Returned dictionaries are copies. The complete original ledger, including
    order and duplicate occurrences, remains owned by the caller unchanged.
    """
    unique,facts,_=_selection(bindings)
    return unique,facts


def stable_phase(bindings,*,phase,stable_fn):
    """Call the supplied unchanged checker once with exact unique rows.

    Every invocation reconstructs the selection. Distinct requested-path aliases
    are distinct checks even when all resolved physical fields are identical.
    This function emits counts, not an independent admission certificate.
    """
    require(phase in ('pre','post') and type(phase) is str,'explicit pre/post stability phase required')
    require(callable(stable_fn),'explicit authenticated-by-caller stability delegate required')
    unique,facts,original_keys=_selection(bindings)
    selected_keys=[identity_key(row) for row in unique]
    stable_fn(unique)  # No retry, fallback or remembered outcome.
    require([identity_key(row) for row in unique]==selected_keys,'stability delegate changed its selected snapshot')
    require(type(bindings) is list and [identity_key(row) for row in bindings]==original_keys,
            'complete caller ledger changed during stability phase')
    return dict(facts,phase=phase,delegate_calls=1,delegate_returned=True)
