"""Strict paired ten-remap TESForm and corrected BGSE comparison."""
import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,class_metadata_compare as cm,rtti_bgse_six_compare as bg
from rtti_hkp_viewer_compare import relocated
T=M/'out/phase2-tesform-load-typed-v4-mirror';B=M/'out/phase2-bgs-load-typed-v4-mirror';TM=M/'out/phase2-class-typed-v4/tesform-manifest.json';BM=M/'out/phase2-class-typed-v4/bgs-manifest.json';U=F/'build/units.json';C=M/'out/phase2-class-census/census-fa366.json';OUT=M/'out/phase2-load-typed-v4-paired-report.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def objects(path,idx):
 manifest=path/'mirror-manifest.json';run=json.loads((path/'compile-result.json').read_bytes())
 if run['unit_index']!=idx or run['mirror_manifest_sha256']!=sha(manifest) or json.loads(manifest.read_bytes())['units_sha256']!=sha(U):raise ValueError('compile/manifest mismatch')
 result={}
 for row in run['outcomes']:
  p=path/(row['tag']+'.obj')
  if row['rc'] or row.get('trace_valid') is not True or sha(p)!=row['object_sha256']:raise ValueError('bad compiled input')
  result[row['tag']]=Coff(str(p))
 if set(result)!={'original','candidate'}:raise ValueError('missing object')
 return result

