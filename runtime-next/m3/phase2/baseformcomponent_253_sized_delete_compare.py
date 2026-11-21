"""Verify private 253 sized-delete experiment against archived actual production."""
import copy,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out';D=O/'phase2-bfc-253-sized-delete';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=D/'comparison.json'
 if out.exists():raise FileExistsError('preserve report')
 m=json.loads((D/'mirror-manifest.json').read_text());run=json.loads((D/'compile-result.json').read_text());old=json.loads((D/'units.original').read_text());new=json.loads((D/'units.generated').read_text());audit=json.loads((O/'phase2-baseformcomponent-core/root-baseline-audit.json').read_text());p=O/'phase2-bfc-cohort-production-archive/0253.obj'
 if sha(D/'units.original')!=m['units_sha256'] or sha(D/'units.generated')!=m['candidate_recipe_sha256'] or sha(p)!=audit['object_sha256']['253'] or run['unit_index']!=253 or run['mirror_manifest_sha256']!=sha(D/'mirror-manifest.json'):raise ValueError('pinned input mismatch')
 if [i for i,(a,b) in enumerate(zip(old['units'],new['units'])) if a!=b]!=[253]:raise ValueError('recipe scope differs')
 objects={'production':Coff(str(p))}
 for row in run['outcomes']:
  path=D/(row['tag']+'.obj')
  if row['rc'] or not row['trace_valid'] or sha(path)!=row['object_sha256']:raise ValueError('compile invalid')
  objects[row['tag']]=Coff(str(path))
 if set(objects)!={'production','original','candidate'}:raise ValueError('missing object')
 pe=Pe(paths.REF_IMAGE);info=struct.unpack('<10I',pe.read(0x11620ac,40));action=struct.unpack('<II',pe.read(info[2],8))
 if info[0]!=0x19930522 or info[1]!=1 or info[2]!=0x11620a4 or action!=(0xffffffff,0xf157c0) or pe.read(0x8c4d40,2)!=bytes.fromhex('6a6c') or pe.read(0xf157c0,2)!=bytes.fromhex('6a6c'):raise ValueError('reference size/FuncInfo mismatch')
 names=recipe_names(old['units']);base=copy.deepcopy(old['units'][253]);ev=O/'phase2-baseformcomponent-core/local-string-evidence-v3.json'
 if sha(ev)!='3ed975d088d8623b8958b42a6084115fab4d2a607698c91376453d35c7658ad7':raise ValueError('binding proof differs')
 base['symbols'].update(json.loads(ev.read_text())['source_derived_local_bindings']['253'])
 def strict(obj,spec):
  rows=compare(obj,pe,spec)
  if len(rows)!=807 or any(x['verdict']!='match' for x in rows):raise ValueError('function reference mismatch')
  return rows
 strict(objects['production'],base)
 def pair(a,b,spec,extra):
  result=copy.deepcopy(spec);result['symbols'].update(extra);facts=[];norm={}
  for f in spec['functions']:
   x,xr=relocated(a,f['symbol'],f['size'],{});y,yr=relocated(b,f['symbol'],f['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('code differs '+f['address'])
   for v,w in zip(xr,yr):
    if v==w:continue
    if (v[0],v[1],v[3])!=(w[0],w[1],w[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (v,w)):raise ValueError('nonliteral relocation differs '+f['address'])
    x1=a.named(v[2]);y1=b.named(w[2]);xs=a.sections[x1['section']];ys=b.sections[y1['section']]
    if x1['value']!=y1['value'] or xs['name']!='.rdata' or ys['name']!='.rdata' or xs['relocs'] or ys['relocs'] or xs['data']!=ys['data'] or v[2] not in spec['symbols']:raise ValueError('literal source pool mismatch')
    value=spec['symbols'][v[2]]
    if w[2] in norm and norm[w[2]]!=v[2]:raise ValueError('ambiguous literal mapping')
    norm[w[2]]=v[2];result['symbols'][w[2]]=value;facts.append({'function':f['address'],'offset':v[0],'before':v[2],'after':w[2],'bound_va':value,'pool_offset':x1['value'],'pool_sha256':hashlib.sha256(xs['data']).hexdigest()})
  strict(b,result);return result,facts
 orig,f1=pair(objects['production'],objects['original'],base,{});candidate,f2=pair(objects['original'],objects['candidate'],orig,{m['proposed_symbol']:m['proposed_target']});rows=strict(objects['candidate'],candidate);sections,inferred,errors=eh_sections(objects['candidate'],pe,candidate,rows,names)
 matching=[x for x in sections if x[0]<=0xf157c0<x[1] and x[3]=='0x008c4d10']
 if len(matching)!=1 or not matching[0][2] or any('0x008c4d10' in x for x in errors):raise ValueError('sized EH cleanup mismatch')
 sym=objects['candidate'].by_name.get(m['proposed_symbol'],[])
 if not sym or not any(x['section']==0 for x in sym):raise ValueError('expected class delete symbol absent')
 out.write_text(json.dumps({'scope':'private sized-delete candidate; no production integration','manifest_sha256':sha(D/'mirror-manifest.json'),'compile_sha256':sha(D/'compile-result.json'),'production_object_sha256':sha(p),'objects':{x['tag']:x['object_sha256'] for x in run['outcomes']},'strict_functions':807,'production_to_original_literals':f1,'original_to_candidate_literals':f2,'reference_allocation_size':108,'reference_cleanup_size':108,'reference_funcinfo':'0x011620ac','reference_unwind_map':'0x011620a4','reference_unwind_action':'0x00f157c0','target_cleanup_section':matching[0],'all_eh_errors':errors,'failed_eh_sections':sum(not x[2] for x in sections),'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()},'limitations':['actual installed production SG labels and full image/ownership require reproof','unrelated EH errors remain separately visible','no runtime proof']},indent=2));print(json.dumps({'strict_functions':807,'target_cleanup_match':True,'literal_changes':len(f1)+len(f2),'other_eh_errors':len(errors)}))
if __name__=='__main__':main()
