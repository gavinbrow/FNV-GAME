"""Private transactional staging primitive for the V14 factory draft.

The caller must have already validated the complete observation stream. This
primitive is not a production driver or authority gate. A separately reviewed
process-tree memory watchdog and input/operation gates are still mandatory.
"""
from __future__ import annotations
import hashlib
import copy
import json
import os
from pathlib import Path
import re
import tempfile


class CleanupIncomplete(ValueError, RuntimeError):
    """Scratch or its contents changed; preserve it for reconciliation."""


def stage_and_publish(parent, final_name, selections, produce, validate, *, max_bytes):
    """Publish the complete staged set once; remove our scratch on failure.

    Each producer yields a (simple filename, bytes) pair. The validator receives
    only a detached immutable list of filename/hash/length facts. No partial
    destination is exposed by this function. Native process memory and power-loss
    durability are outside this primitive's guarantees.
    """
    if os.name != 'nt':
        raise ValueError('Windows no-replace rename is required')
    parent = Path(parent).resolve(strict=True)
    if not parent.is_dir() or not isinstance(final_name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', final_name):
        raise ValueError('exact private parent and simple destination required')
    if type(max_bytes) is not int or max_bytes <= 0 or max_bytes > 128 * 1024 * 1024:
        raise ValueError('exact bounded output byte limit required')
    if type(selections) is not list or not selections or len(selections) > 55:
        raise ValueError('finite nonempty candidate list required')
    selections = tuple(copy.deepcopy(selections))
    destination = parent / final_name
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('destination already exists')
    scratch = Path(tempfile.mkdtemp(prefix='.v14-stage-', dir=parent)).resolve(strict=True)
    if scratch.parent != parent:
        raise ValueError('scratch escaped parent')
    original_stat = scratch.stat(follow_symlinks=False)
    identity = (original_stat.st_dev, original_stat.st_ino)
    def owned_scratch():
        try:
            stat = scratch.stat(follow_symlinks=False)
            return not scratch.is_symlink() and scratch.is_dir() and (stat.st_dev, stat.st_ino) == identity
        except OSError:
            return False
    def require_owned():
        if not owned_scratch():
            raise ValueError('owned scratch identity changed')
    facts = []
    owned_files = {}
    total = 0
    published = False
    try:
        for selection in selections:
            name, data = produce(copy.deepcopy(selection))
            require_owned()
            if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+\.obj', name) or type(data) is not bytes:
                raise ValueError('strict staged object name and byte payload required')
            total += len(data)
            if total > max_bytes:
                raise ValueError('staged output byte limit exceeded')
            target = scratch / name
            with target.open('xb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            st = target.stat(follow_symlinks=False)
            owned_files[name] = (st.st_dev, st.st_ino)
            facts.append((name, hashlib.sha256(data).hexdigest(), len(data)))
        sealed = tuple(facts)
        if validate(sealed) is not True:
            raise ValueError('complete staged validation rejected')
        require_owned()
        if {p.name for p in scratch.iterdir()} != {row[0] for row in sealed}:
            raise ValueError('unexpected staged entries')
        for name, expected_hash, expected_length in sealed:
            item = scratch / name
            st = item.stat(follow_symlinks=False)
            if item.is_symlink() or not item.is_file() or st.st_size != expected_length or (st.st_dev, st.st_ino) != owned_files[name]:
                raise ValueError('staged object identity changed')
            with item.open('rb') as stream:
                if hashlib.sha256(stream.read(expected_length + 1)).hexdigest() != expected_hash:
                    raise ValueError('staged object content changed')
        manifest = json.dumps({'members': sealed, 'bytes': total}, separators=(',', ':'), sort_keys=True).encode()
        if total + len(manifest) > max_bytes:
            raise ValueError('staged manifest exceeds output byte limit')
        with (scratch / 'staged-manifest.json').open('xb') as stream:
            stream.write(manifest)
            stream.flush()
            os.fsync(stream.fileno())
        st = (scratch / 'staged-manifest.json').stat(follow_symlinks=False)
        owned_files['staged-manifest.json'] = (st.st_dev, st.st_ino)
        require_owned()
        if {p.name for p in scratch.iterdir()} != {row[0] for row in sealed} | {'staged-manifest.json'}:
            raise ValueError('unexpected staged entries at publication')
        if sum(p.stat(follow_symlinks=False).st_size for p in scratch.iterdir()) != total + len(manifest):
            raise ValueError('staged output byte census changed')
        # Windows rename refuses an existing destination; no overwrite fallback.
        os.rename(scratch, destination)
        published = True
        return sealed
    finally:
        if not published and owned_scratch():
            # Never recursively delete a changed directory or unowned entry.
            try:
                entries = list(scratch.iterdir())
                if all(p.name in owned_files and not p.is_symlink() and p.is_file() and
                       (p.stat(follow_symlinks=False).st_dev, p.stat(follow_symlinks=False).st_ino)==owned_files[p.name]
                       for p in entries):
                    for p in entries:
                        p.unlink()
                    scratch.rmdir()
                else:
                    raise CleanupIncomplete('unowned scratch contents preserved')
            except OSError:
                raise CleanupIncomplete('scratch cleanup failed; reconciliation required')
        elif not published:
            raise CleanupIncomplete('scratch identity changed; reconciliation required')
