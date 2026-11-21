"""Compile exactly one reviewed source unit and its private name overlay."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
M3=HERE.parent; RN=M3.parent; PROJECT=RN.parent; OUT=M3/'out/phase2-hkp-constraint-viewer'
sys.path.insert(0,str(RN/'pinned-build'))
import compile_units_v3 as CU


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest=json.loads((OUT/'manifest.json').read_text()); overlay=OUT/'hkpconstraintviewer.cpp'; original=PROJECT/'fnv_decomp'/manifest['source']
    if sha(overlay)!=manifest['overlay_sha256'] or sha(original)!=manifest['source_sha256']: raise ValueError('source digest mismatch')
    result=OUT/'compile-result.json'; tmp=OUT/'compiler-tmp'; plans=[('original',original),('overlay',overlay)]
    paths=[result,tmp]+[OUT/('2501.%s.%s'%(tag,ext)) for tag,_ in plans for ext in ('obj','log')]
    if any(p.exists() for p in paths): raise FileExistsError('refusing to overwrite a previous compile attempt')
    tc=CU.find_toolchains()['sp1']
    if not tc.get('ok'): raise RuntimeError('VC2008 SP1 compiler unavailable or wrong version')
    vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None)
    tmp.mkdir();env['TMP']=env['TEMP']=str(tmp)
    outcomes=[]
    for tag,source in plans:
        obj=OUT/('2501.%s.obj'%tag); log=OUT/('2501.%s.log'%tag)
        cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+manifest['flags']+['/I'+str(PROJECT/'fnv_decomp/include'),str(source),'/Fo'+str(obj)]
        p=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900)
        with log.open('x',encoding='utf8') as f:f.write(p.stdout+'\n'+p.stderr)
        row={'source':tag,'source_sha256':sha(source),'rc':p.returncode,'object_present':obj.is_file()}
        if obj.is_file():row['object_sha256']=sha(obj)
        outcomes.append(row)
        if p.returncode or not obj.is_file():break
    meta={'unit_index':manifest['unit_index'],'compiler_version':tc['version'],'flags':manifest['flags'],'outcomes':outcomes}
    with result.open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
    print(json.dumps(meta))
    if len(outcomes)!=2 or any(x['rc'] or not x['object_present'] for x in outcomes):raise SystemExit(1)

if __name__=='__main__':main()
