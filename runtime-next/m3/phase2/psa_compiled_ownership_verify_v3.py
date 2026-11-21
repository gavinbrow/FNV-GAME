"""Read-only verification of compiled M3 and complete selector outputs."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-psa-metadata-ownership-proposal';E=M/'out/phase2-native-source-positive/evidence';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 output=P/'compiled-proof-v3.json'
 if output.exists():raise FileExistsError(output)
 fixture=json.loads((P/'compiled-m3-v3/fixture-result.json').read_bytes());old=json.loads((E/'m3_manifest.json').read_bytes())['entries'];new=json.loads((P/'compiled-m3-v3/m3_manifest.json').read_bytes())['entries'];before=json.loads((E/'dv1_pieces.json').read_bytes())['pieces'];after=json.loads((P/'compiled-selector-replay-v3/dv1_pieces.json').read_bytes())['pieces'];natives=[(0x110fbe8,20),(0x110fbfc,16),(0x110fc0c,13),(0x110fc1c,28),(0x1196e20,26)];keys=lambda l:{(z['va'],z['size'],z['unit'],z['kind']) for z in l};expected={(a,n,620,k) for (a,n),k in zip(natives,['rtti4','rtti3','rtti2','rtti1','rtti0'])}
 if keys(after)-keys(before)!=expected or keys(before)-keys(after):raise ValueError('selector ownership changed')
 actual=[z for z in after if (z['va'],z['size']) in natives];original={z['va']+f[0] for z in old if z['va'] in (0x110fbe8,0x1196e1e) for f in z.get('fields',[])};native={z['va']+f[0] for z in actual for f in z['relocs']};resid={z['va']+f[0] for z in new if z['va'] in (0x110fc19,0x1196e1e,0x1196e3a) for f in z.get('fields',[])}
 if len(original)!=61 or len(native)!=9 or len(resid)!=52 or native&resid or native|resid!=original:raise ValueError('relocation partition mismatch')
 if any(z['unit']!=620 or z['nunits']!=1 for z in actual):raise ValueError('native producer identity')
 log=json.loads((P/'compiled-selector-replay-v3/dv1_log.json').read_bytes())
 if log['library_opt_in']['selected']!=405 or log['library_opt_in']['bytes']!=16730:raise ValueError('library mismatch')
 result={'scope':'private compiled M3+archived placement selector fixture','fixture_sha256':h(P/'compiled-m3-v3/fixture-result.json'),'pieces_sha256':h(P/'compiled-selector-replay-v3/dv1_pieces.json'),'old_relocation_sites':61,'native_relocation_sites':9,'residual_relocation_sites':52,'native_sections':5,'unit620_singletons':True,'prior_pieces_removed':0,'limitations':['no fresh phase0, final image or runtime','E weak vtable remains excluded']};output.write_text(json.dumps(result,indent=2)+'\n');print('PASS 61 sites, 5 native sections')
if __name__=='__main__':main()
