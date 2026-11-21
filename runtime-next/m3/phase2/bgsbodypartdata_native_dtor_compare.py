"""Private 621 native destructor trial: no recipe or source mutation."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out/phase2-bgsbodypartdata-native-dtor-v1';A=M/'out/phase2-psa-w103-provider-archive';sys.path[:0]=[str(F/'tools'),str(M.parent),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
from build_and_match import eh_sections,recipe_names
import paths
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=O/'independent-dtor-comparison.json'
 if out.exists():raise FileExistsError(out)
 run=json.loads((O/'compile-result.json').read_bytes());manifest=O/'mirror-manifest.json'
 if h(manifest)!=run['mirror_manifest_sha256'] or {z['tag'] for z in run['outcomes']}!={'original','candidate'}:raise ValueError('compile manifest')
 for z in run['outcomes']:
  if z['rc'] or not z['trace_valid'] or h(O/(z['tag']+'.obj'))!=z['object_sha256']:raise ValueError('invalid compile')
 capture=json.loads((A/'capture.json').read_bytes());donor=A/'2656.obj'
 if h(donor)!=capture['files']['2656.obj']:raise ValueError('donor identity')
 recipe=json.loads((A/'units.json').read_bytes())['units'];pe=Pe(paths.REF_IMAGE);before=Coff(str(O/'original.obj'));after=Coff(str(O/'candidate.obj'));owner=Coff(str(donor));results={}
 for tag,c in [('original',before),('candidate',after)]:
  r=compare(c,pe,recipe[621]);sec,inf,err=eh_sections(c,pe,recipe[621],r,recipe_names(recipe));results[tag]={'functions':len(r),'matches':sum(x['verdict']=='match' for x in r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'eh_sections':len(sec),'eh_failed':[x for x in sec if not x[2]],'eh_errors':err}
 sym='??1BGSBodyPartData@@UAE@XZ';old='??1FUN_005e4bc0@@UAE@XZ';ns=after.named(sym);os=owner.named(old);nd=after.sections[ns['section']]['data'];od=owner.sections[os['section']]['data'];nr=[(o,after.symbols[i]['name'],k) for o,i,k in after.sections[ns['section']]['relocs']];orr=[(o,owner.symbols[i]['name'],k) for o,i,k in owner.sections[os['section']]['relocs']]
 result={'scope':'private native destructor body/relocation structural comparison; no owner mapping or transfer','candidate_sha256':h(O/'candidate.obj'),'donor_sha256':h(donor),'recipe_sha256':h(A/'units.json'),'results':results,'native_dtor':{'extent':len(nd),'sha256':hashlib.sha256(nd).hexdigest(),'relocations':nr},'source_owner_dtor':{'extent':len(od),'sha256':hashlib.sha256(od).hexdigest(),'relocations':orr},'raw_body_equal':nd==od,'limits':['relocation names/targets require independent same-unit source binding and reference checks','donor normal 174-function proof and full graph/weak ownership separate','private mirror is not installed']};out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'results':results,'native_size':len(nd),'owner_size':len(od),'raw_equal':nd==od,'native_relocs':nr,'owner_relocs':orr}))
if __name__=='__main__':main()
