"""Guarded generator-backed seven-unit source transaction; builds are separate."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

H = Path(__file__).resolve().parent
M = H.parent
R = M.parent.parent
F = R / 'fnv_decomp'
V = M / 'out/phase2-source-integration6757-v2'
S = M / 'out/phase2-source-integration6757'
T = M / 'out/phase2-source-integration6757-transaction-v2'
sys.path.insert(0, str(H))
import rtti_tesform_bindings_transaction as locks

BASE = '6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
NEW = '825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
PROPOSAL = 'e2b8c9590ef174448f1898c3168b37846ade5af85a74ba5cef03731cc9b237d9'
# Set only after private package generation and independent review.
PIN = '9422dd1642f66ddca78a1b161b040cdb55847afd3ad447fbf66e86a6ed47e9da'
REL = sorted([
    'build/units.json', 'src/fallout/ai/actor.cpp', 'src/fallout/ai/middlehighprocess.cpp',
    'src/fallout/interface/forenderedmenu.cpp', 'src/tesobjecttree.cpp', 'src/TESObjectTREE.h',
    'src/fallout_shared/bgsbodypart.cpp', 'src/fallout_shared/bgsbodypartdata.cpp',
    'src/fallout_shared/bgsbodypartdata.h', 'src/fallout_shared/bgsbodypart_decls.h',
] + [folder + name + '_native.h' for folder in ('include/', 'src/fallout_shared/')
     for name in ('BGSBodyPart', 'BodyPartInfo', 'FileEntryList', 'TESModelPSA', 'TESModel')])


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def read(path):
    return path.read_bytes() if path.exists() else None


def sha(path):
    return digest(path.read_bytes())


def recipe_guard(old, new):
    a, b = json.loads(old), json.loads(new)
    if digest(old) != BASE or digest(new) != NEW or a.keys() != b.keys():
        raise ValueError('recipe identity changed')
    if any(a[k] != b[k] for k in a if k != 'units') or len(a['units']) != len(b['units']):
        raise ValueError('recipe structure changed')
    if [i for i, (x, y) in enumerate(zip(a['units'], b['units'])) if x != y] != [253, 370, 425, 620, 2909]:
        raise ValueError('recipe unit scope changed')
    for x, y in zip(a['units'], b['units']):
        if any(x[k] != y[k] for k in ('source', 'compiler', 'flags')):
            raise ValueError('source path, compiler or flags changed')
    spans = lambda d: Counter((f['address'], f['size']) for u in d['units'] for f in u['functions'])
    if spans(a) != spans(b):
        raise ValueError('function address/size multiset changed')
    if '??_ETESModelPSA@@UAEPAXI@Z' in b['units'][620]['symbols']:
        raise ValueError('unproved weak E binding is excluded')


def prepare():
    if T.exists():
        raise FileExistsError(T)
    if sha(V / 'manifest.json') != PROPOSAL or sha(F / 'build/units.json') != BASE:
        raise ValueError('proposal or live recipe changed')
    m = json.loads((V / 'manifest.json').read_bytes())
    audit = json.loads((V / 'root-ordinary-review.json').read_bytes())
    if (audit['candidate_recipe_sha256'] != NEW or audit['proposal_sha256'] != PROPOSAL
            or audit['function_count'] != 1100 or audit['ordinary_eh_sections'] != 389
            or audit['recipe_eh_tails'] != 8 or audit['bad_tails'] or audit['tail_conflicts']):
        raise ValueError('independent ordinary proof incomplete')
    old, new = (F / 'build/units.json').read_bytes(), (V / 'units.generated').read_bytes()
    recipe_guard(old, new)
    if sorted(list(m['source_files']) + ['build/units.json']) != REL:
        raise ValueError('source payload scope changed')
    source = json.loads((S / 'manifest.json').read_bytes())
    required = {}
    paths = [V / 'manifest.json', V / 'root-ordinary-review.json', S / 'manifest.json',
             S / 'independent-source-audit.json', S / 'psa-alias-demand-review.json',
             M / 'out/phase2-source-integration6757-lane/paired-source-pools-253-2909.json',
             M / 'out/phase2-source-integration6757-lane/tool-freeze.json']
    for i in (253, 370, 425, 620, 621, 2909, 2910):
        d = M / 'out/phase2-source-integration6757-lane' / str(i)
        paths += [d / name for name in ('mirror-manifest.json', 'compile-result.json', 'candidate.obj', 'original.obj')]
    for path in paths:
        required[path.relative_to(R).as_posix()] = sha(path)
    for path, value in source['evidence_sha256'].items():
        if sha(R / path) != value:
            raise ValueError('original evidence changed')
        required[path] = value
    closure = {}
    for graph in source['closure'].values():
        for path, value in graph['original']['files'].items():
            if path in closure and closure[path] != value:
                raise ValueError('conflicting source closure')
            if sha(F / path) != value:
                raise ValueError('live source closure changed')
            closure[path] = value
    payloads = {}
    for rel, x in m['source_files'].items():
        original, candidate = read(F / rel), (S / 'payload' / rel).read_bytes()
        if digest(original) != x['preimage'] or digest(candidate) != x['candidate']:
            raise ValueError('source preimage or payload changed: ' + rel)
        payloads[rel] = (original, candidate)
    payloads['build/units.json'] = (old, new)
    T.mkdir()
    files = []
    for i, rel in enumerate(REL):
        before, after = payloads[rel]
        names = {'original': str(i) + '.original' if before is not None else None,
                 'candidate': str(i) + '.candidate'}
        if before is not None:
            (T / names['original']).write_bytes(before)
        (T / names['candidate']).write_bytes(after)
        files.append(dict(path=rel, old_sha256=digest(before), new_sha256=digest(after), **names))
    manifest = {'base_recipe_sha256': BASE, 'candidate_recipe_sha256': NEW,
                'files': files, 'required_inputs': required, 'source_closure': closure,
                'limitations': ['Fresh production comparisons, exact image/relocations, controls and repeat gameplay are required.',
                                'Weak E binding remains excluded; full class and Phase 2 recovery remain open.']}
    (T / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
    print(json.dumps({'files': len(files), 'manifest_sha256': sha(T / 'manifest.json'), 'installed': False}))


def atomic(path, data):
    if data is None:
        path.unlink(missing_ok=True)
        return
    fd, name = tempfile.mkstemp(prefix='combined-native-', dir=T)
    tmp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def operations(m, action):
    out = []
    for x in m['files']:
        p = (F / x['path']).resolve()
        if not p.is_relative_to(F.resolve()):
            raise ValueError('source target escapes checkout')
        old = (T / x['original']).read_bytes() if x['original'] else None
        new = (T / x['candidate']).read_bytes()
        current = read(p)
        if digest(old) != x['old_sha256'] or digest(new) != x['new_sha256']:
            raise ValueError('payload identity changed')
        allowed = [x['old_sha256']] if action == 'apply' else [x['new_sha256']] if action == 'restore' else [x['old_sha256'], x['new_sha256']]
        if digest(current) not in allowed:
            raise ValueError('unknown target state: ' + x['path'])
        out.append((p, current, new if action == 'apply' else old))
    return out


def execute(ops, marker, applied, action):
    changed, created = [], []
    try:
        for p, previous, wanted in ops:
            if previous != wanted:
                changed.append((p, previous))
                atomic(p, wanted)
        for p in ([marker, applied] if action == 'apply' else [marker]):
            with p.open('x', encoding='utf8') as f:
                created.append(p)
                json.dump({'action': action, 'manifest_sha256': PIN, 'fresh_production_gate_required': True}, f)
    except BaseException:
        errors = []
        for p, previous in reversed(changed):
            try:
                atomic(p, previous)
            except BaseException as exc:
                errors.append(str(p) + ': ' + str(exc))
        for p in created:
            p.unlink(missing_ok=True)
        if errors:
            raise RuntimeError('rollback incomplete; use recover: ' + '; '.join(errors))
        raise


def run(action):
    guards = locks.acquire_guard()
    try:
        raw = (T / 'manifest.json').read_bytes()
        if not PIN or digest(raw) != PIN:
            raise ValueError('transaction is unpinned or changed')
        m = json.loads(raw)
        if [x['path'] for x in m['files']] != REL or m['base_recipe_sha256'] != BASE or m['candidate_recipe_sha256'] != NEW:
            raise ValueError('transaction scope changed')
        by_path = {x['path']: x for x in m['files']}
        recipe = by_path['build/units.json']
        recipe_guard((T / recipe['original']).read_bytes(), (T / recipe['candidate']).read_bytes())
        if action == 'apply':
            for rel, value in m['required_inputs'].items():
                p = (R / rel).resolve()
                if not p.is_relative_to(R.resolve()) or sha(p) != value:
                    raise ValueError('required evidence changed: ' + rel)
            for rel, value in m['source_closure'].items():
                p = (F / rel).resolve()
                if not p.is_relative_to(F.resolve()) or sha(p) != value:
                    raise ValueError('source closure changed: ' + rel)
        if action == 'restore' and not (T / 'applied.json').exists():
            raise ValueError('transaction not applied')
        marker = T / (('recover-%d-%d.json' % (os.getpid(), time.time_ns())) if action == 'recover' else action + '-result.json')
        if marker.exists():
            raise FileExistsError('action already recorded')
        execute(operations(m, action), marker, T / 'applied.json', action)
        print(json.dumps({'action': action, 'files': len(REL), 'manifest_sha256': PIN, 'fresh_production_gate_required': True}))
    finally:
        for p in reversed(guards):
            p.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'apply', 'restore', 'recover'))
    action = parser.parse_args().action
    prepare() if action == 'prepare' else run(action)
