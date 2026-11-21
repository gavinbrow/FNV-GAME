"""Check source-supported unit425 ctor binding using archived private mirrors."""
import copy,hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-forenderedmenu-node-view-mirror';P=M/'out/phase2-forenderedmenu-node-view';D=M/'out/phase2-forenderedmenu-ctor-proof';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 unitsfile=F/'build/units.json';data=unitsfile.read_bytes()
 if hashlib.sha256(data).hexdigest()!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('recipe changed')
 units=json.loads(data)['units'];u=copy.deepcopy(units[425]);owner=copy.deepcopy(units[2629]);f=[x for x in owner['functions'] if x['address']=='0x004391c0']
 if len(f)!=1 or f[0]['symbol']!='??0FUN_004391c0@@QAE@XZ' or f[0]['size']!=156 or u['symbols'].get('??0NiAlphaProperty@@QAE@XZ')!='0x004391c0':raise ValueError('source owner mismatch')
 source=F/'src/staging/blk_00420000_od.cpp';text=source.read_text();required=['class FUN_004391c0 : public NiSpawnBase','FUN_004391c0::FUN_004391c0()','    void Init6(unsigned int a);\n    unsigned short m_0018;']
 if any(text.count(x)!=1 for x in required):raise ValueError('owner source body mismatch')
 obj=RN/'pinned-build/obj_v3/2629.obj';D.mkdir(exist_ok=False);shutil.copyfile(obj,D/'2629.obj');shutil.copyfile(source,D/'owner.cpp');shutil.copyfile(unitsfile,D/'units.json')
 c=Coff(str(D/'2629.obj'));pe=Pe(paths.REF_IMAGE);owner['functions']=f;result=compare(c,pe,owner)
 if len(result)!=1 or result[0]['verdict']!='match':raise ValueError('source owner body fails reference')
 report=json.loads((O/'compile-result.json').read_text());objs={'production':Coff(str(O/'production-baseline.obj'))}
 for row in report['outcomes']:
  p=O/(row['tag']+'.obj')
  if row['rc'] or not row['trace_valid'] or sha(p)!=row['object_sha256']:raise ValueError('mirror invalid')
  objs[row['tag']]=Coff(str(p))
 binding={'??0FUN_004391c0@@QAE@XZ':'0x004391c0'};u['symbols'].update(binding);candidate=json.loads((P/'unit-overlay.json').read_text());candidate['symbols'].update(binding)
 results={}
 for tag,spec in [('production',u),('original',u),('candidate',candidate)]:
  rows=compare(objs[tag],pe,spec);sections,inferred,errors=eh_sections(objs[tag],pe,spec,rows,recipe_names(units));results[tag]={'functions':len(rows),'matches':sum(x['verdict']=='match' for x in rows),'eh_sections':len(sections),'eh_failed':sum(not x[2] for x in sections),'eh_errors':errors,'inferred':{k:hex(v) for k,v in inferred.items()}}
  if len(rows)!=44 or any(x['verdict']!='match' for x in rows) or any(not x[2] for x in sections) or errors:raise ValueError('reference/EH mismatch '+tag)
 out={'scope':'source-backed unit-local constructor binding; no canonical class identity claim','owner_unit':2629,'owner_object_sha256':sha(D/'2629.obj'),'owner_source_sha256':sha(D/'owner.cpp'),'recipe_sha256':sha(D/'units.json'),
   'owner_reference_match':True,'owner_reference_relocations':len(result[0]['relocations']),'binding':binding,
   'caller_reference':'0x007fc32b allocates 0x1c and 0x007fc348 calls constructor on allocation; owner source base size0x18 plus 2-byte member rounds to0x1c',
   'owner_source_scope_warning':'same global surrogate spelling has incompatible source base views; this does not prove ODR compatibility',
   'mirror_manifest_sha256':sha(O/'mirror-manifest.json'),'compile_result_sha256':sha(O/'compile-result.json'),'results':results}
 (D/'proof.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'output':str(D/'proof.json'),'sha256':sha(D/'proof.json'),'results':results}))
if __name__=='__main__':main()
