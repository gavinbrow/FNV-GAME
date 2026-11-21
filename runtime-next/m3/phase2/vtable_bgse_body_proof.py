"""Check generated BGSE deleting destructor against source-backed body mapping."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;sys.path[:0]=[str(P/'fnv_decomp/tools'),str(RN)];from compare import Coff,Pe,compare;import paths
O=M/'out/phase2-bgsencounterzone-six-override';D=M/'out/phase2-vtable-bgse-search'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((O/'manifest.json').read_text());u=json.loads((P/'fnv_decomp/build/units.json').read_bytes())['units'][2];obj=O/'0002.combined.obj';c=json.loads((O/'compile-result.json').read_text());row=next(x for x in c['outcomes'] if x['source']=='combined')
 if row['rc'] or sha(obj)!=row['object_sha256']:raise ValueError('compiled candidate mismatch')
 f=[x for x in u['functions'] if x['address']=='0x00525cb0'];d=[x for x in m['proposed_function_symbol_changes'] if x['address']=='0x00525ce0']
 if len(f)!=1 or f[0]['symbol']!='?Destroy@FUN_00525cb0_shell@@QAEPAU1@I@Z' or f[0]['size']!=44 or len(d)!=1 or d[0]['after']!='??1BGSEncounterZone@@UAE@XZ':raise ValueError('source mapping mismatch')
 original=json.loads((O/'coff-comparison-v2.json').read_text());
 for tag in ('original','combined'):
  match=[x for x in original['reference_comparator'][tag] if x['address']=='0x00525ce0']
  if len(match)!=1 or match[0]['verdict']!='match':raise ValueError('native destructor proof missing')
 old='?FUN_00525ce0@FUN_00525cb0_shell@@QAEXXZ';new=d[0]['after'];
 if u['symbols'].get(old)!='0x00525ce0' or (new in u['symbols'] and u['symbols'][new]!='0x00525ce0'):raise ValueError('destructor callee source mapping ambiguous')
 v=copy.deepcopy(u);v['functions']=[dict(f[0],symbol='??_GBGSEncounterZone@@UAEPAXI@Z')];v['symbols'][new]='0x00525ce0';rows=compare(Coff(obj),Pe(paths.REF_IMAGE),v)
 if len(rows)!=1 or rows[0]['verdict']!='match' or len(rows[0]['relocations'])!=2 or not all(x['match'] for x in rows[0]['relocations']):raise ValueError('generated body or relocation mismatch')
 out={'scope':'generated scalar-deleting destructor compared at source recipe shell address, no vtable target used','object_sha256':sha(obj),'recipe_sha256':sha(P/'fnv_decomp/build/units.json'),'comparison_sha256':sha(O/'coff-comparison-v2.json'),'source_address':f[0]['address'],'source_symbol':f[0]['symbol'],'generated_symbol':v['functions'][0]['symbol'],'size':44,'callee_mapping':{'source_symbol':old,'native_symbol':new,'address':'0x00525ce0','basis':'same independently checked source destructor'},'verdict':rows[0]['verdict'],'relocations':rows[0]['relocations'],'limitations':['placement and ownership need independent checks','weak library precedence outside frozen cohort is unresolved','class ABI and runtime gates are separate']}
 path=D/'generated-body-proof.json';
 if path.exists():raise FileExistsError('refusing overwrite')
 path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'verdict':out['verdict'],'relocations':len(out['relocations'])}))
if __name__=='__main__':main()
