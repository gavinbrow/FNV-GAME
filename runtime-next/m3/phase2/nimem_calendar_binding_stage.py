"""Stage source-owned unit368 Calendar binding, retaining original EH evidence."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';O=R/'phase2-nimem-calendar-binding-v1';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
import tescontainer_install,paths
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior evidence')
 audit=R/'phase2-nimem-final-gap-audit.json';fields=R/'phase2-nimem-final-eh-field-inventory.json';idx=R/'phase2-nimem-next-source-proof-index-v4.json'
 pins={audit:'a5e490dd8ea490f92c4789bc952e97e626e33d72aa4b7568be7ba660abac01af',fields:'28b9bb6c92186db28bb0a5a535de64b59f4eaf1df22e15eece1edbe605913c45',idx:'f02c075f5dff6da865990f0fb85c06eb49192955389f42f5610195cfe5e9b826',P/'manifest.json':'c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53',P/'units.generated':'13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876'}
 for p,h in pins.items():
  if sha(p)!=h:raise ValueError('proof mismatch '+str(p))
 proof=json.loads(audit.read_text());owner=proof['calendar_owner'];name=owner['symbol'];address=owner['address']
 if owner['unit']!=574 or owner['strict_matches']!=17 or owner['strict_functions']!=17 or owner['method_result']['verdict']!='match' or address!='0x00867d60' or name!='?GetDayOfMonth@Calendar@@QAEHXZ':raise ValueError('owner evidence differs')
 base=(P/'units.generated').read_bytes();before=json.loads(base);unit=copy.deepcopy(before['units'][368]);symbols=unit['symbols']
 if name in symbols:raise ValueError('binding already exists')
 symbols[name]=address;afterraw=tescontainer_install.replace_unit(base,368,unit);after=json.loads(afterraw)
 if [i for i,(a,b) in enumerate(zip(before['units'],after['units'])) if a!=b]!=[368]:raise ValueError('unexpected recipe edits')
 d=R/'phase2-nimem-combined-825d-run/unit-0368';obj=d/'candidate.obj';c=Coff(str(obj));pe=Pe(paths.REF_IMAGE);r=compare(c,pe,unit)
 if len(r)!=123 or any(x['verdict']!='match' for x in r):raise ValueError('Calendar binding fails caller replay')
 eh=[]
 for x in proof['eh_units']:
  i=x['unit'];q=R/('phase2-nimem-combined-825d-run/unit-%04d/candidate.obj'%i);c=Coff(str(q));results=compare(c,pe,after['units'][i]);s,inf,errors=eh_sections(c,pe,after['units'][i],results,recipe_names(after['units']));failed=[list(z) for z in s if not z[2]];eh.append({'unit':i,'object_sha256':sha(q),'before_failed':len(x['after_failed_sections']),'after_failed':len(failed),'before_errors':len(x['after_errors']),'after_errors':len(errors),'failed_sections':failed,'errors':errors,'inferred_names':len(inf)})
 O.mkdir();(O/'units.original').write_bytes(base);(O/'units.generated').write_bytes(afterraw)
 manifest={'parent_recipe_sha256':sha(O/'units.original'),'candidate_recipe_sha256':sha(O/'units.generated'),'binding':{'unit':368,'symbol':name,'address':address,'source_owner_unit':574,'source_owner_object_sha256':owner['object_sha256']},'recipe_changed_units_from_parent':[368],'proof_sha256':{p.name:h for p,h in pins.items()},'caller_object_sha256':sha(obj),'caller_functions':123,'caller_matches':123,'eh_before_failed':sum(x['before_failed'] for x in eh),'eh_after_failed':sum(x['after_failed'] for x in eh),'eh_before_errors':sum(x['before_errors'] for x in eh),'eh_after_errors':sum(x['after_errors'] for x in eh),'eh_units':eh,'limitations':['private binding-only proposal; no source or recipe installation','unit1592 PTR remains unresolved and its prior exact failure evidence remains applicable','EH proof reports actual before/after; unresolved sections and outside owners remain explicit']}
 (O/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'candidate_recipe_sha256':manifest['candidate_recipe_sha256'],'eh_before_after':[manifest['eh_before_failed'],manifest['eh_after_failed'],manifest['eh_before_errors'],manifest['eh_after_errors']],'manifest_sha256':sha(O/'manifest.json')}))
if __name__=='__main__':main()
