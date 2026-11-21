"""Private PSA experiment: freeze, compile, then compare; run only in compiler lane."""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
M = H.parent
RN = M.parent
ROOT = RN.parent
FN = ROOT / 'fnv_decomp'
OUT = M / 'out/phase2-bgsbodypart-psa-proposal'
sys.path[:0] = [str(H), str(RN), str(FN / 'tools'), str(RN / 'pinned-build')]

def include_closure(source):
    pending=[source]; seen={}; external=set()
    while pending:
        path=pending.pop().resolve()
        if path in seen:
            continue
        if not path.is_relative_to(FN.resolve()):
            raise ValueError('include escapes source tree')
        data=path.read_bytes(); seen[path]=digest(path)
        for style,name in re.findall(rb'^\s*#\s*include\s*(["<])([^">\r\n]+)[">]',data,re.M):
            name=name.decode('ascii')
            if style==b'<':
                external.add(name); continue
            found=next((x for x in (path.parent/name,FN/'src/fallout_shared'/name,FN/'src'/name,FN/'include'/name) if x.is_file()),None)
            if found is None:
                external.add(name)
            else:
                pending.append(found)
    return ([{'path':p.relative_to(FN.resolve()).as_posix(),'sha256':v} for p,v in sorted(seen.items(),key=lambda x:str(x[0]))],sorted(external))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load():
    return json.loads((OUT / 'manifest.json').read_text())


def freeze():
    meta = load()
    paths = {'620.cpp': FN/'src/fallout_shared/bgsbodypart.cpp',
             '620.h': FN/'src/fallout_shared/bgsbodypart_decls.h',
             '621.cpp': FN/'src/fallout_shared/bgsbodypartdata.cpp',
             '621.h': FN/'src/fallout_shared/bgsbodypartdata.h', 'units': FN/'build/units.json'}
    for k, p in paths.items():
        if digest(p) != meta['input_sha256'][k]:
            raise ValueError('input changed: ' + k)
    outputs = {'620.cpp': OUT/'620/bgsbodypart.cpp', '620.h': OUT/'620/bgsbodypart_decls.h',
               '621.cpp': OUT/'621/bgsbodypartdata.cpp', '621.h': OUT/'621/bgsbodypartdata.h'}
    for k in ('620.cpp', '621.cpp', '621.h'):
        if digest(outputs[k]) != meta['input_sha256'][k]:
            raise ValueError('mirror is not byte-identical to original: ' + k)
    if digest(outputs['620.h']) != meta['candidate_header_sha256']:
        raise ValueError('candidate override changed')
    closure = {}
    for index in (620, 621):
        rows, system = include_closure(paths[str(index)+'.cpp'])
        closure[str(index)] = {'quoted': rows, 'system': system}
    frozen = {'schema': 1, 'provenance': 'byte-identical source mirrors and unit621 header; unit620 header is sole override',
              'manifest_sha256': digest(OUT/'manifest.json'), 'files': {k: digest(v) for k,v in paths.items()},
              'mirrors': {k: digest(v) for k,v in outputs.items()}, 'include_closure': closure}
    target = OUT/'lane-freeze.json'
    with target.open('x', encoding='utf8') as f:
        json.dump(frozen, f, indent=2)
    print(json.dumps({'freeze': str(target), 'sha256': digest(target)}))


def validate():
    f = json.loads((OUT/'lane-freeze.json').read_text())
    if digest(OUT/'manifest.json') != f['manifest_sha256']:
        raise ValueError('manifest changed')
    meta = load()
    for row in f['include_closure'].values():
        for item in row['quoted']:
            if digest(FN/item['path']) != item['sha256']:
                raise ValueError('include changed: '+item['path'])
        for name in row['system']:
            if any((p/name).is_file() for p in (FN/'src/fallout_shared',FN/'src',FN/'include')):
                raise ValueError('external include newly shadowed: '+name)
    if digest(FN/'build/units.json') != f['files']['units']:
        raise ValueError('recipe changed')
    for index, source, header in ((620,'bgsbodypart.cpp','bgsbodypart_decls.h'),(621,'bgsbodypartdata.cpp','bgsbodypartdata.h')):
        for kind,name in (('cpp',source),('h',header)):
            if digest(OUT/str(index)/name) != f['mirrors'][str(index)+'.'+kind]:
                raise ValueError('mirror changed')
    return meta, f


