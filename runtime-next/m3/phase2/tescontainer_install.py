"""Generate/apply/restore the reviewed TESContainer pilot with exact input guards.

All protected edits are deterministic generator outputs. Apply/restore require
the coordinator's released build lane. No build, commit or publication is done.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tescontainer_experiment as experiment

PROJECT = experiment.PROJECT
FN = experiment.FN
PILOT = experiment.OUT
OUT = experiment.M3 / 'out/phase2-tescontainer-install-v1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def replace_unit(raw, index, replacement):
    text = raw.decode('utf-8')
    doc = json.loads(text)
    arrays = list(re.finditer(r'"units"\s*:\s*\[', text))
    if len(arrays) != 1:
        raise ValueError('ambiguous recipe array key')
    position = arrays[0].end()
    decoder = json.JSONDecoder()
    for current in range(index + 1):
        while text[position].isspace() or text[position] == ',':
            position += 1
        start = position
        value, position = decoder.raw_decode(text, position)
        if value != doc['units'][current]:
            raise ValueError('recipe range does not decode to expected unit')
    generated = text[:start] + json.dumps(replacement, indent=2) + text[position:]
    result = json.loads(generated)
    expected = json.loads(text)
    expected['units'][index] = replacement
    if result != expected:
        raise ValueError('recipe edit exceeds the selected unit')
    return generated.encode('utf-8')


def prepare():
    experiment.check_inputs()
    report_path = PILOT / 'comparison-v2.json'
    report = json.loads(report_path.read_bytes())
    mapped_path = PILOT / 'unit-overlay-v2.json'
    mapped = json.loads(mapped_path.read_bytes())
    if report.get('isolated_checks_passed') is not True or report['unit_overlay_sha256'] != experiment.digest(mapped_path):
        raise ValueError('reviewed isolated checks and exact unit recipe are required')
    if len(report['functions']) != 31 or report['metadata']['emitted_tables'] != 1:
        raise ValueError('unexpected reviewed scope')
    current_units = (FN / 'build/units.json').read_bytes()
    original = json.loads(current_units)['units'][980]
    if mapped['source'] != original['source'] or mapped['flags'] != original['flags'] or mapped['compiler'] != original['compiler']:
        raise ValueError('cannot change source path, compiler or flags')
    if len(mapped['functions']) != len(original['functions']):
        raise ValueError('cannot change function scope')
    for before, after in zip(original['functions'], mapped['functions']):
        if {k: v for k, v in before.items() if k != 'symbol'} != {k: v for k, v in after.items() if k != 'symbol'}:
            raise ValueError('cannot change function address, size or other recipe attributes')
    generated_units = replace_unit(current_units, 980, mapped)
    files = [(experiment.SOURCE, (PILOT / 'tescontainer.cpp').read_bytes()),
             ('include/TESContainer.h', (PILOT / 'TESContainer.h').read_bytes()),
             ('build/units.json', generated_units)]
    if (FN / 'include/TESContainer.h').exists():
        raise ValueError('canonical header target already exists')
    OUT.mkdir(parents=False, exist_ok=False)
    entries = []
    for index, (relative, data) in enumerate(files):
        path = FN / relative
        previous = path.read_bytes() if path.exists() else None
        generated_name = '%d.generated' % index
        (OUT / generated_name).write_bytes(data)
        if previous is not None:
            (OUT / ('%d.original' % index)).write_bytes(previous)
        entries.append(dict(path=relative, old_sha256=sha(previous) if previous is not None else None,
                            new_sha256=sha(data), generated=generated_name,
                            original=('%d.original' % index) if previous is not None else None))
    manifest = dict(schema_version=1, unit_index=980, files=entries,
                    evidence_sha256=experiment.digest(report_path),
                    scope='One native header and source-supported virtual override plus compiler-local literal-label recipe updates. Other TU class declarations/ODR remain open.')
    with (OUT / 'manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2)
    print(json.dumps(dict(files=len(entries), generated_units_sha256=sha(generated_units), status='prepared; not installed')))


def atomic_write(path, data):
    if OUT.resolve().drive != path.resolve().drive:
        raise ValueError('per-file atomic replacement requires one volume')
    # Unique private temporary files leave no protected-tree debris and cannot
    # block a later recovery after process death. Retain interrupted private
    # files for inspection; recovery always uses the hash-checked payloads.
    descriptor, name = tempfile.mkstemp(prefix=path.name + '.phase2-', dir=OUT)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise


def install(restore=False, recover=False):
    if (PROJECT / 'runtime-next/build.lock').exists():
        raise ValueError('build lane is locked; source transaction refused')
    manifest = json.loads((OUT / 'manifest.json').read_bytes())
    if experiment.digest(PILOT / 'comparison-v2.json') != manifest['evidence_sha256']:
        raise ValueError('reviewed comparison evidence changed')
    if restore and not recover and not (OUT / 'applied.json').exists():
        raise ValueError('no applied transaction to restore')
    result_path = OUT / ('recovered.json' if recover else 'restored.json' if restore else 'applied.json')
    if result_path.exists():
        raise FileExistsError('transaction action already recorded')
    operations = []
    for entry in manifest['files']:
        path = (FN / entry['path']).resolve()
        if not path.is_relative_to(FN.resolve()):
            raise ValueError('protected target escapes source tree')
        expected = entry['new_sha256'] if restore else entry['old_sha256']
        current = sha(path.read_bytes()) if path.exists() else None
        if recover:
            allowed = (entry['old_sha256'], entry['new_sha256'])
        else:
            allowed = (expected,)
        if current not in allowed:
            raise ValueError('protected file changed; refusing to overwrite: ' + entry['path'])
        name = entry['original'] if restore else entry['generated']
        data = (OUT / name).read_bytes() if name is not None else None
        wanted = entry['old_sha256'] if restore else entry['new_sha256']
        if (sha(data) if data is not None else None) != wanted:
            raise ValueError('transaction payload digest changed')
        operations.append((path, data, path.read_bytes() if path.exists() else None))
    completed = []
    marker_owned = False
    result = dict(action='recover' if recover else 'restore' if restore else 'apply', files=len(operations),
                  manifest_sha256=experiment.digest(OUT / 'manifest.json'))
    try:
        for path, data, previous in operations:
            if data is None and path.exists():
                path.unlink()
            elif data is not None:
                atomic_write(path, data)
            completed.append((path, previous))
        # Marker failure participates in rollback. The separate explicit recover
        # action handles process death between per-file atomic replacements.
        with result_path.open('x', encoding='utf-8') as stream:
            marker_owned = True
            json.dump(result, stream, indent=2)
    except BaseException:
        for path, previous in reversed(completed):
            if previous is None and path.exists():
                path.unlink()
            elif previous is not None:
                atomic_write(path, previous)
        if marker_owned and result_path.exists():
            result_path.unlink()
        raise
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'apply', 'restore', 'recover'])
    action = parser.parse_args().action
    {'prepare': prepare, 'apply': install, 'restore': lambda: install(True),
     'recover': lambda: install(True, True)}[action]()


if __name__ == '__main__':
    main()
