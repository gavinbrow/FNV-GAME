"""Held child: no project import before the parent and complete source pins pass."""
import hashlib
import json
import sys
import types
from pathlib import Path


def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def main():
    # One frame and EOF. The parent closes its writer after sending; EOF before
    # a complete frame is failure, never permission to run an orphan payload.
    raw = sys.stdin.buffer.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024 or not raw.endswith(b'\n') or raw.count(b'\n') != 1:
        raise ValueError('held session framing/EOF')
    envelope = json.loads(raw, object_pairs_hook=pairs)
    if json.dumps(envelope, sort_keys=True, separators=(',', ':')).encode() + b'\n' != raw:
        raise ValueError('noncanonical session')
    path = Path(envelope['parent_source'])
    source = path.read_bytes()
    if len(source) > 1024 * 1024 or hashlib.sha256(source).hexdigest() != envelope['parent_sha256']:
        raise ValueError('parent source pin')
    name = '_fnv_verified_held_bootstrap_v1'
    if name in sys.modules:
        raise ValueError('held runtime already registered')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    sys.modules[name] = module
    try:
        module.child_main(envelope)
    finally:
        # No registration or live capability survives child entry completion.
        if sys.modules.get(name) is module:
            del sys.modules[name]


if __name__ == '__main__':
    main()