def compile_all():
    import compile_units_v3 as CU
    meta, _ = validate()
    result = OUT/'lane-compile.json'
    if result.exists():
        raise FileExistsError(result)
    tc = CU.find_toolchains()['sp1']
    if not tc.get('ok'):
        raise RuntimeError('VC2008 SP1 unavailable')
    vc = Path(tc['vc'])
    env = CU.make_env(vc, Path(tc['sdk']) if tc['sdk'] != 'None' else None)
    tmp = OUT/'lane-tmp'
    tmp.mkdir()
    env['TMP'] = env['TEMP'] = str(tmp)
    rows = []
    for index in (620,621):
        spec = meta['units'][str(index)]
        for tag in ('original','mirror'):
            source = FN/spec['source'] if tag == 'original' else OUT/str(index)/Path(spec['source']).name
            obj = OUT/('%04d.%s.obj' % (index,tag))
            log = OUT/('%04d.%s.log' % (index,tag))
            if obj.exists() or log.exists():
                raise FileExistsError(str(obj))
            inc = ([] if tag == 'original' else ['/I'+str(FN/'src/fallout_shared'), '/I'+str(FN/'src')])
            cmd = [str(vc/'bin/cl.exe'),'/c','/nologo']+spec['flags']+inc+['/I'+str(FN/'include'),str(source),'/Fo'+str(obj)]
            p = subprocess.run(cmd,cwd=OUT,env=env,capture_output=True,text=True,errors='replace',stdin=subprocess.DEVNULL,timeout=900)
            log.write_text(p.stdout+'\n'+p.stderr,encoding='utf8')
            row = {'unit':index,'tag':tag,'rc':p.returncode,'source_sha256':digest(source),
                   'object_sha256':digest(obj) if obj.is_file() else None,'log_sha256':digest(log)}
            rows.append(row)
            if p.returncode or not obj.is_file():
                result.write_text(json.dumps({'outcomes':rows},indent=2),encoding='utf8')
                raise RuntimeError('compile failed; inspect saved log')
    result.write_text(json.dumps({'compiler_version':tc['version'],'outcomes':rows},indent=2),encoding='utf8')
    print(json.dumps({'compiled':len(rows),'result':str(result)}))


def compare_all():
    from compare import Coff, Pe, compare
    import paths
    from rtti_hkp_viewer_compare import relocated
    meta, _ = validate()
    result = json.loads((OUT/'lane-compile.json').read_text())
    rows = {(x['unit'],x['tag']):x for x in result['outcomes']}
    if len(rows)!=4 or any(x['rc'] for x in rows.values()):
        raise ValueError('four successful objects required')
    units = json.loads((FN/'build/units.json').read_text())['units']
    pe = Pe(paths.REF_IMAGE)
    reports = {}
    for index in (620,621):
        cs = {}
        for tag in ('original','mirror'):
            p=OUT/('%04d.%s.obj'%(index,tag))
            if digest(p)!=rows[index,tag]['object_sha256']:
                raise ValueError('object digest mismatch')
            cs[tag]=Coff(str(p))
        unit=units[index]
        # Explicitly anchored by original constructor and destructor disassembly;
        # native symbols are accepted only if actually present in emitted COFF.
        aliases = ({'??0TESModelPSA@@QAE@XZ':'??0FUN_005e3be0@@QAE@XZ',
                    '??1TESModelPSA@@QAE@XZ':'??1FUN_005e3c60_psa@@QAE@XZ'} if index==620 else {})
        present={s['name'] for s in cs['mirror'].symbols.values() if s and 'name' in s}
        aliases={k:v for k,v in aliases.items() if k in present}
        mapped=copy.deepcopy(unit)
        for native,old in aliases.items():
            if old not in unit['symbols']:
                raise ValueError('alias missing original recipe')
            mapped['symbols'][native]=unit['symbols'][old]
        functions=[]
        for f in unit['functions']:
            try:
                a,ar=relocated(cs['original'],f['symbol'],f['size'],{})
                b,br=relocated(cs['mirror'],f['symbol'],f['size'],aliases)
                functions.append({'address':f['address'],'symbol':f['symbol'],'bytes_equal':a==b,
                                  'relocations_equal':ar==br,'original_relocations':len(ar),'mirror_relocations':len(br)})
            except (ValueError,KeyError,IndexError) as exc:
                functions.append({'address':f['address'],'symbol':f['symbol'],'error':str(exc)})
        refs={}
        for tag,spec in (('original',unit),('mirror',mapped)):
            try:
                refs[tag]=compare(cs[tag],pe,spec)
            except Exception as exc:
                refs[tag]={'fatal':type(exc).__name__+': '+str(exc)}
        # Save every section and relocation descriptor; function equality alone is not an EH gate.
        sections={}
        for tag,c in cs.items():
            sections[tag]=[{'name':s['name'],'size':len(s['data']),
                            'sha256':hashlib.sha256(s['data']).hexdigest(),
                            'relocations':[(o,k,c.symbols[j]['name']) for o,j,k in s['relocs']]}
                           for s in c.sections if s and 'data' in s]
        reports[str(index)]={'functions':functions,'applied_emitted_aliases':aliases,'reference':refs,'sections':sections}
    output=OUT/'lane-comparison.json'
    with output.open('x',encoding='utf8') as f:
        json.dump(reports,f,indent=2,default=str)
    print(json.dumps({'comparison':str(output),'counts':{k:len(v['functions']) for k,v in reports.items()},
                      'status':'raw results require independent EH and metadata review; no automatic pass'}))


if __name__ == '__main__':
    {'freeze':freeze,'compile':compile_all,'compare':compare_all}[sys.argv[1]]()
