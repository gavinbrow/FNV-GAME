"""Compile/check the private six-byte W-tail fixture in a coordinated lane."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;PROJECT=RN.parent;OUT=M/'out/phase2-hkp-hierarchy-v1'
sys.path[:0]=[str(M),str(RN/'pinned-build'),str(PROJECT/'fnv_decomp/tools')]
import gen_m3 as g,compile_units_v3 as cu,splice
from compare import Coff


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    meta=json.loads((OUT/'tail-fixture.json').read_text());src=OUT/'tail-fixture.cpp';obj=OUT/'tail-fixture.obj';log=OUT/'tail-fixture.log';report=OUT/'tail-fixture-result.json';tmp=OUT/'tail-compiler-tmp'
    if sha(src)!=meta['source_sha256']:raise ValueError('fixture digest mismatch')
    if any(p.exists() for p in (obj,log,report,tmp)):raise FileExistsError('refusing overwrite')
    tc=cu.find_toolchains()['sp1']
    if not tc.get('ok'):raise RuntimeError('VC2008 SP1 unavailable')
    vc=Path(tc['vc']);env=cu.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp)
    flags=['/MT','/Od','/Oy-','/GS','/EHsc','/Gy'];cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+flags+[str(src),'/Fo'+str(obj)]
    p=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900)
    with log.open('x',encoding='utf8') as f:f.write(p.stdout+'\n'+p.stderr)
    result={'rc':p.returncode,'object_present':obj.is_file(),'source_sha256':meta['source_sha256'],'compiler_version':tc['version'],'flags':flags}
    if p.returncode==0 and obj.is_file():
        result['object_sha256']=sha(obj);e=g.build_entries([meta['selection']])[0];original_path=g.obj_path;original_neg=g.ANYNEG
        try:
            g.obj_path=lambda k:str(obj);g.ANYNEG=False;bad=g.check([e])
        finally:g.obj_path=original_path;g.ANYNEG=original_neg
        result['self_check_errors']=bad
        if not bad:
            data,rel,section,flags,storage=splice.slice_entry(Coff(str(obj)),e)
            result['verified']={'section':section,'storage':storage,'byte_count':len(data),'relocations':[{'offset':x[0],'symbol':x[1],'addend':x[2]} for x in rel]}
    with report.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
    if p.returncode or not obj.is_file() or result.get('self_check_errors'):raise SystemExit(1)

if __name__=='__main__':main()
