"""Post-V14 native LINK control draft, permanently disabled for real operations.

V14 diagnostic link_once checks stable input identities, unchanged response,
actual default libraries, cleared LINK/CL environment and one LINK invocation;
the held launcher additionally uses a Windows Job, child birth identities,
lease checks and durable exclusive records. This draft launches nothing and
implements only synthetic validation/receipt mechanics. A future independently
reviewed fixed launcher must authenticate all source/runtime/peer pins and own
actual process handles, Job containment, lease and once-only transition.
"""
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re

# Intentionally unset; future immutable accepted artifacts and reviews required.
FIXED_PROFILE = None
SOURCE_PINS = None
RUNTIME_PINS = None
PEER_PINS = None
WATCHDOG_PIN = None


def need(ok, message):
    if not ok: raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def sha(data):return hashlib.sha256(data).hexdigest()


def digest_ok(value):return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def _json(data):
    def pairs(items):
        out={}
        for key,value in items:
            need(key not in out,'duplicate JSON key');out[key]=value
        return out
    return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite')))


def _validate_profile(profile):
    """Proposed schema only: exact data is not an independent approval."""
    need(type(profile) is dict and set(profile)=={'kind','version','operation','response','preparation',
         'source_pins','runtime_pins','peer_pins','watchdog','lease','outputs'} and
         profile['kind']=='successor-diagnostic-native-link' and type(profile['version']) is int and profile['version']==1,
         'profile schema')
    op=profile['operation'];response=profile['response'];prep=profile['preparation']
    need(type(op) is dict and set(op)=={'id','linker_identity','command','working_directory'} and
         type(op['id']) is str and re.fullmatch('[A-Za-z0-9_-]{1,80}',op['id']) and
         type(op['command']) is list and len(op['command'])==2 and
         type(op['working_directory']) is str and op['working_directory'], 'fixed operation schema')
    need(type(response) is dict and set(response)=={'path','sha256'} and
         type(response['path']) is str and response['path'] and digest_ok(response['sha256']) and
         op['command']==[op['linker_identity']['path'],'@'+response['path']], 'response command differs')
    _identity(op['linker_identity'])
    need(type(prep) is dict and set(prep)=={'manifest_sha256','semantic_sha256','publication_sha256',
         'preparation_terminal_sha256','input_bindings'} and all(digest_ok(prep[k]) for k in
         ('manifest_sha256','semantic_sha256','publication_sha256','preparation_terminal_sha256')) and
         type(prep['input_bindings']) is list and prep['input_bindings'], 'exact preparation schema')
    for row in prep['input_bindings']:_identity(row)
    need(type(profile['source_pins']) is dict and profile['source_pins'] and
         type(profile['runtime_pins']) is dict and profile['runtime_pins'] and
         all(type(k) is str and k and digest_ok(v) for group in ('source_pins','runtime_pins')
             for k,v in profile[group].items()), 'source/runtime pins')
    peers=profile['peer_pins'];need(type(peers) is dict and set(peers)=={'preparation','semantic','operation','watchdog'} and
         all(digest_ok(x) for x in peers.values()) and len(set(peers.values()))==4, 'independent peer pins')
    lease=profile['lease'];need(type(lease) is dict and set(lease)=={'owner','resource','slot','row_sha256'} and
         type(lease['owner']) is str and lease['owner'] and lease['resource']=='CPU_heavy' and
         type(lease['slot']) is int and lease['slot'] in (1,2) and digest_ok(lease['row_sha256']), 'CPU lease scope')
    watchdog=profile['watchdog'];need(type(watchdog) is dict and set(watchdog)=={'source_sha256','protocol_sha256'} and
         all(digest_ok(x) for x in watchdog.values()), 'watchdog pins')
    outputs=profile['outputs'];need(type(outputs) is dict and set(outputs)=={'stdout','stderr','executable','map'} and
         all(type(x) is str and x for x in outputs.values()) and len(set(outputs.values()))==4, 'output scope')
    return profile


def _identity(identity):
    need(type(identity) is dict and set(identity)=={'requested_path','path','sha256','size','device','inode'} and
         all(type(identity[k]) is str and identity[k] for k in ('requested_path','path')) and digest_ok(identity['sha256']) and
         all(type(identity[k]) is int and identity[k]>=0 for k in ('size','device','inode')), 'physical identity')