def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 if sha(U)!='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8':raise ValueError('recipe changed')
 units=json.loads(U.read_bytes())['units'];census=json.loads(C.read_bytes())
 if census['inputs']['units_sha256']!=sha(U):raise ValueError('census stale')
 t=objects(T,998);b=objects(B,2);tm=json.loads(TM.read_bytes());bm=json.loads(BM.read_bytes());tu=units[998];bu=units[2]
 def unique(coff,prefix,defined):
  matches=[name for name,items in coff.by_name.items() if name.startswith(prefix) and 'BGSLoadFormBuffer' in name and any((x['section']>0)==defined for x in items)]
  if len(matches)!=1:raise ValueError('typed method symbol ambiguous '+prefix)
  return matches[0]
 discovered={'tes_load':unique(t['candidate'],'?LoadGame@TESForm@@',True),'bgs_load':unique(b['candidate'],'?LoadGame@BGSEncounterZone@@',True),'bgs_revert':unique(b['candidate'],'?Revert@BGSEncounterZone@@',True),'base_load':unique(b['candidate'],'?LoadGame@TESForm@@',False),'base_revert':unique(b['candidate'],'?Revert@TESForm@@',False)}
 if discovered['tes_load']!=discovered['base_load']:raise ValueError('base LoadGame class-key differs across units')
 if len({x.split('@@',1)[1] for x in discovered.values()})!=1:raise ValueError('derived/base typed method contracts differ')
 for item in tm['proposed_function_symbol_changes']:
  if item['address']=='0x00484da0':item['after']=discovered['tes_load']
 for item in bm['proposed_function_symbol_changes']:
  if item['address']=='0x005264a0':item['after']=discovered['bgs_load']
  if item['address']=='0x00526570':item['after']=discovered['bgs_revert']
 changes={x['before']:x['after'] for x in tm['proposed_function_symbol_changes']};norm={v:k for k,v in changes.items()}
 if len(changes)!=len(tm['proposed_function_symbol_changes']) or len(tu['functions'])!=128 or len(bu['functions'])!=24:raise ValueError('unexpected function scope')
 production=RN/'pinned-build/obj_v3/0998.obj';repair=M/'out/phase2-tesform-binding-repair-v3/manifest.json';evidence=json.loads(repair.read_bytes())
 if sha(production)!='6ccea781163b57f7835a002ec7b9e97e321828584b3a3dadb034cf183f9ea676':raise ValueError('production object changed')
 pe=Pe(paths.REF_IMAGE);prod=Coff(str(production));base=compare(prod,pe,tu)
 if len(base)!=128 or any(x['verdict']!='match' for x in base):raise ValueError('strict production baseline fails')
 def derive(oldcoff,newcoff,unit,renames,bindings):
  mapped=copy.deepcopy(unit); mapping={};facts=[];normal={v:k for k,v in renames.items()}
  for f in unit['functions']:
   a,ar=relocated(oldcoff,f['symbol'],f['size'],{});b,br=relocated(newcoff,renames.get(f['symbol'],f['symbol']),f['size'],normal)
   if a!=b or len(ar)!=len(br):raise ValueError('code/relocation count mismatch '+f['address'])
   for x,y in zip(ar,br):
    if x==y:continue
    if (x[0],x[1],x[3])!=(y[0],y[1],y[3]) or not all(re.fullmatch(r'\$SG\d+',v[2]) for v in (x,y)):raise ValueError('nonliteral relocation mismatch '+f['address'])
    p=oldcoff.named(x[2]);q=newcoff.named(y[2]);ps=oldcoff.sections[p['section']];qs=newcoff.sections[q['section']]
    if p['value']!=q['value'] or ps['name']!='.rdata' or qs['name']!='.rdata' or ps['data']!=qs['data'] or ps['relocs'] or qs['relocs'] or x[2] not in bindings:raise ValueError('literal pool provenance mismatch')
    value=bindings[x[2]]
    if y[2] in mapping and mapping[y[2]]!=value:raise ValueError('literal ambiguity')
    mapping[y[2]]=value;normal[y[2]]=x[2];facts.append({'function':f['address'],'field_offset':x[0],'before':x[2],'after':y[2],'binding':value,'pool_offset':p['value'],'pool_sha256':hashlib.sha256(ps['data']).hexdigest()})
  for f in unit['functions']:
   a,ar=relocated(oldcoff,f['symbol'],f['size'],{});b,br=relocated(newcoff,renames.get(f['symbol'],f['symbol']),f['size'],normal)
   if a!=b or ar!=br:raise ValueError('normalized function mismatch '+f['address'])
  for f in mapped['functions']:f['symbol']=renames.get(f['symbol'],f['symbol'])
  mapped['symbols'].update(mapping)
  for x in tm['proposed_function_symbol_changes'] if renames else []:mapped['symbols'][x['after']]=x['address']
  return mapped,facts
 # First ground mirror-original label numbers against source-backed production object.
 torig,origfacts=derive(prod,t['original'],tu,{},tu['symbols']);tcand,candfacts=derive(t['original'],t['candidate'],torig,changes,torig['symbols'])
 for name,obj,spec in [('TES mirror original',t['original'],torig),('TES candidate',t['candidate'],tcand)]:
  rows=compare(obj,pe,spec)
  if len(rows)!=128 or any(x['verdict']!='match' for x in rows):raise ValueError(name+' strict reference failed')
 # Three no-op aliases need independent full-body proof of this exact object.
 proofpath=T/'noop-proof.json';proof=json.loads(proofpath.read_bytes());fold=tm['proposed_noop_fold']
 if proof['object_sha256']!=sha(T/'candidate.obj') or proof['recipe_sha256']!=sha(U) or proof['identical_bodies'] is not True or {x['symbol'] for x in proof['bodies']}!=set(fold['new_symbols']+[fold['source_body_symbol']]):raise ValueError('no-op proof mismatch')
 lo=int(fold['source_address'],16);owners=[(i,f) for i,u in enumerate(units) for f in u['functions'] if int(f['address'],16)<lo+11 and lo<int(f['address'],16)+f['size']]
 if len(owners)!=1 or owners[0][0]!=998 or owners[0][1]['symbol']!=fold['source_body_symbol']:raise ValueError('no-op owner ambiguity')
 mapped,normb=bg.make_unit(bu,bm)
 external=json.loads((M/'out/phase2-class-typed-v4/manifest.json').read_text())['base_external_symbol_aliases']
 if len(external)!=2:raise ValueError('expected two load-buffer source-backed external bindings')
 for x in external:
  x['after']=discovered['base_load'] if 'LoadGame@TESForm' in x['before'] else discovered['base_revert']
  if bu['symbols'].get(x['before'])!=x['address']:raise ValueError('old external binding changed')
  if x['after'] in mapped['symbols'] and mapped['symbols'][x['after']]!=x['address']:raise ValueError('external binding collision')
  mapped['symbols'][x['after']]=x['address'];normb[x['after']]=x['before']
 for x in tm['proposed_function_symbol_changes']:
  if x['after'] in mapped['symbols'] and mapped['symbols'][x['after']]!=x['address']:raise ValueError('source binding collision')
  mapped['symbols'][x['after']]=x['address']
 for name in fold['new_symbols']:
  if name in mapped['symbols'] and mapped['symbols'][name]!=fold['source_address']:raise ValueError('no-op binding collision')
  mapped['symbols'][name]=fold['source_address']
 bf=[]
 for f,new in zip(bu['functions'],mapped['functions']):
  normal=bg.normalization_for_function(f['symbol'],normb);a,ar=relocated(b['original'],f['symbol'],f['size'],{});z,zr=relocated(b['candidate'],new['symbol'],new['size'],normal)
  if a!=z or ar!=zr:raise ValueError('BGSE function mismatch '+f['address'])
  bf.append(f['address'])
 for name,obj,spec in [('BGSE original',b['original'],bu),('BGSE candidate',b['candidate'],mapped)]:
  rows=compare(obj,pe,spec)
  if len(rows)!=24 or any(x['verdict']!='match' for x in rows):raise ValueError(name+' strict reference failed')
 graph=cm.compare_class(B/'candidate.obj',mapped,units,census,'.?AVBGSEncounterZone@@');tables=graph['tables']
 if len(tables)!=1 or not tables[0].get('graph_fields_equal') or tables[0]['emitted_slot_count']!=78:raise ValueError('BGSE graph mismatch')
 slots=tables[0]['slots'];selected=[s for s in slots if s['index'] in (20,21,22,23,37,38,39,42,43,44,45,46,47)]
 output={'scope':'private paired candidate; source ABI and final placement remain open','discovered_typed_symbols':discovered,'units_sha256':sha(U),'tes_obj_sha256':sha(T/'candidate.obj'),'bgs_obj_sha256':sha(B/'candidate.obj'),'tes_functions_equal_and_strict':128,'bgs_functions_equal_and_strict':24,'original_literal_fields':origfacts,'candidate_literal_fields':candfacts,'noop_proof_sha256':sha(proofpath),'graph':graph,'selected_slots':selected,'limitations':['historical method names and const qualifications remain hypotheses','source integration, final ICF/ownership and runtime gates not performed']}
 OUT.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'tes_functions':128,'bgs_functions':24,'matched_slots':sum(x['match'] for x in slots),'selected_slots':selected}))
if __name__=='__main__':main()
