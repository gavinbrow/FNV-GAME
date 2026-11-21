"""Read-only split overlay dry-run against one explicitly named placement snapshot."""
import sys,pickle,json,hashlib,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;D=M/'out/phase2-library-splits';sys.path[:0]=[str(R/'data-v1'),str(R/'data-v2'),str(R/'data-v3'),str(H),str(M)];import place,libsecs
from common import SEC,orig_reloc_sites,read_ref
sp=importlib.util.spec_from_file_location('staged_library_splits',D/'candidate-library_overlay.py');mod=importlib.util.module_from_spec(sp);sys.modules[sp.name]=mod;sp.loader.exec_module(mod)
if len(sys.argv) not in (2,3):raise SystemExit('usage: python -I dry_run_library_splits.py <existing-dv1-placed.pkl> [selection.json]')
p=Path(sys.argv[1]);raw=p.read_bytes();st=pickle.loads(raw);a=M/'out/batch8-promoted-default-verified/evidence';m=json.load(open(a/'m3_manifest.json'))['entries'];dv=json.load(open(a/'dv1_pieces.json'))['pieces'];chunks=[(x['va'],x['va']+x['size'],x['section'],x['file']) for x in json.load(open(R/'data-v3/out/manifest.json'))];fields={SEC[r[0]]['va']+r[1] for r in json.load(open(R/'data-v3/symbolic.json'))['fields']};sel=Path(sys.argv[2]) if len(sys.argv)==3 else D/'selection.json';digest=hashlib.sha256(sel.read_bytes()).hexdigest();out,info=mod.select_library(sel,digest,st,[(x['va'],x['size']) for x in m],dv,chunks,fields,set(orig_reloc_sites()),read_ref,libsecs);print(json.dumps({'placement_sha256':hashlib.sha256(raw).hexdigest(),'result':info},indent=2))
