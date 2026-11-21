"""Run the serialized build command while recording and watching its source inputs.

This is a supplementary evidence wrapper, not a replacement for build locks,
function matching, mutation checks or gameplay. Reports stay in private m3/out.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CODE_SUFFIXES = {'.py', '.cmd', '.bat', '.h', '.hpp', '.cpp', '.c', '.inl', '.inc', '.def', '.rc'}
GENERATED_DIRS = {'out', 'gen', 'logs', 'snapshot', '__pycache__', '.git', 'obj', 'obj_v3', 'obj_v2', 'obj_v1'}


def paths_to_watch(project, explicit_inputs):
    paths = set()
    roots = [project / 'runtime-next', project / 'fnv_decomp/src',
             project / 'fnv_decomp/include', project / 'fnv_decomp/tools']
    for root in roots:
        for current, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d.lower() not in GENERATED_DIRS]
            # Class-analysis scripts are independent of the build. Only the
            # explicitly imported production helpers and this wrapper are inputs.
            if Path(current).resolve() == (project / 'runtime-next/m3/phase2').resolve():
                files = [name for name in files if name in ('library_overlay.py', 'cost245_records.py', 'run_frozen.py', 'selector_bridge.py', 'generation_bridge.py', 'validate_type_name_literal.py', 'rtti-descriptor-allowlist.json')]
                dirs[:] = []
            for name in files:
                path = Path(current) / name
                suffixes = {'.py', '.cmd', '.bat'} if root == project / 'runtime-next' else CODE_SUFFIXES
                if path.suffix.lower() in suffixes or (path.name == 'rtti-descriptor-allowlist.json' and Path(current).resolve() == (project / 'runtime-next/m3/phase2').resolve()):
                    paths.add(path.resolve())
    paths.add((project / 'fnv_decomp/build/units.json').resolve())
    paths.update(p.resolve() for p in explicit_inputs)
    return sorted(paths)


def snapshot(paths):
    result = {}
    for path in paths:
        data = path.read_bytes()
        stat = path.stat()
        result[str(path)] = dict(sha256=hashlib.sha256(data).hexdigest(), size=len(data),
                                 mtime_ns=stat.st_mtime_ns)
    return result


def changed(before, after):
    return sorted(p for p in set(before) | set(after)
                  if p not in before or p not in after or before[p]['sha256'] != after[p]['sha256'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--input', type=Path, action='append', default=[])
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('supply a command after --')
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    explicit = list(args.input)
    absent = []
    seeds = []
    if args.catalog:
        catalog = json.loads(args.catalog.read_bytes())
        if catalog.get('schema_version') != 1:
            raise ValueError('unsupported input catalog')
        explicit += [args.catalog] + [Path(p) for p in catalog['watch']]
        absent = [Path(p) for p in catalog['optional_absent']]
        seeds = [Path(p) for p in catalog['generated_seeds']]
        if any(p.exists() for p in absent):
            raise ValueError('catalog optional input appeared before launch; regenerate catalog')
    paths = paths_to_watch(PROJECT, explicit)
    before = snapshot(paths)
    with (evidence / 'inputs-before.json').open('x', encoding='utf-8') as stream:
        json.dump(before, stream, indent=2)
    if seeds:
        seed_folder = evidence / 'generated-seeds-before'
        seed_folder.mkdir()
        seed_manifest = snapshot(seeds)
        for index, path in enumerate(seeds):
            shutil.copy2(path, seed_folder / ('%d-%s' % (index, path.name)))
        with (seed_folder / 'manifest.json').open('x', encoding='utf-8') as stream:
            json.dump(seed_manifest, stream, indent=2)
    config = {k: v for k, v in os.environ.items()
              if k.startswith(('FNV_M3', 'FNV_COFF_WEAK')) or k in ('DV_M3', 'DV3_SKIP', 'FNV_DV1_LIB_COFF_INDEX_V2')}
    # Deliberately record only this allowlisted build configuration, never the
    # whole environment, which may contain unrelated private credentials.
    with (evidence / 'command.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(command=command, build_environment=config), stream, indent=2)
    observed_changes = set()
    started = time.time()
    process = subprocess.Popen(command, cwd=PROJECT, stdin=subprocess.DEVNULL)
    with (evidence / 'process.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(pid=process.pid, started_unix=started), stream)
    while process.poll() is None:
        for path in paths:
            try:
                stat = path.stat()
                old = before[str(path)]
                if stat.st_size != old['size'] or stat.st_mtime_ns != old['mtime_ns']:
                    observed_changes.add(str(path))
            except OSError:
                observed_changes.add(str(path))
        observed_changes.update(str(p) for p in absent if p.exists())
        time.sleep(2)
    after = snapshot(paths_to_watch(PROJECT, explicit))
    observed_changes.update(str(p) for p in absent if p.exists())
    differences = changed(before, after)
    with (evidence / 'inputs-after.json').open('x', encoding='utf-8') as stream:
        json.dump(after, stream, indent=2)
    stable = not differences and not observed_changes
    result = dict(command_rc=process.returncode, input_freeze_passed=stable,
                  watched_files=len(before), final_digest_changes=differences,
                  observed_metadata_changes=sorted(observed_changes),
                  seconds=round(time.time() - started, 1),
                  scope='Source/recipe and explicitly named input identity only. Does not prove all environment/toolchain dependencies, matching, placement, gameplay or whole-phase completion.')
    with (evidence / 'result.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(dict(command_rc=process.returncode, input_freeze_passed=stable,
                          watched_files=len(before), observed_changes=len(observed_changes),
                          final_digest_changes=len(differences))), flush=True)
    if process.returncode or not stable:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
