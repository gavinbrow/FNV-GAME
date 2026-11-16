"""Synthetic protocol tests; no processes, compiler, reference or native calls."""
import datetime as dt
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'tools/rebuild/factory_held_launcher_v2.py'
spec = importlib.util.spec_from_file_location('held_test', PATH)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
cs = importlib.util.spec_from_file_location('child_test', PATH.with_name('factory_held_child_v2.py'))
c = importlib.util.module_from_spec(cs); cs.loader.exec_module(c)


class HeldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, body):
        path = self.root / name; path.write_bytes(body)
        return str(path), hashlib.sha256(body).hexdigest()

    def lease_profile(self):
        self.now = dt.datetime.now(dt.timezone.utc)
        self.row = dict(owner='/root/test', resource='CPU_heavy', slot=1,
                        state='granted', granted_utc=(self.now - dt.timedelta(seconds=1)).isoformat(),
                        max_seconds=900, scope='fixed-op', input_pins={'source': 'a' * 64}, review_sha256='b' * 64)
        self.registry = self.root / 'resource-leases.json'
        self.write_registry()
        return dict(owner='/root/test', slot=1, registry=str(self.registry),
                    lease_sha256=h.digest({k: v for k, v in self.row.items() if k != 'state'}))

    def write_registry(self, rows=None):
        self.registry.write_text(json.dumps(dict(schema_version=1, CPU_heavy_capacity=2,
                                                leases=[self.row] if rows is None else rows)))

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            json.loads('{"pid":1,"pid":2}', object_pairs_hook=h.pairs)

    def test_pin_reads_snapshot_and_rejects_drift(self):
        path, pin = self.put('source.py', b'x=1\n')
        self.assertEqual(h.read_pin(path, pin), b'x=1\n')
        Path(path).write_bytes(b'x=2\n')
        with self.assertRaisesRegex(ValueError, 'hash'):
            h.read_pin(path, pin)

    def test_pinned_file_bound(self):
        path, pin = self.put('large', b'ab')
        with self.assertRaisesRegex(ValueError, 'bound'):
            h.read_pin(path, pin, 1)

    def test_stream_hash_bounds_and_changed_input(self):
        path, pin = self.put('metadata', b'x' * (h.MAX_FRAME + 13))
        self.assertEqual(h.stream_pin(path, pin, 2 * h.MAX_FRAME), h.MAX_FRAME + 13)
        with self.assertRaisesRegex(ValueError, 'bound'): h.stream_pin(path, pin, h.MAX_FRAME)
        Path(path).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'hash'): h.stream_pin(path, pin, h.MAX_FRAME)

    def test_metadata_exact_count_and_streaming_caps(self):
        profile = dict(parent_source='parent', parent_sha256='a', child_source='child', child_sha256='b',
                       python='python', python_sha256='c', sources={}, metadata_inputs={str(i): 'd' for i in range(22)})
        with patch.object(h, 'read_pin', lambda *args: b''), patch.object(h, 'source_snapshot', lambda *args: {}):
            with patch.object(h, 'stream_pin', lambda path, pin, limit: 8 * h.MAX_FRAME):
                h.verify_authorities(profile)
            with patch.object(h, 'stream_pin', lambda path, pin, limit: 9 * h.MAX_FRAME):
                with self.assertRaisesRegex(ValueError, 'aggregate metadata'): h.verify_authorities(profile)
            profile['metadata_inputs'].pop('0')
            with self.assertRaisesRegex(ValueError, 'exact metadata count'): h.verify_authorities(profile)

    def test_current_grant_and_running_same_identity(self):
        profile = self.lease_profile(); grant = h.lease(profile, self.now)
        self.row['state'] = 'running'; self.write_registry()
        self.assertEqual(h.lease(profile, self.now), grant)

    def test_lease_wrong_owner_slot_scope_source_revocation_expiry(self):
        for field, value in [('owner', '/root/other'), ('slot', 2), ('scope', 'foreign'),
                             ('input_pins', {'source': 'c' * 64}), ('state', 'released')]:
            with self.subTest(field=field):
                profile = self.lease_profile(); self.row[field] = value; self.write_registry()
                with self.assertRaises(ValueError): h.lease(profile, self.now)
        profile = self.lease_profile()
        with self.assertRaisesRegex(ValueError, 'expiry'):
            h.lease(profile, self.now + dt.timedelta(seconds=900))

    def test_duplicate_lease_and_lock_fail_closed(self):
        profile = self.lease_profile(); self.write_registry([self.row, self.row])
        with self.assertRaisesRegex(ValueError, 'unique'): h.lease(profile, self.now)
        self.write_registry(); (self.root / 'resource-leases.lock').touch()
        with self.assertRaisesRegex(ValueError, 'locked'): h.lease(profile, self.now)

    def test_phase_order_repeat_and_missing_completion(self):
        guard = h.Guard({'phase_schedule': ['before', 'after', 'before', 'after']}, {}, None, None)
        guard.refresh = lambda: None; guard.record = lambda phase: None
        with self.assertRaisesRegex(ValueError, 'reordered'): guard.check('after')
        guard.check('before')
        with self.assertRaisesRegex(ValueError, 'incomplete'): guard.complete()
        for phase in ['after', 'before', 'after']: guard.check(phase)
        guard.complete()
        with self.assertRaisesRegex(ValueError, 'reordered'): guard.check('after')

    def test_failed_phase_guard_does_not_advance(self):
        guard = h.Guard({'phase_schedule': ['publication']}, {}, None, None)
        guard.refresh = lambda: h.need(False, 'revoked')
        with self.assertRaisesRegex(ValueError, 'revoked'): guard.check('publication')
        self.assertEqual(guard.checks, [])

    def test_snapshot_executes_verified_bytes_not_changed_disk(self):
        path, pin = self.put('project_module.py', b'value=1\n')
        profile = {'sources': {'test_project_snapshot': dict(path=path, sha256=pin)}}
        snapshots = h.source_snapshot(profile); Path(path).write_bytes(b'value=2\n')
        finder = h.SnapshotFinder(profile, snapshots)
        module = types.ModuleType('test_project_snapshot'); finder.exec_module(module)
        self.assertEqual(module.value, 1)
        with self.assertRaises(ValueError): h.source_snapshot(profile)

    def test_preloaded_project_module_is_rejected(self):
        finder = h.SnapshotFinder({}, {'already_loaded': b''})
        with patch.dict(sys.modules, {'already_loaded': types.ModuleType('already_loaded')}):
            with self.assertRaisesRegex(ValueError, 'preloaded'): finder.find_spec('already_loaded')

    def test_unverified_project_import_no_disk_fallback(self):
        folder = self.root / 'tools' / 'rebuild'; folder.mkdir(parents=True)
        parent = folder / 'parent.py'; parent.touch()
        (folder / 'unreviewed.py').write_text('raise RuntimeError("must never run")')
        finder = h.SnapshotFinder({'parent_source': str(parent), 'project_module_roles': []}, {})
        with patch.object(sys, 'path', [str(folder)]):
            with self.assertRaisesRegex(ValueError, 'unbound nonstdlib'): finder.find_spec('unreviewed')

    def test_held_eof_truncation_multiple_frames_and_wrong_pin_exit(self):
        for raw in (b'', b'{', b'{}', b'{}\n{}\n', b' { }\n'):
            with self.subTest(raw=raw), patch.object(c.sys, 'stdin', types.SimpleNamespace(buffer=io.BytesIO(raw))):
                with self.assertRaises(ValueError): c.main()
        path, _ = self.put('parent.py', b'raise RuntimeError("must never run")')
        raw = h.canonical(dict(parent_source=path, parent_sha256='0' * 64)) + b'\n'
        with patch.object(c.sys, 'stdin', types.SimpleNamespace(buffer=io.BytesIO(raw))):
            with self.assertRaisesRegex(ValueError, 'parent source pin'): c.main()

    def test_parent_command_fresh_isolated_pinned_no_execution(self):
        command = h.parent_command('python.exe', 'parent.py', 'a' * 64, 'profile.json', 'b' * 64)
        self.assertEqual(command[:5], ['python.exe', '-I', '-S', '-B', '-c'])
        self.assertIn('sha256(b).hexdigest()', command[5])
        compile(command[5], '<synthetic-loader>', 'exec')

    def make_guard(self):
        profile = self.lease_profile()
        profile.update(control=str(self.root), python=str(self.root / 'python.exe'),
                       phase_schedule=['bootstrap'])
        parent = dict(pid=101, creation=123, image=profile['python'])
        child = dict(pid=202, creation=456, image=profile['python'])
        envelope = dict(nonce='a' * 64, job='Local\\FNV-held-' + 'a' * 64,
                        parent=parent, child=child, profile_path='bound-profile', profile_sha256='b' * 64)
        (self.root / 'started.json').write_bytes(h.canonical(envelope))
        (self.root / 'intent.json').write_bytes(h.canonical(dict(profile_sha256=envelope['profile_sha256'],
            session={k: v for k, v in envelope.items() if k != 'child'}, lease=h.lease(profile), state='once-only-intent')))
        events = []
        class FakeKernel:
            def __init__(self):
                self.k = types.SimpleNamespace(OpenJobObjectW=lambda *args: 99,
                    CloseHandle=lambda handle: events.append('close') or True, GetCurrentProcess=lambda: 88)
                self.parent = 101; self.bad_identity = False; self.member = True; self.memory = h.MEMORY
            def parent_pid(self): return self.parent
            def open_identity(self, expected):
                events.append('identity')
                h.need(not self.bad_identity, 'PID reuse/image identity')
            def job_check(self, handle): h.kernel_limits(0x2200, self.memory)
            def in_job(self, process, handle): return self.member
            def census(self, handle): return [202]
        kernel = FakeKernel()
        return h.Guard(profile, envelope, kernel, None), events

    def refresh_patches(self, guard):
        return patch.multiple(h, load_profile=lambda *args: guard.profile, verify_authorities=lambda profile: None)

    def test_child_checks_close_before_postclose_identity_and_payload(self):
        guard, events = self.make_guard()
        with self.refresh_patches(guard), patch.object(h.os, 'getpid', lambda: 202):
            guard.check('bootstrap')
        self.assertEqual(events, ['identity', 'identity', 'close', 'identity', 'identity'])
        guard.complete()

    def test_wrong_parent_child_pid_reused_pid_nonce_profile_and_session(self):
        for fault in ('parent', 'child', 'reuse', 'nonce', 'profile', 'session'):
            guard, _ = self.make_guard()
            with self.subTest(fault=fault):
                if fault == 'parent': guard.kernel.parent = 999
                if fault == 'child': guard.envelope['child']['pid'] = 999
                if fault == 'reuse': guard.kernel.bad_identity = True
                if fault == 'nonce': guard.envelope['nonce'] = 'g' * 64
                if fault == 'session': (self.root / 'started.json').write_text('{}')
                with self.refresh_patches(guard), patch.object(h.os, 'getpid', lambda: 202):
                    if fault == 'profile':
                        with patch.object(h, 'load_profile', lambda *args: {}):
                            with self.assertRaises(ValueError): guard.check('bootstrap')
                    else:
                        with self.assertRaises(ValueError): guard.check('bootstrap')
                self.assertEqual(guard.checks, [])

    def test_job_limit_breakaway_membership_and_close_failure(self):
        for flags, memory in [(0x200, h.MEMORY), (0x2200 | 0x800, h.MEMORY), (0x2200, h.MEMORY - 1)]:
            with self.assertRaisesRegex(ValueError, 'Job cap'): h.kernel_limits(flags, memory)
        for fault in ('membership', 'memory', 'close'):
            guard, events = self.make_guard()
            if fault == 'membership': guard.kernel.member = False
            if fault == 'memory': guard.kernel.memory = h.MEMORY - 1
            if fault == 'close': guard.kernel.k.CloseHandle = lambda handle: events.append('close-failed') or False
            with self.subTest(fault=fault), self.refresh_patches(guard), patch.object(h.os, 'getpid', lambda: 202):
                with self.assertRaises(ValueError): guard.check('bootstrap')
            self.assertEqual(guard.checks, [])
            self.assertEqual(events.count('close') + events.count('close-failed'), 1)

    def test_lease_revoked_between_job_close_and_protected_work(self):
        guard, events = self.make_guard()
        def revoke(handle):
            events.append('close'); self.row['state'] = 'released'; self.write_registry(); return True
        guard.kernel.k.CloseHandle = revoke
        with self.refresh_patches(guard), patch.object(h.os, 'getpid', lambda: 202):
            with self.assertRaisesRegex(ValueError, 'revoked'): guard.check('bootstrap')
        self.assertEqual(guard.checks, [])

    def test_after_entry_failure_keeps_incomplete_schedule(self):
        guard = h.Guard({'phase_schedule': ['after-publication', 'after-entry']}, {}, None, None)
        guard.refresh = lambda: None; guard.record = lambda phase: None
        guard.check('after-publication')
        guard.refresh = lambda: h.need(False, 'lease expired after publication')
        with self.assertRaisesRegex(ValueError, 'after publication'): guard.check('after-entry')
        with self.assertRaisesRegex(ValueError, 'incomplete'): guard.complete()

    def profile_fixture(self):
        private = ROOT / 'build' / 'rebuild'; private.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='held-synthetic-', dir=private)
        self.addCleanup(temporary.cleanup); area = Path(temporary.name)
        source = area / 'fixture.py'; source.write_bytes(b'fixture=True\n')
        python = area / 'authored-runtime-placeholder'; python.write_bytes(b'not executable')
        profile = self.lease_profile()
        profile.update(schema='held-factory-v1', role='factory-v14', memory_bytes=h.MEMORY, seconds=h.SECONDS,
            entry=['cached_frontier_code_factory_v14_driver', 'held_entry'], operation={'fixed': 'operation-A'},
            phase_schedule=['bootstrap', 'before-entry', 'before-metadata', 'after-metadata',
                 'before-source-snapshots', 'after-source-snapshots', 'before-reference', 'after-reference'] +
                ['before-source', 'after-source', 'before-object', 'after-object'] * 15 +
                ['before-final-stability', 'after-final-stability', 'before-publication', 'after-publication', 'after-entry'],
            project_module_roles=['cached_frontier_code_factory_v14_driver'],sources={'cached_frontier_code_factory_v14_driver': {'path': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}},
            parent_source=str(PATH), parent_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),
            child_source=str(PATH.with_name('factory_held_child_v2.py')),
            child_sha256=hashlib.sha256(PATH.with_name('factory_held_child_v2.py').read_bytes()).hexdigest(),
            python=str(python), python_sha256=hashlib.sha256(python.read_bytes()).hexdigest(),
            control=str(area / 'control'), output=str(area / 'output'), allowed_outputs=['receipt.json'], metadata_inputs={})
        for i in range(22):
            path = area / ('meta-%d.json' % i); path.write_bytes(b'{}')
            profile['metadata_inputs'][str(path)] = hashlib.sha256(b'{}').hexdigest()
        path = area / 'profile.json'; path.write_bytes(h.canonical(profile))
        return profile, path, hashlib.sha256(path.read_bytes()).hexdigest()

    def test_profile_operation_role_runtime_and_source_drift(self):
        profile, path, pin = self.profile_fixture()
        self.assertEqual(h.load_profile(path, pin), profile)
        profile['operation'] = {'fixed': 'operation-B'}; path.write_bytes(h.canonical(profile))
        with self.assertRaisesRegex(ValueError, 'hash'): h.load_profile(path, pin)
        profile['role'] = 'caller-approved'; path.write_bytes(h.canonical(profile))
        with self.assertRaisesRegex(ValueError, 'fixed production'): h.load_profile(path, hashlib.sha256(path.read_bytes()).hexdigest())
        profile['role'] = 'factory-v14'; Path(profile['python']).write_bytes(b'changed runtime')
        with self.assertRaisesRegex(ValueError, 'hash'): h.verify_authorities(profile)

    def launch_fake(self, fault=None):
        profile, path, pin = self.profile_fixture(); events = []; state = {'poll': False, 'resumed': False}
        class FakeKernel:
            parent_in_job = False
            def __init__(self):
                def pipe(reader, writer, security, size):
                    reader._obj.value = 11; writer._obj.value = 12; return True
                def write(handle, frame, size, count, overlapped):
                    events.append('write'); count._obj.value = size
                    state['envelope'] = json.loads(frame)
                    return True
                self.k = types.SimpleNamespace(GetCurrentProcess=lambda: 99, CreatePipe=pipe,
                    SetHandleInformation=lambda *args: True, WriteFile=write,
                    CloseHandle=lambda handle: events.append('close-pipe-%d' % handle) or True)
            def identity(self, handle, pid):
                return dict(pid=int(pid), creation=123 if handle == 99 else 456, image=profile['python'])
            def named_job(self, name): events.append('job'); return 44
            def start_held(self, command, cwd, job, reader):
                events.append('created-suspended'); state['command'] = command
                return types.SimpleNamespace(pid=202, process=22, thread=23)
            def assign(self, job, child): events.append('assigned')
            def open_identity(self, expected): pass
            def creation(self, child): return 456
            def job_check(self, job): events.append('job-query')
            def resume(self, child):
                assert (Path(profile['control']) / 'started.json').is_file()
                events.append('resume'); state['resumed'] = True
            def census(self, job): return [] if state['poll'] or state.get('terminated') else [202]
            def poll(self, child):
                state['poll'] = True
                if fault == 'late-source': Path(profile['python']).write_bytes(b'drift after child publication')
                return 3 if fault == 'incomplete' else 0
            def terminate_job(self, job): events.append('terminate-owned-job'); state['terminated'] = True
            def terminate_process(self, child): events.append('terminate-owned-process')
            def wait(self, child): events.append('wait-owned'); return 2
            def close_process(self, child): events.append('close-owned-process')
            def close_job(self, job): events.append('close-owned-job')
        kernel = FakeKernel(); original_lease = h.lease
        def lease(profile):
            if fault == 'revoked' and state['resumed']: raise ValueError('lease revoked')
            return original_lease(profile)
        clock_values = iter([0, 901, 902, 903, 904])
        clock = (lambda: next(clock_values)) if fault == 'timeout' else (lambda: 0)
        with patch.object(h, 'native', lambda old: kernel), patch.object(h.sys, 'flags', types.SimpleNamespace(isolated=1, no_site=1)), \
             patch.object(h.sys, 'dont_write_bytecode', True), patch.object(h, 'lease', lease), \
             patch.object(h.time, 'monotonic', clock):
            receipt = h.launch(path, pin)
        return receipt, events, state, profile

    def test_mocked_parent_full_success_order_and_canonical_frame(self):
        receipt, events, state, profile = self.launch_fake()
        self.assertEqual(receipt['status'], 'completed-unreviewed')
        self.assertFalse(receipt['output_quarantined'])
        self.assertLess(events.index('assigned'), events.index('resume'))
        self.assertLess(events.index('resume'), events.index('write'))
        self.assertLess(events.index('write'), events.index('close-pipe-12'))
        self.assertNotIn('terminate-owned-job', events)
        self.assertEqual(state['envelope']['child']['creation'], 456)
        self.assertEqual(state['command'][1:5], ['-I', '-S', '-B', '-c'])
        self.assertEqual(json.loads((Path(profile['control']) / 'started.json').read_bytes()), state['envelope'])

    def test_mocked_parent_timeout_revocation_incomplete_and_late_failure_quarantine(self):
        for fault in ('timeout', 'revoked', 'incomplete', 'late-source'):
            with self.subTest(fault=fault):
                receipt, events, state, profile = self.launch_fake(fault)
                self.assertEqual(receipt['status'], 'failed')
                self.assertTrue(receipt['output_quarantined'])
                self.assertTrue(receipt['outputs_require_successful_terminal_and_independent_review'])
                self.assertIn('terminate-owned-job', events)
                self.assertIn('wait-owned', events)
                self.assertEqual(events.count('close-owned-process'), 1)
                self.assertEqual(events.count('close-owned-job'), 1)
                self.assertTrue((Path(profile['control']) / 'terminal.json').is_file())

    def test_mocked_child_entry_result_schedule_and_incomplete_exit(self):
        import builtins
        for status, blocked, expected in [('completed-unreviewed', 0, None), ('completed-incomplete', 1, 3),
                                           ('unknown', 0, ValueError)]:
            profile, path, pin = self.profile_fixture()
            envelope = dict(parent_source=str(PATH), parent_sha256=profile['parent_sha256'],
                profile_path=str(path), profile_sha256=pin, nonce='a' * 64, job='Local\\FNV-held-' + 'a' * 64,
                parent={}, child={})
            states = []
            class FakeGuard:
                def __init__(self, profile, envelope, kernel, old): self.profile = profile; self.checks = []
                def check(self, phase):
                    self.assert_phase(phase); self.checks.append(phase); states.append(phase)
                def assert_phase(self, phase):
                    h.need(phase == self.profile['phase_schedule'][len(self.checks)], 'mocked child schedule')
                def complete(self): h.need(self.checks == self.profile['phase_schedule'], 'mocked child incomplete')
            def held_entry(profile, guard):
                # This test mocks the driver adapter; the separate real
                # capability tests below cover authentication itself.
                h._ENTRY_CLAIM = guard
                for phase in profile['phase_schedule'][2:-1]: guard.check(phase)
                return dict(status=status, summary=dict(requested=15, emitted=15-blocked, blocked=blocked))
            original_import = builtins.__import__
            def importer(name, *args, **kwargs):
                if name == 'cached_frontier_code_factory_v14_driver': return types.SimpleNamespace(held_entry=held_entry)
                return original_import(name, *args, **kwargs)
            with self.subTest(status=status), patch.object(h, 'old_module', lambda: None), patch.object(h, 'native', lambda old: None), \
                 patch.object(h, 'preflight_imports', lambda *args: None), \
                 patch.object(h, 'Guard', FakeGuard), patch.object(h.sys, 'flags', types.SimpleNamespace(isolated=1, no_site=1)), \
                 patch.object(h.sys, 'dont_write_bytecode', True), patch.object(h.sys, 'path', [sys.base_prefix]), \
                 patch.object(h.sys, 'meta_path', list(sys.meta_path)), patch.object(builtins, '__import__', importer):
                if expected is ValueError:
                    with self.assertRaisesRegex(ValueError, 'terminal status'): h.child_main(envelope)
                elif expected == 3:
                    with self.assertRaises(SystemExit) as error: h.child_main(envelope)
                    self.assertEqual(error.exception.code, 3)
                else: h.child_main(envelope)
            self.assertEqual(states, profile['phase_schedule'])

    def issued_runtime_fixture(self):
        profile, path, pin = self.profile_fixture(); control = Path(profile['control']); control.mkdir()
        runtime = types.ModuleType(h.RUNTIME_NAME); runtime.__file__ = str(PATH)
        exec(compile(PATH.read_bytes(), str(PATH), 'exec'), runtime.__dict__)
        verifier = types.ModuleType('_independently_verified_bootstrap'); verifier.__file__ = str(PATH)
        exec(compile(PATH.read_bytes(), str(PATH), 'exec'), verifier.__dict__)
        envelope = dict(parent_source=str(PATH), parent_sha256=profile['parent_sha256'], profile_path=str(path),
            profile_sha256=pin, nonce='a' * 64, job='Local\\FNV-held-' + 'a' * 64,
            parent=dict(pid=101, creation=123, image=profile['python']),
            child=dict(pid=h.os.getpid(), creation=456, image=profile['python']))
        (control / 'started.json').write_bytes(h.canonical(envelope))
        (control / 'intent.json').write_bytes(h.canonical(dict(profile_sha256=pin,
            session={k: v for k, v in envelope.items() if k != 'child'}, lease=h.lease(profile), state='once-only-intent')))
        events = []
        class Kernel:
            def __init__(self):
                self.k = types.SimpleNamespace(OpenJobObjectW=lambda *args: 99,
                    CloseHandle=lambda handle: events.append('job-close') or True, GetCurrentProcess=lambda: 88)
            def parent_pid(self): return 101
            def open_identity(self, expected): events.append('identity')
            def job_check(self, handle): events.append('job-query')
            def in_job(self, *args): return True
            def census(self, handle): return [h.os.getpid()]
        guard = runtime.Guard(profile, envelope, Kernel(), None)
        guard.check('bootstrap'); guard.check('before-entry')
        runtime._ACTIVE_SESSION = (guard, profile, runtime.digest(envelope), runtime.digest(profile['operation']))
        return verifier, runtime, profile, guard, events

    def test_real_capability_fresh_session_once_and_no_op_or_unissued_guard_rejected(self):
        verifier, runtime, profile, guard, events = self.issued_runtime_fixture()
        class FakeGuard:
            def __init__(self): self.profile = profile
            def check(self, phase): pass
            def refresh(self): pass
        with patch.dict(sys.modules, {h.RUNTIME_NAME: runtime}), \
             patch.object(sys, 'flags', types.SimpleNamespace(isolated=1, no_site=1)), patch.object(sys, 'dont_write_bytecode', True):
            for fake in (FakeGuard(), runtime.Guard(profile, guard.envelope, guard.kernel, None)):
                before = list(events)
                with self.assertRaises(ValueError):
                    verifier.authenticate_runtime(runtime, profile, fake, parent_sha256=profile['parent_sha256'])
                self.assertEqual(events, before)
            before = len(events)
            self.assertIs(verifier.authenticate_runtime(runtime, profile, guard, parent_sha256=profile['parent_sha256']), guard)
            self.assertIn('job-query', events[before:]); self.assertIn('job-close', events[before:])
            with self.assertRaisesRegex(ValueError, 'already claimed'):
                verifier.authenticate_runtime(runtime, profile, guard, parent_sha256=profile['parent_sha256'])

    def test_forged_runtime_no_op_verifier_class_or_wrong_globals_rejected(self):
        verifier, runtime, profile, guard, events = self.issued_runtime_fixture()
        for fault in ('no-op-verifier', 'forged-class', 'wrong-globals'):
            forged = types.ModuleType(h.RUNTIME_NAME); forged.__file__ = str(PATH)
            exec(compile(PATH.read_bytes(), str(PATH), 'exec'), forged.__dict__)
            forged_guard = forged.Guard(profile, guard.envelope, guard.kernel, None)
            if fault == 'no-op-verifier':
                exec('def require_held_guard(profile, guard):\n return guard\n', forged.__dict__)
            elif fault == 'forged-class':
                exec('class Guard:\n def check(self, phase): pass\n def refresh(self): pass\n', forged.__dict__)
                forged_guard = forged.Guard()
            else:
                forged.require_held_guard = runtime.require_held_guard
            before = list(events)
            with self.subTest(fault=fault), patch.dict(sys.modules, {h.RUNTIME_NAME: forged}):
                with self.assertRaises(ValueError):
                    verifier.authenticate_runtime(forged, profile, forged_guard, parent_sha256=profile['parent_sha256'])
            self.assertEqual(events, before)

    def test_issued_capability_rejects_profile_operation_session_and_live_lease_drift(self):
        for fault in ('profile', 'operation', 'session', 'lease'):
            verifier, runtime, profile, guard, events = self.issued_runtime_fixture()
            passed_profile = profile
            if fault == 'profile': passed_profile = dict(profile)
            if fault == 'operation': profile['operation'] = {'fixed': 'foreign'}
            if fault == 'session': guard.envelope['nonce'] = 'b' * 64
            if fault == 'lease': self.row['state'] = 'released'; self.write_registry()
            with self.subTest(fault=fault), patch.dict(sys.modules, {h.RUNTIME_NAME: runtime}), \
                 patch.object(sys, 'flags', types.SimpleNamespace(isolated=1, no_site=1)), patch.object(sys, 'dont_write_bytecode', True):
                with self.assertRaises(ValueError):
                    verifier.authenticate_runtime(runtime, passed_profile, guard, parent_sha256=profile['parent_sha256'])
            self.assertIsNone(runtime._ENTRY_CLAIM)

    def test_closed_project_roles_must_have_all_source_pins(self):
        profile,path,pin=self.profile_fixture()
        profile['project_module_roles'].append('omitted_project_role'); path.write_bytes(h.canonical(profile))
        with self.assertRaisesRegex(ValueError,'closed project role'):
            h.load_profile(path,hashlib.sha256(path.read_bytes()).hexdigest())

    def test_missing_project_role_never_resolves_installed_same_name(self):
        finder=h.SnapshotFinder({'project_module_roles':['omitted_project_role']},{})
        with patch.object(h.importlib.machinery.PathFinder,'find_spec',side_effect=AssertionError('fallback queried')):
            with self.assertRaisesRegex(ValueError,'missing project source role'): finder.find_spec('omitted_project_role')
        finder=h.SnapshotFinder({'project_module_roles':[]},{})
        with patch.object(h.importlib.machinery.PathFinder,'find_spec',side_effect=AssertionError('fallback queried')):
            with self.assertRaisesRegex(ValueError,'unbound nonstdlib'): finder.find_spec('installed_project_alias')

    def test_stdlib_same_name_outside_trusted_runtime_is_rejected_after_sys_path_insert(self):
        (self.root/'json.py').write_text('raise RuntimeError("unreviewed external module")')
        finder=h.SnapshotFinder({'project_module_roles':[]},{})
        with patch.object(sys,'path',[str(self.root)]):
            with self.assertRaisesRegex(ValueError,'outside trusted installation'): finder.find_spec('json')

    def test_both_literal_dynamic_import_forms_reject_unbound_module(self):
        import importlib
        (self.root/'unbound_tool.py').write_text('raise RuntimeError("must never execute")')
        finder=h.SnapshotFinder({'project_module_roles':[]},{})
        with patch.object(sys,'path',[str(self.root)]),patch.object(sys,'meta_path',[finder]+list(sys.meta_path)):
            for importer in (__import__,importlib.import_module):
                with self.assertRaisesRegex(ValueError,'unbound nonstdlib'): importer('unbound_tool')

    def test_preflight_rejects_preloaded_omitted_role_and_external_alias(self):
        profile={'project_module_roles':['project_role'],'parent_source':str(PATH)}
        with patch.dict(sys.modules,{'project_role':types.ModuleType('project_role')},clear=True):
            with self.assertRaisesRegex(ValueError,'missing project source role'): h.preflight_imports(profile,{})
            with self.assertRaisesRegex(ValueError,'project module preloaded'): h.preflight_imports(profile,{'project_role':b''})
        profile['project_module_roles']=[]
        fake=types.ModuleType('external_alias');fake.__file__=str(self.root/'outside.py')
        with patch.dict(sys.modules,{'external_alias':fake},clear=True):
            with self.assertRaisesRegex(ValueError,'nonstdlib'): h.preflight_imports(profile,{})

    def test_preflight_rejects_project_source_aliased_as_stdlib(self):
        fake=types.ModuleType('json');fake.__file__=str(PATH)
        with patch.dict(sys.modules,{'json':fake},clear=True):
            with self.assertRaisesRegex(ValueError,'project source alias'):
                h.preflight_imports({'project_module_roles':[],'parent_source':str(PATH)},{})

    def test_preflight_accepts_only_known_stdlib_origins(self):
        main=types.ModuleType('__main__')
        with patch.dict(sys.modules,{'__main__':main,'sys':sys,'json':json},clear=True):
            h.preflight_imports({'project_module_roles':[],'parent_source':str(PATH)},{})

    def test_grounded_typing_alias_identity_is_bound_to_trusted_parent(self):
        import typing
        with patch.dict(sys.modules,{'typing':typing,'typing.io':typing.io,'typing.re':typing.re},clear=True):
            h.preflight_imports({'project_module_roles':[],'parent_source':str(PATH)},{})
            with self.assertRaisesRegex(ValueError,'unverified typing alias'):
                h.runtime_origin('typing.io',None,types.ModuleType('typing.io'))

    def test_third_party_and_arbitrary_origins_under_python_prefix_rejected(self):
        for folder in ('Lib/site-packages','Lib/dist-packages','arbitrary'):
            origin=str(Path(sys.base_prefix)/folder/'json'/'third_party.py')
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                h.runtime_origin('json.third_party',types.SimpleNamespace(origin=origin))


if __name__ == '__main__': unittest.main()
