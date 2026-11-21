"""Compare archived actual objects and prove installed local literal bindings."""
import hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';B=O/'phase2-flags-script-production-before';A=O/'phase2-flags-script-production-after';DEST=A/'literal-proof.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if DEST.exists():raise FileExistsError('preserve evidence')
 up=F/'build/units.json';oldp=B/'units.json';oh='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';nh='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
 if sha(oldp)!=oh or sha(up)!=nh:raise ValueError('recipe changed')
 old=json.loads(oldp.read_text())['units'];new=json.loads(up.read_text())['units'];arch=json.loads((B/'manifest.json').read_text());run=json.loads((A/'compile-result.json').read_text());pe=Pe(paths.REF_IMAGE);result=[]
 if run['recipe_sha256']!=nh:raise ValueError('compile recipe differs')
 for i,n in ((998,128),(1111,82),(1112,1)):
  bp=B/('%04d.obj'%i);ap=A/('%04d.obj'%i);entry=next(x for x in arch['files'] if Path(x['archive']).name==bp.name);done=next(x for x in run['results'] if x['index']==i)
  if sha(bp)!=entry['sha256'] or sha(ap)!=done['object_sha256'] or done['rc'] or done['status']!='ok':raise ValueError('object provenance differs')
  bc=Coff(str(bp));ac=Coff(str(ap));orig=compare(bc,pe,old[i]);actual=compare(ac,pe,new[i])
  if len(orig)!=n or len(actual)!=n or any(x['verdict']!='match' for x in orig+actual):raise ValueError('strict reference mismatch')
  fs={x['address']:x for x in new[i]['functions']};facts=[]
  for f in old[i]['functions']:
   g=fs[f['address']];x,xr=relocated(bc,f['symbol'],f['size'],{});y,yr=relocated(ac,g['symbol'],g['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('code changed '+f['address'])
   for v,w in zip(xr,yr):
    if v==w:continue
    if (v[0],v[1],v[3])!=(w[0],w[1],w[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (v,w)):raise ValueError('nonliteral relocation changed')
    a=bc.named(v[2]);b=ac.named(w[2]);sa=bc.sections[a['section']];sb=ac.sections[b['section']]
    if sa['name']!='.rdata' or sb['name']!='.rdata' or sa['relocs'] or sb['relocs'] or a['value']!=b['value'] or sa['data']!=sb['data']:raise ValueError('literal pool changed')
    value=old[i]['symbols'].get(v[2]);actualvalue=new[i]['symbols'].get(w[2])
    if value is None or value!=actualvalue:raise ValueError('installed binding differs from source pool')
    facts.append({'function':f['address'],'field_offset':v[0],'before':v[2],'after':w[2],'bound_va':value,'pool_offset':a['value'],'pool_sha256':hashlib.sha256(sa['data']).hexdigest()})
  result.append({'unit':i,'functions':n,'before_object_sha256':sha(bp),'after_object_sha256':sha(ap),'strict_before':n,'strict_after':n,'changed_literal_fields':facts})
 DEST.write_text(json.dumps({'before_recipe_sha256':oh,'after_recipe_sha256':nh,'before_archive_manifest_sha256':sha(B/'manifest.json'),'after_compile_result_sha256':sha(A/'compile-result.json'),'reference_sha256':sha(Path(paths.REF_IMAGE)),'units':result,'status':'actual installed recipe agrees with all paired literal fields; no correction needed','limits':['ordinary EH tails, placement/ownership, full image and gameplay are separate gates']},indent=2));print([(x['unit'],len(x['changed_literal_fields'])) for x in result])
if __name__=='__main__':main()
