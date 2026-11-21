"""Strict production-grounded comparison for the BaseFormComponent core cohort mirrors."""
import argparse,copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
from rtti_mirror_compare import exception_sections
import paths
D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True,type=int,help='unit index from pinned BFC cohort');ap.add_argument('--production-object-sha256',required=True);ap.add_argument('--report',default='comparison.json');ap.add_argument('--mirror',type=Path,required=True);a=ap.parse_args();out=a.mirror.resolve()
 try:out.relative_to((M/'out').resolve())
 except ValueError:raise ValueError('mirror outside private out')
 if Path(a.report).name!=a.report:raise ValueError('report must be a filename')
 result=out/a.report
 if result.exists():raise FileExistsError('refusing overwrite')
 mf=out/'mirror-manifest.json';m=json.loads(mf.read_text());run=json.loads((out/'compile-result.json').read_text());up=F/'build/units.json'
 if sha(up)!=D or m['units_sha256']!=D or run['unit_index']!=a.unit or run['mirror_manifest_sha256']!=sha(mf):raise ValueError('input recipe/manifest mismatch')
 objs={}
 for row in run['outcomes']:
  p=out/(row['tag']+'.obj')
  if row['rc'] or not row['trace_valid'] or sha(p)!=row['object_sha256']:raise ValueError('compiled object invalid')
  objs[row['tag']]=Coff(str(p))
 if set(objs)!={'original','candidate'}:raise ValueError('missing mirror object')
 pp=RN/('pinned-build/obj_v3/%04d.obj'%a.unit)
 if sha(pp)!=a.production_object_sha256.lower():raise ValueError('production object changed')
 prod=Coff(str(pp));unit=json.loads(up.read_text())['units'][a.unit];cohort=json.loads((M/'out/phase2-baseformcomponent-core/manifest.json').read_text());matches=[x for x in cohort['units'] if x['unit']==a.unit];
 if len(matches)!=1:raise ValueError('unit absent from cohort')
 expected=len(matches[0]['functions'])
 if len(unit['functions'])!=expected:raise ValueError('unit function count changed')
 evidence=M/'out/phase2-baseformcomponent-core';pins={'local-string-evidence-v2.json':'9a1f91688af828346366171165b9373219e46d6329f02ae1948e509f457f5744','local-string-evidence-v3.json':'3ed975d088d8623b8958b42a6084115fab4d2a607698c91376453d35c7658ad7','external-binding-evidence.json':'806cf0b2566329e44ee4771b190f39beb8f974d7ade3cc9c1f7bd504ee6cf444','archived-immediate-evidence.json':'6f82006094857bab1a12c3acee1adc01e8eb1fe212e4759d86e61b0541bf988b'}
 for name,digest in pins.items():
  if sha(evidence/name)!=digest:raise ValueError('binding evidence changed')
 def bind(k,v):
  unit['symbols'][k]=v # Evidence pins and same-unit provenance justify replacing stale local labels.
 for name in ('local-string-evidence-v2.json','local-string-evidence-v3.json'):
  e=json.loads((evidence/name).read_text())
  for k,v in e['source_derived_local_bindings'].get(str(a.unit),{}).items():bind(k,v)
 for x in json.loads((evidence/'external-binding-evidence.json').read_text())['fields']:
  if x['unit']==a.unit and x['status']=='source-unique-reference-agree':bind(x['symbol'],x['source_target'])
 for x in json.loads((evidence/'archived-immediate-evidence.json').read_text())['fields']:
  if x['unit']==a.unit:bind(x['symbol'],x['archived_source_immediate_va'])
 pe=Pe(paths.REF_IMAGE);r=compare(prod,pe,unit)
 if len(r)!=expected or any(x['verdict']!='match' for x in r):raise ValueError('production baseline not strict reference match')
 def derive(old,new,spec):
  result=copy.deepcopy(spec);norm={};facts=[]
  for f in spec['functions']:
   x,xr=relocated(old,f['symbol'],f['size'],{});y,yr=relocated(new,f['symbol'],f['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('code or relocation count changed '+f['address'])
   for v,w in zip(xr,yr):
    if v==w:continue
    if re.fullmatch(r'\$extra_\d+\$\d+',v[2]) and re.fullmatch(r'\$extra_\d+\$\d+',w[2]):
     a=old.named(v[2]);b=new.named(w[2]);of=old.named(f['symbol']);nf=new.named(f['symbol'])
     if (v[0],v[1],v[3])!=(w[0],w[1],w[3]) or a['section']!=of['section'] or b['section']!=nf['section'] or a['value']!=b['value'] or a['storage']!=6 or b['storage']!=6:raise ValueError('extra label target differs')
     norm[w[2]]=v[2];facts.append({'function':f['address'],'field_offset':v[0],'before':v[2],'after':w[2],'same_function_section_value':a['value']});continue
    if (v[0],v[1],v[3])!=(w[0],w[1],w[3]) or not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (v,w)):raise ValueError('nonliteral relocation differs '+f['address'])
    p=old.named(v[2]);q=new.named(w[2]);ps=old.sections[p['section']];qs=new.sections[q['section']]
    if p['value']!=q['value'] or ps['name']!='.rdata' or qs['name']!='.rdata' or ps['data']!=qs['data'] or ps['relocs'] or qs['relocs'] or v[2] not in spec['symbols']:raise ValueError('literal pool/source evidence differs')
    value=spec['symbols'][v[2]]
    if w[2] in norm and norm[w[2]]!=v[2]:raise ValueError('ambiguous literal mapping')
    norm[w[2]]=v[2];result['symbols'][w[2]]=value;facts.append({'function':f['address'],'field_offset':v[0],'before':v[2],'after':w[2],'bound_va':value,'pool_offset':p['value'],'pool_sha256':hashlib.sha256(ps['data']).hexdigest()})
  for f in spec['functions']:
   x,xr=relocated(old,f['symbol'],f['size'],{});y,yr=relocated(new,f['symbol'],f['size'],norm)
   if x!=y or xr!=yr:raise ValueError('normalized code/reloc mismatch '+f['address'])
  r=compare(new,pe,result)
  if len(r)!=expected or any(x['verdict']!='match' for x in r):raise ValueError('mirror not strict reference match')
  return result,facts
 first,f1=derive(prod,objs['original'],unit);second,f2=derive(objs['original'],objs['candidate'],first)
 e1=exception_sections(objs['original']);e2=exception_sections(objs['candidate'])
 if e1!=e2:raise ValueError('EH section evidence differs; review required')
 output={'unit':a.unit,'production_obj_sha256':sha(pp),'functions':expected,'production_reference_matches':expected,'mirror_original_reference_matches':expected,'mirror_candidate_reference_matches':expected,'production_to_mirror_literals':f1,'mirror_to_candidate_literals':f2,'eh_named_section_tails_equal':len(e1),'scope':'full mapped functions and named EH section tails; other generated sections, ODR and final production label placement remain separate'}
 result.write_text(json.dumps(output,indent=2));print(json.dumps({'unit':a.unit,'functions':expected,'literal_changes':len(f1)+len(f2),'eh_sections':len(e1)}))
if __name__=='__main__':main()
