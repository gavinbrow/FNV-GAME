"""Reverse sized-delete fix: give the class a 1-arg operator delete next to its sized one."""
import re, sys
from pathlib import Path
FN = Path(r'C:\Projects\Decompilation\fnv_decomp')
T = [('src/fallout/interface/interface.cpp', 3739), ('src/fallout_shared/distant terrain system/bgsdistantobjectblock.cpp', 1534),
     ('src/fallout_shared/distant terrain system/bgsdistantobjectblock.cpp', 1756), ('src/fallout_shared/extradatalist.cpp', 18733),
     ('src/fallout_shared/pathfinding/navmesh_util.cpp', 2448), ('src/gamebryo2.2/corelibs/nimain/nistream.cpp', 323),
     ('src/staging/blk_00440000_od.cpp', 3764), ('src/staging/blk_00680000_od.cpp', 2763)]
only = sys.argv[1:]
by = {}
for f, ln in T: by.setdefault(f, []).append(ln)
for f, lns in by.items():
    if only and f not in only: continue
    p = FN / f; raw = p.read_bytes().decode('utf-8', 'surrogateescape'); nl = '\r\n' if '\r\n' in raw else '\n'
    t = raw.split(nl)
    for ln in sorted(lns, reverse=True):
        for i in range(ln - 1, min(len(t), ln + 150)):
            m = re.match(r'(\s*)((?:static\s+)?(?:void\s+)(?:__cdecl\s+)?operator delete)\(void\s*\*[^,)]*,\s*unsigned( int)?\s*\w*\)', t[i])
            if m:
                t.insert(i, m.group(1) + m.group(2) + '(void*);'); print('inserted', f, i + 1); break
        else: print('NOT FOUND', f, ln)
    p.write_bytes(nl.join(t).encode('utf-8', 'surrogateescape'))
