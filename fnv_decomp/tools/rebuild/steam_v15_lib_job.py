"""Fixed once-only Steam import LIB candidate; execution is disabled pending review.

The Job/output monitors are sampled. A started or uncertain operation is never
replayed. The resulting library is unreviewed metadata, not runtime approval.
"""
import json
import os
from pathlib import Path
import time

import factory_job_launcher as base
import crt_v15_job_launcher_v2 as adapter

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / 'build/rebuild/steam-import-v15-native-candidate-v1'
OUT = ROOT / 'build/rebuild/steam-import-v15-lib-once-v1'
VC = Path(r'C:\Projects\Decompilation\FNV\tools\vc2008\VC\bin')
OWNER = '/root/terra_integration_v15/startup_steam_fast'
REVIEW_PATH = None
LEASE_SCOPE = None
LIMIT = 1024 * 1024
ALLOWED = ('intent.json', 'started.json', 'terminal.json', 'lib.stdout',
           'lib.stderr', 'steam-api-callbacks.lib', 'steam-api-callbacks.exp')


def command():
    return [str(VC / 'lib.exe'), '/NOLOGO', '/MACHINE:X86',
            '/DEF:' + str(PACKET / 'steam-api-callbacks.def'),
            '/OUT:' + str(OUT / 'steam-api-callbacks.lib')]


def environment(systemroot):
    return {'SystemRoot': systemroot, 'PATH': str(VC) + os.pathsep + str(Path(systemroot) / 'System32'),
            'TEMP': str(OUT), 'TMP': str(OUT)}


def validate(review, review_hash):
    base.need(REVIEW_PATH is not None and LEASE_SCOPE is not None, 'fixed review and lease scope not installed')
    base.need(review.get('kind') == 'steam-v15-lib-once-review' and review.get('approved') is True,
              'independent review absent')
    base.need(review.get('driver_sha256') == base.file_hash(__file__) and
              review.get('base_sha256') == base.file_hash(base.__file__) and
              review.get('adapter_sha256') == base.file_hash(adapter.__file__), 'source identity')
    base.need(review.get('command') == command() and review.get('environment') == environment(os.environ['SystemRoot'])
              and review.get('output') == str(OUT), 'operation differs')
    base.need(review.get('limits') == {'seconds': 30, 'memory_bytes': 1024**3, 'log_bytes': LIMIT}, 'limits differ')
    pins = review.get('inputs'); base.need(type(pins) is dict and pins, 'input pins absent')
    required = [VC / 'lib.exe', PACKET / 'steam-api-callbacks.def', PACKET / 'operation-plan.json',
                ROOT / 'build/rebuild/steam-import-v15-owned-metadata-receipt.json']
    receipt = json.loads(required[-1].read_text())
    dll = Path(receipt['dll_path_private'])
    base.need(receipt['dll_sha256'] == '59ed854645eaa237463eb22f3c5a25f726d7cb2f29440f00a1ec0a4d73d0207a'
              and pins.get(str(dll)) == receipt['dll_sha256'], 'owned DLL pin differs')
    base.need(base.file_hash(required[1]) == 'd7803cd0b3020bd1e29c48d6de3cee4bc99c58f4e856efe8fc980dc3b591a736'
              and base.file_hash(required[-1]) == '2ff4fca25792a2494655a76292f51de86d1f06d1fad0125d168e0da0e82986d2',
              'fixed DEF or metadata receipt differs')
    # Pin the complete VC binary-directory DLL roster used by the selected PATH.
    dlls = sorted(p for p in VC.iterdir() if p.is_file() and p.suffix.lower() == '.dll')
    base.need(review.get('vc_dll_roster') == [str(p) for p in dlls], 'VC DLL roster differs')
    base.need(all(str(p) in pins for p in required + dlls), 'required inputs absent')
    base.verify_inputs({'inputs': pins})
    registry = json.loads(base.REGISTRY.read_text())
    rows = [x for x in registry['leases'] if x.get('owner') == OWNER and x.get('resource') == 'CPU_heavy'
            and x.get('slot') == review.get('slot') and x.get('scope') == LEASE_SCOPE]
    base.need(len(rows) == 1, 'lease scope absent')
    lease_pins = rows[0]['input_pins']
    base.need(lease_pins.get(Path(__file__).name) == base.file_hash(__file__) and
              lease_pins.get(Path(REVIEW_PATH).name) == review_hash, 'lease pins differ')
    return {'owner': OWNER, 'slot': review['slot'], 'lease_pins': lease_pins, 'review_sha256': review_hash}


