"""Use reviewed fa366 recipe transition with existing exclusive mirror compiler."""
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import vtable_tesform_savegame_mirrors as scope
import rtti_mirror_compile as driver
if __name__=='__main__':driver.main()
