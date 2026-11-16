"""Held child: no project import before the parent and complete source pins pass."""
import hashlib
import json
import os
import sys
import types
from pathlib import Path

DIAGNOSTIC_LIMIT = 16384
SAFE_MESSAGES = frozenset(('unverified Guard implementation', 'unverified held verifier implementation',
    'unbound nonstdlib import', 'missing project source role', 'project module preloaded',
    'held runtime missing', 'actual runtime Guard class required', 'authentic issued Guard required',
    'unissued Guard/profile', 'driver did not authenticate held capability'))


def diagnostic(error):
    # Never render traceback source lines, locals, reprs, or arbitrary exception
    # values. Only these known constant messages may cross the capture channel.
    message = error.args[0] if len(error.args) == 1 and type(error.args[0]) is str else None
    message = message if message in SAFE_MESSAGES else '[exception value redacted]'
    frames=[]; node=error.__traceback__
    while node is not None and len(frames)<32:
        code=node.tb_frame.f_code
        frames.append(dict(file=Path(code.co_filename).name[:96],function=code.co_name[:96],line=node.tb_lineno))
        node=node.tb_next
    value=dict(kind='held-child-exception-v1',exception_type=type(error).__name__[:96],message=message,
               frames=frames,frames_truncated=node is not None,locals_or_payload_included=False)
    body=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()+b'\n'
    if len(body)>DIAGNOSTIC_LIMIT:raise ValueError('diagnostic bound')
    return body


def run():
    try:
        main()
        return 0
    except BaseException as error:
        code=error.code if type(error) is SystemExit and type(error.code) is int and 0<=error.code<=255 else 1
        if code == 0:return 0
        try:
            body=diagnostic(error);offset=0
            while offset<len(body):
                written=os.write(2,body[offset:])
                if written<=0:raise OSError('diagnostic write failed')
                offset+=written
        except BaseException:
            pass  # Failure still returns nonzero; never print an unsafe fallback.
        return code


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
    name = '_fnv_verified_held_bootstrap_v3'
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
    raise SystemExit(run())
