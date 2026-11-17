# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# Batch 7: generic typed objects 'G' (packed struct of runs). Run classes: P pointers (void*, 0 = null), U unsigned dwords, H int, I unsigned (declared head), J long, K unsigned long,
# M float, N double, S char string (NUL terminated, padded), B bytes, Z zero bytes.  A run descriptor is [cls, count] (count = elements; S/B/Z: bytes; N: doubles).
PRINT = frozenset(list(range(0x20, 0x7f)) + [9, 10, 13])
RUN_SZ = {'P': 4, 'U': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'M': 4, 'N': 8, 'S': 1, 'B': 1, 'Z': 1}
RUN_CTY = {'P': 'void*', 'U': 'unsigned', 'H': 'int', 'I': 'unsigned', 'J': 'long', 'K': 'unsigned long', 'M': 'float', 'N': 'double', 'S': 'char', 'B': 'unsigned char', 'Z': 'unsigned char'}
MAXRUNS = 1500


def _plaus_f(raw):
    v = struct.unpack('<f', raw)[0]
    if v != v or v in (float('inf'), float('-inf')) or v == 0 or not (1e-6 <= abs(v) <= 1e9): return False
    return any(struct.pack('<f', float('%.*g' % (p, v))) == raw for p in range(1, 7))


def _plaus_d(raw):
    v = struct.unpack('<d', raw)[0]
    if v != v or v in (float('inf'), float('-inf')) or v == 0 or not (1e-9 <= abs(v) <= 1e12): return False
    return any(struct.pack('<d', float('%.*g' % (p, v))) == raw for p in range(1, 13))


def _floatok4(raw, tc):
    if tc == 'M':
        v = struct.unpack('<f', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 1.1754944e-38))
    v = struct.unpack('<d', raw)[0]; return not (math.isnan(v) or math.isinf(v) or (v != 0 and abs(v) < 2.2250738585072014e-308))


def _site_in(lo, hi):          # an original .reloc site in [lo, hi)
    i = bisect.bisect_left(ORIG_SITES, lo); return i < len(ORIG_SITES) and ORIG_SITES[i] < hi


