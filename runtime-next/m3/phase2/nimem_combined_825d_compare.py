"""Run the unchanged ordinary comparator and record unnormalized COFF metadata."""
import argparse, hashlib, json, sys
from pathlib import Path
import nimem_operators_825d_compare as base
import nimem_kind_section_review as kind
P=Path(__file__).resolve().parent.parent/'out/phase2-nimem-combined-825d'
PIN='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--production-object',type=Path,required=True);ap.add_argument('--production-object-sha256',required=True);a=ap.parse_args()
    if sha(P/'manifest.json')!=PIN: raise ValueError('combined proposal changed')
    m=json.loads((a.out/'mirror-manifest.json').read_text())
    if m.get('proposal_manifest_sha256')!=PIN: raise ValueError('mirror proposal mismatch')
    base.P=P
    base.main()
    facts={}
    for tag,path in [('production',a.production_object),('original',a.out/'original.obj'),('candidate',a.out/'candidate.obj')]:
        c=base.Coff(str(path)); rows=[]
        for sec in c.sections[1:]:
            if sec is None: continue
            rows.append({'name':sec['name'],'size':len(sec['data']),'sha256':hashlib.sha256(sec['data']).hexdigest(),'relocations':[(off,kind,c.symbols[j]['name']) for off,j,kind in sec['relocs']]})
        facts[tag]=rows
    dest=a.out/'coff-sections-raw.json'
    if dest.exists(): raise FileExistsError('preserve existing raw section evidence')
    orig=base.Coff(str(a.out/'original.obj'));cand=base.Coff(str(a.out/'candidate.obj'))
    o,c=kind.records(orig),kind.records(cand);oa,ca=kind.aux(orig),kind.aux(cand)
    normalized={'only_original_sections':sum((o-c).values()),'only_candidate_sections':sum((c-o).values()),'nondebug_sections_equal':o==c,'comdat_and_weak_equal':oa==ca,'normalization':'exact NiMemObject TD class/struct spelling only; no API/deleting-wrapper normalization'}
    dest.write_text(json.dumps({'unit':a.unit,'sections':facts,'kind_normalized_pair':normalized,'limits':['raw unnormalized records retained; normalized comparison establishes no ownership or reference acceptance']},indent=2))
if __name__=='__main__':main()
