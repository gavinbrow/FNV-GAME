"""Prove unresolved external fields with same-unit historical immediates."""
import argparse,collections,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';RUN=M/'out/phase2-nimem-kind-cohort-run';ARCH=M/'out/phase2-nimem-kind-production-archive';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 snap=json.loads(a.snapshot.read_text());recipe=RUN/'units.snapshot.json';u=json.loads(recipe.read_text())['units'];inventory={x['unit']:x for x in json.loads((ARCH/'manifest.json').read_text())['objects']};groups=collections.defaultdict(list)
 for z in snap['fields']:
  if z['status']=='source-binding-not-unique':groups[z['unit'],z['function']].append(z)
 pe=Pe(paths.REF_IMAGE);rows=[];counts=collections.Counter()
 for (i,address),group in groups.items():
  f=next(x for x in u[i]['functions'] if x['address']==address);cp=ARCH/('%04d.obj'%i)
  if sha(cp)!=inventory[i]['sha256']:raise ValueError('production archive changed')
  cc=Coff(str(cp));cb,cr=relocated(cc,f['symbol'],f['size'],{});offsets={z['field_offset'] for z in group};success=None;reasons=[]
  for date in ('20261115','20261116'):
   op=RN/('pinned-build/obj_v3.bak-%s/%04d.obj'%(date,i))
   if not op.exists():reasons.append(date+': object absent');continue
   try:
    oc=Coff(str(op));r=compare(oc,pe,dict(u[i],functions=[f]))[0]
    if r['verdict']!='match':raise ValueError('archive not strict reference match')
    ob,orr=relocated(oc,f['symbol'],f['size'],{});mask={j for o in offsets for j in range(o,o+4)}
    if len(ob)!=len(cb) or any(x!=y and j not in mask for j,(x,y) in enumerate(zip(ob,cb))):raise ValueError('whole function differs outside fields')
    if orr!=[x for x in cr if x[0] not in offsets]:raise ValueError('other relocation graph differs')
    for z in group:
     off=z['field_offset'];rr=[x for x in cr if x[0]==off]
     if len(rr)!=1 or rr[0][1:]!=(6,z['symbol'],0) or any(x[0]==off for x in orr):raise ValueError('field relocation shape differs')
     if ob[off:off+4]!=pe.read(int(address,16)+off,4):raise ValueError('archived immediate differs from reference')
    success=(date,op,ob);break
   except (ValueError,KeyError,IndexError,struct.error) as e:reasons.append(date+': '+str(e))
  for z in group:
   row=dict(z)
   if success:
    date,op,ob=success;off=z['field_offset'];row.update(status='archived-source-immediate-agrees',target='0x%08x'%int.from_bytes(ob[off:off+4],'little'),archived_date=date,archived_object_sha256=sha(op),production_object_sha256=sha(cp))
   else:row.update(status='unresolved',reasons=reasons)
   counts[row['status']]+=1;rows.append(row)
 out.write_text(json.dumps({'scope':'same-unit archived whole-function strict reference plus current relocation paired to source immediate','snapshot_sha256':sha(a.snapshot),'recipe_sha256':sha(recipe),'archive_manifest_sha256':sha(ARCH/'manifest.json'),'counts':dict(counts),'fields':rows,'limits':['source spelling or original field alone is not treated as identity proof','unresolved fields remain unresolved; no recipe or comparator changes']},indent=2));print(json.dumps({'counts':counts}))
if __name__=='__main__':main()
