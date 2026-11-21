"""Compile unit925 baseline and private SkyObject candidate, in a private lane."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;RN=M3.parent;PROJECT=RN.parent;FN=PROJECT/'fnv_decomp';OUT=M3/'out/phase2-skyobject-destructor-v1'
sys.path.insert(0,str(RN/'pinned-build'));import compile_units_v3 as CU


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    meta=json.loads((OUT/'manifest.json').read_text());original=FN/meta['source'];overlay=OUT/'skyobject.cpp';header=OUT/'skyobject.h';unit=FN/'build/units.json'
    checks=[(original,meta['input_sha256']['source']),(unit,meta['input_sha256']['units']),(overlay,meta['source_overlay_sha256']),(header,meta['header_overlay_sha256'])]+[(FN/r['path'],r['sha256']) for r in meta['original_include_closure']]
    for path,digest in checks:
        if sha(path)!=digest:raise ValueError('input digest mismatch: '+path.name)
    if (FN/'src/malloc.h').exists() or (FN/'src/stddef.h').exists():raise ValueError('unexpected source-directory system include shadow')
    tmp=OUT/'compiler-tmp';result=OUT/'compile-result.json';plans=[('original',original),('combined',overlay)]
    if any(p.exists() for p in [tmp,result]+[OUT/('0925.%s.%s'%(tag,ext)) for tag,_ in plans for ext in ('obj','log')]):raise FileExistsError('refusing overwrite')
    tc=CU.find_toolchains()['sp1']
    if not tc.get('ok'):raise RuntimeError('VC2008 SP1 compiler unavailable or wrong version')
    vc=Path(tc['vc']);env=CU.make_env(vc,Path(tc['sdk']) if tc['sdk']!='None' else None);tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);rows=[]
    for tag,src in plans:
        obj=OUT/('0925.%s.obj'%tag);log=OUT/('0925.%s.log'%tag)
        # The private source picks the private override header first; subsequent quoted
        # includes resolve to the original src directory, then the normal include root.
        includes=(['/I'+str(FN/'src/fallout_shared/sky'),'/I'+str(FN/'src')] if tag=='combined' else [])+['/I'+str(FN/'include')]
        cmd=[str(vc/'bin/cl.exe'),'/c','/nologo']+meta['flags']+includes+[str(src),'/Fo'+str(obj)]
        p=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900)
        with log.open('x',encoding='utf8') as f:f.write(p.stdout+'\n'+p.stderr)
        row={'source':tag,'source_sha256':sha(src),'rc':p.returncode,'object_present':obj.is_file()}
        if obj.is_file():row['object_sha256']=sha(obj)
        rows.append(row)
        if p.returncode or not obj.is_file():break
    report={'unit_index':925,'flags':meta['flags'],'compiler_version':tc['version'],'outcomes':rows}
    with result.open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
    if len(rows)!=2 or any(x['rc'] or not x['object_present'] for x in rows):raise SystemExit(1)

if __name__=='__main__':main()
