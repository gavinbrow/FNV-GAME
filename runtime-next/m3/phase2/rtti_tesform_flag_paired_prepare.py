"""Snapshot both private overlay closures and build a serialized compile plan."""
import hashlib,json,re,shutil
from pathlib import Path
H=Path(__file__).resolve().parent; M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';T=M/'out/phase2-tesform-flag-slots';B=M/'out/phase2-bgsencounterzone-six-override';O=M/'out/phase2-tesform-flag-paired-closure'
def sha(b):return hashlib.sha256(b).hexdigest()
def closure(root,local,source_dir):
 todo=[root];seen={};external=set()
 while todo:
  p=todo.pop().resolve()
  if p in seen:continue
  data=p.read_bytes();seen[p]=sha(data)
  for style,n in re.findall(rb'^\s*#\s*include\s*(["<])([^">\r\n]+)[">]',data,re.M):
   name=n.decode('ascii')
   if style==b'<':external.add(name);continue
   choices=[p.parent/name,local/name,source_dir/name,F/'include'/name]
   found=next((x for x in choices if x.is_file()),None)
   if found is None:raise ValueError('missing quoted include '+name)
   todo.append(found)
 return [{'path':str(p.relative_to(P.resolve())).replace('\\','/'),'sha256':v} for p,v in sorted(seen.items(),key=lambda kv:str(kv[0]))],sorted(external)
def main():
 tm=json.loads((T/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text());units=(F/'build/units.json').read_bytes()
 if sha(units)!='a7470e7f0f8c59ea4b201a1e1f72bb552d3bbd00596db2fdc4911b94b6c18a56':raise ValueError('units changed')
 for name,digest in tm['outputs'].items():
  if sha((T/name).read_bytes())!=digest:raise ValueError('TES overlay changed '+name)
 for name,key in [('bgsencounterzone.cpp','source_overlay_sha256'),('bgsencounterzone_decls.h','header_overlay_sha256')]:
  if sha((B/name).read_bytes())!=bm[key]:raise ValueError('BGSE overlay changed '+name)
 if O.exists():raise FileExistsError('refusing overwrite')
 O.mkdir();(O/'tes').mkdir();(O/'bgs').mkdir()
 for n in ('tesform.cpp','tesform_TESForm.h','tesform_calls.h'):shutil.copyfile(T/n,O/'tes'/n)
 for n in ('bgsencounterzone.cpp','bgsencounterzone_decls.h'):shutil.copyfile(B/n,O/'bgs'/n)
 shutil.copyfile(T/'bgsencounterzone_TESForm.h',O/'bgs/bgsencounterzone_TESForm.h')
 specs=[('tes_original',F/'src/fallout_shared/tesform.cpp',F/'src/fallout_shared'),('tes_overlay',O/'tes/tesform.cpp',F/'src/fallout_shared'),('bgs_original',F/'src/bgsencounterzone.cpp',F/'src'),('bgs_overlay',O/'bgs/bgsencounterzone.cpp',F/'src')]
 rows={}
 for tag,src,srcdir in specs:
  files,system=closure(src,src.parent,srcdir);rows[tag]={'files':files,'system_includes':system,'source_dir':str(srcdir.relative_to(P)).replace('\\','/')}
 meta={'units_sha256':sha(units),'census_sha256':'e7ae33cc2404a8d9628ad2148bcd9292479f5a0964caa2405433f2b6053bf333','tes_manifest_sha256':sha((T/'manifest.json').read_bytes()),'bgs_manifest_sha256':sha((B/'manifest.json').read_bytes()),'closures':rows,'status':'prepared; no compiler run; 128 and 24 functions plus complete observed graph require independent checks'}
 (O/'closure-manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({k:len(v['files']) for k,v in rows.items()}))
if __name__=='__main__':main()
