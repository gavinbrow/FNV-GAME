"""Stage the source-supported unit1592 vtable target on the Calendar revision."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-calendar-binding-v1';O=R/'phase2-nimem-psys-pointer-binding-v1';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
import tescontainer_install,paths
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve previous proposal')
 pins={P/'manifest.json':'1b15812e89bd4167f7a10032d20e775721f351473d47721cc12269169b68858e',P/'units.generated':'92b5d4058d196208672a6479f1d5e33414c2e022172fa3f3674d1d8e12ede9b8',R/'phase2-nimem-1592-psys-color-pointer-proof.json':'5b7c3ca71cd48d1050d23c46091cb151f8f78072b3ddd956dc8f6632ceb730bb',R/'phase2-nimem-final-eh-field-inventory.json':'28b9bb6c92186db28bb0a5a535de64b59f4eaf1df22e15eece1edbe605913c45',R/'phase2-nimem-next-source-composed/manifest.json':'c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53'}
 for p,h in pins.items():
  if sha(p)!=h:raise ValueError('pinned evidence changed')
 proof=json.loads((R/'phase2-nimem-1592-psys-color-pointer-proof.json').read_text());binding=proof['diagnostic_binding'];name='?PTR_010bffe4@@3DA'
 if set(binding)!={name} or proof['strict_matches']!=10 or proof['rtti_type']!='.?AVNiPSysColorModifier@@':raise ValueError('source and RTTI proof differs')
 base=(P/'units.generated').read_bytes();before=json.loads(base);unit=copy.deepcopy(before['units'][1592]);
 if name in unit['symbols']:raise ValueError('binding already exists')
 unit['symbols'][name]=binding[name];after=tescontainer_install.replace_unit(base,1592,unit);result=json.loads(after)
 if [i for i,(a,b) in enumerate(zip(before['units'],result['units'])) if a!=b]!=[1592]:raise ValueError('unexpected recipe changes')
 obj=R/'phase2-nimem-combined-825d-run/unit-1592/candidate.obj'
 if sha(obj)!=proof['candidate_object_sha256']:raise ValueError('candidate object changed')
 pe=Pe(paths.REF_IMAGE);c=Coff(str(obj));rows=compare(c,pe,unit);sections,inf,errors=eh_sections(c,pe,unit,rows,recipe_names(result['units']))
 if len(rows)!=10 or any(x['verdict']!='match' for x in rows):raise ValueError('strict 1592 replay failed')
 O.mkdir();(O/'units.original').write_bytes(base);(O/'units.generated').write_bytes(after)
 manifest={'parent_recipe_sha256':sha(O/'units.original'),'candidate_recipe_sha256':sha(O/'units.generated'),'recipe_changed_units_from_parent':[1592],'binding':{'unit':1592,'symbol':name,'value':binding[name],'basis':'same-source independently matching stand-in factory and reference RTTI primary locator'},'candidate_object_sha256':sha(obj),'strict_functions':len(rows),'strict_matches':sum(x['verdict']=='match' for x in rows),'ordinary_eh_failed':sum(not x[2] for x in sections),'ordinary_eh_errors':errors,'proof_sha256':{str(p.relative_to(R)):h for p,h in pins.items()},'limitations':['private local binding; no installed recipe or native metadata ownership claim','Calendar-stage 23 located EH failures and 18 errors remain separately evidenced','generated COMDAT ownership, ODR and final image/runtime remain open']};(O/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'candidate_recipe_sha256':manifest['candidate_recipe_sha256'],'manifest_sha256':sha(O/'manifest.json'),'strict':len(rows)}))
if __name__=='__main__':main()
