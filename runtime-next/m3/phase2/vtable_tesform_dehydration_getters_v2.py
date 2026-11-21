"""Extend dehydration getters candidate to its actual unit-local TESForm view."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';A=M/'out/phase2-tesform-dehydration-getters';O=M/'out/phase2-tesform-dehydration-getters-v2'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((A/'manifest.json').read_bytes());files={n:(A/n).read_bytes() for n in m['outputs']}
 if any(sha(files[n])!=v for n,v in m['outputs'].items()):raise ValueError('prior candidate changed')
 p=F/'src/fallout_shared/TESForm.h';raw=p.read_bytes()
 if sha(raw)!='64686709136dcc39175a9e5b731b4001c5f491e2e66a37ac9b19daf34d0e1142':raise ValueError('unit-local header changed')
 text=raw.decode().replace('\r\n','\n');old='virtual bool Unk_2D(void);';new='virtual bool Unk_2D(void) const;'
 if text.count(old)!=1:raise ValueError('local view anchor mismatch')
 files['src__fallout_shared__TESForm.h']=text.replace(old,new,1).encode();O.mkdir(parents=False,exist_ok=False)
 for n,b in files.items():(O/n).write_bytes(b)
 m['input_sha256']['src/fallout_shared/TESForm.h']=sha(raw);m['outputs']={n:sha(b) for n,b in files.items()};m['scope']='private getter hypothesis including actual unit633 local TESForm declaration';m['limitations']+=['unit633 resolves src/fallout_shared/TESForm.h; this extra local view expands affected cohort']
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m['outputs']))
if __name__=='__main__':main()
