"""rebuild .rsrc: extract_res (build-time binaries) -> rc_lite (.rc -> .res) -> cvtres.exe -> link_rsrc (section image)."""
import subprocess, os, sys
here = os.path.dirname(os.path.abspath(__file__))
CVTRES = (__import__('os').environ.get('FNV_MSVC9_ROOT', r'C:\Projects\Decompilation\FNV\tools\vc2008') + r'\VC\bin\cvtres.exe')
def build(rva):
    import extract_res  # noqa (runs extraction on import)
    import rc_lite, link_rsrc
    b = os.path.join(here, 'build')
    open(os.path.join(b, 'resources.res'), 'wb').write(rc_lite.compile_rc(os.path.join(here, 'res-src', 'resources.rc')))
    subprocess.run([CVTRES, '/MACHINE:X86', '/NOLOGO', '/OUT:' + os.path.join(b, 'resources.obj'), os.path.join(b, 'resources.res')], check=True)
    return link_rsrc.layout(os.path.join(b, 'resources.obj'), rva)
if __name__ == '__main__':
    import pefile
    img = build(0xe74000); ref = pefile.PE(sys.argv[1]).get_data(0xe74000, len(img))
    print(len(img), 'rsrc identical to reference:', img == ref)
