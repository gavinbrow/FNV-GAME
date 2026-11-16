"""Fixed post-V14 wrapper draft: intentionally disabled pending accepted pins.

No command line inputs, caller approvals, injectable delegates or native calls.
PINNED_POLICY and runtime identities must be filled by a separately reviewed
future source revision. This wrapper and the interpreter/runtime import closure
must be independently authenticated before launch; no self-hash proves trust.
"""
import copy
import base64
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
PREPARE_PIN = None
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
            type(WRAPPER_PIN) is dict and type(PREPARE_PIN) is dict and type(INTERPRETER_PIN) is dict and type(STDLIB_ROOT) is str and
            type(PROCESS_RUNTIME_PIN) is dict and type(REQUIRED_ROLE_PINS) is tuple and
            REQUIRED_ROLE_PINS, 'successor pins are not frozen')
    require(set(BOOTSTRAP_PIN)=={'path','sha256'} and
            BOOTSTRAP_PIN['path']=='tools/rebuild/application_successor_operation_v10.py', 'bootstrap path differs')
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
    require(PREPARE_PIN.get('path')=='tools/rebuild/application_successor_prepare_v5.py', 'prepare path differs')
    prepare_bytes=runtime.read_bound(ROOT,PREPARE_PIN,authority,4*1024*1024)
    prepare=types.ModuleType('_successor_pinned_prepare')
    prepare.__file__=str(ROOT/PREPARE_PIN['path'])
    exec(compile(prepare_bytes,prepare.__file__,'exec'),prepare.__dict__)
    require(prepare.SOURCE_PATHS==runtime.SOURCE_PATHS and
            set(graph)==set(prepare.SOURCE_PATHS) and
            all(graph[name]['path']==path for name,path in prepare.SOURCE_PATHS.items()),
            'prepare and loader source profiles differ')
    return runtime,manifest,resources,ledger,authority,finder,prepare


def _validate_producer_peers(manifest, resources):
    """No producer/handoff/native peer schemas are accepted yet."""
    raise RuntimeError('independent producer peer schemas and pins are not available')


def _semantic_work(prepare, manifest, resources, ledger, finder, guard):
    """Wire exact role inputs to V12 inside the already installed finder."""
    _validate_producer_peers(manifest,resources)
    operation=manifest['operation']
    role_pins={row['role']:row['pin'] for row in manifest['inputs']}
    require(len(role_pins)==len(ledger), 'role ledger size differs')
    identities={role:ledger[i] for i,role in enumerate(role_pins)}
    prepare.ROLE_PINS=copy.deepcopy(role_pins)
    prepare.SOURCE_GRAPH={name:row for name,row in manifest['sources'].items() if name!='runtime'}
    prepare.check_graph(prepare.SOURCE_GRAPH)
    guard();args=prepare._arguments(resources,identities)
    prepare._phase_role_binding(operation,identities)
    composer=prepare._fixed_module('application_successor_compose_v12')
    guard();result=composer.compose(**args);guard()
    require(type(result) is dict and result.get('kind')=='post-v14-composed-evidence-v12' and
            all(result.get(k) is False for k in ('admission_approved','link_approved','execution_approved')) and
            type(result.get('response')) is dict and type(result['response'].get('response_bytes')) is bytes,
            'composition output scope differs')
    return result


def _encode_evidence(value):
    """Preserve complete output, encoding bytes without dropping unknown fields."""
    if type(value) is bytes:return {'$bytes_base64':base64.b64encode(value).decode('ascii')}
    if type(value) is list:return [_encode_evidence(x) for x in value]
    if type(value) is dict:
        require(all(type(k) is str for k in value),'output keys must be strings')
        return {k:_encode_evidence(v) for k,v in value.items()}
    require(value is None or type(value) in (str,int,float,bool),'unsupported output value')
    return value


def _publish_semantic(runtime, operation, result, guard, started_sha):
    """Exclusive full output publication precedes phase and terminal receipts."""
    journal=runtime.contained(ROOT,operation['journal'],exists=True)
    response=result['response']['response_bytes']
    require(type(response) is bytes and len(response)>0,'response bytes required')
    receipt=canonical({'kind':'successor-semantic-composition-v12','evidence':_encode_evidence(result)})+b'\n'
    require(len(receipt)+len(response)<=128*1024*1024,'semantic output cap')
    guard();runtime.write_once(journal/'semantic.json',receipt);guard()
    runtime.write_once(journal/'response.rsp',response);guard()
    require((journal/'semantic.json').read_bytes()==receipt and (journal/'response.rsp').read_bytes()==response,
            'semantic publication drift')
    publication={'kind':'successor-semantic-publication','started_sha256':started_sha,
                 'semantic_sha256':sha(receipt),'response_sha256':sha(response)}
    runtime.write_once(journal/'semantic-publication.json',canonical(publication)+b'\n');guard()


def _perform(state, process):
    """Internal fixed wiring; process must come from an authenticated loader.

    This is not an authority-bearing public seam. Until run() has a reviewed
    process loader it is deliberately unreachable from the entry point.
    """
    from datetime import datetime, timezone
    runtime,manifest,resources,ledger,authority,finder,prepare=state
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
            runtime.read_bound(ROOT,PREPARE_PIN,fresh,4*1024*1024)
            require(prepare.SOURCE_PATHS==runtime.SOURCE_PATHS, 'prepare source profile changed')
            require(canonical(fresh)==canonical(authority),'authority identity changed')
            current=[]
            for entry in manifest['inputs']:
                data=runtime.read_bound(ROOT,entry['pin'],current)
                require(data==resources[entry['role']] and sha(data)==entry['pin']['sha256'],
                        'resource role bytes changed')
            require(canonical(current)==canonical(ledger),'resource identity changed')
            runtime_guard()
        guard()
        require(type(operation['phases']) is list and len(operation['phases'])==1 and
                operation['phases'][0]['name']=='compose-v12', 'exact composition phase required')
        started=runtime.begin(ROOT,operation,PINNED_POLICY['manifest']['sha256'],guard)
        def fresh(phase):
            guard();before=copy.deepcopy(ledger)
            facts=phase_fn(ledger,phase=phase,stable_fn=stable_fn)
            require(ledger==before and facts.get('cross_phase_cache_used') is False and
                    facts.get('original_ledger_rewritten') is False,'fresh stability ledger changed')
            guard();return facts
        pre=fresh('pre')
        result=_semantic_work(prepare,manifest,resources,ledger,finder,guard)
        post=fresh('post')
        require('wrapper_stability' not in result,'wrapper evidence collision')
        result['wrapper_stability']={'pre':pre,'post':post,'input_bindings':copy.deepcopy(ledger)}
        _publish_semantic(runtime,operation,result,guard,started)
        fresh('post')
        runtime.phase(ROOT,operation,0,ledger,phase_fn,stable_fn,guard,started)
        return runtime.finish(ROOT,operation,started,guard)


def run():
    """Prepare-only entry; independent producer peers and runtime launcher are not available.

    This intentionally remains unreachable while the frozen pins are absent.
    A separately authenticated launcher must verify the Python, stdlib and
    process-inspection closure before this entry, and a reviewed watchdog must
    produce the child record and own the actual CPU lease.
    """
    runtime,manifest,resources,ledger,authority,finder,prepare=_startup()
    # No unverified psutil import. This must be replaced by a reviewed,
    # authenticated runtime loader when PROCESS_RUNTIME_PIN is finalized.
    raise RuntimeError('authenticated process runtime loader is not installed')


if __name__=='__main__':
    run()
