"""Derive source-grounded SG mappings for combined private 253/2909 objects."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-source-integration6757';D=M/'out/phase2-source-integration6757-lane';OUT=D/'paired-source-pools-253-2909.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve proof')
 old=json.loads((P/'units.original').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units'];bindings=json.loads((M/'out/phase2-nimem-kind-source-bindings-final.json').read_text());capture=json.loads((D/'capture.json').read_text());pe=Pe(paths.REF_IMAGE);out=[]
 for i in (253,2909):
  d=D/str(i);run=json.loads((d/'compile-result.json').read_text());mm=d/'mirror-manifest.json';c=next(x for x in capture['captured'] if x['unit']==i)
  if run['unit_index']!=i or run['mirror_manifest_sha256']!=sha(mm) or c['manifest_sha256']!=sha(mm) or sha(d/'production-baseline.obj')!=c['production_object_sha256']:raise ValueError('capture differs')
  objs={}
  for z in run['outcomes']:
   p=d/(z['tag']+'.obj')
   if z['rc'] or not z['trace_valid'] or sha(p)!=z['object_sha256']:raise ValueError('compile invalid')
   objs[z['tag']]=Coff(str(p))
  spec=copy.deepcopy(old[i]);spec['symbols'].update({k:v['target'] for k,v in bindings['units'].get(str(i),{}).items()});strict=compare(objs['original'],pe,spec);base=compare(Coff(str(d/'production-baseline.obj')),pe,spec)
  if any(x['verdict']!='match' for x in strict+base) or len(strict)!=len(spec['functions']):raise ValueError('baseline strict mismatch')
  candidate=copy.deepcopy(new[i]);facts=[];seen={};oldf={x['address']:x for x in spec['functions']}
  for f in candidate['functions']:
   prev=oldf[f['address']];x,xr=relocated(objs['original'],prev['symbol'],prev['size'],{});y,yr=relocated(objs['candidate'],f['symbol'],f['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('function/relocations differ '+f['address'])
   for a,b in zip(xr,yr):
    if a==b:continue
    if (a[0],a[1],a[3])!=(b[0],b[1],b[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (a,b)):raise ValueError('nonliteral relocation differs '+f['address'])
    q=objs['original'].named(a[2]);r=objs['candidate'].named(b[2]);qs=objs['original'].sections[q['section']];rs=objs['candidate'].sections[r['section']]
    if q['value']!=r['value'] or qs['name']!='.rdata' or rs['name']!='.rdata' or qs['relocs'] or rs['relocs'] or qs['data']!=rs['data'] or a[2] not in spec['symbols']:raise ValueError('source pool mismatch')
    value=spec['symbols'][a[2]]
    if b[2] in seen and seen[b[2]]!=value:raise ValueError('ambiguous candidate label')
    seen[b[2]]=value;candidate['symbols'][b[2]]=value;facts.append({'function':f['address'],'field_offset':a[0],'original_label':a[2],'candidate_label':b[2],'target':value,'pool_offset':q['value'],'pool_sha256':hashlib.sha256(qs['data']).hexdigest()})
  rows=compare(objs['candidate'],pe,candidate)
  if len(rows)!=len(candidate['functions']) or any(x['verdict']!='match' for x in rows):raise ValueError('candidate strict mismatch')
  out.append({'unit':i,'functions':len(rows),'original_object_sha256':sha(d/'original.obj'),'candidate_object_sha256':sha(d/'candidate.obj'),'compile_result_sha256':sha(d/'compile-result.json'),'facts':facts,'candidate_bindings':seen})
 OUT.write_text(json.dumps({'scope':'same-unit full source pool and function fields; combined private objects only','old_recipe_sha256':sha(P/'units.original'),'candidate_recipe_sha256':sha(P/'units.generated'),'baseline_binding_proof_sha256':sha(M/'out/phase2-nimem-kind-source-bindings-final.json'),'units':out,'limits':['candidate recipe labels provisional until actual production compiler output is checked','other units, EH/RTTI and final image gates remain separate']},indent=2));print(json.dumps([(x['unit'],x['functions'],len(x['facts'])) for x in out]))
if __name__=='__main__':main()
