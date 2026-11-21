"""Exclusive-lane compiler wrapper for the typed-baseline flag-pair mirrors."""
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import vtable_tesform_two_flagpairs_mirrors
import rtti_mirror_compile as compiler
if __name__=='__main__':compiler.main()
