"""Prepare one pinned private mirror from the combined or kind-only cohort."""
import argparse, hashlib, json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent; F=M.parent.parent/'fnv_decomp'
P=M/'out/phase2-nimem-combined-825d'; K=M/'out/phase2-nimemobject-coherent-kind'
PIN='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3'
BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    out=a.out.resolve();raw=(F/'build/units.json').read_bytes();mr=(P/'manifest.json').read_bytes()
    if out.exists() or not out.is_relative_to((M/'out').resolve()) or sha(raw)!=BASE or sha(mr)!=PIN: raise ValueError('output or input identity differs')
    m=json.loads(mr);rows=m['combined_api_units']+m['fresh_kind_only_units'];matches=[r for r in rows if r['unit']==a.unit]
    if len(matches)!=1: raise ValueError('unit outside unique scope')
    row=matches[0];u=json.loads(raw)['units'][a.unit]
    if any(row[k]!=u[k] for k in ('source','flags','functions','compiler')) or row['eh_tails']!=u.get('eh_tails',[]): raise ValueError('unit recipe differs')
    ov={}
    if a.unit in {r['unit'] for r in m['fresh_kind_only_units']}:
        km=json.loads((K/'manifest.json').read_bytes())
        if sha((K/'manifest.json').read_bytes())!='5e4610cd17372885861964b9e25238925b5d69f8c0f2287065107fee7ac445d6': raise ValueError('kind payload manifest differs')
        for x in km['files']:
            b=(K/x['generated']).read_bytes()
            if sha(b)!=x['after_sha256']: raise ValueError('kind payload differs')
            ov[x['path']]=b
    else:
        for rel,h in m['source_payload_sha256'].items():
            b=(P/'payload'/rel).read_bytes()
            if sha(b)!=h: raise ValueError('combined payload differs')
            ov[rel]=b
    original=core.walk(F,row['source'],{});candidate=core.walk(F,row['source'],ov)
    if original!=row['original'] or candidate!=row['candidate']: raise ValueError('closure differs')
    out.mkdir(parents=True)
    for tag,g in (('original',original),('candidate',candidate)):
        for rel,digest in g['files'].items():
            b=ov[rel] if tag=='candidate' and rel in ov else (F/rel).read_bytes()
            if sha(b)!=digest: raise ValueError('input changed')
            q=out/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    result={'schema_version':1,'source':row['source'],'unit':a.unit,'units_sha256':BASE,'proposal_manifest_sha256':PIN,'original_inputs':original['files'],'original':original,'candidate':candidate,'production_include_order':['/I<mirror>/include'],'limits':['private experiment; compiler trace and complete code, EH, weak and linkage gates required']}
    (out/'mirror-manifest.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
