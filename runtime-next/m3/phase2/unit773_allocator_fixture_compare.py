"""Read-only 773 pair comparison: strict mapped functions, EH, RTTI and owner evidence."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';D=R/'phase2-unit773-allocator-fixture';Q=R/'phase2-nimem-psys-pointer-binding-v1/units.generated';N=R/'phase2-nimemobject-native-operators-v2';C=R/'phase2-class-census/census-6757.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
from class_metadata_compare import ObjectRecords,compare_class
import paths
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=D/'independent-comparison.json'
 if out.exists():raise FileExistsError(out)
 pins={D/'mirror-manifest.json':'798dd12f1265f82408eaeb7aa05003feefd64875f6d1293bcf9ad5821ff72b4c',Q:'5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad',N/'manifest.json':'d092423e8d52181996e5d250e0555581a03f979e38cb89dd974925db01b12139',N/'independent-review.json':'a8de71805bf5a136162f9f28853f36d8d721001d9fcdb6993f59bcd9bffa4270'}
 if any(sha(p)!=h for p,h in pins.items()):raise ValueError('pinned input drift')
 review=json.loads((N/'independent-review.json').read_bytes());nm=json.loads((N/'manifest.json').read_bytes());units=json.loads(Q.read_bytes())['units'];spec=units[773];run=json.loads((D/'compile-result.json').read_bytes());mirror=json.loads((D/'mirror-manifest.json').read_bytes())
 if run['mirror_manifest_sha256']!=sha(D/'mirror-manifest.json') or run['unit_index']!=773 or run['flags']!=spec['flags'] or len(spec['functions'])!=39:raise ValueError('compile identity')
 owners={}
 for i,symbol,address,size,count in [(2734,'??2NiMemObject@@SAPAXI@Z','0x00aa13e0',62,43),(1664,'??3NiMemObject@@SAXPAXI@Z','0x00aa1460',34,3)]:
  f=[x for x in units[i]['functions'] if x['symbol']==symbol and x['address']==address and x['size']==size];r=review['units'][str(i)]
  if len(f)!=1 or r['candidate']['strict_functions']!=count or not r['all_mapped_bytes_and_relocations_equal'] or sha(N/str(i)/'candidate.obj')!=r['candidate']['object_sha256']:raise ValueError('source owner proof')
  owner=next(z for z in nm['owners'] if z['unit']==i)
  if owner['candidate']!=symbol or owner['address']!=address:raise ValueError('owner provenance')
  owners[symbol]=address
 if spec['symbols'].get('??2NiMemObjectAllocation@@SAPAXI@Z')!='0x00aa13e0' or spec['symbols'].get('__operator_delete_sized')!='0x00aa1460':raise ValueError('existing source binding')
 objects={}
 for row in run['outcomes']:
  if row['tag'] not in ('original','candidate') or row['rc'] or not row['trace_valid'] or sha(D/(row['tag']+'.obj'))!=row['object_sha256']:raise ValueError('compile outcome')
  objects[row['tag']]=Coff(str(D/(row['tag']+'.obj')))
 if set(objects)!={'original','candidate'}:raise ValueError('pair missing')
 pe=Pe(paths.REF_IMAGE)
 if sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('reference drift')
 specs={'original':spec,'candidate':copy.deepcopy(spec)};specs['candidate']['symbols'].update(owners);results={}
 for tag,obj in objects.items():
  rows=compare(obj,pe,specs[tag]);sec,inf,errors=eh_sections(obj,pe,specs[tag],rows,recipe_names(units));tails,bad,_,_,conf=eh_tails([specs[tag]],[{'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}],pe)
  results[tag]={'functions':len(rows),'strict_matches':sum(x['verdict']=='match' for x in rows),'failures':[x for x in rows if x['verdict']!='match'],'eh_sections':sec,'eh_errors':errors,'bad_tails':bad,'conflicts':conf}
 differences=[];calls=[]
 for f in spec['functions']:
  a,ar=relocated(objects['original'],f['symbol'],f['size'],{});b,br=relocated(objects['candidate'],f['symbol'],f['size'],{})
  if a!=b or ar!=br:differences.append({'address':f['address'],'bytes_equal':a==b,'original_relocations':ar,'candidate_relocations':br})
  for tag,rs in [('original',ar),('candidate',br)]:
   for r in rs:
    if 'NiMemObject' in r[2] or 'operator_delete_sized' in r[2]:calls.append({'function':f['address'],'variant':tag,'field':r})
 census=json.loads(C.read_bytes());graphs=[]
 for name,va in [('ImageSpaceModifierInstanceDOF',0x110ce68),('ImageSpaceModifierInstanceDRB',0x110cf64)]:
  obj=objects['candidate'];sym=obj.named('??_R3'+name+'@@8');actual=ObjectRecords(obj).hierarchy((sym['section'],sym['value']));ref=next(x for x in census['hierarchies'] if x['va']==va);expected={'attributes':ref['attributes'],'bases':[{k:b[k] for k in ('type_name','contained_bases','pmd','attributes','preorder_parent_index')} for b in ref['bases']]};graphs.append({'class':name,'native':actual,'reference':expected,'matches':actual==expected})
 metadata=[compare_class(D/'candidate.obj',specs['candidate'],units,census,'.?AV'+name+'@@') for name in ('ImageSpaceModifierInstanceDOF','ImageSpaceModifierInstanceDRB')]
 verdict=all(x['strict_matches']==39 and not x['eh_errors'] and not x['bad_tails'] and not x['conflicts'] and all(s[2] for s in x['eh_sections']) for x in results.values()) and all(x['matches'] for x in graphs)
 report={'status':'DIAGNOSTIC; independent allocation-call and pair review required','ordinary_gate_passed':verdict,'owner_source_proof_sha256':sha(N/'independent-review.json'),'compile_result_sha256':sha(D/'compile-result.json'),'census_sha256':sha(C),'owner_local_bindings':owners,'results':results,'mapped_pair_differences':differences,'allocator_relocations':calls,'graphs':graphs,'full_locator_and_slot_diagnostics':metadata,'limits':['local owner bindings diagnostic only; no global alias or source installation','review allocation sizes, all changed call and EH relocations against source contracts','graph comparison excludes final placement and alias ownership','all source/header consumers and runtime remain separate']};out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'ordinary_gate_passed':verdict,'graph_matches':[x['matches'] for x in graphs],'pair_differences':len(differences),'allocator_relocations':len(calls)}))
if __name__=='__main__':main()
