"""Compile one private hierarchy-hypothesis source using the pinned unit recipe."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;RN=M3.parent;PROJECT=RN.parent;OUT=M3/'out/phase2-hkp-hierarchy-v1'
sys.path.insert(0,str(RN/'pinned-build'));import compile_units_v3 as CU


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    manifest=json.loads((OUT/'manifest.json').read_text());source=OUT/'hkpconstraintviewer.cpp';original=PROJECT/'fnv_decomp'/manifest['source'];units=PROJECT/'fnv_decomp/build/units.json'
    if sha(source)!=manifest['overlay_sha256'] or sha(original)!=manifest['source_sha256'] or sha(units)!=manifest['units_sha256']:raise ValueError('input hash changed')
    obj=OUT/'2501.hierarchy.obj';log=OUT/'2501.hierarchy.log';result=OUT/'compile-result.json';tmp=OUT/'compiler-tmp'
    if any(x.exists() for x in (obj,log,result,tmp)):raise FileExistsError('refusing overwrite')
    tc=CU.find_toolchains()['sp1']
    if not tc.get('ok'):raise RuntimeError('VC2008 SP1 compiler unavailable or wrong version')
    vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp)
    cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+manifest['flags']+['/I'+str(PROJECT/'fnv_decomp/include'),str(source),'/Fo'+str(obj)]
    p=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900)
    with log.open('x',encoding='utf8') as f:f.write(p.stdout+'\n'+p.stderr)
    meta={'rc':p.returncode,'object_present':obj.is_file(),'overlay_sha256':manifest['overlay_sha256'],'unit_index':2501,'compiler_version':tc['version'],'flags':manifest['flags']}
    if obj.is_file():meta['object_sha256']=sha(obj)
    with result.open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
    print(json.dumps(meta))
    if p.returncode or not obj.is_file():raise SystemExit(1)

if __name__=='__main__':main()
