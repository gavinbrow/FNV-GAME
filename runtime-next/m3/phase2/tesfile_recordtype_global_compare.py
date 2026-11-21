"""Prove TESFile record-type global correction and every shifted literal binding."""
import copy,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-tesfile-recordtype-global';ARCH=M/'out/phase2-nimem-kind-production-archive';MAP=M/'out/phase2-nimem-kind-source-bindings-final.json';OUT=D/'comparison.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve prior proof')
 m=json.loads((D/'manifest.json').read_text());op=D/'units.original';np=D/'units.generated';run=json.loads((D/'compile-result.json').read_text());mm=D/'mirror-manifest.json'
 if sha(op)!=m['base_recipe_sha256'] or sha(np)!=m['candidate_recipe_sha256'] or sha(F/'build/units.json')!=m['base_recipe_sha256'] or sha(ARCH/'0995.obj')!=m['archived_object_sha256'] or run['unit_index']!=995 or run['mirror_manifest_sha256']!=sha(mm):raise ValueError('input mismatch')
 old=json.loads(op.read_text())['units'];new=json.loads(np.read_text())['units'];production=Coff(str(ARCH/'0995.obj'));objs={'production':production}
 for x in run['outcomes']:
  q=D/(x['tag']+'.obj')
  if x['rc'] or not x['trace_valid'] or sha(q)!=x['object_sha256']:raise ValueError('compile invalid')
  objs[x['tag']]=Coff(str(q))
 if set(objs)!={'production','original','candidate'}:raise ValueError('object pair missing')
 pe=Pe(paths.REF_IMAGE);spec=copy.deepcopy(old[995]);mapping=json.loads(MAP.read_text())['units'].get('995',{});spec['symbols'].update({k:v['target'] for k,v in mapping.items()})
 for n in ('$SG7025','$SG8028','$SG8627','$SG8632'):spec['symbols'].pop(n,None)
 special={(x['function'],x['field_offset']) for x in m['original_fields']};facts=[]
 def derive(a,b,previous,target,allow_global):
  result=copy.deepcopy(target);seen={};changed=[]
  for f in previous['functions']:
   x,xr=relocated(a,f['symbol'],f['size'],{});y,yr=relocated(b,f['symbol'],f['size'],{})
   if x!=y or len(xr)!=len(yr):raise ValueError('function or relocation shape changed '+f['address'])
   for v,w in zip(xr,yr):
    key=(f['address'],v[0]);is_special=key in special
    if (v[0],v[1],v[3])!=(w[0],w[1],w[3]):raise ValueError('relocation field differs')
    if is_special:
     if not re.fullmatch(r'\$SG\d+',v[2]) or (allow_global and w[2]!='?DAT_011873c8@@3IA') or (not allow_global and not re.fullmatch(r'\$SG\d+',w[2])):raise ValueError('global correction field differs')
     t=a.named(v[2]);ss=a.sections[t['section']];end=ss['data'].find(b'\0',t['value']);data=ss['data'][t['value']:end+1]
     if data!=b'TOFTQ\0' or pe.read(0x11873c8,len(data))==data or struct.unpack('<I',pe.read(int(f['address'],16)+v[0],4))[0]!=0x11873c8:raise ValueError('literal/global distinction differs')
     changed.append({'function':f['address'],'field_offset':v[0],'before':v[2],'after':w[2],'target':'0x011873c8','classification':'literal-to-global' if allow_global else 'legacy-invalid-literal'});continue
    if v==w:continue
    if not all(re.fullmatch(r'\$SG\d+',z[2]) for z in (v,w)):raise ValueError('nonliteral relocation changed '+f['address'])
    a1=a.named(v[2]);b1=b.named(w[2]);sa=a.sections[a1['section']];sb=b.sections[b1['section']]
    if sa['name']!='.rdata' or sb['name']!='.rdata' or sa['relocs'] or sb['relocs'] or v[2] not in previous['symbols']:raise ValueError('source pool mismatch '+f['address'])
    value=previous['symbols'][v[2]];end=sa['data'].find(b'\0',a1['value']);end2=sb['data'].find(b'\0',b1['value']);content=sa['data'][a1['value']:end+1];content2=sb['data'][b1['value']:end2+1]
    if end<0 or end2<0 or content!=content2 or pe.read(int(value,16),len(content))!=content:raise ValueError('source pool reference content differs')
    if w[2] in seen and seen[w[2]]!=value:raise ValueError('ambiguous candidate label')
    seen[w[2]]=value;result['symbols'][w[2]]=value;changed.append({'function':f['address'],'field_offset':v[0],'before':v[2],'after':w[2],'target':value,'original_pool_offset':a1['value'],'candidate_pool_offset':b1['value'],'literal_sha256':hashlib.sha256(content).hexdigest(),'original_pool_sha256':hashlib.sha256(sa['data']).hexdigest(),'candidate_pool_sha256':hashlib.sha256(sb['data']).hexdigest(),'classification':'same-unit-pool'})
  return result,changed
 prodrows=compare(production,pe,spec);prod_bad=[x['address'] for x in prodrows if x['verdict']!='match'];expected=sorted({x[0] for x in special})
 if sorted(prod_bad)!=expected:raise ValueError('unexpected production baseline failures '+str(prod_bad))
 orig,first=derive(production,objs['original'],spec,spec,False);origrows=compare(objs['original'],pe,orig)
 if sorted(x['address'] for x in origrows if x['verdict']!='match')!=expected:raise ValueError('original mismatch outside known invalid literal')
 target=copy.deepcopy(new[995]);target['symbols'].update(orig['symbols'])
 for name in ('$SG7025','$SG8028','$SG8627','$SG8632'):target['symbols'].pop(name,None)
 target['symbols']['?DAT_011873c8@@3IA']='0x011873c8';cand,second=derive(objs['original'],objs['candidate'],orig,target,True)
 rows=compare(objs['candidate'],pe,cand)
 if len(rows)!=87 or any(x['verdict']!='match' for x in rows):raise ValueError('candidate strict mismatch '+str([(x['address'],x['errors']) for x in rows if x['verdict']!='match'][:4]))
 sections,inf,err=eh_sections(objs['candidate'],pe,cand,rows,recipe_names(old));done=[{'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}}];tails,bad,guessed,_,conf=eh_tails([cand],done,pe)
 OUT.write_text(json.dumps({'scope':'source-global correction; no literal alias to initialized-zero global','manifest_sha256':sha(D/'manifest.json'),'baseline_map_sha256':sha(MAP),'production_object_sha256':sha(ARCH/'0995.obj'),'compile_result_sha256':sha(D/'compile-result.json'),'production_semantic_baseline_failures':prod_bad,'original_semantic_baseline_failures':expected,'candidate_strict_functions':len(rows),'production_to_original':first,'original_to_candidate':second,'candidate_derived_bindings':{x['after']:x['target'] for x in second if x['classification']=='same-unit-pool'},'ordinary_eh':{'located_sections':len(sections),'failed_sections':sum(not x[2] for x in sections),'errors':err,'recipe_tails':len(tails),'bad':bad,'inferred_tails':len(guessed),'conflicts':conf},'limits':['startup initialization and semantic value of DAT_011873c8 remain unproved','candidate SG labels require actual production rederivation','candidate is private; final image/ownership/runtime remain separate']},indent=2));print(json.dumps({'candidate_strict':len(rows),'legacy_mismatches':len(prod_bad),'paired_literals':sum(x['classification']=='same-unit-pool' for x in second),'eh_errors':len(err),'eh_failed_sections':sum(not x[2] for x in sections),'bad_tails':len(bad)}))
if __name__=='__main__':main()
