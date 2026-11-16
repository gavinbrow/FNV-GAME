"""One-shot held factory successor; cooperative trusted local single writer.

The independently reviewed external profile digest is the admission identity.
There is no configured production operation here and no uncontained fallback.
Lease/process/filesystem checks are sampled, not hostile-user/ABA protection.
The known Python installation and stdlib are trusted, project imports are not.
"""
import ctypes
import datetime as dt
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import sysconfig
import time
import types

OLD_SHA = '8bdabc1ae1b7852c0686e754032ecd249ad2b2f1e5e5a6a055eb1f3b10c3c2d7'
MEMORY = 1024 ** 3
SECONDS = 900
MAX_FRAME = 1024 ** 2
RUNTIME_NAME = '_fnv_verified_held_bootstrap_v2'
_ACTIVE_SESSION = None
_ENTRY_CLAIM = None


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def bounded_json(path):
    with Path(path).open('rb') as stream:
        body = stream.read(MAX_FRAME + 1)
    need(len(body) <= MAX_FRAME, 'control JSON bound')
    return json.loads(body, object_pairs_hook=pairs)


def kernel_limits(flags, memory):
    need(flags == 0x2200 and memory == MEMORY, 'Job cap/breakaway mismatch')


def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def read_pin(path, pin, limit=MAX_FRAME):
    path = Path(path)
    before = path.stat()
    need(before.st_size <= limit and path.is_file(), 'pinned file bound/type')
    with path.open('rb') as stream:
        body = stream.read(limit + 1)
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'pinned file drift')
    need(len(body) <= limit and hashlib.sha256(body).hexdigest() == pin, 'pinned file hash')
    return body


def stream_pin(path, pin, limit):
    """Full fresh hash with bounded memory; no cross-phase hash/stat cache."""
    path = Path(path); before = path.stat()
    need(before.st_size <= limit and path.is_file(), 'stream input bound/type')
    sha = hashlib.sha256(); size = 0
    with path.open('rb') as stream:
        while True:
            part = stream.read(MAX_FRAME)
            if not part:
                break
            size += len(part); need(size <= limit, 'growing stream bound'); sha.update(part)
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'stream drift')
    need(sha.hexdigest() == pin, 'stream input hash')
    return size


def load_profile(path, pin):
    value = json.loads(read_pin(path, pin), object_pairs_hook=pairs)
    need(type(value) is dict and value.get('schema') == 'held-factory-v1', 'profile schema')
    need(value['role'] == 'factory-v14' and value['memory_bytes'] == MEMORY and
         type(value['memory_bytes']) is int and value['seconds'] == SECONDS and
         type(value['seconds']) is int, 'fixed production profile')
    need(value['entry'] == ['cached_frontier_code_factory_v14_driver', 'held_entry'], 'fixed entry')
    need(type(value['owner']) is str and value['owner'].startswith('/root/') and
         type(value['slot']) is int and value['slot'] in (1, 2), 'lease owner/slot')
    need(type(value['operation']) is dict and value['operation'], 'fixed operation')
    schedule = (['bootstrap', 'before-entry', 'before-metadata', 'after-metadata',
                 'before-source-snapshots', 'after-source-snapshots', 'before-reference', 'after-reference'] +
                ['before-source', 'after-source', 'before-object', 'after-object'] * 15 +
                ['before-final-stability', 'after-final-stability', 'before-publication', 'after-publication', 'after-entry'])
    need(value['phase_schedule'] == schedule, 'fixed 15-selection phase schedule')
    need(type(value['sources']) is dict and value['sources'], 'source closure')
    roles = value['project_module_roles']
    need(type(roles) is list and all(type(name) is str and name and all(part.isidentifier() for part in name.split('.')) for name in roles)
         and len(roles) == len(set(roles)) and set(roles) == set(value['sources']), 'closed project role/source binding')
    need(value['entry'][0] in value['sources'], 'entry absent from source closure')
    need(all(Path(v['path']).is_absolute() for v in value['sources'].values()), 'absolute source paths')
    need(Path(value['parent_source']).is_absolute() and Path(value['child_source']).is_absolute() and
         Path(value['python']).is_absolute() and Path(value['registry']).is_absolute(), 'absolute authority paths')
    return value


