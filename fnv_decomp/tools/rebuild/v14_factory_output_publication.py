"""V14 full-output receipt publication primitive; no production authority.

The directory is exclusive unadmitted staging. On failure it is retained for
reconciliation; this module does not resume, clean, or adopt a failed run. The
caller must authenticate the operation and source and independently check all
proofs before requesting publication. A stable private filesystem is assumed.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

MAX_BYTES = 128 * 1024 * 1024
MAX_FILES = 1024


def _inventory(root, expected_names):
    found = {}
    todo = [('', root)]
    directories = {''}
    for name in expected_names:
        p = PurePosixPath(name)
        if (not isinstance(name, str) or not name or '\\' in name or p.is_absolute() or
            p.as_posix() != name or any(part in ('', '.', '..') for part in p.parts)):
            raise ValueError('noncanonical output name')
        for i in range(1, len(p.parts)):
            directories.add('/'.join(p.parts[:i]))
    count = 0
    while todo:
        prefix, directory = todo.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                count += 1
                if count > MAX_FILES:
                    raise ValueError('output entry limit')
                name = prefix + '/' + entry.name if prefix else entry.name
                # Windows DirEntry.stat may omit physical file identity.
                st = Path(entry.path).stat(follow_symlinks=False)
                if stat.S_ISLNK(st.st_mode) or getattr(st, 'st_file_attributes', 0) & 0x400:
                    raise ValueError('output reparse point')
                if stat.S_ISDIR(st.st_mode):
                    if name not in directories:
                        raise ValueError('unexpected output directory')
                    todo.append((name, Path(entry.path)))
                elif stat.S_ISREG(st.st_mode) and name in expected_names:
                    found[name] = (Path(entry.path), st)
                else:
                    raise ValueError('unexpected output entry')
    if set(found) != expected_names:
        raise ValueError('incomplete output census')
    return found


def _verify(root, pins, budget):
    found = _inventory(root, set(pins))
    total = 0
    identities = {}
    for name, expected in pins.items():
        path, before = found[name]
        total += before.st_size
        if total > budget:
            raise ValueError('output limit')
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(chunk)
        after = path.stat(follow_symlinks=False)
        identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) or h.hexdigest() != expected:
            raise ValueError('output drift or hash mismatch')
        identities[name] = identity
    return identities, total


def publish_complete(staging, artifact_sha256, operation_sha256, journal, stable, *, summary, max_bytes=MAX_BYTES):
    """Publish a hash-bound complete receipt after validation; never clean partials.

    artifact_sha256 is the exact complete nested file census, including the
    already-closed terminal journal but excluding the two receipt names. The
    callback must raise on unstable inputs; it is checked before and after the
    hardlink. Summary is arithmetically checked but the caller must validate it
    against actual member and quarantine artifacts. Receipts require independent
    outcome review and are not admission.
    """
    if os.name != 'nt':
        raise ValueError('Windows hardlink publication required')
    supplied_root = Path(staging)
    supplied_stat = supplied_root.stat(follow_symlinks=False)
    if supplied_root.is_symlink() or getattr(supplied_stat, 'st_file_attributes', 0) & 0x400:
        raise ValueError('staging reparse point')
    root = supplied_root.resolve(strict=True)
    st = root.stat(follow_symlinks=False)
    if not root.is_dir() or root.is_symlink():
        raise ValueError('private staging directory required')
    root_identity = (st.st_dev, st.st_ino)
    if type(artifact_sha256) is not dict or not artifact_sha256 or len(artifact_sha256) > MAX_FILES:
        raise ValueError('exact nonempty output census required')
    if any(not isinstance(k, str) or not isinstance(v, str) or re.fullmatch('[0-9a-f]{64}', v) is None
           for k, v in artifact_sha256.items()):
        raise ValueError('invalid output digest')
    artifact_sha256 = dict(artifact_sha256)
    if type(operation_sha256) is not str or re.fullmatch('[0-9a-f]{64}', operation_sha256) is None:
        raise ValueError('operation digest required')
    if type(max_bytes) is not int or not 0 < max_bytes <= MAX_BYTES:
        raise ValueError('bounded output size required')
    if (type(summary) is not dict or set(summary) != {'requested','emitted','blocked'} or
        any(type(summary[k]) is not int or summary[k] < 0 for k in summary) or
        not 0 < summary['requested'] <= 55 or summary['emitted'] + summary['blocked'] != summary['requested']):
        raise ValueError('exact complete terminal partition required')
    summary = dict(summary)
    if getattr(journal, 'closed', None) is not True or not callable(stable):
        raise ValueError('closed journal and stability guard required')
    try:
        journal_path = Path(journal.name).resolve(strict=True)
        journal_name = journal_path.relative_to(root).as_posix()
    except (OSError, TypeError, ValueError):
        raise ValueError('closed staging journal required')
    if journal_name not in artifact_sha256:
        raise ValueError('journal absent from exact output census')
    pending, final = root / 'receipt.pending.json', root / 'receipt.json'
    if pending.exists() or final.exists() or pending.is_symlink() or final.is_symlink():
        raise FileExistsError('receipt already exists')
    def same_root():
        try:
            current = root.stat(follow_symlinks=False)
            return not root.is_symlink() and root.is_dir() and (current.st_dev, current.st_ino) == root_identity
        except OSError:
            return False
    def ensure_root():
        if not same_root():
            raise ValueError('staging identity changed')
    ensure_root(); stable(); ensure_root()
    before, total = _verify(root, artifact_sha256, max_bytes)
    receipt = {'schema_version': 1, 'kind': 'v14-factory-staged-output-receipt',
               'status': 'completed-incomplete' if summary['blocked'] else 'completed-unreviewed',
               'operation_sha256': operation_sha256, 'summary': summary,
               'output_sha256': artifact_sha256, 'provider_selected': False, 'runtime_eligible': False}
    raw = (json.dumps(receipt, sort_keys=True, separators=(',', ':')) + '\n').encode()
    if total + 2 * len(raw) > max_bytes:
        raise ValueError('receipt exceeds output budget')
    created = None
    linked = False
    try:
        with pending.open('xb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        pending_st = pending.stat(follow_symlinks=False)
        created = (pending_st.st_dev, pending_st.st_ino)
        ensure_root(); stable(); ensure_root()
        # Ensure all source artifacts and the unpublished receipt are unchanged.
        pins = dict(artifact_sha256, **{'receipt.pending.json': hashlib.sha256(raw).hexdigest()})
        current, _ = _verify(root, pins, max_bytes)
        if any(current[k] != before[k] for k in artifact_sha256):
            raise ValueError('output identity changed before publication')
        os.link(pending, final)
        linked = True
        ensure_root(); stable(); ensure_root()
        pins['receipt.json'] = pins['receipt.pending.json']
        current, _ = _verify(root, pins, max_bytes)
        if any(current[k] != before[k] for k in artifact_sha256):
            raise ValueError('output identity changed after publication')
        fs = final.stat(follow_symlinks=False)
        ps = pending.stat(follow_symlinks=False)
        if (fs.st_dev, fs.st_ino) != created or (ps.st_dev, ps.st_ino) != created:
            raise ValueError('receipt identity changed')
        return receipt
    except BaseException:
        # Remove only our canonical link, never a replacement or pending evidence.
        if linked and created is not None and same_root():
            try:
                f = final.stat(follow_symlinks=False)
                if not final.is_symlink() and (f.st_dev, f.st_ino) == created:
                    final.unlink()
            except FileNotFoundError:
                pass
        raise
