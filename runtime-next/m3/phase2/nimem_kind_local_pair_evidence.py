"""Pair local SG baseline fields with strictly matching same-unit archived COFF."""
import argparse,collections,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';RUN=M/'out/phase2-nimem-kind-cohort-run';ARCH=M/'out/phase2-nimem-kind-production-archive';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--snapshot',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 snap=json.loads(a.snapshot.read_text());recipe=RUN/'units.snapshot.json';u=json.loads(recipe.read_text())['units'];inventory={x['unit']:x for x in json.loads((ARCH/'manifest.json').read_text())['objects']};pe=Pe(paths.REF_IMAGE);rows=[];counts=collections.Counter();cache={};maps=collections.defaultdict(dict)
 for z in snap['fields']:
  if z['status']!='local-label-deferred':continue
  i=z['unit'];f=next(x for x in u[i]['functions'] if x['address']==z['function']);off=z['field_offset'];cp=ARCH/('%04d.obj'%i)
  if sha(cp)!=inventory[i]['sha256']:raise ValueError('production archive changed')
  if i not in cache:cache[i]=Coff(str(cp))
  current=cache[i];cb,cr=relocated(current,f['symbol'],f['size'],{});newrel=[x for x in cr if x[0]==off];result={'unit':i,'function':f['address'],'field_offset':off,'current_label':z['symbol'],'status':'unresolved','reasons':[]}
  if len(newrel)!=1 or newrel[0][2]!=z['symbol']:raise ValueError('current relocation differs')
  for date in ('20261115','20261116'):
   oldpath=RN/('pinned-build/obj_v3.bak-%s/%04d.obj'%(date,i))
   if not oldpath.exists():result['reasons'].append(date+': object absent');continue
   try:
    oc=Coff(str(oldpath));check=compare(oc,pe,dict(u[i],functions=[f]))[0]
    if check['verdict']!='match':raise ValueError('archived function not strict reference match')
    ob,orr=relocated(oc,f['symbol'],f['size'],{})
    if ob!=cb or [(v[0],v[1],v[3]) for v in orr]!=[(v[0],v[1],v[3]) for v in cr]:raise ValueError('function or relocation shapes differ')
    prior=[x for x in orr if x[0]==off]
    if len(prior)!=1 or not re.fullmatch(r'\$SG\d+',prior[0][2]):raise ValueError('prior local label not paired')
    label=prior[0][2];bound=u[i]['symbols'].get(label)
    if bound is None:raise ValueError('prior label lacks unit recipe binding')
    x=oc.named(label);y=current.named(z['symbol']);xs=oc.sections[x['section']];ys=current.sections[y['section']]
    if xs['name']!='.rdata' or ys['name']!='.rdata' or xs['relocs'] or ys['relocs']:raise ValueError('pool not plain rdata')
    xe=xs['data'].find(b'\0',x['value']);ye=ys['data'].find(b'\0',y['value'])
    if xe<0 or ye<0:raise ValueError('unterminated string')
    data=xs['data'][x['value']:xe+1]
    if data!=ys['data'][y['value']:ye+1] or pe.read(int(bound,16),len(data))!=data:raise ValueError('pool content disagreement')
    raw=pe.read(int(f['address'],16)+off,4);observed=struct.unpack('<I',raw)[0];expected=(int(bound,16)+newrel[0][3])&0xffffffff
    if newrel[0][1]!=6 or observed!=expected:raise ValueError('reference relocation field differs')
    priorbound=maps[i].get(z['symbol'])
    if priorbound is not None and priorbound!=bound:raise ValueError('conflicting same-unit label binding')
    maps[i][z['symbol']]=bound;result.update(status='source-paired-reference-agree',archived_date=date,old_object_sha256=sha(oldpath),current_object_sha256=sha(cp),prior_label=label,source_bound_va=bound,literal_sha256=hashlib.sha256(data).hexdigest(),literal_size=len(data));result.pop('reasons');break
   except (ValueError,KeyError,IndexError,struct.error) as e:result['reasons'].append(date+': '+str(e))
  counts[result['status']]+=1;rows.append(result)
 out.write_text(json.dumps({'scope':'same-unit archived strict function and source recipe paired to current object local field; no cross-unit labels','snapshot_sha256':sha(a.snapshot),'recipe_sha256':sha(recipe),'archive_manifest_sha256':sha(ARCH/'manifest.json'),'counts':dict(counts),'fields':rows,'unit_local_bindings':{str(k):v for k,v in maps.items()},'limits':['source object is historical and provenance must be retained','unresolved fields remain unresolved; no recipe or comparator changes']},indent=2));print(json.dumps({'counts':counts,'units':len(maps)}))
if __name__=='__main__':main()
