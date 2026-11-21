"""Read-only split-tail pointer negative-control artifact audit."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;sys.path[:0]=[str(ROOT/'fnv_decomp/tools'),str(H)]
from compare import Coff
from next_data_artifact_audit import pe_sections
B=M/'out/phase2-native-source-positive';C=M/'out/phase2-native-source-p2wp';OUT=C/'evidence/independent-p2wp-proof.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 states=[]
 for d in (B,C):
  f=d.with_name(d.name+'-freeze');r=load(f/'result.json')
  if r['command_rc'] or not r['input_freeze_passed'] or r['final_digest_changes'] or r['observed_metadata_changes']:raise ValueError('freeze failed')
  states.append(load(f/'inputs-before.json'))
 names=['runtime-next/layout-v2/make_image.py','runtime-next/m3/gen_m3.py','runtime-next/m3/m3secs.py','runtime-next/m3/splice.py','runtime-next/m3/phase2/cost245_records.py','runtime-next/m3/phase2/library_overlay.py','runtime-next/m3/phase2/selection.json','runtime-next/m3/phase2/library_candidates.json','runtime-next/m3/config.py','runtime-next/m3/phase2/run_frozen.py','fnv_decomp/build/units.json'];pins={}
 for n in names:
  p=str((ROOT/n).resolve());a=states[0].get(p);b=states[1].get(p)
  if not a or not b or a['sha256']!=b['sha256']:raise ValueError('freeze input mismatch '+n)
  pins[n]=a['sha256']
 expected=load((B).with_name('phase2-native-source-positive-preflight.json'))
 for row in expected['required']:
  relative=Path(row['path']).resolve().relative_to(ROOT.resolve()).as_posix()
  if pins.get(relative)!=row['sha256']:raise ValueError('preflight required input mismatch '+relative)
 if pins['runtime-next/m3/phase2/selection.json']!='a0a8e8d2c9818f777f6e07ae18b5cc7d55ff94ca0bd6ccd952ff98ab836d9c3a' or pins['runtime-next/m3/phase2/library_candidates.json']!='74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700':raise ValueError('default selection digest mismatch')
 if pins[names[-1]]!='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68':raise ValueError('recipe changed')
 source=[k for k in states[0] if '\\fnv_decomp\\src\\' in k.lower() or '\\fnv_decomp\\include\\' in k.lower()]
 if len(source)!=5497:raise ValueError('unexpected source/include snapshot count')
 if any(k not in states[1] or states[0][k]['sha256']!=states[1][k]['sha256'] for k in source):raise ValueError('source snapshot changed')
 results=[]
 for d in (B,C):
  e=d/'evidence';m=load(e/'m3_gen.log.json');dv=load(e/'dv1_log.json');entry=next(x for x in load(e/'m3_manifest.json')['entries'] if x['va']==0x11a7e40)
  if m['kept']!=8268 or m['dropped'] or dv['library_opt_in']['selected']!=405 or dv['library_opt_in']['bytes']!=16730 or entry['size']!=32:raise ValueError('counts/extent mismatch')
  obj=e/('m3_data.obj' if entry.get('obj',0)==0 else 'm3_data_%d.obj'%entry['obj']);c=Coff(str(obj));s=c.named(entry['sym']);z=c.sections[s['section']]
  rel=sorted((off-s['value'],c.symbols[i]['name'],k) for off,i,k in z['relocs'] if s['value']<=off<s['value']+32)
  if [x[0] for x in rel]!=list(range(0,32,4)) or any(x[2]!=6 for x in rel):raise ValueError('unexpected COFF fields')
  image,base,sections=pe_sections(d/'FalloutNV_selfbuilt.exe');chunks={x['file']:x for x in load(e/'data-v3-manifest.json')};order=['rdata_03','rdata_02','rdata_01','rdata_00'];offs={};pos=0
  for n in order:
   x=chunks[n];pos+=(x['va']-pos)%16;offs[n]=pos;pos+=x['size']
  def translate(va):
   matches=[x for x in chunks.values() if x['va']<=va<x['va']+x['size'] and x['section'] in ('.data','.rdata')]
   if len(matches)!=1:raise ValueError('target chunk ambiguity')
   x=matches[0];return sections[x['section']]['va']+(offs[x['file']] if x['section']=='.rdata' else 0)+va-x['va']
  newva=translate(entry['va']);fileoff=sections['.data']['offset']+newva-sections['.data']['va'];words=struct.unpack_from('<8I',image,fileoff)
  for i,target in enumerate(entry['tgts']):
   if words[i]!=translate(target):raise ValueError('PE target differs at cell '+str(i))
  results.append({'image_sha256':sha(d/'FalloutNV_selfbuilt.exe'),'object_sha256':sha(obj),'relocations':rel,'original_targets':entry['tgts'],'final_words':list(words),'final_va':newva})
 a,b=results
 if a['image_sha256']!='c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f' or a['image_sha256']==b['image_sha256']:raise ValueError('image identity mismatch')
 if a['relocations'][0][1]!='_M3D_01063e58' or b['relocations'][0][1]!='_M3D_011020c4' or a['relocations'][1:]!=b['relocations'][1:] or a['final_words'][1:]!=b['final_words'][1:] or a['final_words'][0]==b['final_words'][0]:raise ValueError('unexpected pointer mutation')
 log=(C/'logs/01-m3-gen.log').read_text(errors='replace');verify=(C/'logs/05-data-v3.log').read_text(errors='replace')
 if 'NEGATIVE CONTROL (p2 tail pointer)' not in log or 'ROUND TRIP FAILED' not in verify or 'DIFFERENT' not in verify:raise ValueError('expected failure evidence absent')
 out={'scope':'archived actual DIR32 and translated PE pointer control','control':'p2wp','freeze_inputs_sha256':pins,'source_files_equal':len(source),'positive':a,'control_image':b,'other_seven_relocations_and_final_words_equal':True,'roundtrip_failure_observed':True,'counts':{'m3':8268,'library':405,'library_bytes':16730}}
 OUT.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'output':str(OUT),'sha256':sha(OUT),'old_final':hex(a['final_words'][0]),'new_final':hex(b['final_words'][0]),'control_image':b['image_sha256']}))
if __name__=='__main__':main()
