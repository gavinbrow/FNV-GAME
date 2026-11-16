"""Create a private runtime-only startup caller variant; never compile or link.

This fixes only three source call declarations/names. It does not establish ABI,
provider closure, source rights, original MATCH, or runtime correctness.
"""
from pathlib import Path
import difflib
import hashlib
import json
import sys

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / 'src/fallout/misc/main.cpp'
SOURCE_SHA = '89d09f8b4ba6d9758fca0ac3ebd32e18c9cc82c68a739c044457ed5c005ae3c5'
DEST = REPO / 'build/rebuild/startup-direct-variant-v1'
REPLACEMENTS = (
    (b'int __cdecl FUN_004b7920(...);', b'class BipedNodeNames\n{\n  public:\n    static void InitializeMultiBounds();\n};'),
    (b'int __cdecl FUN_00a1c6f0(...);', b'void __cdecl FUN_00a1c6f0(void);'),
    (b'int __cdecl FUN_0045b020(...);', b'void __cdecl FUN_0045b020(void);'),
    (b'                FUN_004b7920();', b'                BipedNodeNames::InitializeMultiBounds();'),
)


def transform(source):
    if type(source) is not bytes or hashlib.sha256(source).hexdigest() != SOURCE_SHA:
        raise ValueError('original main.cpp identity differs')
    out = source
    # Match the original newline convention in the added class declaration.
    newline = b'\r\n' if b'\r\n' in source else b'\n'
    for old, new in REPLACEMENTS:
        if out.count(old) != 1:
            raise ValueError('expected unique declaration/call differs')
        out = out.replace(old, new.replace(b'\n', newline), 1)
    return out


def main():
    source = SOURCE.read_bytes()
    variant = transform(source)
    # Exclusive output; a prior or interrupted operation must be reconciled.
    DEST.mkdir(parents=False, exist_ok=False)
    with (DEST / 'main.cpp').open('xb') as f:
        f.write(variant)
    diff = ''.join(difflib.unified_diff(source.decode('utf-8').splitlines(keepends=True),
        variant.decode('utf-8').splitlines(keepends=True), fromfile='original/main.cpp',
        tofile='experimental/main.cpp'))
    with (DEST / 'source.diff').open('x', encoding='utf-8', newline='') as f:
        f.write(diff)
    receipt = {'kind':'experimental-runtime-startup-source-variant-v1', 'source_sha256':SOURCE_SHA,
        'variant_sha256':hashlib.sha256(variant).hexdigest(), 'changes':len(REPLACEMENTS),
        'native_operation_performed':False, 'original_match_claimed':False,
        'provider_or_ABI_approved':False, 'runtime_ready':False}
    with (DEST / 'receipt.json').open('x', encoding='utf-8', newline='\n') as f:
        json.dump(receipt, f, sort_keys=True, indent=2); f.write('\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit('no arguments accepted')
    main()
