"""Derive production literal-label correction for the applied typed transaction."""
import argparse,copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-typed-transaction';C=T/'production-correction';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths,tescontainer_install as recipe,tesform_typed_transaction as tx

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tes-object-sha256',required=True);ap.add_argument('--bgs-object-sha256',required=True);a=ap.parse_args();guards=tx.lock.acquire_guard()
 try:
  m=tx.manifest()
  if not (T/'applied.json').exists():raise ValueError('typed transaction not applied')
  for x in m['files']:
   p=F/x['path']
   if sha(p.read_bytes())!=x['new_sha256']:raise ValueError('installed input not staged candidate '+x['path'])
  if C.exists():raise FileExistsError('refusing overwrite')
  original=(T/'5.generated').read_bytes();doc=json.loads(original);unit=doc['units'][998];bu=doc['units'][2];production=RN/'pinned-build/obj_v3/0998.obj';bp=RN/'pinned-build/obj_v3/0002.obj'
  if sha(production.read_bytes())!=a.tes_object_sha256.lower() or sha(bp.read_bytes())!=a.bgs_object_sha256.lower():raise ValueError('production object mismatch')
  mirrorpath=M/'out/phase2-tesform-typed-mirror/candidate.obj';report=json.loads((M/'out/phase2-typed-paired-report.json').read_text())
  if sha(mirrorpath.read_bytes())!=report['tes_obj_sha256']:raise ValueError('mirror object changed')
  old=Coff(str(mirrorpath));new=Coff(str(production));pe=Pe(paths.REF_IMAGE);changes={};facts=[]
  for f in unit['functions']:
   x,xr=relocated(old,f['symbol'],f['size'],{});y,yr=relocated(new,f['symbol'],f['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('function/relocation count mismatch '+f['address'])
   for v,w in zip(xr,yr):
    if v==w:continue
    if (v[0],v[1],v[3])!=(w[0],w[1],w[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (v,w)):raise ValueError('nonliteral change '+f['address'])
    p=old.named(v[2]);q=new.named(w[2]);ps=old.sections[p['section']];qs=new.sections[q['section']]
    if p['value']!=q['value'] or ps['name']!='.rdata' or qs['name']!='.rdata' or ps['data']!=qs['data'] or ps['relocs'] or qs['relocs'] or v[2] not in unit['symbols']:raise ValueError('literal pool changed')
    value=unit['symbols'][v[2]]
    if w[2] in changes and changes[w[2]]!=value:raise ValueError('ambiguous literal')
    changes[w[2]]=value;facts.append({'function':f['address'],'offset':v[0],'mirror_label':v[2],'production_label':w[2],'binding':value,'pool_offset':p['value'],'pool_sha256':sha(ps['data'])})
  corrected=copy.deepcopy(unit);corrected['symbols'].update(changes);check=compare(new,pe,corrected)
  if len(check)!=128 or any(x['verdict']!='match' for x in check):raise ValueError('production TESForm strict reference mismatch')
  fold=m['noop_fold'];owner=next(f for f in unit['functions'] if f['address']==fold['source_address']);bodies=[]
  for symbol in [fold['source_body_symbol']]+fold['new_symbols']:
   body,rel=relocated(new,symbol,owner['size'],{})
   if rel or body!=pe.read(int(owner['address'],16),owner['size']):raise ValueError('production no-op body differs '+symbol)
   sym=new.named(symbol);sec=new.sections[sym['section']];start=sym['value'];nxt=[x['value'] for x in new.symbols.values() if x['section']==sym['section'] and x['type']&0x20 and x['value']>start and not x['name'].startswith('__catch$')];end=min(nxt) if nxt else len(sec['data'])
   if end-start<owner['size'] or any(x not in (0xcc,0x90) for x in sec['data'][start+owner['size']:end]):raise ValueError('production no-op extent differs '+symbol)
   bodies.append(symbol)
  diag=copy.deepcopy(bu);diag['symbols']['??1TESForm@@UAE@XZ']='0x00483630'
  for x in m['unit998_function_remaps']:diag['symbols'][x['after']]=x['address']
  for n in m['noop_fold']['new_symbols']:diag['symbols'][n]=m['noop_fold']['source_address']
  br=compare(Coff(str(bp)),pe,diag)
  if len(br)!=24 or any(x['verdict']!='match' for x in br):raise ValueError('production BGSE strict reference mismatch')
  generated=recipe.replace_unit(original,998,corrected);n=json.loads(generated)
  if [i for i,(x,y) in enumerate(zip(doc['units'],n['units'])) if x!=y] not in ([],[998]) or any(doc[k]!=n[k] for k in doc if k!='units'):raise ValueError('correction scope mismatch')
  C.mkdir();(C/'units.original').write_bytes(original);(C/'units.generated').write_bytes(generated)
  meta={'transaction_manifest_sha256':tx.PROOF,'original_sha256':sha(original),'generated_sha256':sha(generated),'tes_object_sha256':a.tes_object_sha256.lower(),'bgs_object_sha256':a.bgs_object_sha256.lower(),'literal_facts':facts,'unit998_matches':128,'unit2_diagnostic_matches':24,'production_noop_symbols':bodies,'status':'private production correction; requires independent review before applying; no full build yet'}
  (C/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'literal_fields':len(facts),'recipe_sha256':sha(generated),'tes_matches':128,'bgs_matches':24}))
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':main()
