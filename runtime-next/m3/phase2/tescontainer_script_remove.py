"""Remove an unused TESContainer static-only shell in two script units."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';PRIOR=M/'out/phase2-tescontainer-script-shell';O=M/'out/phase2-tescontainer-script-removal'
OLD='class TESContainer\n{\n  public:\n    static bool IsValidContainerType(unsigned char type);\n};'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((PRIOR/'manifest.json').read_text());data={k:(F/k).read_bytes() for k in m['inputs']}
 for k,v in data.items():
  if sha(v)!=m['inputs'][k]:raise ValueError('prior source evidence changed '+k)
 if sha((F/'build/units.json').read_bytes())!=m['base_units_sha256']:raise ValueError('recipe changed')
 h=data['src/fallout_shared/tesscript_decls.h'].decode('utf-8-sig').replace('\r\n','\n')
 if h.count(OLD)!=1 or len(re.findall(r'\bTESContainer\b',h))!=1:raise ValueError('header declaration or uses changed')
 header=h.replace(OLD,'',1).encode();units={}
 for index in (1111,1112):
  p=M/('out/phase2-tescontainer-script-%d-mirror/mirror-manifest.json'%index);mirror=json.loads(p.read_text());names=[]
  for rel in mirror['original']['files']:
   data=(F/rel).read_bytes()
   if sha(data)!=mirror['original']['files'][rel]:raise ValueError('include closure changed '+rel)
   if re.search(rb'\bTESContainer\b',data):names.append(rel)
  if names!=['src/fallout_shared/tesscript_decls.h']:raise ValueError('additional include/macro reference in closure '+repr(names))
  units[str(index)]={'mirror_manifest_sha256':sha(p.read_bytes()),'original_project_files':mirror['original']['files'],'unresolved':mirror['original']['unresolved']}
 O.mkdir(exist_ok=False);(O/'tesscript_decls.h').write_bytes(header)
 meta={'base_units_sha256':m['base_units_sha256'],'original_header_sha256':m['inputs']['src/fallout_shared/tesscript_decls.h'],'candidate_header_sha256':sha(header),'original_closures':units,'scope':'remove an unused static-only global shell; no new include or canonical class definition introduced','limits':['quoted system and angle includes are unresolved by source scanner and require compiler trace','preprocessor evaluation, macro expansion and global class identity not proved','all 83 mapped functions, EH, reference fields and actual production labels still require verification'],'status':'private and uncompiled; shared files unchanged'}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'candidate_sha256':sha(header),'units':2,'closure_reference_files':1}))
if __name__=='__main__':main()
