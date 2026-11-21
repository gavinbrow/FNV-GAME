"""Replay private library ownership against archived placement and actual claims."""
import argparse,hashlib,importlib.util,json,pickle,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent
sys.path[:0]=[str(RN/'data-v1'),str(RN/'data-v2'),str(RN/'data-v3'),str(H),str(M)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);p.add_argument('--chunks',type=Path,required=True);p.add_argument('--symbolic',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);p.add_argument('--libsecs-snapshot',type=Path,required=True);p.add_argument('--common-snapshot',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise FileExistsError(a.out)
 if sha(a.libsecs_snapshot)!=sha(RN/'data-v2/libsecs.py') or sha(a.common_snapshot)!=sha(RN/'data-v3/common.py'):raise ValueError('current replay tools differ from archived tools')
 import place,libsecs
 from common import SEC,orig_reloc_sites,read_ref
 overlay=M/'out/phase2-library-splits/candidate-library_overlay.py'
 if sha(overlay)!='dbdc7d9440ed99f4f64716fc77445df0f7cff21a5472925e875526b1cc9be1f7':raise ValueError('staged library hook changed')
 spec=importlib.util.spec_from_file_location('private_library_replay',overlay);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 e=a.evidence;state=e/'data-v1-scratch/dv1_placed.pkl';summary=load(a.summary)
 if sha(state)!=summary['provenance']['data_v1_scratch_sha256']['dv1_placed.pkl']:raise ValueError('archived placement hash mismatch')
 st=pickle.loads(state.read_bytes());manifest=load(e/'m3_manifest.json')['entries'];pieces=load(e/'dv1_pieces.json')['pieces'];accepted=[x for x in pieces if not x.get('library_opt_in')]
 chunks=[(x['va'],x['va']+x['size'],x['section'],x['file']) for x in load(a.chunks)];symbolic=load(a.symbolic);fields={SEC[r[0]]['va']+r[1] for r in symbolic['fields']}
 selection=e/'library_candidates.json';out,info=mod.select_library(selection,sha(selection),st,[(x['va'],x['size']) for x in manifest],accepted,chunks,fields,set(orig_reloc_sites()),read_ref,libsecs)
 actual={(x['va'],x['size'],x['unit']):x for x in pieces if x.get('library_opt_in')}
 if len(actual)!=len(out) or any((x['va'],x['size'],x['unit']) not in actual or hashlib.sha256(x['data']).hexdigest()!=hashlib.sha256(bytes.fromhex(actual[(x['va'],x['size'],x['unit'])]['data'])).hexdigest() for x in out):raise ValueError('replay differs from archived pieces')
 report={'scope':'read-only staged hook replay against archived placement, M3 and non-library DV1 claims','placement_sha256':sha(state),'selection_sha256':sha(selection),'chunks_sha256':sha(a.chunks),'symbolic_sha256':sha(a.symbolic),'libsecs_sha256':sha(a.libsecs_snapshot),'common_sha256':sha(a.common_snapshot),'hook_sha256':sha(overlay),'result':info,'m3_claims':len(manifest),'nonlibrary_dv1_claims':len(accepted),'matches_archived_library_pieces':True,'limitations':['reads installed compiler libraries only after validating each selected archive/member hash','final-image integration remains separate']}
 a.out.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'selected':len(out),'bytes':sum(x['size'] for x in out),'out':str(a.out)}))
if __name__=='__main__':main()