def run(path, expected_hash):
    base.need(os.name == 'nt' and REVIEW_PATH is not None and LEASE_SCOPE is not None, 'operation disabled')
    path = Path(path).resolve(strict=True)
    base.need(path == Path(REVIEW_PATH).resolve(strict=True) and base.file_hash(path) == expected_hash, 'review differs')
    review = json.loads(path.read_text()); binding = validate(review, expected_hash); grant = base.lease(binding)
    base.need(base.lease_remaining(grant) > 35, 'lease too short')
    OUT.mkdir(exist_ok=False)
    base.save_new(OUT / 'intent.json', {'state': 'UNKNOWN', 'command': command(), 'review_sha256': expected_hash})
    backend = adapter.Windows(); job = child = None; owned = []; closed = drained = False; code = reason = None
    start = time.monotonic()
    try:
        base.need(base.lease(binding) == grant and base.lease_remaining(grant) > 32, 'lease changed')
        base.verify_inputs({'inputs': review['inputs']})
        job = backend.create_job(review['nested_parent_allowed'], 1024**3)
        with (OUT / 'lib.stdout').open('xb') as so, (OUT / 'lib.stderr').open('xb') as se:
            child = backend.start_logged(command(), OUT, job, review['environment'], so, se, owned)
            created = backend.creation(child); backend.assign(job, child)
            base.save_new(OUT / 'started.json', {'pid': int(child.pid), 'creation_time': created, 'state': 'suspended-in-job'})
            base.need(base.lease(binding) == grant and backend.creation(child) == created, 'lease or identity changed')
            base.verify_inputs({'inputs': review['inputs']}); backend.resume(child)
            while True:
                base.need(time.monotonic() - start < 30 and base.lease_remaining(grant) > 1, 'deadline')
                base.need(base.lease(binding) == grant, 'lease changed')
                base.need(base.owned_size(OUT, ALLOWED) <= 5 * 1024 * 1024, 'sampled tree limit')
                base.need(os.fstat(so.fileno()).st_size + os.fstat(se.fileno()).st_size <= LIMIT, 'sampled log limit')
                if code is None: code = backend.poll(child)
                if code is not None and not backend.census(job): drained = True; break
                time.sleep(.05)
            base.need(code == 0, 'LIB failed')
            base.verify_inputs({'inputs': review['inputs']})
    except BaseException as e:
        reason = type(e).__name__ + ': ' + str(e)
        if child is None and owned: child = owned[0]
        if child is not None:
            try:
                backend.terminate_job(job); code = backend.wait(child); until = time.monotonic() + 10
                while backend.census(job):
                    base.need(time.monotonic() < until, 'job drain timeout'); time.sleep(.05)
                drained = True
            except BaseException as stop: reason += '; termination uncertain: ' + type(stop).__name__
    finally:
        if child is not None:
            try: backend.close_process(child); closed = True
            except BaseException: reason = (reason or '') + '; process close uncertain'
        if job is not None:
            try: backend.close_job(job)
            except BaseException: reason = (reason or '') + '; Job close uncertain'
    archive = OUT / 'steam-api-callbacks.lib'
    digest = base.file_hash(archive, 4 * 1024 * 1024) if reason is None and archive.is_file() else None
    base.save_new(OUT / 'terminal.json', {'state': 'completed-unreviewed' if digest and drained and closed else 'failed-or-unknown',
        'reason': reason, 'returncode': code, 'job_empty_observed': drained, 'archive_sha256': digest,
        'elapsed_seconds': time.monotonic() - start, 'limits_sampled': True,
        'dll_loaded': False, 'alias_applied': False, 'runtime_provider_adopted': False})


if __name__ == '__main__':
    raise SystemExit('Disabled until exact review and fixed lease policy are installed.')
