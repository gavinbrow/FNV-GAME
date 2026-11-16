"""One-shot original CRT alias fixture; compile/link only, never execute."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SP1 = ROOT / 'build/rebuild/toolchains/sp1'
OUT = ROOT / 'build/rebuild/crt-v15-alias-component-v1'
SRC = ROOT / 'runtime/probes/crt_v15_alias_fixture.cpp'
HASHES = {
 str(SRC): 'c37f82fea744ad096615ad7b8f4c9be16925063df22f4dda501412520d7a0a59',
 str(SP1/'VC/bin/cl.exe'): '2954bed141f2f283e3109b2187406704a2d5cb6378cb3074f1b09bc5045d65c1',
 str(SP1/'VC/bin/link.exe'): 'db188969504987decffb77e15f64f1b7eb94215cea12aa6cd7901510bb21e804',
 str(SP1/'VC/bin/c1xx.dll'): '93380e0bc9505d70896ec06d973cf6e06e4a4f27ee61f5365df1c83353151a45',
 str(SP1/'VC/bin/c2.dll'): 'e3dd31ec4cb066fdf27cea24efc37944bb9d6a2720e6310213217e571f288404',
 str(SP1/'VC/lib/libcmt.lib'): 'bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411',
 str(SP1/'VC/lib/oldnames.lib'): '586557972e98e688993eb5a0a0f69996cbb2803cce9d276e8bf6ed61473d1048',
 str(SP1/'SDK/Lib/kernel32.lib'): 'a739cdc6ebbf16d052ea7a02927081ba0574ea335eaa43b4c14b7ca8b837c15f',
}
A = '_fnv_undefined_86b5006e5d6d2a0348c632bbd16e24c66b0a3804def721a1235e0f2a4af3c7e9'
B = '_fnv_undefined_d9896c4c820aa59aae9e417910a0bfa1c7374957003b682c2810dddb89febb3d'
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify():
    for p, expected in HASHES.items():
        if digest(p) != expected: raise RuntimeError('input hash mismatch: '+Path(p).name)
def note(stage, **kw):
    with (OUT/'progress.jsonl').open('a', encoding='utf8') as f:
        f.write(json.dumps(dict(stage=stage, **kw))+'\n'); f.flush(); os.fsync(f.fileno())
def main():
    if len(sys.argv)!=3: raise SystemExit('requires independent review path and trusted SHA-256')
    review=Path(sys.argv[1]).resolve(strict=True)
    if digest(review)!=sys.argv[2].lower(): raise RuntimeError('review hash mismatch')
    r=json.loads(review.read_text(encoding='utf8'))
    if r.get('approved') is not True or r.get('runner_sha256')!=digest(__file__) or r.get('source_sha256')!=HASHES[str(SRC)] or r.get('allow_native_compile_link') is not True or r.get('allow_execute') is not False: raise RuntimeError('review does not approve exact operation')
    if os.name!='nt': raise RuntimeError('requires Windows')
    if any(os.environ.get(k) for k in ('LINK','_LINK_','LIBPATH')): raise RuntimeError('implicit link options')
    verify()
    OUT.mkdir()  # Exclusive one-shot; any prior or uncertain attempt prevents rerun.
    env=os.environ.copy()
    for key in ('CL','_CL_','LINK','_LINK_','LIBPATH'): env.pop(key,None)
    env['INCLUDE']=str(SP1/'VC/include')+';'+str(SP1/'SDK/Include')
    env['LIB']=str(SP1/'VC/lib')+';'+str(SP1/'SDK/Lib')
    env['PATH']=str(SP1/'VC/bin')+os.pathsep+env['PATH']
    obj=OUT/'fixture.obj'; exe=OUT/'fixture.exe'; mapping=OUT/'fixture.map'
    commands=[ [str(SP1/'VC/bin/cl.exe'),'/nologo','/c','/MT','/EHsc','/GR','/Od','/Fo'+str(obj),str(SRC)],
      [str(SP1/'VC/bin/link.exe'),'/nologo','/machine:x86','/subsystem:console','/incremental:no','/verbose:lib','/out:'+str(exe),'/map:'+str(mapping),'/include:'+A,'/include:'+B,'/alternatename:'+A+'=___CxxFrameHandler3','/alternatename:'+B+'=___RTDynamicCast',str(obj)] ]
    note('started', review_sha256=sys.argv[2].lower(), commands=commands)
    try:
        for index,command in enumerate(commands):
            verify(); note('command_started', index=index)
            result=subprocess.run(command,cwd=OUT,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
            (OUT/('compile.log' if index==0 else 'link.log')).write_bytes(result.stdout)
            note('command_finished', index=index, returncode=result.returncode)
            verify()
            if result.returncode: raise RuntimeError('command failed: '+str(index))
        note('completed', fixture_execution=False, game_execution=False, artifacts={p.name:digest(p) for p in (obj,exe,mapping,OUT/'compile.log',OUT/'link.log')})
    except BaseException as e:
        note('failed_or_uncertain', error=repr(e)); raise
if __name__=='__main__': main()
