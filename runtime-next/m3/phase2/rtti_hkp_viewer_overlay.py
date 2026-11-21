"""Create one private, collision-checked source overlay; never edit fnv_decomp."""
import hashlib,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
M3=HERE.parent
PROJECT=M3.parent.parent
SOURCE_REL='src/havok/physics/utilities/visualdebugger/viewer/dynamics/hkpconstraintviewer.cpp'
SOURCE_SHA='56f8a3086fece5c976a9f274dbb7183d8e1de7df74240b0c9d1be70b79695030'
UNITS_SHA='ae4182c8062cf566210935d284b6663a83ab63e077b41d8e147fa66cb7aca70e'
OLD='FUN_00d698b0'
NEW='hkpConstraintViewer'
FLAGS=['/MT','/O2','/GS','/EHsc','/Gy']


def sha(b): return hashlib.sha256(b).hexdigest()


def rename_source(data):
    old=OLD.encode('ascii'); new=NEW.encode('ascii')
    if re.search(rb'\b'+re.escape(new)+rb'\b',data): raise ValueError('original class name already exists in source')
    if not re.search(rb'\bclass\s+'+re.escape(old)+rb'\s*:',data): raise ValueError('expected global class declaration absent')
    patched,n=re.subn(rb'\b'+re.escape(old)+rb'\b',new,data)
    if n!=4: raise ValueError('unexpected source token count: %d'%n)
    return patched


def scan_name(name):
    command=['rg','-l','-w','-F',name,str(PROJECT/'fnv_decomp/src'),str(PROJECT/'fnv_decomp/include'),'-g','*.cpp','-g','*.h','-g','*.hpp','-g','*.inl']
    p=subprocess.run(command,capture_output=True,text=True,errors='replace')
    if p.returncode not in (0,1): raise RuntimeError('source collision scan failed: '+p.stderr)
    return sorted(Path(x).resolve() for x in p.stdout.splitlines())


def main():
    fn=PROJECT/'fnv_decomp';source=fn/SOURCE_REL;units_path=fn/'build/units.json';data=source.read_bytes();ub=units_path.read_bytes()
    if sha(data)!=SOURCE_SHA or sha(ub)!=UNITS_SHA: raise ValueError('source or unit recipe has changed')
    if scan_name(NEW): raise ValueError('original name occurs elsewhere: reject collision')
    if scan_name(OLD)!=[source.resolve()]: raise ValueError('synthetic identity has other source references')
    includes=re.findall(rb'^\s*#\s*include\s*([^\r\n]+)',data,re.M)
    if includes!=[b'<windows.h>']: raise ValueError('unexpected include closure')
    units=json.loads(ub)['units']; hits=[(i,u) for i,u in enumerate(units) if u.get('source')==SOURCE_REL]
    if len(hits)!=1: raise ValueError('ambiguous unit recipe')
    i,u=hits[0]
    if i!=2501 or u.get('compiler')!='sp1' or u.get('flags')!=FLAGS: raise ValueError('unexpected compiler recipe')
    patched=rename_source(data)
    out=M3/'out/phase2-hkp-constraint-viewer'
    out.mkdir(parents=False,exist_ok=False)
    dest=out/'hkpconstraintviewer.cpp'
    with dest.open('xb') as f:f.write(patched)
    meta={'schema_version':1,'scope':'isolated source-name experiment; no class-layout or vtable equivalence implied',
          'source':SOURCE_REL,'source_sha256':SOURCE_SHA,'units_sha256':UNITS_SHA,'unit_index':i,
          'compiler':'sp1','flags':FLAGS,'old_name':OLD,'new_name':NEW,'replaced_tokens':4,
          'overlay_sha256':sha(patched),'reference_type_descriptor_va':'0x011b616c',
          'reference_name_prefix_bytes':34,'current_w_owner':'M3_011b616c','current_w_owner_bytes':40,
          'status':'uncompiled; partial name experiment; base classes and virtual slots unresolved',
          'warning':'do not install into protected sources or frozen selection; no recovered-byte claim'}
    with (out/'manifest.json').open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
    print(json.dumps({'directory':str(out),'overlay_sha256':meta['overlay_sha256'],'unit_index':i,'status':meta['status']}))


if __name__=='__main__':main()
