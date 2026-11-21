"""Bounded independent proof for compiler-emitted TESForm no-op fold candidates."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths
from rtti_hkp_viewer_compare import relocated
SYMS=['?ClearData@TESForm@@UAEXXZ','?Init@TESForm@@UAEXXZ','?Free@TESForm@@UAEXXZ'];VA='0x00483710';SIZE=11

def main(objpath,compile_result,output):
 objpath=Path(objpath);compile_result=Path(compile_result);output=Path(output)
 if output.exists():raise FileExistsError('refusing overwrite')
 c=json.loads(compile_result.read_text()); rows=[x for x in c['outcomes'] if x.get('source')=='tes_overlay' or x.get('tag')=='candidate']
 if c.get('unit_index',998)!=998 or len(rows)!=1 or rows[0]['rc'] or (rows[0].get('tag')=='candidate' and (c.get('unit_index')!=998 or rows[0].get('trace_valid') is not True)) or hashlib.sha256(objpath.read_bytes()).hexdigest()!=rows[0]['object_sha256']:raise ValueError('overlay object differs from compile evidence')
 u=json.loads((F/'build/units.json').read_bytes())['units'][998];f=[f for f in u['functions'] if f['address']==VA]
 if len(f)!=1 or f[0]['symbol']!=SYMS[0] or f[0]['size']!=SIZE:raise ValueError('source recipe mismatch')
 o=Coff(str(objpath));data=[];results=[];pe=Pe(paths.REF_IMAGE)
 for name in SYMS:
  raw,rel=relocated(o,name,SIZE,{})
  if rel:raise ValueError('no-op contains relocations; cannot prove fold')
  spec=copy.deepcopy(u);spec['functions']=[dict(f[0],symbol=name)];spec['symbols']=dict(u['symbols']);spec['symbols'].pop(name,None)
  r=compare(o,pe,spec)
  if len(r)!=1 or r[0]['verdict']!='match':raise ValueError('no-op does not match source recipe target')
  sym=o.named(name);sec=o.sections[sym['section']];start=sym['value']
  nxt=[x['value'] for x in o.symbols.values() if x['section']==sym['section'] and x['type']&0x20 and x['value']>start and not x['name'].startswith('__catch$')]
  end=min(nxt) if nxt else len(sec['data'])
  if end-start<SIZE or any(b not in (0xcc,0x90) for b in sec['data'][start+SIZE:end]):raise ValueError('generated no-op extent differs from recipe')
  data.append(raw);results.append({'symbol':name,'section':sym['section'],'offset':sym['value'],'reference_verdict':r[0]['verdict'],'relocations':len(rel)})
 if len(set(data))!=1:raise ValueError('compiler emitted no-op bodies differ')
 out={'scope':'three complete generated function bodies independently compared at source-backed target; does not install or prove final ICF placement','object_sha256':hashlib.sha256(objpath.read_bytes()).hexdigest(),'recipe_sha256':hashlib.sha256((F/'build/units.json').read_bytes()).hexdigest(),'source_target':VA,'size':SIZE,'bodies':results,'identical_bodies':True,'limitations':['assembler fold mapping and duplicate ownership not yet installed','no proof of full class hierarchy or global ODR']}
 output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'equal':True,'size':SIZE,'symbols':len(results)}))
if __name__=='__main__':
 if len(sys.argv)!=4:raise SystemExit('usage: python -I vtable_tesform_noop_compare.py OBJ COMPILE_RESULT OUT_JSON')
 main(*sys.argv[1:])