def _lease_fixture(profile, registry, now):
    """A future trusted lock/registry reader supplies this exact live snapshot."""
    need(type(registry) is dict and type(registry.get('schema_version')) is int and registry['schema_version']==1 and
         type(registry.get('CPU_heavy_capacity')) is int and registry['CPU_heavy_capacity']==2 and
         type(registry.get('leases')) is list, 'registry schema')
    policy=profile['lease']; rows=[row for row in registry['leases'] if type(row) is dict and
         all(row.get(k)==policy[k] for k in ('owner','resource','slot')) and row.get('state') in ('granted','running')]
    need(len(rows)==1,'unique CPU lease required');row=rows[0]
    identity={k:v for k,v in row.items() if k!='state'}
    need(sha(canonical(identity))==policy['row_sha256'] and type(row.get('max_seconds')) is int and
         row['max_seconds']>0,'CPU lease identity')
    start=datetime.fromisoformat(row['granted_utc'].replace('Z','+00:00'))
    need(start.tzinfo is not None and start.utcoffset()==timedelta(0) and now.tzinfo is not None and
         now.utcoffset()==timedelta(0) and start<=now<start+timedelta(seconds=row['max_seconds']), 'CPU lease expired')
    return identity


def _watchdog_fixture(profile, watchdog, observed):
    """Synthetic seam; live handle/Job observation cannot be supplied by caller."""
    need(type(watchdog) is dict and set(watchdog)=={'kind','profile_sha256','parent','child','job','nonce'} and
         watchdog['kind']=='successor-link-watchdog-started' and watchdog['profile_sha256']==sha(canonical(profile)) and
         type(watchdog['job']) is str and watchdog['job'] and digest_ok(watchdog['nonce']), 'watchdog record')
    for role in ('parent','child'):
        row=watchdog[role];need(type(row) is dict and set(row)=={'pid','creation','image'} and
          type(row['pid']) is int and row['pid']>0 and type(row['creation']) is int and row['creation']>0 and
          type(row['image']) is str and row['image'], 'process birth identity')
    need(watchdog['parent']['pid']!=watchdog['child']['pid'] and
         watchdog['child']['image']==profile['operation']['linker_identity']['path'] and type(observed) is dict and
         observed=={'parent':watchdog['parent'],'child':watchdog['child'],'job':watchdog['job']},
         'live process or Job identity differs')
    return watchdog


def _response_fixture(profile, response, bindings):
    need(type(response) is bytes and sha(response)==profile['response']['sha256'] and
         type(bindings) is list and canonical(bindings)==canonical(profile['preparation']['input_bindings']),
         'response or full binding ledger differs')


def _write_once(path,value):
    data=canonical(value)+b'\n'
    with Path(path).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    need(Path(path).read_bytes()==data,'receipt readback differs')
    return sha(data)


def _begin_fixture(folder,profile,response,bindings,lease,watchdog):
    """Durable once intent; a partial folder is UNKNOWN and blocks all retry."""
    _validate_profile(profile);_response_fixture(profile,response,bindings)
    folder=Path(folder);need(not folder.exists(),'operation already exists; reconcile')
    folder.mkdir()
    return _write_once(folder/'intent.json',{'kind':'successor-link-intent','profile_sha256':sha(canonical(profile)),
        'response_sha256':sha(response),'lease':lease,'watchdog':watchdog,'state':'UNKNOWN'})


def _finish_fixture(folder,profile,intent_sha,response,bindings,lease,watchdog,observation):
    """A receipt is evidence only; synthetic caller is not operation authority."""
    _validate_profile(profile);_response_fixture(profile,response,bindings)
    folder=Path(folder);raw=(folder/'intent.json').read_bytes();need(digest_ok(intent_sha) and sha(raw)==intent_sha,'intent drift')
    intent=_json(raw);need(intent=={'kind':'successor-link-intent','profile_sha256':sha(canonical(profile)),
        'response_sha256':sha(response),'lease':lease,'watchdog':watchdog,'state':'UNKNOWN'}, 'operation/lease/PID drift')
    need(type(observation) is dict and set(observation)=={'returncode','stdout_sha256','stderr_sha256','timed_out'} and
         type(observation['returncode']) is int and all(digest_ok(observation[k]) for k in ('stdout_sha256','stderr_sha256')) and
         observation['timed_out'] is False, 'terminal observation schema')
    return _write_once(folder/'terminal.json',{'kind':'successor-link-terminal','intent_sha256':intent_sha,
        'response_sha256':sha(response),'observation':observation,'executable_execution':False,
        'runtime_eligible':False,'admission_approved':False})


def run():
    # No caller arguments or booleans can enable this entry.
    raise RuntimeError('native LINK disabled: accepted exact profile, peers and authenticated launcher are unavailable')


if __name__=='__main__':run()
