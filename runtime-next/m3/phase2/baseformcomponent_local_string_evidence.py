"""Prove local SG baseline fields only through paired archived source COFF."""
import collections,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';S=M/'out/phase2-baseformcomponent-core';O=S/'local-string-evidence.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 up=F/'build/units.json';audit=json.loads((S/'root-baseline-audit.json').read_text());
 if sha(up)!=D or audit['recipe_sha256']!=D:raise ValueError('recipe differs')
 units=json.loads(up.read_text())['units'];pe=Pe(paths.REF_IMAGE);rows=[];stats=collections.Counter();objecthash={};maps=collections.defaultdict(dict)
 for row in audit['units']:
  if row['unit_only_matches']==row['functions']:continue
  i=row['unit'];current=RN/('pinned-build/obj_v3/%04d.obj'%i);archive=RN/('pinned-build/obj_v3.bak-20261116/%04d.obj'%i)
  if sha(current)!=audit['object_sha256'][str(i)]:raise ValueError('production object changed '+str(i))
  cc=Coff(str(current));current_checks=compare(cc,pe,units[i]);has_sg=any(not z.get('match') and re.fullmatch(r'\$SG\d+',z['symbol']) for f in current_checks for z in f['relocations'])
  if not has_sg:continue
  if not archive.exists():
   stats['archive-missing']+=1;continue
  oc=Coff(str(archive));oldchecks={}
  try:oldchecks={x['address']:x for x in compare(oc,pe,units[i])}
  except (ValueError,KeyError,IndexError) as e:pass
  objecthash[str(i)]={'current_sha256':sha(current),'archive_sha256':sha(archive)}
  specs={x['address']:x for x in units[i]['functions']}
  for f in current_checks:
   for z in f['relocations']:
    if z.get('match') or not re.fullmatch(r'\$SG\d+',z['symbol']):continue
    rec={'unit':i,'function':f['address'],'field_offset':z['offset'],'current_label':z['symbol'],'status':'unproved'};spec=specs[f['address']]
    try:
     old=oldchecks.get(f['address'])
     if not old or old['verdict']!='match':raise ValueError('archived function is not strict reference match')
     ob,orr=relocated(oc,spec['symbol'],spec['size'],{});cb,crr=relocated(cc,spec['symbol'],spec['size'],{})
     if ob!=cb or [(x[0],x[1],x[3]) for x in orr]!=[(x[0],x[1],x[3]) for x in crr]:raise ValueError('archived/current code or relocation shapes differ')
     olds=[x for x in orr if x[0]==z['offset']];curr=[x for x in crr if x[0]==z['offset']]
     if len(olds)!=1 or len(curr)!=1 or curr[0][2]!=z['symbol'] or not re.fullmatch(r'\$SG\d+',olds[0][2]):raise ValueError('archived local field not paired')
     oldname=olds[0][2];bound=units[i]['symbols'].get(oldname)
     if bound is None:raise ValueError('archived local label lacks unit source binding')
     x=oc.named(oldname);y=cc.named(z['symbol']);xs=oc.sections[x['section']];ys=cc.sections[y['section']]
     if xs['name']!='.rdata' or ys['name']!='.rdata' or xs['relocs'] or ys['relocs']:raise ValueError('literal pool is not plain rdata')
     xe=xs['data'].find(b'\0',x['value']);ye=ys['data'].find(b'\0',y['value'])
     if xe<0 or ye<0:raise ValueError('literal is unterminated')
     data=xs['data'][x['value']:xe+1]
     if data!=ys['data'][y['value']:ye+1] or pe.read(int(bound,16),len(data))!=data:raise ValueError('source and reference literal content differs')
     addr=int(f['address'],16)+z['offset'];ref=struct.unpack('<I',pe.read(addr,4))[0];expected=(int(bound,16)+curr[0][3])&0xffffffff
     if curr[0][1]!=6 or expected!=ref:raise ValueError('field does not resolve to source-bound target')
     prior=maps[i].get(z['symbol'])
     if prior is not None and prior!=bound:raise ValueError('current local label has conflicting bindings')
     maps[i][z['symbol']]=bound;rec.update(status='archived-source-and-reference-agree',archived_label=oldname,source_bound_va=bound,literal_size=len(data),literal_sha256=hashlib.sha256(data).hexdigest(),archived_pool_offset=x['value'],current_pool_offset=y['value'])
    except (ValueError,KeyError,IndexError,struct.error) as e:rec['reason']=str(e)
    stats[rec['status']]+=1;rows.append(rec)
 out={'scope':'diagnostic only; each local label is paired at the same function relocation against archived same-unit COFF, strict source recipe and reference; no cross-unit local binding','units_sha256':sha(up),'baseline_audit_sha256':sha(S/'root-baseline-audit.json'),'object_hashes':objecthash,'field_counts':dict(stats),'fields':rows,'source_derived_local_bindings':{str(k):v for k,v in maps.items()},'limits':['strict archived function match and identical code/relocation shapes required','unproved fields stay unproved; source-derived mappings are not installed','same bytes/fields do not establish class/RTTI/ownership equivalence']}
 O.write_text(json.dumps(out,indent=2));print(json.dumps({'fields':len(rows),'counts':stats}))
if __name__=='__main__':main()
