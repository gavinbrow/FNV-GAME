"""Check forward-declaration-only unit980 mirror and derive candidate literal labels."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tescontainer-980-forward-mirror';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 outputs=[O/'literal-analysis.json',O/'unit-overlay.json']
 if any(p.exists() for p in outputs):raise FileExistsError('refusing overwrite')
 m=json.loads((O/'mirror-manifest.json').read_text());run=json.loads((O/'compile-result.json').read_text());up=F/'build/units.json'
 if sha(up)!=m['units_sha256'] or sha(O/'mirror-manifest.json')!=run['mirror_manifest_sha256'] or run['unit_index']!=980:raise ValueError('inputs changed')
 rows={x['tag']:x for x in run['outcomes']};coff={}
 for tag in ('original','candidate'):
  p=O/(tag+'.obj');r=rows[tag]
  if r['rc'] or not r['trace_valid'] or sha(p)!=r['object_sha256']:raise ValueError('object evidence invalid')
  coff[tag]=Coff(str(p))
 unit=json.loads(up.read_text())['units'][980]
 if len(unit['functions'])!=31:raise ValueError('function count changed')
 pe=Pe(paths.REF_IMAGE);oldref=compare(coff['original'],pe,unit)
 if len(oldref)!=31 or any(x['verdict']!='match' for x in oldref):raise ValueError('mirror baseline not strict 31/31')
 names={};facts=[];functions=[]
 for f in unit['functions']:
  old,ro=relocated(coff['original'],f['symbol'],f['size'],{});new,rn=relocated(coff['candidate'],f['symbol'],f['size'],{})
  if old!=new or len(ro)!=len(rn):raise ValueError('function code or relocation count changed '+f['address'])
  for x,y in zip(ro,rn):
   if x==y:continue
   if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (x,y)):raise ValueError('nonliteral relocation changed '+f['address'])
   if x[2] not in unit['symbols']:raise ValueError('old literal is not recipe bound '+x[2])
   pools=[]
   for c,name in ((coff['original'],x[2]),(coff['candidate'],y[2])):
    s=c.named(name);sec=c.sections[s['section']]
    if sec['name']!='.rdata' or sec['relocs']:raise ValueError('invalid literal pool')
    pools.append((s['value'],sec['data']))
   if pools[0]!=pools[1]:raise ValueError('literal pool or offset differs')
   addr=int(unit['symbols'][x[2]],16);d=pools[0][1];n=pools[0][0];end=d.find(b'\0',n)
   if end<0 or pe.read(addr,end-n+1)!=d[n:end+1]:raise ValueError('literal reference mismatch')
   if y[2] in names and names[y[2]]!=x[2]:raise ValueError('ambiguous new label')
   names[y[2]]=x[2];facts.append({'function':f['address'],'offset':x[0],'before':x[2],'after':y[2],'bound_va':unit['symbols'][x[2]],'pool_offset':n,'pool_size':len(d),'pool_sha256':hashlib.sha256(d).hexdigest()})
  functions.append({'address':f['address'],'bytes_equal':True})
 candidate=copy.deepcopy(unit);symbols=dict(candidate['symbols'])
 # Retain original mapping keys unless a new key must be changed; source proof
 # and all-function strict reference gate detect any collision or reused label.
 for new,old in names.items():symbols[new]=unit['symbols'][old]
 candidate['symbols']=symbols;ref=compare(coff['candidate'],pe,candidate)
 if len(ref)!=31 or any(x['verdict']!='match' for x in ref):raise ValueError('candidate strict reference not 31/31')
 report={'unit':980,'source_sha256':sha(F/unit['source']),'original_obj_sha256':sha(O/'original.obj'),'candidate_obj_sha256':sha(O/'candidate.obj'),'literal_changes':facts,'functions':functions,'baseline_reference_matches':31,'candidate_reference_matches':31,'scope':'isolated production-layout mirror; actual installed production object and full build reproof still required'}
 outputs[0].write_text(json.dumps(report,indent=2));outputs[1].write_text(json.dumps(candidate,indent=2));print(json.dumps({'functions':31,'literal_changes':len(facts),'strict_reference_matches':31}))
if __name__=='__main__':main()
