"""Fixed post-V14 wrapper draft: intentionally disabled pending accepted pins.

No command line inputs, caller approvals, injectable delegates or native calls.
PINNED_POLICY and runtime identities must be filled by a separately reviewed
future source revision. This wrapper and the interpreter/runtime import closure
must be independently authenticated before launch; no self-hash proves trust.
"""
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
# Intentionally unset: a reviewer must freeze an exact immutable policy here.
PINNED_POLICY = None
# Exact file pins for this wrapper's V5 bootstrap and Python executable.
BOOTSTRAP_PIN = None
WRAPPER_PIN = None
INTERPRETER_PIN = None
# Interpreter stdlib and third-party process module must be authenticated by
# the future launcher; the identities and closure do not yet exist.
STDLIB_ROOT = None
PROCESS_RUNTIME_PIN = None
# Ordered (role, exact {path, sha256}) pairs from independently reviewed artifacts.
REQUIRED_ROLE_PINS = None


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def bootstrap():
    """Read pinned V5 bytes before executing any project module."""
    require(type(PINNED_POLICY) is dict and type(BOOTSTRAP_PIN) is dict and
            type(WRAPPER_PIN) is dict and type(INTERPRETER_PIN) is dict and type(STDLIB_ROOT) is str and
            type(PROCESS_RUNTIME_PIN) is dict and type(REQUIRED_ROLE_PINS) is tuple and
            REQUIRED_ROLE_PINS, 'successor pins are not frozen')
    require(set(BOOTSTRAP_PIN)=={'path','sha256'} and
            BOOTSTRAP_PIN['path']=='tools/rebuild/application_successor_operation_v7.py', 'bootstrap path differs')
    path=(ROOT/BOOTSTRAP_PIN['path']).resolve(strict=True)
    require(path.is_relative_to(ROOT) and path.is_file(), 'bootstrap path escaped')
    data=path.read_bytes()
    require(len(data)<=4*1024*1024 and sha(data)==BOOTSTRAP_PIN['sha256'], 'bootstrap hash differs')
    module=types.ModuleType('_successor_pinned_bootstrap')
    module.__file__=str(path)
    exec(compile(data,str(path),'exec'),module.__dict__)
    return module


def _validate_roles(manifest, source_sha):
    """Role names, multiplicity and pinned implementation are part of policy."""
    sources=manifest['sources']; inputs=manifest['inputs']; op=manifest['operation']
    require(type(sources) is dict and {'runtime','application_link_diagnostic','exact_binding_stability'}<=set(sources),
            'closed source graph required')
    require(sources['runtime']==BOOTSTRAP_PIN and
            sources['application_link_diagnostic']['path']=='tools/rebuild/application_link_diagnostic.py' and
            sources['exact_binding_stability']['path']=='tools/rebuild/exact_binding_stability.py', 'fixed source roles differ')
    require(type(REQUIRED_ROLE_PINS) is tuple and REQUIRED_ROLE_PINS and type(inputs) is list,
            'fixed ordered role pins required')
    expected=[];roles=set();paths=set()
    for entry in REQUIRED_ROLE_PINS:
        require(type(entry) is tuple and len(entry)==2, 'fixed role pair required')
        role,pin=entry
        require(type(role) is str and role and role not in roles and type(pin) is dict and
                set(pin)=={'path','sha256'} and type(pin['path']) is str and pin['path'] and
                type(pin['sha256']) is str and len(pin['sha256'])==64 and
                all(c in '0123456789abcdef' for c in pin['sha256']) and pin['path'] not in paths,
                'distinct exact role pins required')
        roles.add(role);paths.add(pin['path']);expected.append({'role':role,'pin':pin})
    require(canonical(inputs)==canonical(expected), 'manifest resource roles or exact pins differ')
    require(type(op) is dict and source_sha==sources['runtime']['sha256'], 'runtime pin differs')


def _startup():
    runtime=bootstrap(); authority=[]
    manifest=runtime.verify_manifest(ROOT,PINNED_POLICY,authority)
    _validate_roles(manifest,BOOTSTRAP_PIN['sha256'])
    ledger=[]; resources={}
    for entry in manifest['inputs']:
        resources[entry['role']]=runtime.read_bound(ROOT,entry['pin'],ledger)
    require(canonical(ledger)==canonical(manifest['operation']['input_bindings']), 'full resource ledger differs')
    graph={name:pin for name,pin in manifest['sources'].items() if name!='runtime'}
    finder=runtime.source_finder(ROOT,graph,authority,STDLIB_ROOT,main_pin=WRAPPER_PIN)
    # Bind bootstrap and all authority inputs in the same guard ledger.
    runtime.read_bound(ROOT,BOOTSTRAP_PIN,authority,4*1024*1024)
    return runtime,manifest,resources,ledger,authority,finder


def _perform(state, process):
    """Internal fixed wiring; process must come from an authenticated loader.

    This is not an authority-bearing public seam. Until run() has a reviewed
    process loader it is deliberately unreachable from the entry point.
    """
    from datetime import datetime, timezone
    runtime,manifest,resources,ledger,authority,finder=state
    operation=manifest['operation']
    with runtime.SnapshotSession(finder):
        diagnostic=importlib.import_module('application_link_diagnostic')
        stability=importlib.import_module('exact_binding_stability')
        stable_fn=diagnostic.stable; phase_fn=stability.stable_phase
        runtime_guard=runtime.RuntimeGuard(ROOT,operation,process,finder,lambda:datetime.now(timezone.utc))
        main_module=sys.modules.get('__main__')
        def guard():
            runtime_guard()
            require(sys.modules.get('__main__') is main_module and
                    getattr(main_module,'__file__',None)==str((ROOT/WRAPPER_PIN['path']).absolute()), 'main changed')
            require(diagnostic.stable is stable_fn and stability.stable_phase is phase_fn, 'stable delegates changed')
            fresh=[]
            runtime.verify_manifest(ROOT,PINNED_POLICY,fresh)
            runtime.read_bound(ROOT,WRAPPER_PIN,fresh,4*1024*1024)
            for pin in (p for name,p in manifest['sources'].items() if name!='runtime'):
                runtime.read_bound(ROOT,pin,fresh,4*1024*1024)
            runtime.read_bound(ROOT,BOOTSTRAP_PIN,fresh,4*1024*1024)
            require(canonical(fresh)==canonical(authority),'authority identity changed')
            current=[]
            for entry in manifest['inputs']:
                data=runtime.read_bound(ROOT,entry['pin'],current)
                require(data==resources[entry['role']] and sha(data)==entry['pin']['sha256'],
                        'resource role bytes changed')
            require(canonical(current)==canonical(ledger),'resource identity changed')
            runtime_guard()
        guard()
        started=runtime.begin(ROOT,operation,PINNED_POLICY['manifest']['sha256'],guard)
        for index in range(len(operation['phases'])):
            runtime.phase(ROOT,operation,index,ledger,phase_fn,stable_fn,guard,started)
        return runtime.finish(ROOT,operation,started,guard)


def run():
    """Prepare phase receipts only. No native operation or process is launched.

    This intentionally remains unreachable while the frozen pins are absent.
    A separately authenticated launcher must verify the Python, stdlib and
    process-inspection closure before this entry, and a reviewed watchdog must
    produce the child record and own the actual CPU lease.
    """
    runtime,manifest,resources,ledger,authority,finder=_startup()
    # No unverified psutil import. This must be replaced by a reviewed,
    # authenticated runtime loader when PROCESS_RUNTIME_PIN is finalized.
    raise RuntimeError('authenticated process runtime loader is not installed')


if __name__=='__main__':
    run()
