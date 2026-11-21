"""Read-only dry-run for an existing explicitly named DV1 placement pickle."""
import sys,pickle,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent;sys.path[:0]=[str(R/'data-v1'),str(R/'data-v2'),str(R/'data-v3'),str(H),str(M)];import place,libsecs,library_overlay
from common import SEC,orig_reloc_sites,read_ref
if len(sys.argv)!=2:raise SystemExit('usage: python -I dry_run_library.py <existing-dv1-placed.pkl>')
p=Path(sys.argv[1]);st=pickle.load(open(p,'rb'));a=M/'out/batch8-promoted-default-verified/evidence';m=json.load(open(a/'m3_manifest.json'))['entries'];dv=json.load(open(a/'dv1_pieces.json'))['pieces'];chunks=[(x['va'],x['va']+x['size'],x['section'],x['file']) for x in json.load(open(R/'data-v3/out/manifest.json'))];fields={SEC[r[0]]['va']+r[1] for r in json.load(open(R/'data-v3/symbolic.json'))['fields']};selection=M/'out/phase2-library/selection.json';digest=hashlib.sha256(selection.read_bytes()).hexdigest()
out,info=library_overlay.select_library(selection,digest,st,[(x['va'],x['size']) for x in m],dv,chunks,fields,set(orig_reloc_sites()),read_ref,libsecs);print(json.dumps({'placement_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'result':info},indent=2))
