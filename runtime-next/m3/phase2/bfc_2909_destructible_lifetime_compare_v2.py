"""Compare private 2909 lifetime fix using unchanged ordinary EH oracle."""
import copy,hashlib,json,re,sys,struct
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-bfc-2909-destructible-lifetime';OUT=D/'comparison-v2.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior output')
 manifest=json.loads((D/'manifest.json').read_text());op=D/'units.original';np=D/'units.generated'
 if sha(op)!=manifest['base_recipe_sha256'] or sha(np)!=manifest['candidate_recipe_sha256']:raise ValueError('recipe evidence differs')
 old=json.loads(op.read_text())['units'];new=json.loads(np.read_text())['units'];pe=Pe(paths.REF_IMAGE);results={}
 vals=struct.unpack('<9I',pe.read(0x1147064,36));actions=[struct.unpack('<II',pe.read(vals[2]+8*i,8)) for i in range(vals[1])]
 if vals[0]!=0x19930522 or vals[1]!=5 or vals[2]!=0x1147088 or actions[3][1]!=0xef4a8e:raise ValueError('reference FuncInfo mismatch')
 for i in (2909,2910):
  folder=D/str(i);mm=folder/'mirror-manifest.json';run=json.loads((folder/'compile-result.json').read_text())
  if run['unit_index']!=i or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('compile identity differs')
  results[str(i)]={};paired={}
  ca=Coff(str(folder/'original.obj'));cb=Coff(str(folder/'candidate.obj'))
  for f in old[i]['functions']:
   a,ar=relocated(ca,f['symbol'],f['size'],{});b,br=relocated(cb,f['symbol'],f['size'],{})
   if a!=b or len(ar)!=len(br):raise ValueError('function or relocation shape differs '+f['address'])
   for x,y in zip(ar,br):
    if x==y:continue
    if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (x,y)):raise ValueError('nonliteral relocation differs '+f['address'])
    xs=ca.named(x[2]);ys=cb.named(y[2]);xp=ca.sections[xs['section']];yp=cb.sections[ys['section']]
    if xs['value']!=ys['value'] or xp['name']!='.rdata' or yp['name']!='.rdata' or xp['relocs'] or yp['relocs'] or xp['data']!=yp['data'] or x[2] not in old[i]['symbols']:raise ValueError('source pool differs')
    va=old[i]['symbols'][x[2]]
    if y[2] in paired and paired[y[2]]!=va:raise ValueError('ambiguous pool binding')
    paired[y[2]]=va
  results[str(i)]['paired_source_literal_bindings']=paired
  for tag in ('original','candidate'):
   row=next(x for x in run['outcomes'] if x['tag']==tag);obj=folder/(tag+'.obj')
   if row['rc'] or not row['trace_valid'] or sha(obj)!=row['object_sha256']:raise ValueError('compile object differs')
   spec=copy.deepcopy(old[i] if tag=='original' else new[i])
   if tag=='candidate':spec['symbols'].update(paired)
   c=Coff(str(obj));r=compare(c,pe,spec)
   if len(r)!=len(spec['functions']) or any(x['verdict']!='match' for x in r):raise ValueError('strict functions failed '+str((i,tag,[(x['address'],x['errors']) for x in r if x['verdict']!='match'][:5])))
   sections,inferred,errors=eh_sections(c,pe,spec,r,recipe_names(old));targets=[x for x in sections if x[0]<=0xef4a8e<x[1] and x[3]=='0x0051b6e0']
   if i==2909 and (len(targets)!=1 or (tag=='original' and targets[0][2]) or (tag=='candidate' and not targets[0][2])):raise ValueError('cleanup behavior not as hypothesized')
   done=[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}}];tails,bad,inf,_,conf=eh_tails([spec],done,pe)
   results[str(i)][tag]={'object_sha256':sha(obj),'strict_functions':len(r),'eh_sections':len(sections),'failed_sections':sum(not x[2] for x in sections),'eh_errors':errors,'target_cleanup':targets,'recipe_tails':len(tails),'bad_tails':bad,'inferred_tails':inf,'inferred_names':{k:'0x%08x'%v for k,v in inferred.items()},'inference_conflicts':conf}
 OUT.write_text(json.dumps({'manifest_sha256':sha(D/'manifest.json'),'reference_sha256':sha(Path(paths.REF_IMAGE)),'reference_funcinfo':'0x01147064','reference_unwind_map':'0x01147088','reference_state3_action':'0x00ef4a8e','results':results,'limits':['full RTTI/hierarchy layout, object sections, source ODR and final placement require separate review','compiler literal labels may require independently derived paired pool bindings; never borrow them']},indent=2));print(json.dumps(results))
if __name__=='__main__':main()
