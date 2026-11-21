"""Write reviewed in-memory unit symbol translations as private comparison input."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;OUT=M/'out/phase2-hkp-hierarchy-v1';sys.path.insert(0,str(H));import rtti_hkp_hierarchy_compare as c


def main():
 manifest=json.loads((OUT/'manifest.json').read_text());units=PROJECT/'fnv_decomp/build/units.json';raw=units.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=manifest['units_sha256']:raise ValueError('unit recipe changed')
 unit=json.loads(raw)['units'][2501];result=copy.deepcopy(unit);mapped={}
 for name,value in unit['symbols'].items():
  new=c.translated(name)
  if new in mapped and mapped[new]!=value:raise ValueError('translated symbol collision')
  mapped[new]=value
 result['symbols']=mapped
 result['functions']=[dict(f,symbol=c.translated(f['symbol']),fold_aliases=[c.translated(s) for s in f.get('fold_aliases',[])]) for f in unit['functions']]
 target=OUT/'unit-overlay.json'
 with target.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
 print(json.dumps({'unit_index':2501,'functions':len(result['functions']),'symbols':len(mapped),'unit_overlay_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
