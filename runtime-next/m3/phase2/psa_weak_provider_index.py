"""Finite, immutable COFF E/G provider index for an explicitly archived cohort."""
import argparse,hashlib,json,re,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Coff
NAMES={f'??_{kind}{cls}@@UAEPAXI@Z' for kind in 'EG' for cls in ('TESModelPSA','BGSBodyPartData')}|{'??1TESModelPSA@@UAE@XZ','??1BGSBodyPartData@@UAE@XZ'}
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if sys.flags.optimize:raise ValueError('optimized Python disables validation assumptions')
 ap=argparse.ArgumentParser();ap.add_argument('--objects',type=Path,required=True);ap.add_argument('--compile-log',type=Path,required=True);ap.add_argument('--recipe',type=Path,required=True);ap.add_argument('--freeze-before',type=Path,required=True);ap.add_argument('--freeze-result',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 meta=[a.compile_log,a.recipe,a.freeze_before,a.freeze_result];first={str(p.resolve()):h(p) for p in meta};freeze=json.loads(a.freeze_result.read_bytes())
 if freeze['command_rc']!=0 or not freeze['input_freeze_passed'] or freeze['final_digest_changes'] or freeze['observed_metadata_changes']:raise ValueError('freeze failed')
 snapshot=json.loads(a.freeze_before.read_bytes());matches=[v for k,v in snapshot.items() if k.lower().replace('\\','/').endswith('/fnv_decomp/build/units.json')]
 if len(matches)!=1 or matches[0].get('sha256')!=h(a.recipe):raise ValueError('frozen recipe mismatch')
 units=json.loads(a.recipe.read_bytes())['units'];logs=[json.loads(x) for x in a.compile_log.read_text().splitlines() if x.strip()];idx={}
 for z in logs:
  i=z['index']
  if i in idx or not 0<=i<len(units) or z['status']!='ok' or z['rc']!=0 or z['source']!=units[i]['source'] or z['compiler']!=units[i]['compiler']:raise ValueError('compile list mismatch')
  idx[i]=z
 if set(idx)!=set(range(len(units))):raise ValueError('incomplete compile cohort')
 paths=[a.objects/('%04d.obj'%i) for i in range(len(units))];before=[h(p) for p in paths];rows=[];directives=[]
 for i,p in enumerate(paths):
  c=Coff(str(p));ptr,count=struct.unpack_from('<II',c.data,8)
  for sec in c.sections:
   if sec and sec['name']=='.drectve':
    data=sec['data'];named=any(n.encode() in data for n in NAMES);tokens=[x.decode('ascii','replace') for x in re.findall(rb'(?i)/(?:DEFAULTLIB|ALTERNATENAME):[^\s]+',data)]
    if named or tokens:directives.append({'unit':i,'sha256':hashlib.sha256(data).hexdigest(),'target_name_present':named,'provider_directives':tokens})
  if ptr<20 or ptr+18*count>len(c.data):raise ValueError('truncated symbol table')
  for n,s in c.symbols.items():
   if s['name'] not in NAMES:continue
   row={'unit':i,'object_sha256':before[i],'index':n,'name':s['name'],'section':s['section'],'storage':s['storage'],'type':s['type'],'value':s['value']}
   if s['storage']==105:
    raw=struct.unpack_from('<8sIhHBB',c.data,ptr+18*n)
    if raw[5]!=1 or n+1>=count:raise ValueError('weak aux count')
    aux=c.data[ptr+18*(n+1):ptr+18*(n+2)];tag,characteristic=struct.unpack_from('<II',aux)
    if any(aux[8:]) or tag not in c.symbols:raise ValueError('weak aux malformed')
    row.update(aux_fallback=c.symbols[tag]['name'],aux_characteristic=characteristic)
   rows.append(row)
 after=[h(p) for p in paths]
 if before!=after or any(h(Path(k))!=v for k,v in first.items()):raise ValueError('inputs changed while scanning')
 out.write_text(json.dumps({'scope':'archived recipe compile cohort only; not CRT, V7, M3 or placed namespace','inputs':first,'recipe_count':len(units),'compile_rows':len(logs),'object_hashes':[{'unit':i,'sha256':v,'recipe_flags':units[i]['flags']} for i,v in enumerate(before)],'symbols':rows,'targeted_directives':directives,'limitations':['caller must establish object directory and logs are from same frozen run; compile log does not independently record per-unit flags','no CRT archive member/index search, V7/ICF/overlays, imports or generated pseudo-units covered','strong E absence in this cohort alone does not authorize weak fallback','global ODR and target physical table placement remain separate']},indent=2)+'\n');print(json.dumps({'objects':len(paths),'matching_symbols':len(rows),'output':str(out)}))
if __name__=='__main__':main()
