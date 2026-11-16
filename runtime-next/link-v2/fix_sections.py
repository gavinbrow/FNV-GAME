"""link-v2 fix_sections.py: data-v3's MASM segment _TLS becomes the real TLS template section `.tls$AAA` (between the CRT's `.tls` start marker and `.tls$ZZZ` end marker). usage: python -I fix_sections.py"""
import struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import coffrw
for p in (HERE / 'data_out').glob('tls_*.obj'):
    b = bytearray(p.read_bytes())
    for s in coffrw.sections(bytes(b)):
        if s['name'] == '_TLS': b[s['hdr']:s['hdr'] + 8] = '.tls$AAA'.encode().ljust(8, bytes(1)); print('renamed', p.name)
    # section symbols carry the name too
    for i, nm, v, sec, ty, sc, na, o in coffrw.symbols(bytes(b)):
        if nm == '_TLS' and sc == 3: b[o:o + 8] = '.tls$AAA'.encode()
    p.write_bytes(bytes(b))