def source_snapshot(profile):
    need(len(profile['sources']) <= 128, 'source closure count')
    snapshots = {}; total = 0
    for name, item in profile['sources'].items():
        snapshots[name] = read_pin(item['path'], item['sha256'], min(4 * MAX_FRAME, 16 * MAX_FRAME - total))
        total += len(snapshots[name])
        need(total <= 16 * MAX_FRAME, 'aggregate source closure bound')
    return snapshots


def verify_authorities(profile):
    read_pin(profile['parent_source'], profile['parent_sha256'])
    read_pin(profile['child_source'], profile['child_sha256'])
    read_pin(profile['python'], profile['python_sha256'], 128 * MAX_FRAME)
    source_snapshot(profile)
    # These are reviewed metadata only. Objects, original/reference and selected
    # contribution payloads are deliberately absent: the driver reads them only
    # inside their separately guarded protected phases.
    total = 0
    need(len(profile['metadata_inputs']) == 22, 'exact metadata count')
    for path, pin in profile['metadata_inputs'].items():
        total += stream_pin(path, pin, min(64 * MAX_FRAME, 192 * MAX_FRAME - total))
        need(total <= 192 * MAX_FRAME, 'aggregate metadata bound')


def lease(profile, now=None):
    path = Path(profile['registry'])
    lock = path.with_name('resource-leases.lock')
    need(not lock.exists(), 'lease registry locked')
    before = path.stat()
    need(before.st_size <= 4 * MAX_FRAME, 'lease registry bound')
    with path.open('rb') as stream:
        body = stream.read(4 * MAX_FRAME + 1)
    after = path.stat()
    need(len(body) <= 4 * MAX_FRAME and not lock.exists() and
         (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'lease registry drift')
    registry = json.loads(body, object_pairs_hook=pairs)
    need(type(registry['schema_version']) is int and registry['schema_version'] == 1 and
         type(registry['CPU_heavy_capacity']) is int and registry['CPU_heavy_capacity'] == 2, 'lease schema')
    rows = [row for row in registry['leases'] if row.get('owner') == profile['owner'] and
            row.get('resource') == 'CPU_heavy' and type(row.get('slot')) is int and row['slot'] == profile['slot']]
    need(len(rows) == 1, 'unique owned lease')
    row = rows[0]
    need(row.get('state') in ('granted', 'running'), 'lease revoked')
    # State may transition granted -> running; all grant/scope/source values
    # remain bound, including any extra operation fields in the actual row.
    identity = {key: value for key, value in row.items() if key != 'state'}
    need(digest(identity) == profile['lease_sha256'], 'lease row identity')
    start = dt.datetime.fromisoformat(row['granted_utc'].replace('Z', '+00:00'))
    need(start.utcoffset() == dt.timedelta(0) and type(row['max_seconds']) is int and row['max_seconds'] > 0, 'lease UTC/duration')
    now = now or dt.datetime.now(dt.timezone.utc)
    need(start <= now < start + dt.timedelta(seconds=row['max_seconds']), 'lease expiry')
    return identity


def old_module():
    path = Path(__file__).with_name('factory_job_launcher.py')
    source = read_pin(path, OLD_SHA)
    module = types.ModuleType('_frozen_job_primitives')
    module.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module


def stdlib_name(name):
    return name.split('.')[0] in sys.stdlib_module_names or name in sys.builtin_module_names


def trusted_runtime_path(path):
    path = Path(path).resolve()
    need(not any(part.casefold() in ('site-packages', 'dist-packages') for part in path.parts), 'third-party runtime origin')
    stdlib = Path(sysconfig.get_path('stdlib')).resolve()
    extensions = Path(sys.base_prefix).resolve() / 'DLLs'
    archive = Path(sys.base_prefix).resolve() / ('python%d%d.zip' % sys.version_info[:2])
    need(path.is_relative_to(stdlib) or path.is_relative_to(archive) or
         (path.is_relative_to(extensions) and path.suffix.casefold() == '.pyd'), 'stdlib outside trusted installation')


def runtime_origin(name, spec, module=None):
    """Known stdlib/builtin names from the trusted Python installation only."""
    need(stdlib_name(name), 'unbound nonstdlib import/alias')
    origin = getattr(spec, 'origin', None) or getattr(module, '__file__', None)
    if origin in ('built-in', 'frozen'):
        return
    if origin is None:
        # CPython 3.12 installs these two deprecated typing aliases without a
        # module spec/file. Bind their actual trusted stdlib parent identities;
        # arbitrary originless aliases do not inherit this exception.
        if name in ('typing.io', 'typing.re') and module is not None:
            typing = sys.modules.get('typing')
            need(typing is not None and module is getattr(typing, name.split('.')[1], None), 'unverified typing alias')
            runtime_origin('typing', getattr(typing, '__spec__', None), typing)
            return
        need(name in sys.builtin_module_names, 'unbound runtime module origin')
        return
    trusted_runtime_path(origin)


def preflight_imports(profile, snapshots):
    """Reject project roles and aliases already loaded before snapshot import."""
    roles = set(profile['project_module_roles'])
    need(roles == set(snapshots), 'missing project source role')
    project = Path(profile['parent_source']).resolve().parents[2]
    for name, module in tuple(sys.modules.items()):
        if module is None:
            need(name not in roles and stdlib_name(name), 'preloaded blocked unverified role/alias')
            continue
        need(name not in roles, 'project module preloaded')
        if name == RUNTIME_NAME:
            need(type(module) is types.ModuleType and module.__dict__ is globals(), 'unverified runtime alias')
            continue
        if name == '__main__':
            need(getattr(module, '__file__', None) is None, 'nonisolated main alias')
            continue
        file = getattr(module, '__file__', None)
        if file and file not in ('built-in', 'frozen'):
            need(not Path(file).resolve().is_relative_to(project), 'preloaded project source alias')
        runtime_origin(name, getattr(module, '__spec__', None), module)


class SnapshotFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Only verified immutable bytes supply project imports; no disk fallback."""
    def __init__(self, profile, snapshots):
        self.profile = profile
        self.snapshots = snapshots

    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.snapshots:
            need(fullname not in sys.modules, 'project module preloaded')
            return importlib.util.spec_from_loader(fullname, self)
        # Omitted project roles and same-name installed modules cannot become
        # authority through a path fallback. Nonstdlib imports require pins.
        need(fullname not in self.profile['project_module_roles'], 'missing project source role')
        need(stdlib_name(fullname), 'unbound nonstdlib import')
        candidate = importlib.machinery.PathFinder.find_spec(fullname, path)
        if candidate:
            runtime_origin(fullname, candidate)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        name = module.__name__
        module.__file__ = self.profile['sources'][name]['path']
        exec(compile(self.snapshots[name], module.__file__, 'exec'), module.__dict__)


def native(old):
    class Kernel(old.Windows):
        def __init__(self):
            super().__init__()
            k = self.k
            for name, args, result in (
                ('OpenJobObjectW', [old.DWORD, ctypes.c_int, ctypes.c_wchar_p], old.HANDLE),
                ('OpenProcess', [old.DWORD, ctypes.c_int, old.DWORD], old.HANDLE),
                ('QueryFullProcessImageNameW', [old.HANDLE, old.DWORD, ctypes.c_wchar_p, ctypes.POINTER(old.DWORD)], ctypes.c_int),
                ('CreatePipe', [ctypes.POINTER(old.HANDLE), ctypes.POINTER(old.HANDLE), ctypes.c_void_p, old.DWORD], ctypes.c_int),
                ('SetHandleInformation', [old.HANDLE, old.DWORD, old.DWORD], ctypes.c_int),
                ('WriteFile', [old.HANDLE, ctypes.c_void_p, old.DWORD, ctypes.POINTER(old.DWORD), ctypes.c_void_p], ctypes.c_int)):
                f = getattr(k, name); f.argtypes = args; f.restype = result

        def named_job(self, name):
            self.parent_in_job = self.in_job(self.k.GetCurrentProcess())
            handle = self.k.CreateJobObjectW(None, name)
            need(handle and ctypes.get_last_error() != 183, 'new unique Job required')
            try:
                info = old.Extended(); info.basic.flags = 0x2000 | 0x200; info.job_memory = MEMORY
                flags = old.DWORD()
                need(self.k.GetHandleInformation(handle, ctypes.byref(flags)) and not flags.value & 1, 'Job inheritable')
                need(self.k.SetInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info)), 'Job cap set')
                self.job_check(handle)
                need(self.census(handle) == [], 'new Job nonempty')
                return handle
            except BaseException:
                self.k.CloseHandle(handle)
                raise

        def job_check(self, handle):
            info = old.Extended()
            need(self.k.QueryInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info), None), 'Job cap query')
            kernel_limits(info.basic.flags, info.job_memory)

        def identity(self, handle, pid):
            info = types.SimpleNamespace(process=handle)
            creation = self.creation(info)
            size = old.DWORD(32768); image = ctypes.create_unicode_buffer(size.value)
            need(self.k.QueryFullProcessImageNameW(handle, 0, image, ctypes.byref(size)), 'process image query')
            need(self.k.WaitForSingleObject(handle, 0) == 0x102, 'process not live')
            return {'pid': int(pid), 'creation': creation, 'image': str(Path(image.value).resolve())}

        def open_identity(self, expected):
            handle = self.k.OpenProcess(0x1000 | 0x100000, False, expected['pid'])
            need(handle, 'owned process unavailable')
            try:
                need(self.identity(handle, expected['pid']) == expected, 'PID reuse/image identity')
            finally:
                need(self.k.CloseHandle(handle), 'identity handle close uncertain')

        def parent_pid(self):
            # PROCESS_BASIC_INFORMATION uses pointer-sized slots on x86/x64.
            class PBI(ctypes.Structure):
                _fields_ = [('reserved1', ctypes.c_void_p), ('peb', ctypes.c_void_p),
                            ('reserved2', ctypes.c_void_p * 2), ('pid', ctypes.c_size_t),
                            ('parent', ctypes.c_size_t)]
            query = ctypes.WinDLL('ntdll').NtQueryInformationProcess
            query.argtypes = [old.HANDLE, old.DWORD, ctypes.c_void_p, old.DWORD, ctypes.c_void_p]
            query.restype = ctypes.c_long
            result = PBI()
            need(query(self.k.GetCurrentProcess(), 0, ctypes.byref(result), ctypes.sizeof(result), None) == 0, 'parent PID query')
            return int(result.parent)

        def start_held(self, command, cwd, job, reader):
            size = old.SIZE()
            ok = self.k.InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(size))
            need(not ok and ctypes.get_last_error() == 122 and 0 < size.value <= MAX_FRAME, 'attribute sizing')
            buffer = ctypes.create_string_buffer(size.value); pointer = ctypes.cast(buffer, ctypes.c_void_p)
            need(self.k.InitializeProcThreadAttributeList(pointer, 2, 0, ctypes.byref(size)), 'attribute init')
            try:
                jobs = (old.HANDLE * 1)(job); inherited = (old.HANDLE * 1)(reader)
                need(self.k.UpdateProcThreadAttribute(pointer, 0, 0x2000d, ctypes.byref(jobs), ctypes.sizeof(jobs), None, None), 'atomic Job attribute')
                need(self.k.UpdateProcThreadAttribute(pointer, 0, 0x20002, ctypes.byref(inherited), ctypes.sizeof(inherited), None, None), 'stdin handle allowlist')
                startup = old.StartupEx(); startup.startup.cb = ctypes.sizeof(startup); startup.attributes = pointer
                startup.startup.flags = 0x100; startup.startup.stdin = reader
                process = old.ProcessInfo(); command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
                need(self.k.CreateProcessW(command[0], command_line, None, None, True, 0x4 | 0x08000000 | 0x80000,
                                          None, str(cwd), ctypes.byref(startup), ctypes.byref(process)), 'held suspended create')
                return process
            finally:
                self.k.DeleteProcThreadAttributeList(pointer)
    return Kernel()


class Guard:
    def __init__(self, profile, envelope, kernel, old):
        self.profile, self.envelope, self.kernel, self.old = profile, envelope, kernel, old
        self.checks = []

    def identities_and_lease(self):
        p, e, k = self.profile, self.envelope, self.kernel
        for identity in (e['parent'], e['child']):
            need(set(identity) == {'pid', 'creation', 'image'} and type(identity['pid']) is int and
                 identity['pid'] > 0 and type(identity['creation']) is int and identity['creation'] > 0 and
                 type(identity['image']) is str, 'process identity schema')
        need(os.getpid() == e['child']['pid'] and k.parent_pid() == e['parent']['pid'], 'child/parent PID mismatch')
        k.open_identity(e['parent']); k.open_identity(e['child'])
        need(e['parent']['image'] == str(Path(p['python']).resolve()) and e['child']['image'] == e['parent']['image'], 'interpreter identity')
        lease(p)

    def check(self, phase):
        schedule = self.profile['phase_schedule']
        need(len(self.checks) < len(schedule) and phase == schedule[len(self.checks)], 'missing/reordered phase')
        self.refresh()
        self.checks.append(phase)
        self.record(phase)

    def record(self, phase):
        path = Path(self.profile['control']) / 'phases.jsonl'
        row = canonical({'session': self.envelope['nonce'], 'phase': phase, 'ordinal': len(self.checks)}) + b'\n'
        need(len(row) <= 1024 and (not path.exists() or path.stat().st_size + len(row) <= 4 * MAX_FRAME), 'phase ledger bound')
        with path.open('ab') as stream:
            stream.write(row); stream.flush(); os.fsync(stream.fileno())

    def complete(self):
        need(self.checks == self.profile['phase_schedule'], 'incomplete phase schedule')

    def refresh(self):
        p, e, k = self.profile, self.envelope, self.kernel
        need(type(e['nonce']) is str and len(e['nonce']) == 64 and all(c in '0123456789abcdef' for c in e['nonce']) and
             e['job'] == 'Local\\FNV-held-' + e['nonce'], 'session nonce/Job')
        need(load_profile(e['profile_path'], e['profile_sha256']) == p, 'profile drift')
        control = Path(p['control'])
        started = bounded_json(control / 'started.json')
        intent = bounded_json(control / 'intent.json')
        need(started == e and intent == {'profile_sha256': e['profile_sha256'],
             'session': {key: value for key, value in e.items() if key != 'child'},
             'lease': lease(p), 'state': 'once-only-intent'}, 'durable session drift')
        verify_authorities(p); self.identities_and_lease()
        handle = k.k.OpenJobObjectW(4, False, e['job'])
        need(handle, 'Job query open')
        try:
            k.job_check(handle)
            need(k.in_job(k.k.GetCurrentProcess(), handle), 'child outside owned Job')
            need(os.getpid() in k.census(handle), 'Job census missing child')
        finally:
            # Never retain a child Job handle across a payload or retry a failed
            # close: parent remains the only long-lived kill-on-close owner.
            need(k.k.CloseHandle(handle), 'Job query close uncertain')
        self.identities_and_lease()


def require_held_guard(profile, guard):
    """Consume the sole child-issued entry capability, then recheck live facts.

    This is process-local cooperative authority, not protection against hostile
    Python memory rewriting. A caller-created Guard is never an issued session.
    """
    global _ENTRY_CLAIM
    runtime = sys.modules.get(RUNTIME_NAME)
    need(type(runtime) is types.ModuleType and runtime.__dict__ is globals(), 'unregistered held runtime')
    need(type(guard) is Guard and _ACTIVE_SESSION is not None, 'authentic issued Guard required')
    issued_guard, issued_profile, session_digest, operation_digest = _ACTIVE_SESSION
    need(guard is issued_guard and profile is issued_profile and guard.profile is profile, 'unissued Guard/profile')
    need(_ENTRY_CLAIM is None and guard.checks == ['bootstrap', 'before-entry'], 'entry already claimed or wrong phase')
    need(digest(guard.envelope) == session_digest and digest(profile['operation']) == operation_digest, 'issued session/operation drift')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'fresh held child required')
    need(all(getattr(guard, name).__func__ is getattr(Guard, name) for name in
             ('check', 'refresh', 'identities_and_lease', 'record', 'complete')), 'Guard method substitution')
    # No caller authority boolean: the exact issued session is consumed once.
    # Full current source/profile/session/PID+creation/Job/lease check precedes
    # any driver's protected metadata/native/project-entry access.
    guard.refresh()
    _ENTRY_CLAIM = guard
    return guard


def authenticate_runtime(runtime, profile, guard, *, parent_sha256):
    """Called from a separately loaded, fixed-hash reviewed verifier copy.

    Reject a forged fixed-name module/no-op verifier before trusting its API.
    The driver must pin and verify this source BEFORE executing the copy; the
    supplied hash is that compiled-in driver pin, never an approval boolean.
    """
    need(type(runtime) is types.ModuleType and sys.modules.get(RUNTIME_NAME) is runtime, 'held runtime missing')
    need(type(profile) is dict and profile.get('parent_sha256') == parent_sha256, 'reviewed parent pin differs')
    need(runtime.__name__ == RUNTIME_NAME and Path(runtime.__file__).resolve() == Path(__file__).resolve(), 'held runtime source role')
    expected_class = Guard
    actual_class = runtime.__dict__.get('Guard')
    need(type(actual_class) is type and type(guard) is actual_class, 'actual runtime Guard class required')
    for name in ('check', 'refresh', 'identities_and_lease', 'record', 'complete'):
        actual = actual_class.__dict__.get(name)
        expected = expected_class.__dict__[name]
        need(type(actual) is types.FunctionType and actual.__code__ == expected.__code__ and
             actual.__globals__ is runtime.__dict__, 'unverified Guard implementation')
    for name in ('require_held_guard', 'lease', 'verify_authorities', 'load_profile', 'native', 'read_pin',
                 'source_snapshot', 'canonical', 'digest', 'bounded_json', 'kernel_limits', 'stream_pin', 'need',
                 'stdlib_name', 'runtime_origin', 'preflight_imports', 'trusted_runtime_path'):
        actual = runtime.__dict__.get(name)
        expected = globals()[name]
        need(type(actual) is types.FunctionType and actual.__code__ == expected.__code__ and
             actual.__globals__ is runtime.__dict__, 'unverified held verifier implementation')
    return runtime.require_held_guard(profile, guard)


def child_main(envelope):
    global _ACTIVE_SESSION, _ENTRY_CLAIM
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'fresh isolated child interpreter required')
    need(set(envelope) == {'parent_source', 'parent_sha256', 'profile_path', 'profile_sha256', 'nonce', 'job', 'parent', 'child'}, 'session schema')
    profile = load_profile(envelope['profile_path'], envelope['profile_sha256'])
    need(envelope['parent_source'] == profile['parent_source'] and envelope['parent_sha256'] == profile['parent_sha256'], 'parent authority')
    need(str(Path(__file__).resolve()) == str(Path(profile['parent_source']).resolve()), 'parent module role')
    verify_authorities(profile)
    old = old_module(); kernel = native(old)
    guard = Guard(profile, envelope, kernel, old)
    guard.check('bootstrap')
    snapshots = source_snapshot(profile)
    preflight_imports(profile, snapshots)
    finder = SnapshotFinder(profile, snapshots)
    sys.meta_path.insert(0, finder)
    # -I omits cwd/script/PYTHONPATH. Reject any preexisting project directory
    # entry as well; stdlib/site installation is trusted under this threat model.
    project = Path(profile['parent_source']).resolve().parents[2]
    need(all(not Path(path).resolve().is_relative_to(project) for path in sys.path if path), 'project sys.path exposure')
    module = __import__(profile['entry'][0])
    guard.check('before-entry')
    need(_ACTIVE_SESSION is None and _ENTRY_CLAIM is None, 'child capability already issued')
    _ACTIVE_SESSION = (guard, profile, digest(envelope), digest(profile['operation']))
    try:
        result = getattr(module, profile['entry'][1])(profile, guard)
        need(_ENTRY_CLAIM is guard, 'driver did not authenticate held capability')
        guard.check('after-entry')
        guard.complete()
    finally:
        _ACTIVE_SESSION = None
        _ENTRY_CLAIM = None
    need(type(result) is dict and result.get('status') in ('completed-unreviewed', 'completed-incomplete'), 'driver terminal status')
    summary = result.get('summary')
    need(type(summary) is dict and summary.get('requested') == 15 and
         type(summary.get('emitted')) is int and type(summary.get('blocked')) is int and
         summary['emitted'] >= 0 and summary['blocked'] >= 0 and summary['emitted'] + summary['blocked'] == 15,
         'driver terminal census')
    need((result['status'] == 'completed-unreviewed') == (summary['blocked'] == 0), 'driver status/census mismatch')
    if result['status'] == 'completed-incomplete':
        raise SystemExit(3)


def parent_command(python, parent_source, parent_sha256, profile_path, profile_sha256):
    """Reviewable fresh-parent command. Execute only after independent profile,
    source/runtime/input/watchdog review and fresh lease; this does not launch.
    """
    loader = ("import pathlib,hashlib; p=pathlib.Path(" + repr(str(parent_source)) +
              "); b=p.read_bytes(); assert len(b)<=1048576 and hashlib.sha256(b).hexdigest()==" +
              repr(parent_sha256) + "; d={'__name__':'_verified_held_launcher','__file__':str(p)}; " +
              "exec(compile(b,str(p),'exec'),d); r=d['launch'](" + repr(str(profile_path)) + "," +
              repr(profile_sha256) + "); raise SystemExit(0 if r['status']=='completed-unreviewed' else 1)")
    return [str(python), '-I', '-S', '-B', '-c', loader]


def launch(profile_path, profile_sha256):
    """Run exactly one reviewed external operation. Caller supplies its digest,
    never a command or approval boolean. Use a fresh isolated verified parent.
    """
    profile_path = str(Path(profile_path).resolve(strict=True))
    profile = load_profile(profile_path, profile_sha256)
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'fresh isolated parent interpreter required')
    need(str(Path(__file__).resolve()) == str(Path(profile['parent_source']).resolve()), 'launcher source role')
    verify_authorities(profile); grant = lease(profile)
    old = old_module(); kernel = native(old)
    control, output = Path(profile['control']), Path(profile['output'])
    private = Path(__file__).resolve().parents[2] / 'build' / 'rebuild'
    need(all(path.is_absolute() and path.resolve().is_relative_to(private.resolve()) for path in (control, output)), 'private control/output')
    need(not control.exists() and not output.exists() and control != output and
         not control.is_relative_to(output) and not output.is_relative_to(control), 'fresh exclusive output/control')
    control.mkdir(); nonce = secrets.token_hex(32); job_name = 'Local\\FNV-held-' + nonce
    parent = kernel.identity(kernel.k.GetCurrentProcess(), os.getpid())
    envelope = dict(parent_source=profile['parent_source'], parent_sha256=profile['parent_sha256'],
                    profile_path=profile_path, profile_sha256=profile_sha256, nonce=nonce, job=job_name, parent=parent)
    old.save_new(control / 'intent.json', {'profile_sha256': profile_sha256, 'session': envelope, 'lease': grant, 'state': 'once-only-intent'})
    child = job = reader = writer = None; assigned = False; closed = False; reason = None; code = None
    began = time.monotonic()
    try:
        job = kernel.named_job(job_name)
        # Pipe read handle is the only inherited capability; write end and Job
        # are noninheritable. An explicit HANDLE_LIST excludes unrelated handles.
        r, w = old.HANDLE(), old.HANDLE()
        need(kernel.k.CreatePipe(ctypes.byref(r), ctypes.byref(w), None, MAX_FRAME), 'pipe create')
        reader, writer = r.value, w.value
        need(kernel.k.SetHandleInformation(reader, 1, 1), 'pipe reader inheritance')
        loader = "import pathlib,hashlib; p=pathlib.Path(" + repr(profile['child_source']) + "); b=p.read_bytes(); assert len(b)<=1048576 and hashlib.sha256(b).hexdigest()==" + repr(profile['child_sha256']) + "; exec(compile(b,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
        command = [profile['python'], '-I', '-S', '-B', '-c', loader]
        verify_authorities(profile); need(lease(profile) == grant, 'precreate lease')
        child = kernel.start_held(command, private, job, reader)
        kernel.assign(job, child); assigned = True
        envelope['child'] = kernel.identity(child.process, child.pid)
        old.save_new(control / 'started.json', envelope)
        # Fresh identities, caps, exact source and current lease precede resume.
        kernel.open_identity(parent); need(kernel.creation(child) == envelope['child']['creation'], 'child FILETIME drift')
        kernel.job_check(job); verify_authorities(profile); need(lease(profile) == grant, 'preresume lease')
        kernel.resume(child)
        handle, reader = reader, None
        need(kernel.k.CloseHandle(handle), 'parent reader close uncertain')
        frame = canonical(envelope) + b'\n'; need(len(frame) <= 4096, 'small held-session frame bound')
        written = old.DWORD(); need(kernel.k.WriteFile(writer, frame, len(frame), ctypes.byref(written), None) and written.value == len(frame), 'session write')
        handle, writer = writer, None
        need(kernel.k.CloseHandle(handle), 'held writer close uncertain')
        while True:
            need(time.monotonic() - began < SECONDS and lease(profile) == grant, 'supervisor deadline/lease')
            old.owned_size(output, profile['allowed_outputs']); kernel.job_check(job)
            code = kernel.poll(child)
            if code is not None and not kernel.census(job):
                break
            time.sleep(.05)
        need(code == 0, 'held child failed')
        verify_authorities(profile); need(lease(profile) == grant, 'postexit lease')
    except BaseException as error:
        reason = type(error).__name__ + ': ' + str(error)
        if child is not None:
            try:
                if assigned:
                    kernel.terminate_job(job)
                else:
                    kernel.terminate_process(child)
                kernel.wait(child)
                need(not kernel.census(job), 'termination census not empty')
            except BaseException as stop:
                reason += '; owned termination uncertain: ' + type(stop).__name__
    finally:
        for handle in (reader, writer):
            if handle:
                if not kernel.k.CloseHandle(handle):
                    reason = reason or 'pipe close uncertain'
        if child is not None:
            try:
                kernel.close_process(child); closed = True
            except BaseException:
                reason = reason or 'process close uncertain'
        if job is not None:
            try:
                kernel.close_job(job)
            except BaseException:
                reason = reason or 'Job close uncertain'
    receipt = {'status': 'completed-unreviewed' if reason is None else 'failed', 'reason': reason,
               'returncode': code, 'session_nonce': nonce, 'profile_sha256': profile_sha256,
               'pid': int(child.pid) if child else None, 'process_handles_closed': closed,
               'elapsed_seconds': time.monotonic() - began, 'provider_selected': False, 'runtime_eligible': False,
               'kernel_job_memory_bytes': MEMORY, 'supervisor_seconds': SECONDS,
               'parent_crash_kill_observed': False, 'lease_and_filesystem_checks_are_sampled': True}
    # A publisher may have completed before a later identity/lease/after-entry
    # check failed. Such files are retained solely for bounded reconciliation;
    # the terminal receipt is mandatory for any independent outcome admission.
    receipt['outputs_require_successful_terminal_and_independent_review'] = True
    receipt['output_quarantined'] = reason is not None
    old.save_new(control / 'terminal.json', receipt)
    return receipt
