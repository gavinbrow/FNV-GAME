"""Strict source-backed 128-function comparison of the private no-op mirror."""
import sys,json,copy,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;sys.path[:0]=[str(P/'fnv_decomp/tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
N=M/'out/phase2-tesform-noop-slots';O=M/'out/phase2-tesform-noop-mirror';B=M/'out/phase2-tesform-binding-repair-v2';OUT=O/'whole-unit-proof.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 m=json.loads((N/'manifest.json').read_bytes());run=json.loads((O/'compile-result.json').read_bytes());obj={x['tag']:O/(x['tag']+'.obj') for x in run['outcomes']}
 if run.get('unit_index')!=998 or set(obj)!={'original','candidate'}:raise ValueError('compile scope mismatch')
 for x in run['outcomes']:
  if x['rc'] or x.get('trace_valid') is not True or sha(obj[x['tag']])!=x['object_sha256']:raise ValueError('object/trace mismatch')
 recipe=B/'units.generated';u=json.loads(recipe.read_bytes())['units'][998];a=Coff(str(obj['original']));b=Coff(str(obj['candidate']));changes={x['before']:x['after'] for x in m['proposed_function_symbol_changes']};norm={v:k for k,v in changes.items()};mapping={};facts=[]
 if len(u['functions'])!=128 or len(changes)!=5:raise ValueError('unexpected function scope')
 for x in u['functions']:
  d,r=relocated(a,x['symbol'],x['size'],{});e,s=relocated(b,changes.get(x['symbol'],x['symbol']),x['size'],norm)
  if d!=e or len(r)!=len(s):raise ValueError('function bytes/relocation count changed '+x['address'])
  for z,w in zip(r,s):
   if z==w:continue
   if (z[0],z[1],z[3])!=(w[0],w[1],w[3]) or not all(re.fullmatch(r'\$SG\d+',v[2]) for v in (z,w)):raise ValueError('nonliteral relocation difference')
   p=a.named(z[2]);q=b.named(w[2]);ps=a.sections[p['section']];qs=b.sections[q['section']]
   if p['value']!=q['value'] or ps['name']!='.rdata' or qs['name']!='.rdata' or ps['data']!=qs['data'] or ps['relocs'] or qs['relocs'] or z[2] not in u['symbols']:raise ValueError('literal provenance mismatch')
   value=u['symbols'][z[2]]
   if w[2] in mapping and mapping[w[2]]!=value:raise ValueError('literal mapping collision')
   mapping[w[2]]=value;norm[w[2]]=z[2];facts.append({'function':x['address'],'field_offset':z[0],'old':z[2],'new':w[2],'source_binding':value,'pool_offset':p['value'],'pool_sha256':hashlib.sha256(ps['data']).hexdigest(),'pool_size':len(ps['data'])})
 v=copy.deepcopy(u)
 for f in v['functions']:f['symbol']=changes.get(f['symbol'],f['symbol'])
 v['symbols'].update(mapping)
 for x in m['proposed_function_symbol_changes']:v['symbols'][x['after']]=x['address']
 for x in u['functions']:
  d,r=relocated(a,x['symbol'],x['size'],{});e,s=relocated(b,changes.get(x['symbol'],x['symbol']),x['size'],norm)
  if d!=e or r!=s:raise ValueError('normalized comparison failed')
 rows=compare(b,Pe(paths.REF_IMAGE),v)
 if len(rows)!=128 or any(x['verdict']!='match' for x in rows):raise ValueError('strict candidate reference compare failed')
 payload={'scope':'private mirror 128 functions; no class/global/placement proof','recipe_sha256':sha(recipe),'original_obj_sha256':sha(obj['original']),'candidate_obj_sha256':sha(obj['candidate']),'functions':128,'raw_equal':128,'normalized_relocations_equal':128,'strict_reference_matches':128,'literal_facts':facts,'literal_bindings':mapping,'limitations':['repair-v2 recipe remains a staged baseline','literal numbering is build-path dependent and must be rederived for each production object','BGSE paired object, 78-slot graph, alias ownership and global ODR remain separate']}
 OUT.write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps({'functions':128,'literal_fields':len(facts),'strict_matches':128}))
if __name__=='__main__':main()