def layout(va, raw, head, labels):
    """reference bytes of one piece -> run descriptors [[cls, count], ...] (exact: every byte is accounted for; pointers only at original .reloc sites; no label strictly inside a multi-byte element)"""
    n = len(raw); cells = []; p = 0; brk_next = False

    def lab_in(lo, hi):
        i = bisect.bisect_right(labels, lo); return i < len(labels) and labels[i] < hi
    if head in ('H', 'I', 'J', 'K') and n >= 4 and not _site_in(va + 1, va + 4):
        cells.append(['P' if va in ORIG_SET else head, 4, 1]); p = 4; brk_next = True
    elif head == 'M' and n >= 4 and not _site_in(va, va + 4) and not lab_in(va, va + 4) and _floatok4(raw[:4], 'M'):
        cells.append(['M', 4, 1]); p = 4; brk_next = True
    elif head == 'N' and n >= 8 and not _site_in(va, va + 8) and not lab_in(va, va + 8) and _floatok4(raw[:8], 'N'):
        cells.append(['N', 8, 1]); p = 8; brk_next = True
    while p < n:
        a = va + p; c = None
        if a in ORIG_SET and p + 4 <= n: c = ['P', 4, 0]
        elif raw[p] == 0:
            q = p
            while q < n and raw[q] == 0 and (va + q) not in ORIG_SET: q += 1
            if q - p >= 16: c = ['Z', q - p, 0]
        if c is None and raw[p] in PRINT:
            j = p
            while j < n and raw[j] in PRINT: j += 1
            if j - p >= 4 and j < n and raw[j] == 0 and not _site_in(a, va + j + 1):
                e = j + 1
                while (va + e) % 4 and e < n and raw[e] == 0 and (va + e) not in ORIG_SET: e += 1
                c = ['S', e - p, 0]
        if c is None and a % 4 == 0 and p + 4 <= n and not _site_in(a + 1, a + 4) and not lab_in(a, a + 4):
            w = raw[p:p + 4]
            if w == b'\0\0\0\0': c = ['z', 4, 0]
            elif a % 8 == 0 and p + 8 <= n and not _site_in(a + 4, a + 8) and not lab_in(a, a + 8) and _plaus_d(raw[p:p + 8]): c = ['N', 8, 0]
            elif _plaus_f(w): c = ['M', 4, 0]
            else: c = ['U', 4, 0]
        if c is None: c = ['B', 1, 0]
        if brk_next: c[2] = 1; brk_next = False
        cells.append(c); p += c[1]
    assert p == n
    for i, c in enumerate(cells):      # zero dwords join the neighbouring dword-class run
        if c[0] != 'z': continue
        pc = next((x[0] for x in reversed(cells[:i]) if x[0] != 'z'), None) if i and not c[2] else None
        nc = next((x[0] for x in cells[i + 1:] if x[0] != 'z'), None) if not (i + 1 < len(cells) and cells[i + 1][2]) else None
        c[0] = pc if pc in ('P', 'U', 'M') else (nc if nc in ('P', 'U', 'M') else 'U')
    runs = []
    for c in cells:
        if runs and not c[2] and runs[-1][0] == c[0] and c[0] != 'S': runs[-1][1] += c[1] // RUN_SZ[c[0]]
        else: runs.append([c[0], c[1] // RUN_SZ[c[0]]])
    return runs


def g_items(va, raw, runs):
    """run descriptors + reference bytes -> items per run (P: (is_site, value); other dword/float/double: raw bytes of one element; S/B/Z: the bytes)"""
    out = []; p = 0
    for cls, cnt in runs:
        sz = RUN_SZ[cls]; nb = cnt * sz; seg = raw[p:p + nb]
        if cls == 'P': it = [((va + p + 4 * k) in ORIG_SET, struct.unpack('<I', seg[4 * k:4 * k + 4])[0]) for k in range(cnt)]
        elif cls in ('S', 'B', 'Z'): it = seg
        else: it = [seg[sz * k:sz * (k + 1)] for k in range(cnt)]
        out.append(it); p += nb
    assert p == len(raw)
    return out


def g_fields(e):
    """pointer fields [offset, '', 0] and their target VAs of a G entry (from the run items)"""
    f = []; t = []; p = 0
    for (cls, cnt), it in zip(e['runs'], e['items']):
        if cls == 'P':
            for k, (site, v) in enumerate(it):
                if site: f.append([p + 4 * k, '', 0]); t.append(v)
        p += cnt * RUN_SZ[cls]
    e['fields'] = f; e['tgts'] = t


def g_render(e, ext):
    """struct definition text and initializer text of a G entry; extern "C" targets are added to ext {tv: decl}"""
    mem = []; ini = []
    for k, ((cls, cnt), it) in enumerate(zip(e['runs'], e['items'])):
        if cls == 'S':
            mem.append('char r%d[%d];' % (k, cnt)); assert it[-1] == 0; ini.append(cstr(it[:-1]))
            continue
        mem.append('%s r%d[%d];' % (RUN_CTY[cls], k, cnt))
        if cls == 'P':
            cs = []
            for site, v in it:
                if not site: cs.append('0'); continue
                code = TLO <= v < THI; ext[v] = 'extern "C" void M3F_%08x(void);' % v if code else 'extern "C" char M3D_%08x;' % v
                cs.append('(void*)&%s_%08x' % ('M3F' if code else 'M3D', v))
                RENDER_STAT['extern'] += 1
            ini.append('{%s}' % ', '.join(cs))
        elif cls == 'B': ini.append('{%s}' % ', '.join(str(b) for b in it))
        elif cls == 'Z': ini.append('{0}')
        else: ini.append('{%s}' % ', '.join(fmt({'U': 'I', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'M': 'M', 'N': 'N'}[cls], x) for x in it))
    return 'struct M3S_%08x { %s };' % (e['va'], ' '.join(mem)), '{%s}' % ', '.join(ini)


def check_g(e, data, rel, tab):
    """generic object: relocation offsets == original .reloc sites inside, each DIR32 with target + addend == the reference dword and addend bytes == reference minus target;
    every other byte equals the reference. -> reason or None"""
    ref_ = bytes.fromhex(e['ref']); sites = sorted(f - e['va'] for f in ORIG_SITES if e['va'] <= f < e['va'] + e['size'])
    if [r[0] for r in rel] != sites: return 'reloc sites %s != original .reloc sites %s' % ([r[0] for r in rel][:8], sites[:8])
    mask = bytearray(len(ref_))
    for off, nm, add in rel:
        refv = struct.unpack('<I', ref_[off:off + 4])[0]; tv = splice.resolve(nm, tab)
        if tv is None: return 'offset %d: unresolvable target %s' % (off, nm)
        if (tv + add) & 0xffffffff != refv: return 'offset %d: target %x + addend %d != reference value %x' % (off, tv, add, refv)
        if int.from_bytes(data[off:off + 4], 'little') != (refv - tv) & 0xffffffff: return 'offset %d: addend bytes %s' % (off, data[off:off + 4].hex())
        mask[off:off + 4] = b'\1\1\1\1'
    if len(data) != len(ref_): return 'size'
    if not any(mask) and data == ref_: return None
    for i in range(len(ref_)):
        if not mask[i] and data[i] != ref_[i]: return 'byte %d (va %08x): %02x != ref %02x' % (i, e['va'] + i, data[i], ref_[i])
    return None


