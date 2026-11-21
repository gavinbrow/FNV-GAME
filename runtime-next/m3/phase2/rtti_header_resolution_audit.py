"""Compare the quoted include candidates for a private and installed header location."""
import argparse,hashlib,json,re
from pathlib import Path

def resolve(header,include,include_dirs):
 for p in [header.parent/include]+[d/include for d in include_dirs]:
  if p.is_file():return p.resolve()
 return None

def main():
 p=argparse.ArgumentParser();p.add_argument('--private-header',required=True,type=Path);p.add_argument('--installed-header',required=True,type=Path);p.add_argument('--private-include',action='append',default=[],type=Path);p.add_argument('--installed-include',action='append',default=[],type=Path);p.add_argument('--require-match',action='store_true');a=p.parse_args()
 private=a.private_header.read_bytes();installed=a.installed_header.read_bytes()
 if private!=installed:raise ValueError('header bytes differ; not a location-only comparison')
 items=[]
 for name in re.findall(rb'^\s*#\s*include\s*"([^"\r\n]+)"',private,re.M):
  n=name.decode('ascii');x=resolve(a.private_header,n,a.private_include);y=resolve(a.installed_header,n,a.installed_include)
  items.append({'include':n,'private':str(x) if x else None,'installed':str(y) if y else None,'same_path':x is not None and x==y,'private_sha256':hashlib.sha256(x.read_bytes()).hexdigest() if x else None,'installed_sha256':hashlib.sha256(y.read_bytes()).hexdigest() if y else None})
 print(json.dumps({'header_sha256':hashlib.sha256(private).hexdigest(),'quoted_includes':items,'same_resolution':all(r['same_path'] for r in items),'scope':'lexical first-level quoted include lookup; guards, preprocessor and toolchain system paths not evaluated'},indent=2))
 if a.require_match and any(not r['same_path'] for r in items):raise SystemExit(1)
if __name__=='__main__':main()
