"""Read-only positive versus library value negative-control artifact audit."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(H)]
from compare import Coff
from next_data_artifact_audit import pe_sections
BASE=M/'out/phase2-next-data-positive-v3';CTRL=M/'out/phase2-next-data-p2lv';OUT=CTRL/'evidence/independent-p2lv-proof.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 frozen=[]
 for folder in (BASE,CTRL):
  f=folder.with_name(folder.name+'-freeze');result=load(f/'result.json')
  if result['command_rc'] or not result['input_freeze_passed'] or result['final_digest_changes'] or result['observed_metadata_changes']:raise ValueError('freeze failed')
  frozen.append(load(f/'inputs-before.json'))
 names=['runtime-next/layout-v2/make_image.py','runtime-next/m3/gen_m3.py','runtime-next/m3/m3secs.py','runtime-next/m3/splice.py','runtime-next/m3/phase2/cost245_records.py','runtime-next/m3/phase2/library_overlay.py','runtime-next/m3/out/phase2-next-data-transaction6757/selection.json','runtime-next/m3/out/phase2-next-data-transaction6757/library_candidates.json','fnv_decomp/build/units.json']
 watched={}
 for name in names:
  path=str((ROOT/name).resolve());a=frozen[0].get(path);b=frozen[1].get(path)
  if not a or not b or a['sha256']!=b['sha256']:raise ValueError('frozen input mismatch '+name)
  watched[name]=a['sha256']
 if watched[names[-1]]!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('recipe changed')
 sourcepaths=[k for k in frozen[0] if '\\fnv_decomp\\src\\' in k.lower() or '\\fnv_decomp\\include\\' in k.lower()]
 if any(k not in frozen[1] or frozen[0][k]['sha256']!=frozen[1][k]['sha256'] for k in sourcepaths):raise ValueError('source snapshot differs')
 results=[]
 for folder in (BASE,CTRL):
  e=folder/'evidence';m=load(e/'m3_gen.log.json');dv=load(e/'dv1_log.json');pieces=load(e/'dv1_pieces.json')['pieces'];p=next(x for x in pieces if x['va']==0x101ffbc)
  if m['kept']!=8268 or m['dropped'] or dv['library_opt_in']['selected']!=405 or dv['library_opt_in']['bytes']!=16730 or p['data']!='2a00' or p['relocs'] or p['library_opt_in'] is not True:raise ValueError('selection/piece mismatch')
  image,base,sections=pe_sections(folder/'FalloutNV_selfbuilt.exe');chunks={x['file']:x for x in load(e/'data-v3-manifest.json')};pos=0;offsets={}
  for n in ('rdata_03','rdata_02','rdata_01','rdata_00'):
   x=chunks[n];pos+=(x['va']-pos)%16;offsets[n]=pos;pos+=x['size']
  chunk=chunks[p['chunk']];va=sections['.rdata']['va']+offsets[p['chunk']]+p['va']-chunk['va'];off=sections['.rdata']['offset']+va-sections['.rdata']['va']
  results.append({'image_sha256':sha(folder/'FalloutNV_selfbuilt.exe'),'piece_sha256':sha(e/'dv1_pieces.json'),'source_va':hex(p['va']),'final_va':hex(va),'pe_bytes':image[off:off+2].hex(),'archived_piece_bytes':p['data']})
 a,b=results
 if a['image_sha256']!='c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f' or a['image_sha256']==b['image_sha256'] or a['pe_bytes']!='2a00' or b['pe_bytes']!='2b00':raise ValueError('PE control mismatch')
 verify=(CTRL/'logs/05-data-v3.log').read_text(errors='replace')
 if 'NEGATIVE CONTROL (p2 library value): VA 0101ffbc offset 0 changed from 2a to 2b' not in verify or 'ROUND TRIP FAILED' not in verify or 'rdata_00 .rdata bytes 635344 DIFFERENT' not in verify:raise ValueError('expected diagnostics missing')
 obj=CTRL/'evidence/rdata_00.obj';c=Coff(str(obj));sec=next(x for x in c.sections if x and x['name']=='.rdata');objoff=0x101ffbc-16642048
 out={'scope':'archived DV1 input, control log and actual final PE; splice mutation is in-memory','control':'p2lv','freeze_inputs_sha256':watched,'source_files_equal':len(sourcepaths),'positive':a,'control_image':b,'captured_rdata_object_sha256':sha(obj),'captured_rdata_object_placeholder':sec['data'][objoff:objoff+2].hex(),'counts':{'m3':8268,'library':405,'library_bytes':16730},'roundtrip_failure_observed':True,'archived_dv1_input_unchanged':True}
 OUT.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'output':str(OUT),'sha256':sha(OUT),'positive':a,'control':b}))
if __name__=='__main__':main()
