"""Compile d569-pinned mirrors only after the reviewed two-transition audit."""
import runpy,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import tescontainer_script_mirrors
if __name__=='__main__':runpy.run_path(str(H/'rtti_mirror_compile.py'),run_name='__main__')
