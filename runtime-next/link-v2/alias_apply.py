"""link-v2 alias_apply.py: undefined C_<va> references whose address is a libcmt/libcpmt symbol (opts_extra.txt /ALTERNATENAME:C_<va>=<symbol>) are renamed to that symbol directly in
every linked object (the linker resolved some such aliases to address 0). The /ALTERNATENAME lines stay as a fallback. usage: python -I alias_apply.py"""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import coffrw
alias = {}
for l in open(HERE / 'opts_extra.txt'):
    l = l.strip()
    if l.startswith('/ALTERNATENAME:C_') and not l.split('=', 1)[1].startswith('C_'):
        a, b = l[len('/ALTERNATENAME:'):].split('=', 1); alias[a] = b
n = 0; no = 0
for d in ('obj_rw', 'obj_contrib_rw'):
    for p in (HERE / d).glob('*.obj'):
        b = p.read_bytes(); ren = {nm: alias[nm] for i, nm, v, sec, ty, sc, na, o in coffrw.symbols(b) if sc == 2 and sec == 0 and nm in alias}
        if ren: nb, k = coffrw.rewrite(b, ren); p.write_bytes(nb); n += k; no += 1
print('aliases applied', n, 'objects', no, 'of', len(alias), 'alias names')
