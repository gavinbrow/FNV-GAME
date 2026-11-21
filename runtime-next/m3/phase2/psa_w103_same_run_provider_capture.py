"""Post-run PSA provider capsule: requires same-run frozen input attestation."""
import argparse,gzip,hashlib,json,os,pickle,re,shutil,struct,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;RN=M.parent;sys.path[:0]=[str(H),str(R/'fnv_decomp/tools'),str(RN/'data-v1'),str(RN/'pinned-build'),str(RN)]
import vtable_search_library as V
from compare import Coff,Pe,compare
from build_and_match import recipe_names
import assemble_v3
import paths
PRIMARY='??_ETESModelPSA@@UAEPAXI@Z';FALLBACK='??_GTESModelPSA@@UAEPAXI@Z';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def directive_hits(blob):
 if len(blob)<20:raise ValueError('short object')
 machine,nsec=struct.unpack_from('<HH',blob,0);opts=struct.unpack_from('<H',blob,16)[0];start=20+opts;hits=[]
 if start+40*nsec>len(blob):raise ValueError('truncated section table')
 for i in range(nsec):
  row=struct.unpack_from('<8sIIIIIIHHI',blob,start+i*40);name=row[0].rstrip(b'\0');size=row[3];ptr=row[4]
  if name==b'.drectve':
   if ptr+size>len(blob):raise ValueError('truncated directive section')
   data=blob[ptr:ptr+size]
   tokens=[x.decode('ascii','replace') for x in re.findall(rb'(?i)/(?:DEFAULTLIB|ALTERNATENAME):[^\s]+',data)]
   if tokens or any(n.encode() in data for n in (PRIMARY,FALLBACK)):hits.append({'sha256':hashlib.sha256(data).hexdigest(),'tokens':tokens,'target_name_present':any(n.encode() in data for n in (PRIMARY,FALLBACK))})
 return hits

