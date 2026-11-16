"""Fail-closed post-V14 phase runtime prototype; no operational entry point.

The only configurable entry is a private test seam. A future reviewed wrapper
must embed exact source/input/operation/reviewer pins and authenticate Python,
stdlib, psutil and this module before using these controls. No subprocess or
native operation is launched here. Existing unknown journals must be reconciled,
never retried. The filesystem must be private and stable against hostile writes.
"""
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from types import MappingProxyType


def require(ok, message):
    if not ok: raise ValueError(message)


def digest(data): return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def parse(data):
    def pairs(items):
        obj = {}
        for k, v in items:
            require(k not in obj, 'duplicate key')
            obj[k] = v
        return obj
    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite')))


def hash_string(value): return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


def contained(root, name, *, exists):
    require(type(name) is str and name and not Path(name).is_absolute() and '..' not in Path(name).parts, 'relative path required')
    root = Path(root).resolve(strict=True)
    path = root / name
    resolved = path.resolve(strict=exists)
    require(resolved.is_relative_to(root), 'path escaped root')
    return path


def read_bound(root, pin, ledger, cap=128*1024*1024):
    require(type(pin) is dict and set(pin) == {'path','sha256'} and hash_string(pin['sha256']), 'bad pin')
    requested = contained(root, pin['path'], exists=True)
    resolved = requested.resolve(strict=True)
    with resolved.open('rb') as f:
        before = os.fstat(f.fileno()); data = f.read(cap+1); after = os.fstat(f.fileno())
    current = resolved.stat()
    stamp = lambda s: (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
    require(len(data)<=cap and len(data)==current.st_size and stamp(before)==stamp(after)==stamp(current) and
            requested.resolve(strict=True)==resolved and digest(data)==pin['sha256'], 'binding changed')
    ledger.append({'requested_path':str(requested), 'path':str(resolved), 'sha256':digest(data),
                   'size':current.st_size, 'device':current.st_dev, 'inode':current.st_ino})
    return data


def verify_manifest(root, policy, ledger):
    """Private seam. policy must originate in future immutable reviewed wrapper."""
    require(type(policy) is dict and set(policy)=={'manifest','reviews','expected','reviewers'}, 'exact policy required')
    require(type(policy['reviews']) is dict and set(policy['reviews'])=={'source','input','operation'} and
            type(policy['reviewers']) is dict and set(policy['reviewers'])==set(policy['reviews']) and
            len(set(policy['reviewers'].values()))==3, 'three independent reviewer identities required')
    refs=[policy['manifest']]+list(policy['reviews'].values())
    require(all(type(r) is dict and set(r)=={'path','sha256'} and hash_string(r['sha256']) for r in refs) and
            len({r['path'] for r in refs})==4 and len({r['sha256'] for r in refs})==4, 'distinct anchors required')
    manifest=parse(read_bound(root,policy['manifest'],ledger,4*1024*1024))
    require(manifest==policy['expected'] and type(manifest) is dict and
            set(manifest)=={'kind','version','sources','inputs','operation'} and
            manifest['kind']=='successor-operation-manifest' and type(manifest['version']) is int and manifest['version']==1,
            'exact manifest differs')
    for scope,key in (('source','sources'),('input','inputs'),('operation','operation')):
        review=parse(read_bound(root,policy['reviews'][scope],ledger,4*1024*1024))
        require(review=={'kind':'successor-independent-review','scope':scope,'reviewer':policy['reviewers'][scope],
                         'manifest_sha256':policy['manifest']['sha256'], 'subject_sha256':digest(canonical(manifest[key]))},
                'review differs')
    operation=manifest['operation']
    require(type(operation) is dict and set(operation)=={'id','journal','phases','lease','watchdog'} and
            type(operation['id']) is str and re.fullmatch('[A-Za-z0-9_-]{1,80}',operation['id']) and
            type(operation['phases']) is list and operation['phases'], 'operation schema')
    seen=set()
    for phase in operation['phases']:
        require(type(phase) is dict and set(phase)=={'name','artifact'} and
                type(phase['name']) is str and re.fullmatch('[A-Za-z0-9_-]{1,80}',phase['name']) and
                phase['name'] not in seen, 'phase schema')
        seen.add(phase['name']); contained(root,phase['artifact'],exists=False)
    paths=[operation['journal']]+[x['artifact'] for x in operation['phases']]
    resolved=[contained(root,path,exists=False).resolve() for path in paths]
    require(len(resolved)==len(set(resolved)) and all(not p.is_relative_to(resolved[0]) for p in resolved[1:]),
            'operation paths overlap')
    return manifest


class SnapshotFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, snapshots, paths, workspace, stdlib_root):
        require(set(snapshots)==set(paths) and snapshots, 'exact source graph')
        self.snapshots=MappingProxyType(dict(snapshots)); self.paths=MappingProxyType(dict(paths))
        self.workspace=Path(workspace).resolve(); self.stdlib=Path(stdlib_root).resolve()
    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.snapshots:
            require(path is None and target is None, 'package or reload rejected')
            return importlib.util.spec_from_loader(fullname,self,origin=self.paths[fullname])
        spec=importlib.machinery.PathFinder.find_spec(fullname,path)
        origins=[] if spec is None else ([spec.origin] if spec.origin and spec.origin not in ('built-in','frozen') else [])
        if spec is not None and spec.submodule_search_locations is not None: origins.extend(spec.submodule_search_locations)
        require(fullname.split('.')[0] in sys.stdlib_module_names, 'unreviewed dependency')
        for origin in origins:
            resolved=Path(origin).resolve()
            require(resolved.is_relative_to(self.stdlib) and not resolved.is_relative_to(self.workspace) and
                    'site-packages' not in (p.lower() for p in resolved.parts), 'untrusted stdlib origin')
        return None
    def create_module(self,spec): return None
    def exec_module(self,module):
        name=module.__name__; require(name in self.snapshots,'unreviewed source')
        module.__file__=self.paths[name]
        exec(compile(self.snapshots[name],module.__file__,'exec'),module.__dict__)


