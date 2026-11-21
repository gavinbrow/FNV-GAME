"""Prepare production-path private mirrors for the unit 370 pointer split."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M/'out/phase2-bfc-370-pointer-split';O=M/'out/phase2-bfc-370-pointer-split-mirror';sys.path.insert(0,str(H));import rtti_mirror_prepare as prep
EXPECTED='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 if sha(current)!=EXPECTED:raise ValueError('recipe changed')
 return json.loads(current)
prep.transition=transition
def main():
 m=json.loads((P/'manifest.json').read_text());candidate=(P/'middlehighprocess.cpp').read_bytes()
 if m['units_sha256']!=EXPECTED or sha(candidate)!=m['candidate_sha256'] or sha((P/'unit-overlay.json').read_bytes())!=m['unit_overlay_sha256']:raise ValueError('proposal changed')
 source='src/fallout/ai/middlehighprocess.cpp';result=prep.prepare(source,{source:candidate},O);result['units_sha256']=EXPECTED;result['reviewed_units_sha256']=EXPECTED;result['proposal_sha256']=sha((P/'manifest.json').read_bytes());result['unit_overlay_sha256']=m['unit_overlay_sha256'];(O/'mirror-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 print(json.dumps({'manifest_sha256':sha((O/'mirror-manifest.json').read_bytes()),'original_files':len(result['original']['files']),'candidate_files':len(result['candidate']['files'])}))
if __name__=='__main__':main()
