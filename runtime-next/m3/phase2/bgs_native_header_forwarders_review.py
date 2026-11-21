"""Review actual BGS native header forwarder object pairs."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-bgs-native-header-forwarders-v2';P=M/'out/phase2-bgsbodypart-native-destructor-rebase6757';OUT=D/'independent-review.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve review')
 m=json.loads((D/'manifest.json').read_text());rp=F/'build/units.json';u=json.loads(rp.read_text())['units'];graph=json.loads((P/'graph-unit.json').read_text());pe=Pe(paths.REF_IMAGE);details={};done={'prior':[],'forwarded':[]}
 if sha(rp)!=m['base_recipe_sha256']:raise ValueError('recipe changed')
 for i in (620,621):
  d=D/str(i);run=json.loads((d/'compile-result.json').read_text());spec=graph if i==620 else u[i];objs={};details[str(i)]={}
  if run['unit_index']!=i or run['manifest_sha256']!=sha(D/'manifest.json'):raise ValueError('compile identity differs')
  for tag in ('prior','forwarded'):
   x=next(z for z in run['outcomes'] if z['tag']==tag);p=d/(tag+'.obj')
   if x['rc'] or not x['trace_valid'] or sha(p)!=x['object_sha256']:raise ValueError('compile failed')
   c=Coff(str(p));r=compare(c,pe,spec);sec,inf,err=eh_sections(c,pe,spec,r,recipe_names(u))
   if len(r)!=(15 if i==620 else 10) or any(x['verdict']!='match' for x in r) or err or any(not x[2] for x in sec):raise ValueError('strict function or EH mismatch')
   objs[tag]=c;done[tag].append({'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}});details[str(i)][tag]={'object_sha256':sha(p),'strict_functions':len(r),'eh_sections':len(sec),'inferred_names':len(inf),'project_support_includes':[n for n in x['observed_project_includes'] if n.endswith(('BaseFormComponent.h','layout_support.h'))]}
  for f in spec['functions']:
   a,ar=relocated(objs['prior'],f['symbol'],f['size'],{});b,br=relocated(objs['forwarded'],f['symbol'],f['size'],{})
   if a!=b or ar!=br:raise ValueError('mapped bytes or relocation differs '+f['address'])
 for tag in done:
  tails,bad,inf,_,conf=eh_tails([u[620],u[621]],done[tag],pe)
  if len(tails)!=2 or bad or conf:raise ValueError('listed EH tails differ')
  details[tag+'_tails']={'count':len(tails),'inferred':len(inf),'conflicts':conf}
 graphs=[]
 for n in ('graph-0.json','graph-1.json'):
  p=D/n;x=json.loads(p.read_text());t=x['tables']
  if x['object_sha256']!=details['620']['forwarded']['object_sha256'] or len(t)!=1 or not t[0]['graph_fields_equal'] or not t[0]['slot_prefix_count_equal'] or any(not s['match'] for s in t[0]['slots']):raise ValueError('RTTI graph mismatch')
  graphs.append({'report':n,'sha256':sha(p),'slot_count':len(t[0]['slots'])})
 OUT.write_text(json.dumps({'scope':'private production-layout prior versus forwarding context; no whole-class ABI claim','manifest_sha256':sha(D/'manifest.json'),'recipe_sha256':sha(rp),'documented_620_mapping_sha256':sha(P/'graph-unit.json'),'units':details,'forwarded_reference_graphs':graphs,'limits':['public support headers appear additionally in forwarded include trace; guard behavior and packing require direct preprocessor audit','other consumer contexts not included','weak/COMDAT ownership and final production image/runtime remain separate']},indent=2));print('PASS 15+10 strict functions and relocations; ordinary two tails; two RTTI graphs')
if __name__=='__main__':main()
