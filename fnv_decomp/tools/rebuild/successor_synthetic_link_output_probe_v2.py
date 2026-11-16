"""Authored-synthetic VC++ 2008 SP1 LINK output probe: disabled source draft.

No compiler, linker, game, object or native tool is invoked by this module.
The tiny fixture below is wholly authored for this probe. Private fixture
functions validate hypothetical saved metadata and once-only state; they do
not authenticate caller values or authorize an operation. The actual Windows
held watchdog, exclusive tree setup, runtime/source checks, filesystem observer,
compiler, linker and independent reviews must be separately implemented and
frozen before any future run. No user/game input is accepted as fixture code.
"""
import hashlib
import json
import os
from pathlib import Path
import re

FIXTURE_SOURCE=b'int main(void) { return 0; }\r\n'
FIXTURE_SHA256=hashlib.sha256(FIXTURE_SOURCE).hexdigest()
# Deliberately absent until separately independently reviewed and frozen.
FIXED_PROFILE=None
COMPILER_IDENTITY=None
LINKER_IDENTITY=None
WATCHDOG_IDENTITY=None
SOURCE_REVIEW=None
OPERATION_REVIEW=None


def need(ok, message):
    if not ok:raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def sha(data):return hashlib.sha256(data).hexdigest()


def hash_ok(value):return type(value) is str and re.fullmatch('[0-9a-f]{64}',value) is not None


def _identity(value):
    need(type(value) is dict and set(value)=={'path','sha256','size','device','inode'} and
         type(value['path']) is str and value['path'] and hash_ok(value['sha256']) and
         all(type(value[k]) is int and value[k]>=0 for k in ('size','device','inode')), 'physical identity differs')


def _relative_path(value):
    """Strict portable profile spelling, not a filesystem identity check."""
    need(type(value) is str and value and '\\' not in value and not value.startswith('/') and
         not value.endswith('/'), 'canonical relative path required')
    components=value.split('/')
    reserved=({'CON','PRN','AUX','NUL','CONIN$','CONOUT$'} |
              {'COM'+n for n in '123456789'} | {'LPT'+n for n in '123456789'})
    need(all(re.fullmatch(r'[A-Za-z0-9_.-]+',part) and part not in ('.','..') and
             not part.endswith('.') and part.split('.',1)[0].upper() not in reserved for part in components),
             'unsafe relative path component')
    return value.casefold()


def _profile_fixture(profile):
    """Exact proposed two-stage commands; all paths/reviews are externally fixed."""
    need(type(profile) is dict and set(profile)=={'kind','version','fixture_sha256','compiler','compiler_version','linker','paths',
         'compile_argv','link_argv','lease','watchdog_sha256','source_review_sha256','operation_review_sha256',
         'seconds','memory_bytes','output_bytes'} and profile['kind']=='authored-synthetic-vc2008-link-output-probe' and
         type(profile['version']) is int and profile['version']==1 and profile['fixture_sha256']==FIXTURE_SHA256,
         'probe profile differs')
    need(profile['compiler_version']=='15.00.30729.01', 'VC++ 2008 SP1 version required')
    _identity(profile['compiler']);_identity(profile['linker'])
    paths=profile['paths'];need(type(paths) is dict and set(paths)=={'workspace','source','object','executable','map','control'} and
         all(type(v) is str and v for v in paths.values()) and len({v.casefold() for v in paths.values()})==len(paths),
         'exact disjoint paths required')
    normalized={key:_relative_path(value) for key,value in paths.items()}
    workspace=normalized['workspace']
    need(all(normalized[key].startswith(workspace+'/') for key in paths if key!='workspace'),
         'probe paths must remain under workspace')
    leaves=[normalized[key] for key in paths if key!='workspace']
    need(all(not (a==b or a.startswith(b+'/') or b.startswith(a+'/'))
             for i,a in enumerate(leaves) for b in leaves[i+1:]), 'probe paths overlap')
    need(profile['compile_argv']==[profile['compiler']['path'],'/nologo','/c','/GS-','/Od',
                                   '/Fo'+paths['object'],paths['source']] and
         profile['link_argv']==[profile['linker']['path'],'/NOLOGO','/NODEFAULTLIB','/INCREMENTAL:NO',
              '/SUBSYSTEM:CONSOLE','/ENTRY:main','/OUT:'+paths['executable'],'/MAP:'+paths['map'],paths['object']],
         'probe command differs')
    need(all(hash_ok(profile[k]) for k in ('watchdog_sha256','source_review_sha256','operation_review_sha256')) and
         len({profile[k] for k in ('watchdog_sha256','source_review_sha256','operation_review_sha256')})==3,
         'separate watchdog and reviews required')
    lease=profile['lease'];need(type(lease) is dict and set(lease)=={'owner','resource','slot','grant_sha256'} and
         type(lease['owner']) is str and lease['owner'] and lease['resource']=='CPU_heavy' and
         type(lease['slot']) is int and lease['slot'] in (1,2) and hash_ok(lease['grant_sha256']), 'lease scope differs')
    need(all(type(profile[k]) is int and profile[k]>0 for k in ('seconds','memory_bytes','output_bytes')) and
         profile['seconds']<=180 and profile['memory_bytes']<=1073741824 and profile['output_bytes']<=134217728,
         'resource caps differ')
    return profile