def main():
 if sys.flags.optimize:raise ValueError('optimized Python disables validation assumptions')
 ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--freeze',type=Path,required=True);ap.add_argument('--capture',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();run=a.run.resolve();freeze=a.freeze.resolve();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 capture=json.loads(a.capture.read_bytes());snapshot=json.loads((freeze/'inputs-before.json').read_bytes());result=json.loads((freeze/'result.json').read_bytes());command=json.loads((freeze/'command.json').read_bytes())
 if not result['input_freeze_passed'] or result['command_rc'] or result['final_digest_changes'] or result['observed_metadata_changes']:raise ValueError('run freeze failed')
 if capture.get('run_summary_sha256')!=h(run/'build-summary.json') or capture.get('freeze_result_sha256')!=h(freeze/'result.json'):raise ValueError('postrun capture is not bound to run')
 if command.get('build_environment',{}).get('FNV_COFF_WEAK')!='0':raise ValueError('weak mode not recorded off')
 stable=[R/'fnv_decomp/tools/compare.py',RN/'pinned-build/assemble_v3.py',RN/'build-v7/assemble_v7.py',RN/'build-v7/rebuild.cmd',RN/'data-v1/phase0.py',RN/'data-v1/place.py',RN/'m3/splice.py',RN/'reloc-v7/binding_overlay.json',R/'FNV/tools/vc2008/VC/lib/libcmt.lib',R/'FNV/tools/vc2008/VC/lib/libcpmt.lib']
 for p in stable:
  key=str(p.resolve())
  if key not in snapshot or not p.is_file() or snapshot[key]['sha256']!=h(p):raise ValueError('stable input not frozen '+key)
 rebuild=(RN/'build-v7/rebuild.cmd').read_text(errors='strict')
 if 'set FNV_ICF=1' not in rebuild or 'set FNV_OVERLAY=1' not in rebuild:raise ValueError('final V7 mode not evidenced')
 required=stable+[Path(paths.REF_IMAGE),run/'evidence/0620.obj',run/'build-summary.json',run/'evidence/units.json',run/'evidence/compile_v3.jsonl',run/'evidence/data-v1-scratch/dv1_phase0.pkl',run/'evidence/data-v1-scratch/dv1_placed.pkl',run/'evidence/m3_manifest.json',run/'evidence/dv1_pieces.json',run/'evidence/relocs_v7.tsv.gz',run/'evidence/icf_map.json',M/'out/phase2-bgsbodypart-split-headers-proposal/psa-weak-ownership.json']
 required += [run/'evidence'/('m3_data%s.obj'%('' if i==0 else '_%d'%i)) for i in range(4)]
 for p in required:
  if not p.is_file():raise ValueError('required input absent '+str(p))
  key=str(p.resolve())
  if p in stable:continue
  if capture.get('files',{}).get(key)!=h(p):raise ValueError('generated/output capture missing or changed '+key)
 optional_names=['build-v7/ehvariants_w2.json','build-v7/sg_sidecar_w2.json','reloc-v7/int_constants.json']
 optional={}
 for name in optional_names:
  live=RN/name;key=str(live.resolve());expected=capture.get('optional_files',{}).get(name,'MISSING')
  if expected=='MISSING':raise ValueError('optional namespace presence not captured '+name)
  if expected is None:
   if live.exists():raise ValueError('optional namespace unexpectedly present '+name)
  elif key not in snapshot or not live.is_file() or snapshot[key]['sha256']!=expected or h(live)!=expected:raise ValueError('optional namespace mismatch '+name)
  optional[name]=expected
 variant_file=RN/'build-v7/ehvariants_w2.json';variant_records=json.loads(variant_file.read_bytes()) if variant_file.exists() else []
 variant_objects=[]
 for v in variant_records:
  name=Path(v['obj'])
  if name.is_absolute() or '..' in name.parts:raise ValueError('variant path escapes')
  archived=run/'evidence'/name
  if not archived.is_file() or capture.get('files',{}).get(str(archived.resolve()))!=h(archived):raise ValueError('variant object not captured '+str(name))
  c=Coff(str(archived));variant_objects.append({'unit':v['unit'],'sha256':h(archived),'exact_names':[{'name':q['name'],'storage':q['storage'],'section':q['section']} for q in c.symbols.values() if q['name'] in (PRIMARY,FALLBACK)]})
 overlay=RN/'reloc-v7/binding_overlay.json';overlay_state=h(overlay)
 libs=[R/'FNV/tools/vc2008/VC/lib/libcmt.lib',R/'FNV/tools/vc2008/VC/lib/libcpmt.lib']
 summary=json.loads((run/'build-summary.json').read_bytes())
 if summary.get('status')!='ok' or any(x['rc'] for x in summary['steps']):raise ValueError('run incomplete')
 for n in ('dv1_phase0.pkl','dv1_placed.pkl'):
  if summary['provenance']['data_v1_scratch_sha256'][n]!=h(run/'evidence/data-v1-scratch'/n):raise ValueError('scratch provenance mismatch')
 ownerproof=json.loads((M/'out/phase2-bgsbodypart-split-headers-proposal/psa-weak-ownership.json').read_bytes())
 if not all(ownerproof.get(k) is True for k in ('wrapper_equal_to_source_owner','implicit_dtor_equal_to_unit2909_source_owner','strict_wrapper_reference_match')):raise ValueError('prior source-owner proof absent')
 units=json.loads((run/'evidence/units.json').read_bytes())['units'];spec=dict(units[620]);spec['functions']=[f for f in units[620]['functions'] if f['address'] in ('0x005e3c30','0x0051b950')]
 if len(spec['functions'])!=2 or any(x['verdict']!='match' for x in compare(Coff(str(run/'evidence/0620.obj')),Pe(paths.REF_IMAGE),spec)):raise ValueError('actual native G/dtor strict proof failed')
 before={str(p.resolve()):h(p) for p in required};archives=[]
 for p in libs:
  raw=p.read_bytes();indices=V.validate_archive_indexes(raw);found=[];directives=[];unsupported=[];count=0
  for i,(name,blob) in enumerate(V.archive_members(raw)):
   if name in ('/','//','/SYM64/'):continue
   count+=1
   try:
    for n in (PRIMARY,FALLBACK):
     if V.scan_coff(blob,n.encode()):found.append({'member':i,'name':name,'symbol':n})
    for record in directive_hits(blob):directives.append({'member':i,'name':name,**record})
   except Exception as ex:unsupported.append({'member':i,'name':name,'reason':str(ex)})
  if unsupported:raise ValueError('unsupported CRT members; closure unavailable')
  archives.append({'name':p.name,'sha256':h(p),'members':count,'indices':indices,'strong_definitions':found,'targeted_directives':directives})
 # Cohort indexing is delegated to separately pinned, start/end-hashing driver.
 out.mkdir();index=out/'source-index.json';cmd=[sys.executable,str(H/'psa_weak_provider_index.py'),'--objects',str(RN/'pinned-build/obj_v3'),'--compile-log',str(run/'evidence/compile_v3.jsonl'),'--recipe',str(run/'evidence/units.json'),'--freeze-before',str(freeze/'inputs-before.json'),'--freeze-result',str(freeze/'result.json'),'--out',str(index)];subprocess.run(cmd,check=True)
 # Record named V7 candidates, actual placed entries and exact generated symbols.
 v7=[]
 with gzip.open(run/'evidence/relocs_v7.tsv.gz','rt') as f:
  for line in f:
   if PRIMARY in line or FALLBACK in line:v7.append(line.rstrip().split('\t'))
 icf=json.loads((run/'evidence/icf_map.json').read_bytes());ov=json.loads(overlay.read_bytes()) if overlay_state!='absent' else None
 sys.path[:0]=[str(RN/'data-v2'),str(RN/'data-v3')];original_gzip_open=gzip.open
 def archived_gzip(file,*args,**kwargs):
  if str(Path(file).resolve()).casefold()==str((RN/'build-v7/relocs_v7.tsv.gz').resolve()).casefold():file=run/'evidence/relocs_v7.tsv.gz'
  return original_gzip_open(file,*args,**kwargs)
 gzip.open=archived_gzip
 try:import place
 finally:gzip.open=original_gzip_open
 state=pickle.loads((run/'evidence/data-v1-scratch/dv1_placed.pkl').read_bytes());hits=[]
 for key,s in state.SEC.items():
  for z in s['relocs']:
   if z[2] in (PRIMARY,FALLBACK):hits.append({'units':s['units'],'placement':state.placed.get(key),'offset':z[0],'name':z[2],'phase0_source':z[7]})
 generated=[]
 for i in range(4):
  p=run/'evidence'/('m3_data%s.obj'%('' if i==0 else '_%d'%i));c=Coff(str(p));generated += [{'object':p.name,'name':s['name'],'storage':s['storage'],'section':s['section']} for s in c.symbols.values() if s['name'] in (PRIMARY,FALLBACK)]
 if any(h(Path(k))!=v for k,v in before.items()) or (overlay_state=='absent' and overlay.exists()):raise ValueError('provider input changed during capture')
 fn_targets={n:sorted({f['address'] for u in units for f in u['functions'] if n in [f['symbol']]+f.get('fold_aliases',[])}) for n in (PRIMARY,FALLBACK)}
 unit_targets={n:[{'unit':i,'target':u['symbols'][n]} for i,u in enumerate(units) if n in u.get('symbols',{})] for n in (PRIMARY,FALLBACK)}
 unique=recipe_names(units);imports,thunks=assemble_v3.parse_imports(Pe(paths.REF_IMAGE))
 result={'scope':'same-run attested finite namespace scan; not a weak-linker implementation','capture_sha256':h(a.capture),'run':str(run),'input_hashes':before,'source_index_sha256':h(index),'crt':archives,'v7_matching_lines':v7,'icf':{n:icf.get(n) for n in (PRIMARY,FALLBACK)},'overlay_state':overlay_state,'overlay_exact_names':None if ov is None else {'global':{n:ov['global_name'].get(n) for n in (PRIMARY,FALLBACK)},'unit':[(k,n,v[n]) for k,v in ov['by_unit_name'].items() for n in (PRIMARY,FALLBACK) if n in v],'field':[(k,v) for k,v in ov['by_field'].items() if int(k,16)==0x0104541c]},'placed_matches':hits,'placed_globals':{n:state.gdef.get(n) for n in (PRIMARY,FALLBACK)},'m3_symbols':generated,'directive_scope':'inspected custom V7/phase0/place/libsecs/splice/image paths do not parse .drectve or invoke link.exe; recorded directives are diagnostics, not proof of generic linker behavior','optional_namespaces':optional,'eh_variant_objects':variant_objects,'recipe_function_targets':fn_targets,'recipe_unit_targets':unit_targets,'recipe_unique_targets':{n:unique.get(n) for n in (PRIMARY,FALLBACK)},'exact_import_names':{n:imports.get(n) for n in (PRIMARY,FALLBACK)},'limits':['raw full-member symbol scan proves exact strong-name absence only for enumerated archives; no generic linker search claim','directive token extraction is diagnostic and not a complete generic linker parser; custom resolver paths inspected do not consume directives','capsule does not authorize weak fallback or establish full vtable ownership','caller must hold compiler/build lane across capture; generated outputs are bound by post-terminal capture witness']};(out/'capsule.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'output':str(out),'crt_members':sum(x['members'] for x in archives),'placed_hits':len(hits)}))
if __name__=='__main__':main()
