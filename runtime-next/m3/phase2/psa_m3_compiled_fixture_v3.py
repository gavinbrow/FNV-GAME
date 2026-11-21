"""Private M3 selector fixture; --validate-only never creates output or locks."""
import argparse,builtins,hashlib,json,os,sys,time,struct
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;P=M/'out/phase2-psa-metadata-ownership-proposal';E=M/'out/phase2-native-source-positive/evidence';PIN=P/'compiled-fixture-v3-pins.json';DEST=P/'compiled-m3-v3';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validate():
 if any(k.upper() in ('CL','_CL_') or k.upper().startswith(('FNV_','DV_','CODEX_NEGATIVE')) for k in os.environ):raise ValueError('inherited build environment forbidden')
 data=json.loads(PIN.read_bytes())
 for name,digest in data['files'].items():
  p=Path(name)
  if not p.is_file() or h(p)!=digest:raise ValueError('input changed '+name)
 if h(Path(data['reference_path']))!=data['reference_expected']:raise ValueError('reference changed')
 if DEST.exists():raise FileExistsError(DEST)
 return data
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--validate-only',action='store_true');a=ap.parse_args();validate()
 if a.validate_only:print('PASS preflight; no outputs or compiler');return
 sys.path.insert(0,str(M.parent));import buildlock
 # O_EXCL uses the same global lock as build_all and does not break stale locks.
 fd=os.open(buildlock.LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY);owner=False
 try:
  owner=True;os.write(fd,('%d %f psa-m3-fixture'%(os.getpid(),time.time())).encode());os.close(fd);fd=None;validate()
  DEST.mkdir();sys.path.insert(0,str(M));import splice
  splice.GEN=str(DEST.resolve());splice.MANIFEST=str((DEST/'m3_manifest.json').resolve());splice.OBJ=str((DEST/'m3_data.obj').resolve())
  os.environ['FNV_M3_SEL']=str((P/'selection.v3.json').resolve())
  redirects={str((M.parent/'data-v3/symbolic.json').resolve()).casefold():E/'data-v3-symbolic.json',str((M.parent/'data-v3/out/manifest.json').resolve()).casefold():E/'data-v3-manifest.json'};original_open=builtins.open
  def redirected(file,*args,**kwargs):
   if isinstance(file,(str,os.PathLike)):
    dest=redirects.get(str(Path(file).resolve()).casefold())
    if dest is not None:
     mode=args[0] if args else kwargs.get('mode','r')
     if any(c in mode for c in 'wax+'):raise ValueError('redirect write denied')
     file=dest
   return original_open(file,*args,**kwargs)
  builtins.open=redirected
  try:
   import gen_m3 as G
   if G.GEN!=str(DEST.resolve()) or G.ANYNEG:raise ValueError('unsafe generator context')
   sys.argv=[str(H/'psa_m3_compiled_fixture_v3.py')];G.main()
  finally:builtins.open=original_open
  log=json.loads((DEST/'m3_gen.log.json').read_bytes());manifest=json.loads((DEST/'m3_manifest.json').read_bytes())['entries'];expected={0x110fc19:3,0x1196e1e:2,0x1196e3a:1494};found={x['va']:x for x in manifest if x['va'] in expected}
  if log['dropped'] or set(found)!=set(expected) or any(found[k]['size']!=v for k,v in expected.items()):raise ValueError('residual selection mismatch')
  zero=found[0x1196e1e];zc=splice.Coff(splice.objpath(splice.OBJ,zero.get('obj',0)));zs=zc.named(zero['sym']);zsec=zc.sections[zs['section']];hdr=20+struct.unpack_from('<H',zc.data,16)[0]+40*(zs['section']-1);rawptr=struct.unpack_from('<I',zc.data,hdr+20)[0]
  if zsec['name']!='.data' or not (zsec['flags']&0x80000000) or rawptr==0:raise ValueError('zero prefix not writable file-backed data')
  entry=next(x for x in manifest if x['va']==0x1045408);c=splice.Coff(splice.objpath(splice.OBJ,entry.get('obj',0)));s=c.named(entry['sym']);z=c.sections[s['section']];rr=[c.symbols[i] for off,i,k in z['relocs'] if s['value']<=off<s['value']+entry['size'] and k==6]
  if len(rr)!=1 or rr[0]['name']!='_M3D_0110fbe8' or rr[0]['section']!=0 or splice.resolve(rr[0]['name'])!=0x110fbe8:raise ValueError('tag mismatch')
  result={'pins_sha256':h(PIN),'files':{x.name:h(x) for x in DEST.iterdir() if x.is_file()},'retained_tag':'_M3D_0110fbe8','tag_undefined':True,'limits':['no final image; full private selector uses compiled skip','fresh production placement and whole-program ownership unproved']};(DEST/'fixture-result.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS compiled M3 fixture')
 finally:
  if fd is not None:os.close(fd)
  if owner:
   try:os.unlink(buildlock.LOCK)
   except FileNotFoundError:pass
if __name__=='__main__':main()
