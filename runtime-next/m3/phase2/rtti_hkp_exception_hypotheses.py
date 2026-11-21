"""Prepare source-corroborated, strictly experimental EH declaration variants."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';BASE=M/'out/phase2-hkp-destructor-v2';OUT=M/'out/phase2-hkp-exception-hypotheses'
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 source=(BASE/'hkpconstraintviewer.cpp').read_bytes();manifest=json.loads((BASE/'manifest.json').read_text());
 if sha(source)!=manifest['new_overlay_sha256']:raise ValueError('pinned source mismatch')
 evidence=[('base',F/'src/havok/physics/utilities/visualdebugger/viewer/dynamics/hkpphantomdisplayviewer.cpp',b'FUN_00ddccb0(const void* contexts) throw();'),('listener',F/'src/havok/physics/utilities/visualdebugger/viewer/dynamics/hkpsimulationislandviewer.cpp',b'void FUN_00c93920(hkListenerD64A* pkListener) throw();')]
 for label,p,anchor in evidence:
  if p.read_bytes().count(anchor)!=1:raise ValueError('missing evidence '+label)
 replacements={'base':(b'hkpWorldViewerBase(void* info);',b'hkpWorldViewerBase(void* info) throw();'),'listener':(b'void addListener(hkpWorldPostSimulationListener* listener);',b'void addListener(hkpWorldPostSimulationListener* listener) throw();')}
 OUT.mkdir(exist_ok=False);variants={}
 for name,labels in [('base_only',['base']),('listener_only',['listener']),('both',['base','listener'])]:
  s=source
  for label in labels:
   a,b=replacements[label]
   if s.count(a)!=1:raise ValueError('ambiguous '+label)
   s=s.replace(a,b,1)
  (OUT/(name+'.cpp')).write_bytes(s);variants[name]={'sha256':sha(s),'hypotheses':labels}
 meta={'original_overlay_sha256':sha(source),'evidence':[{'kind':label,'source':p.relative_to(F).as_posix(),'sha256':sha(p.read_bytes())} for label,p,_ in evidence],'variants':variants,'scope':'source-backed surrogate exception specifications only; semantic nothrow contract is not established','status':'uncompiled; compare all 16 mapped functions and constructor EH/relocations, original hierarchy and slots; do not install'}
 (OUT/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(variants))
if __name__=='__main__':main()

