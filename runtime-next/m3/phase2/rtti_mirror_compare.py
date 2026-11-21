"""Read-only COFF/PE and class diagnostics for an already compiled mirror pair."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,rtti_hkp_viewer_compare as helper,rtti_bgse_six_compare as bg,rtti_tesform_paired_compare as tes,class_metadata_compare as cm

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exception_sections(coff):
 rows={}
 for name,entries in coff.by_name.items():
  if not (name.startswith('__ehhandler$') or name.startswith('__ehfuncinfo$') or name.startswith('?dtor$') or name.startswith('?catch$')):continue
  defined=[e for e in entries if e['section']>0]
  if len(defined)!=1:continue
  item=defined[0];sec=coff.sections[item['section']];data=sec['data'][item['value']:]
  rel=[(off-item['value'],typ,coff.symbols[idx]['name']) for off,idx,typ in sec['relocs'] if off>=item['value']]
  rows[name]={'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'relocations':rel,'scope':'section tail, not proven symbol extent'}
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--kind',choices=['body','sky','tes','bgs','bgs_noop','bgs_slot21','sibling','651','plain'],required=True);ap.add_argument('--report',default='comparison-v1.json');a=ap.parse_args();out=a.out;manifest=json.loads((out/'mirror-manifest.json').read_text());compiled=json.loads((out/'compile-result.json').read_text());unitsfile=F/'build/units.json';cpath=M/'out/phase2-class-census/census-e883.json'
 if Path(a.report).name!=a.report:raise ValueError('report must be a filename')
 target=out/a.report
 if target.exists():raise FileExistsError('refusing overwrite')
 if sha(unitsfile)!=manifest['units_sha256'] or sha(out/'mirror-manifest.json')!=compiled['mirror_manifest_sha256']:raise ValueError('manifest mismatch')
 results={r['tag']:r for r in compiled['outcomes']};objects={}
 for tag in ('original','candidate'):
  p=out/(tag+'.obj');r=results[tag]
  if r['rc'] or not r['trace_valid'] or sha(p)!=r['object_sha256']:raise ValueError('object invalid '+tag)
  objects[tag]=Coff(str(p))
 units=json.loads(unitsfile.read_text())['units'];index=compiled['unit_index'];u=units[index];mapped=copy.deepcopy(u);norm={};sky_aliases={};graphname=None
 if a.kind=='tes':
  meta=json.loads((M/'out/phase2-tesform-base-slots/manifest.json').read_text());mapped,norm=tes.tes_unit(u,meta);graphname='.?AVTESForm@@'
 elif a.kind in ('bgs','bgs_noop','bgs_slot21'):
  bgmeta='out/phase2-bgsencounterzone-slot21-corrected/manifest.json' if a.kind=='bgs_slot21' else 'out/phase2-bgsencounterzone-six-override/manifest.json';meta=json.loads((M/bgmeta).read_text());mapped,norm=bg.make_unit(u,meta);tm=json.loads((M/('out/phase2-tesform-noop-slots/manifest.json' if a.kind in ('bgs_noop','bgs_slot21') else 'out/phase2-tesform-base-slots/manifest.json')).read_text())
  for x in tm['proposed_function_symbol_changes']:
   if x['after'] in mapped['symbols'] and mapped['symbols'][x['after']]!=x['address']:raise ValueError('alias collision')
   mapped['symbols'][x['after']]=x['address']
  if a.kind in ('bgs_noop','bgs_slot21'):
   proof=json.loads((M/'out/phase2-tesform-noop-mirror/noop-comparison.json').read_text());fold=tm['proposed_noop_fold'];owners=[f for q in units for f in q['functions'] if f['address']==fold['source_address']]
   if proof.get('object_sha256')!=sha(M/'out/phase2-tesform-noop-mirror/candidate.obj') or proof.get('recipe_sha256')!=sha(unitsfile) or proof.get('identical_bodies') is not True or proof.get('size')!=11 or {x['symbol'] for x in proof.get('bodies',[])}!=set(fold['new_symbols']+[fold['source_body_symbol']]) or len(owners)!=1 or owners[0]['symbol']!=fold['source_body_symbol']:raise ValueError('no-op proof or unique source owner missing')
   for name in fold['new_symbols']:
    if name in mapped['symbols'] and mapped['symbols'][name]!=fold['source_address']:raise ValueError('no-op alias collision')
    mapped['symbols'][name]=fold['source_address']
  graphname='.?AVBGSEncounterZone@@'
 elif a.kind in ('body','sky'):
  mpath=M/('out/phase2-bgsbodypart-slot0/manifest.json' if a.kind=='body' else 'out/phase2-skyobject-destructor-v1/manifest.json');meta=json.loads(mpath.read_text());changes={x['before']:x['after'] for x in meta['proposed_function_symbol_changes']};norm={v:k for k,v in changes.items()}
  for f in mapped['functions']:f['symbol']=changes.get(f['symbol'],f['symbol'])
  for x in meta['proposed_function_symbol_changes']:mapped['symbols'][x['after']]=x['address']
  if a.kind=='sky':
   for x in meta['proposed_external_aliases']:
    if u['symbols'].get(x['old'])!=x['address'] or sum(q.get('symbols',{}).get(x['new'])==x['address'] for q in units)<2:raise ValueError('alias evidence changed')
    mapped['symbols'][x['new']]=x['address'];sky_aliases[x['new']]=x['old']
  graphname='.?AVBGSBodyPart@@' if a.kind=='body' else '.?AVSkyObject@@'
 facts=[]
 for old,new in zip(u['functions'],mapped['functions']):
  try:
   n=bg.normalization_for_function(old['symbol'],norm) if a.kind in ('bgs','bgs_noop','bgs_slot21') else dict(norm)
   if a.kind=='sky' and old['address']=='0x0063f8d0':n.update(sky_aliases);n['??_7SkyObject@@6B@']='??_7FUN_0063f8d0@@6B@'
   b,br=helper.relocated(objects['original'],old['symbol'],old['size'],{});c,cr=helper.relocated(objects['candidate'],new['symbol'],new['size'],n)
   facts.append({'address':old['address'],'bytes_equal':b==c,'relocations_equal':br==cr,'baseline_relocations':br,'candidate_relocations_normalized':cr})
  except (ValueError,KeyError,IndexError) as e:facts.append({'address':old['address'],'error':str(e)})
 pe=Pe(paths.REF_IMAGE);refs={}
 for name,spec in [('original',u),('candidate',mapped)]:
  try:refs[name]=[{'address':r['address'],'verdict':r['verdict'],'errors':len(r['errors']),'byte_differences':len(r['byte_differences']),'failed_relocations':sum(not z.get('match') for z in r['relocations'])} for r in compare(objects[name],pe,spec)]
  except Exception as e:refs[name]={'fatal':type(e).__name__+': '+str(e)}
 ea=exception_sections(objects['original']);eb=exception_sections(objects['candidate']);result={'unit':index,'functions':facts,'reference':refs,'exception_sections':{'original':ea,'candidate':eb,'common_exact':sorted(k for k in ea.keys()&eb.keys() if ea[k]==eb[k]),'original_only':sorted(ea.keys()-eb.keys()),'candidate_only':sorted(eb.keys()-ea.keys())},'scope':'diagnostic; EH section tails are reported separately; all other emitted sections require separate verification'}
 if graphname:
  census=json.loads(cpath.read_text());assert census['inputs']['units_sha256']==manifest['units_sha256'];result['class_metadata']=cm.compare_class(out/'candidate.obj',mapped,units,census,graphname)
 target.write_text(json.dumps(result,indent=2));s={'unit':index,'functions':len(facts),'bytes_equal':sum(x.get('bytes_equal',False) for x in facts),'relocations_equal':sum(x.get('relocations_equal',False) for x in facts),'refs':{k:({'match':sum(x['verdict']=='match' for x in v),'nonmatch':sum(x['verdict']!='match' for x in v)} if isinstance(v,list) else v) for k,v in refs.items()}}
 if 'class_metadata' in result:
  tables=result['class_metadata']['tables'];s['tables']=[{'graph':t.get('graph_fields_equal'),'slots':t.get('emitted_slot_count'),'matched':sum(z['match'] for z in t.get('slots',[]))} for t in tables]
  if a.kind=='bgs_slot21':s['slot_21_and_22']=[{'index':z['index'],'symbol':z['symbol'],'resolved_target':z['resolved_target'],'reference_target':z['reference_target'],'match':z['match']} for t in tables for z in t.get('slots',[]) if z['index'] in (21,22)]
 print(json.dumps(s))
if __name__=='__main__':main()
