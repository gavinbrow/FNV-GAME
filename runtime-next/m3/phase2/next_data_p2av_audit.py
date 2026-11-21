"""Read-only positive versus array negative-control artifact audit."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(H)]
from compare import Coff
from next_data_artifact_audit import pe_sections
BASE=M/'out/phase2-next-data-positive-v3';CTRL=M/'out/phase2-next-data-p2av';OUT=CTRL/'evidence/independent-p2av-proof.json'
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
 info=[];outcomes=[]
 for folder in (BASE,CTRL):
  e=folder/'evidence';log=load(e/'m3_gen.log.json');dv=load(e/'dv1_log.json');manifest=load(e/'m3_manifest.json')['entries'];entry=next(x for x in manifest if x['va']==0x11a7440)
  if log['kept']!=8268 or log['dropped'] or dv['library_opt_in']['selected']!=405 or dv['library_opt_in']['bytes']!=16730:raise ValueError('selection counts mismatch')
  obj=e/('m3_data.obj' if entry.get('obj',0)==0 else 'm3_data_%d.obj'%entry['obj']);coff=Coff(str(obj));sym=coff.named(entry['sym']);sec=coff.sections[sym['section']];data=sec['data'][sym['value']:sym['value']+entry['size']]
  image,base,sections=pe_sections(folder/'FalloutNV_selfbuilt.exe');chunk=next(x for x in load(e/'data-v3-manifest.json') if x['file']=='data_00');va=sections['.data']['va']+entry['va']-chunk['va'];off=sections['.data']['offset']+va-sections['.data']['va'];pe_data=image[off:off+entry['size']]
  if len(data)!=256 or len(pe_data)!=256 or data!=pe_data:raise ValueError('object/image array mismatch')
  outcomes.append((data,pe_data));info.append({'object_sha256':sha(obj),'exe_sha256':sha(folder/'FalloutNV_selfbuilt.exe'),'symbol':entry['sym'],'source_va':hex(entry['va']),'final_va':hex(va),'size':entry['size']})
 if outcomes[0][0][0]!=0 or outcomes[1][0][0]!=1 or outcomes[0][0][1:]!=outcomes[1][0][1:]:raise ValueError('array mutation is not exactly one byte')
 if info[0]['exe_sha256']==info[1]['exe_sha256'] or info[0]['exe_sha256']!='c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f':raise ValueError('image hash gate')
 gen=(CTRL/'logs/01-m3-gen.log').read_text(errors='replace');verify=(CTRL/'logs/05-data-v3.log').read_text(errors='replace')
 if 'NEGATIVE CONTROL (p2 array value)' not in gen or 'ROUND TRIP FAILED' not in verify or 'data_00 .data bytes 262656 DIFFERENT' not in verify:raise ValueError('expected diagnostic missing')
 out={'scope':'archived actual COFF and PE control evidence','control':'p2av','freeze_inputs_sha256':watched,'source_files_equal':len(sourcepaths),'positive':info[0],'control_image':info[1],
      'object_and_pe_mutation':{'offset':0,'old':0,'new':1,'other_255_bytes_equal':True},'counts':{'m3':8268,'library':405,'library_bytes':16730},'roundtrip_failure_observed':True}
 OUT.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'output':str(OUT),'sha256':sha(OUT),'positive':info[0]['exe_sha256'],'control':info[1]['exe_sha256']}))
if __name__=='__main__':main()
