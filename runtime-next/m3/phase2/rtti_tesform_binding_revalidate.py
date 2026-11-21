"""Revalidate reviewed TESForm recipe candidate against accepted default-build object."""
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import rtti_tesform_binding_repair as original
EXPECTED='7bc53b00df792a88a80373a9a4c742b2989df06803a2fca20217700cc57f836f'
def main():
 if original.PIN['current_obj']!='f2d60b88ed1be141c462242f5115fe47ab1c71367814c13b21b4e7107011234b':raise ValueError('prior generator pin changed')
 original.PIN=dict(original.PIN,current_obj=EXPECTED);original.OUT=original.M/'out/phase2-tesform-binding-repair-v3';original.main()
if __name__=='__main__':main()
