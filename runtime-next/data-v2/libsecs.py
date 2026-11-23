r"""data-v2 libsecs.py: data sections of the CRT/STL library members (libcmt.lib, libcpmt.lib) as pseudo-units for data-v1's place.py.
Pseudo unit id = 100000 + member index (not a units.json index). Same record format as phase0.work()."""
import collections
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation') + r'\runtime-next\pinned-build'))
from pathlib import Path
if __import__('os').environ.get('FNV_M3_NOREF2') == '1':      # batch 10 step C: only the pure archive/object parsers are needed; do not execute the module (it opens the code image)
    import ast, types, os as _os
    _up = Path(_os.environ.get('FNV_PROJ_ROOT', r'C:\path\to\Decompilation')) / 'runtime-next' / 'pinned-build' / 'uncovered_v2.py'
    _ns = {'struct': struct, 'Path': Path}
    for _n in ast.parse(_up.read_text(encoding='utf-8')).body:
        if isinstance(_n, ast.FunctionDef) and _n.name in ('read_ar', 'parse_obj'): exec(compile(ast.Module([_n], []), str(_up), 'exec'), _ns)
    U = types.SimpleNamespace(read_ar=_ns['read_ar'], parse_obj=_ns['parse_obj'])
else:
    import uncovered_v2 as U

LIB = Path((__import__('os').environ.get('FNV_MSVC9_ROOT', r'C:\path\to\Decompilation\FNV\tools\vc2008') + r'\VC\lib'))


def lib_units():
    out = {}; uid = 100000
    use_coff_section_indices = __import__('os').environ.get('FNV_DV1_LIB_COFF_INDEX_V2') == '1'
    for ln in ('libcmt.lib', 'libcpmt.lib'):
        for mname, blob in U.read_ar(LIB / ln):
            r = U.parse_obj(blob)
            uid += 1
            if not r: continue
            secs, syms = r
            defs = collections.defaultdict(list)
            for si, (nm, value, sec, ty, sc) in syms.items():
                if sec > 0 and not nm.startswith('.'): defs[sec - 1].append((nm, value, sc))
            lst = []
            for k, s in enumerate(secs):
                fl = s['flags']
                if fl & 0x20 or not s['name'].startswith(('.rdata', '.data', '.xdata', '.CRT', '.bss', 'CONST')): continue
                isbss = bool(fl & 0x80)
                if not isbss and not s['data']: continue
                rl = []
                if not isbss:
                    for ro, si, ty in s['relocs']:
                        nm, value, sec, sty, sc = syms[si]
                        rec = [ro, ty, nm, sec, value, sc, None, None, None]
                        if ty in (6, 7, 0x0B) and ro + 4 <= len(s['data']): rec[6] = struct.unpack_from('<I', s['data'], ro)[0]
                        rl.append(tuple(rec))
                lst.append(dict(u=uid, k=k + (1 if use_coff_section_indices else 0), name=s['name'], flags=fl, data=(b'' if isbss else bytes(s['data'])), size=len(s['data']) if not isbss else 0,
                                relocs=rl, defs=defs.get(k, []), hints=[]))
            if lst: out[uid] = dict(idx=uid, secs=lst, err=None)
    return out