def source_finder(root, sources, ledger, stdlib_root):
    require(type(sources) is dict and 0<len(sources)<=80, 'bounded graph required')
    require(not any(n in sys.modules for n in sources), 'project module preloaded')
    workspace=Path(root).resolve()
    for name,module in tuple(sys.modules.items()):
        origin=getattr(module,'__file__',None)
        if type(origin) is str:
            require(not Path(origin).resolve().is_relative_to(workspace), 'workspace module preloaded')
    snapshots={};paths={}
    for name,pin in sources.items():
        require(type(name) is str and re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',name), 'bad module name')
        snapshots[name]=read_bound(root,pin,ledger,4*1024*1024); paths[name]=str(contained(root,pin['path'],exists=True))
    require(sum(map(len,snapshots.values()))<=8*1024*1024,'graph cap')
    return SnapshotFinder(snapshots,paths,root,stdlib_root)


def _utc(value):
    require(type(value) is str, 'UTC timestamp required')
    dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    require(dt.tzinfo is not None and dt.utcoffset()==timedelta(0), 'UTC timestamp required')
    return dt


def lease_watchdog(root, operation, process, now):
    """Read cooperative registry and child receipt, check real observed identity.

    process is the authenticated psutil current Process in a fixed wrapper.
    Registry lock and records are trusted only in the cooperative private tree.
    """
    lease=operation['lease']; watch=operation['watchdog']
    require(type(lease) is dict and set(lease)=={'lock','registry','owner','resource','slot','input_pins','review_sha256'} and
            lease['resource']=='cpu' and type(lease['slot']) is int and lease['slot']>0 and
            hash_string(lease['review_sha256']), 'lease policy')
    lock=contained(root,lease['lock'],exists=False); registry=contained(root,lease['registry'],exists=True)
    require(not lock.exists(),'registry locked')
    with registry.open('rb') as f: raw=f.read(4*1024*1024+1)
    require(len(raw)<=4*1024*1024 and not lock.exists(),'registry changed under lock')
    state=parse(raw);require(type(state) is dict and state.get('schema_version')==1 and type(state.get('leases')) is list,'registry schema')
    rows=[r for r in state['leases'] if type(r) is dict and all(r.get(k)==lease[k] for k in ('owner','resource','slot','input_pins','review_sha256')) and r.get('state') in ('granted','running')]
    require(len(rows)==1,'unique active lease required'); row=rows[0]
    require(type(row.get('max_seconds')) is int and row['max_seconds']>0,'lease duration')
    grant=_utc(row['granted_utc']);require(grant<=now<grant+timedelta(seconds=row['max_seconds']),'expired lease')
    require(type(watch) is dict and set(watch)=={'record','record_sha256','nonce_env','executable','pins'} and
            hash_string(watch['record_sha256']), 'watchdog policy')
    record=parse(read_bound(root,{'path':watch['record'],'sha256':watch['record_sha256']},[],65536))
    require(type(record) is dict and set(record)=={'kind','child','pins','slot','nonce'} and
            record['kind']=='successor-watchdog-started' and record['slot']==lease['slot'] and
            record['pins']==watch['pins'] and hash_string(record['nonce']) and
            os.environ.get(watch['nonce_env'])==record['nonce'], 'watchdog binding')
    child=record['child'];require(type(child) is dict and set(child)=={'pid','parent_pid','create_time','executable'} and
            type(child['pid']) is int and type(child['parent_pid']) is int and type(child['create_time']) is float and
            child['pid']==os.getpid()==process.pid and child['parent_pid']==os.getppid()==process.ppid() and
            child['create_time']==process.create_time() and child['executable']==process.exe()==watch['executable'], 'child identity')
    return {'lease':copy.deepcopy(row),'child':copy.deepcopy(child),'watchdog_sha256':watch['record_sha256']}


def write_once(path, data):
    with Path(path).open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    require(Path(path).read_bytes()==data,'write mismatch')
    return digest(data)


def begin(root,operation,manifest_sha,guard):
    """Create persistent UNKNOWN journal before any operation; collisions stop."""
    require(hash_string(manifest_sha),'manifest hash')
    guard(); journal=contained(root,operation['journal'],exists=False)
    require(not journal.exists(),'journal exists; reconcile')
    journal.mkdir()
    guard(); data=canonical({'kind':'successor-operation-started','manifest_sha256':manifest_sha,
                             'operation':operation,'state':'UNKNOWN'})+b'\n'
    return write_once(journal/'started.json',data)


def phase(root, operation, index, ledger, stable_phase, stable_fn, guard, started_sha):
    """Fresh pre/post checks around a phase-local exclusive full-ledger artifact."""
    require(type(index) is int and 0<=index<len(operation['phases']) and hash_string(started_sha), 'phase index')
    plan=operation['phases'][index]; journal=contained(root,operation['journal'],exists=True)
    require(digest((journal/'started.json').read_bytes())==started_sha and not (journal/'terminal.json').exists(),'journal drift')
    for prior in operation['phases'][:index]:
        prior_index=operation['phases'].index(prior)
        prior_path=contained(root,prior['artifact'],exists=True)
        prior_receipt=parse((journal/(str(prior_index)+'-phase.json')).read_bytes())
        require(prior_path.is_file() and prior_receipt['name']==prior['name'] and
                prior_receipt['artifact']==prior['artifact'] and prior_receipt['started_sha256']==started_sha and
                prior_receipt['artifact_sha256']==digest(prior_path.read_bytes()), 'prior phase incomplete')
    guard(); before=copy.deepcopy(ledger)
    pre=stable_phase(ledger,phase='pre',stable_fn=stable_fn)
    require(ledger==before and pre.get('cross_phase_cache_used') is False,'ledger drift')
    guard(); artifact=contained(root,plan['artifact'],exists=False)
    content=canonical({'kind':'successor-phase','name':plan['name'],'index':index,'started_sha256':started_sha,
                       'input_bindings':before,'pre':pre})+b'\n'
    artifact_sha=write_once(artifact,content)
    guard(); post=stable_phase(ledger,phase='post',stable_fn=stable_fn)
    require(ledger==before and post.get('cross_phase_cache_used') is False,'ledger drift')
    guard()
    return write_once(journal/(str(index)+'-phase.json'),canonical({'name':plan['name'],'artifact':plan['artifact'],
                      'artifact_sha256':artifact_sha,'post':post,'started_sha256':started_sha})+b'\n')


def finish(root,operation,started_sha,guard):
    journal=contained(root,operation['journal'],exists=True); guard()
    require(digest((journal/'started.json').read_bytes())==started_sha,'journal drift')
    receipts=[]
    for i,p in enumerate(operation['phases']):
        raw=(journal/(str(i)+'-phase.json')).read_bytes(); rec=parse(raw)
        artifact=contained(root,p['artifact'],exists=True)
        require(rec['name']==p['name'] and rec['artifact']==p['artifact'] and rec['started_sha256']==started_sha and
                digest(artifact.read_bytes())==rec['artifact_sha256'], 'phase receipt drift')
        receipts.append(digest(raw))
    guard()
    return write_once(journal/'terminal.json',canonical({'kind':'successor-operation-terminal',
                      'started_sha256':started_sha,'phase_receipts':receipts,'state':'completed'})+b'\n')


class RuntimeGuard:
    """Repeated exact lease, watchdog, process and installed finder checks."""
    def __init__(self, root, operation, process, finder, now):
        self.root=root; self.operation=copy.deepcopy(operation); self.process=process
        self.finder=finder; self.now=now
        self.initial=lease_watchdog(root,self.operation,process,now())
    def __call__(self):
        require(sys.meta_path and sys.meta_path[0] is self.finder,'source finder displaced')
        require(lease_watchdog(self.root,self.operation,self.process,self.now())==self.initial,
                'lease, watchdog or child changed')


class SnapshotSession:
    """Install finder throughout execution and discard loaded graph afterward."""
    def __init__(self, finder): self.finder=finder
    def __enter__(self):
        require(not any(n in sys.modules for n in self.finder.snapshots),'project module preloaded')
        self.old_path=sys.path[:]
        sys.path[:]=[p for p in sys.path if p and not Path(p).resolve().is_relative_to(self.finder.workspace)]
        sys.meta_path.insert(0,self.finder)
        return self.finder
    def __exit__(self,typ,value,tb):
        intact=bool(sys.meta_path and sys.meta_path[0] is self.finder)
        if self.finder in sys.meta_path: sys.meta_path.remove(self.finder)
        sys.path[:]=self.old_path
        for name in self.finder.snapshots: sys.modules.pop(name,None)
        require(intact,'source finder displaced')
        return False
