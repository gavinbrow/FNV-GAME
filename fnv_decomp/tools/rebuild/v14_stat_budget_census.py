"""One-shot exact V14 budgeting census: target lstat only; no target contents."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT=Path(__file__).resolve().parents[2]
PLAN=ROOT/'build/rebuild/v14-exact-stat-only-plan-v1.json'
PLAN_SHA256='6a113addd0ee7fad9748aad68662e6eabf186972fc2e752e1c1c3114e5308669'
OUTPUT=ROOT/'build/rebuild/v14-exact-stat-only-result-v1.json'
CONTROL=ROOT/'build/rebuild/v14-exact-stat-only-control-v1'


def census(plan, lstat=os.lstat):
    """Observe only exact path identity/size; callers must authenticate plan."""
    if (type(plan) is not dict or plan.get('kind')!='v14-exact-source-reference-stat-only-plan' or
            plan.get('production_authorized') is not False or type(plan.get('paths')) is not list or
            len(plan['paths'])!=10):
        raise ValueError('exact ten-path stat plan required')
    rows=plan['paths']; paths=[row['path'] for row in rows]
    if (len(set(paths))!=10 or sum(row.get('role')=='source' for row in rows)!=9 or
            sum(row.get('role')=='reference' for row in rows)!=1 or
            any(type(path) is not str or not Path(path).is_absolute() for path in paths)):
        raise ValueError('unique absolute nine-source/one-reference paths required')
    result=[]
    for row in rows:
        info=lstat(row['path'])
        if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or
                getattr(info,'st_file_attributes',0)&0x400 or type(info.st_size) is not int or info.st_size<0):
            raise ValueError('regular non-reparse target required')
        result.append({'role':row['role'],'path':row['path'],'recipe_id':row.get('recipe_id'),
            'size':info.st_size,'device':info.st_dev,'file_id':info.st_ino,'modified_ns':info.st_mtime_ns})
    return result



def process_identity():
    import ctypes
    if os.name!='nt':
        raise ValueError('Windows process creation identity required')
    class FileTime(ctypes.Structure):
        _fields_=[('low',ctypes.c_ulong),('high',ctypes.c_ulong)]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.GetProcessTimes.argtypes=[ctypes.c_void_p,ctypes.POINTER(FileTime),ctypes.POINTER(FileTime),ctypes.POINTER(FileTime),ctypes.POINTER(FileTime)]
    values=[FileTime() for _ in range(4)]
    if not kernel.GetProcessTimes(kernel.GetCurrentProcess(),*(ctypes.byref(v) for v in values)):
        raise OSError('process creation identity unavailable')
    return {'pid':os.getpid(),'creation_filetime':values[0].low+(values[0].high<<32)}


def write_once(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,sort_keys=True,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())


def run():
    if OUTPUT.exists() or OUTPUT.is_symlink() or CONTROL.exists() or CONTROL.is_symlink():
        raise FileExistsError('exclusive result and control required; never replay')
    identity=process_identity()
    CONTROL.mkdir(parents=False,exist_ok=False)
    write_once(CONTROL/'intent.json',dict(status='started-no-retry',process=identity,plan_sha256=PLAN_SHA256))
    try:
        with PLAN.open('rb') as stream:
            raw=stream.read(1024*1024+1)
        if len(raw)>1024*1024 or hashlib.sha256(raw).hexdigest()!=PLAN_SHA256:
            raise ValueError('reviewed exact plan differs')
        plan=json.loads(raw)
        rows=census(plan)
        result={'schema_version':1,'kind':'v14-exact-source-reference-stat-only-result',
            'status':'metadata-only-not-admission','plan_sha256':PLAN_SHA256,'rows':rows,
            'content_read':False,'content_hash_verified':False,'freshness_proved':False,
            'original_object_accessed':False,'reference_payload_read':False,'production_authorized':False}
        write_once(OUTPUT,result)
        with OUTPUT.open('rb') as stream: result_sha256=hashlib.sha256(stream.read(1024*1024+1)).hexdigest()
        write_once(CONTROL/'terminal.json',dict(status='completed-not-admission',process=identity,result_sha256=result_sha256))
        return result
    except BaseException as error:
        write_once(CONTROL/'terminal.json',dict(status='failed-no-retry',process=identity,error_type=type(error).__name__))
        raise


if __name__=='__main__':
    run()
