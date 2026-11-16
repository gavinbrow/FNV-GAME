"""Post-V14 operation control primitives, source-only and intentionally disabled.

No native operation entry is provided. The independent successor request, exact
input/source manifests and three reviews do not yet exist. The private fixture
seams below are not authority and must not be wired directly to a production
operation. A future independently reviewed fixed wrapper must supply immutable
trust anchors and authenticate the entire runtime/import closure.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def _digest(value):
    return type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _read_pinned(root, ref, ledger, cap=128 * 1024 * 1024):
    """Bind physical identity and bytes; reject escapes and changed observations."""
    _require(type(ref) is dict and set(ref) == {'path', 'sha256'} and _digest(ref['sha256']), 'bad pin')
    root = Path(root).resolve(strict=True)
    rel = Path(ref['path'])
    _require(type(ref['path']) is str and not rel.is_absolute() and '..' not in rel.parts, 'bad relative path')
    requested = root / rel
    resolved = requested.resolve(strict=True)
    _require(resolved.is_relative_to(root) and resolved.is_file(), 'pin outside root')
    with resolved.open('rb') as stream:
        before = os.fstat(stream.fileno())
        data = stream.read(cap + 1)
        after = os.fstat(stream.fileno())
    current = resolved.stat()
    fields = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    _require(len(data) <= cap and fields(before) == fields(after) == fields(current) and
             len(data) == current.st_size and _sha(data) == ref['sha256'] and
             requested.resolve(strict=True) == resolved, 'pin changed')
    ledger.append({'requested_path': str(requested), 'path': str(resolved), 'sha256': _sha(data),
                   'size': current.st_size, 'device': current.st_dev, 'inode': current.st_ino})
    return data


def _manifest_fixture(root, manifest_ref, review_refs, anchors):
    """Synthetic seam: independent fixed anchors must be compiled by a future wrapper.

    Hashes are integrity bindings, not proof of reviewer identity. The separate
    review records must each bind the same manifest and the designated scope.
    """
    _require(type(anchors) is dict and set(anchors) == {'manifest', 'source', 'input', 'operation'}, 'four fixed anchors required')
    _require(all(_digest(v) for v in anchors.values()) and len(set(anchors.values())) == 4, 'distinct fixed hashes required')
    _require(manifest_ref['sha256'] == anchors['manifest'] and type(review_refs) is dict and
             set(review_refs) == {'source', 'input', 'operation'}, 'exact review set required')
    ledger = []
    manifest = _json(_read_pinned(root, manifest_ref, ledger, 4 * 1024 * 1024))
    _require(type(manifest) is dict and set(manifest) == {'kind', 'schema_version', 'sources', 'inputs', 'operation'} and
             manifest['kind'] == 'successor-operation-manifest' and type(manifest['schema_version']) is int and
             manifest['schema_version'] == 1, 'manifest schema')
    reviewers = set()
    for scope in ('source', 'input', 'operation'):
        ref = review_refs[scope]
        _require(ref['sha256'] == anchors[scope], 'review pin differs')
        review = _json(_read_pinned(root, ref, ledger, 4 * 1024 * 1024))
        _require(type(review) is dict and set(review) == {'kind', 'scope', 'manifest_sha256', 'subject_sha256', 'reviewer'} and
                 review['kind'] == 'independent-successor-review' and review['scope'] == scope and
                 review['manifest_sha256'] == anchors['manifest'] and
                 review['subject_sha256'] == _sha(_canonical(manifest[{'source':'sources', 'input':'inputs', 'operation':'operation'}[scope]])) and
                 type(review['reviewer']) is str and review['reviewer'], 'review binding differs')
        reviewers.add(review['reviewer'])
    _require(len(reviewers) == 3, 'independent reviewers required')
    return manifest, ledger


def _source_snapshots_fixture(root, source_pins, ledger):
    """Capture all pinned source bytes before any later import or execution.

    This alone is not an import hook; runtime isolation is a future gate.
    """
    _require(type(source_pins) is dict and 0 < len(source_pins) <= 80, 'bounded source graph required')
    snapshots = {}
    for name, ref in source_pins.items():
        _require(type(name) is str and re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name), 'invalid module name')
        snapshots[name] = _read_pinned(root, ref, ledger, 4 * 1024 * 1024)
    _require(sum(map(len, snapshots.values())) <= 8 * 1024 * 1024, 'source graph cap')
    return snapshots


def _phase_fixture(ledger, phase, stable_phase, stable_delegate):
    """Invoke the unchanged, independently authenticated delegate on each phase.

    Authentication and import isolation remain obligations of a fixed wrapper.
    No selection or result is retained between calls.
    """
    _require(phase in ('pre', 'post') and type(ledger) is list, 'phase and ledger required')
    before = copy.deepcopy(ledger)
    result = stable_phase(ledger, phase=phase, stable_fn=stable_delegate)
    _require(ledger == before and result['cross_phase_cache_used'] is False and
             result['original_ledger_rewritten'] is False, 'ledger or phase changed')
    return {'phase': phase, 'selection': result, 'input_bindings': before}


def _write_exclusive(path, value):
    """Write a durable create-once JSON receipt. Existing or partial files block retry."""
    data = _canonical(value) + b'\n'
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    _require(Path(path).read_bytes() == data, 'receipt post-read differs')
    return _sha(data)


def _start_receipt_fixture(path, *, operation_sha, lease_identity, child_identity):
    """Record one already-authenticated lease and child before a future operation.

    The fixed wrapper must itself acquire and continuously validate the real lease,
    process birth identity and watchdog. This method never grants a lease.
    """
    _require(_digest(operation_sha) and type(lease_identity) is dict and type(child_identity) is dict,
             'bound lease, child and operation required')
    _require(set(lease_identity) == {'registry_sha256', 'owner', 'resource', 'slot', 'granted_utc', 'max_seconds'} and
             _digest(lease_identity['registry_sha256']) and lease_identity['resource'] == 'cpu' and
             type(lease_identity['owner']) is str and lease_identity['owner'] and
             type(lease_identity['slot']) is int and lease_identity['slot'] > 0 and
             type(lease_identity['max_seconds']) is int and lease_identity['max_seconds'] > 0 and
             type(lease_identity['granted_utc']) is str and lease_identity['granted_utc'], 'lease schema')
    _require(set(child_identity) == {'pid', 'parent_pid', 'create_time', 'executable_sha256'} and
             all(type(child_identity[k]) is int and child_identity[k] > 0 for k in ('pid', 'parent_pid')) and
             type(child_identity['create_time']) is str and child_identity['create_time'] and
             _digest(child_identity['executable_sha256']), 'child schema')
    return _write_exclusive(path, {'kind': 'successor-operation-started', 'operation_sha256': operation_sha,
                                    'lease': lease_identity, 'child': child_identity, 'outcome': 'UNKNOWN'})


def _terminal_receipt_fixture(path, *, started_path, started_sha, outcome, evidence):
    _require(_digest(started_sha) and outcome in ('completed', 'failed') and type(evidence) is dict,
             'terminal evidence required')
    data = Path(started_path).read_bytes()
    _require(_sha(data) == started_sha and _json(data).get('outcome') == 'UNKNOWN', 'started receipt differs')
    return _write_exclusive(path, {'kind': 'successor-operation-terminal', 'started_sha256': started_sha,
                                    'outcome': outcome, 'evidence': evidence})