def _held_fixture(profile, held, active_lease):
    """Synthetic session relation only, never a live Job or lease observation."""
    need(type(active_lease) is dict and set(active_lease)=={'owner','resource','slot','grant_sha256'} and
         active_lease==profile['lease'], 'active lease differs')
    need(type(held) is dict and set(held)=={'profile_sha256','parent','child','job','nonce'} and
         held['profile_sha256']==sha(canonical(profile)) and type(held['job']) is str and held['job'] and
         hash_ok(held['nonce']), 'held watchdog session differs')
    for key in ('parent','child'):
        p=held[key];need(type(p) is dict and set(p)=={'pid','creation','image'} and type(p['pid']) is int and p['pid']>0 and
           type(p['creation']) is int and p['creation']>0 and type(p['image']) is str and p['image'],'process identity')
    need(held['parent']['pid']!=held['child']['pid'], 'parent child collision')


def _write_once(path,record):
    data=canonical(record)+b'\n'
    with Path(path).open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    need(Path(path).read_bytes()==data,'receipt readback differs')
    return sha(data)


def _begin_fixture(folder,profile,fixture,held,active_lease):
    _profile_fixture(profile);need(type(fixture) is bytes and fixture==FIXTURE_SOURCE,'authored fixture differs')
    _held_fixture(profile,held,active_lease)
    folder=Path(folder);need(not folder.exists(),'once journal exists; reconcile')
    folder.mkdir()
    return _write_once(folder/'intent.json',{'kind':'authored-probe-intent','profile_sha256':sha(canonical(profile)),
        'fixture_sha256':sha(fixture),'held':held,'lease':active_lease,'state':'UNKNOWN'})


def _inventory_fixture(before, after):
    """Compute saved metadata difference; inventories do not prove all IO."""
    def checked(rows):
        need(type(rows) is list and len(rows)<=10000, 'bounded inventory required')
        result={}
        for row in rows:
            need(type(row) is dict and set(row)=={'relative_path','size','sha256'} and
                 type(row['relative_path']) is str and '/' not in row['relative_path'] and
                 _relative_path(row['relative_path']) not in result and type(row['size']) is int and row['size']>=0 and
                 hash_ok(row['sha256']), 'inventory row differs')
            result[row['relative_path'].casefold()]=row
        return result
    old=checked(before);new=checked(after)
    return {'added':[new[k] for k in sorted(new.keys()-old.keys())],
            'removed':[old[k] for k in sorted(old.keys()-new.keys())],
            'changed':[{'before':old[k],'after':new[k]} for k in sorted(old.keys()&new.keys()) if old[k]!=new[k]],
            'complete_process_io_observed':False,'filesystem_race_free':False}


def run():
    raise RuntimeError('synthetic probe disabled: fixed reviewed profiles and authenticated held launcher unavailable')


if __name__=='__main__':run()
