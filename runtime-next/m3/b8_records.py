"""Source-evidenced 40-byte command-record prefix objects for M3 Phase 1.

The original arrays have unsized declarations; these two spans are only the
records independently observed in source accesses. Opaque fields deliberately
do not claim function signatures or object identity. Generated pointer cells
use the same symbolic-target convention as the M3 table generator.
"""
import struct

RECORD_SIZE = 40
POINTER_OFFSETS = frozenset((0, 4, 12, 20, 24, 28, 32))
# Explicitly scoped to the reviewed, non-overlapping accessed prefixes.
APPROVED_PREFIXES = {0x01190910: 640, 0x0118e8e0: 192}
TYPE = 'M3CommandRecordView'
STRUCT_DEFINITION = (
    'struct M3CommandRecordView { '
    'const char* name; const char* alternate; unsigned int opcode; '
    'const char* description; unsigned int opaque10; void* parameters; '
    'void* opaque18; void* opaque1c; void* opaque20; unsigned int opaque24; };\n'
    'typedef char M3CommandRecordView_size_check[sizeof(M3CommandRecordView)==40 ? 1 : -1];'
)


def build_entry(r, G):
    """Build a generator entry; G is the importing gen_m3 module.

    The caller must independently enforce chunk/ownership/rewritten-range
    constraints against its effective build. This helper checks structure and
    relocations, not final placement.
    """
    va = r['va']; size = r['size']; count = r['n']
    if r.get('tc') != 'R' or APPROVED_PREFIXES.get(va) != count or size != count * RECORD_SIZE:
        raise ValueError('unreviewed command-record prefix')
    name = r.get('generated_name')
    if name != 'M3_%08x' % va or r.get('partial') is not True:
        raise ValueError('a matching synthetic name and partial=true are required')
    section = G.sec_of(va)
    if section != '.data' or G.sec_of(va + size - 1) != section or va % 4:
        raise ValueError('invalid command-record section or alignment')
    raw = G.refbytes(va, size)
    if len(raw) != size:
        raise ValueError('short reference range')
    # Reject cells crossing either end, including a preceding relocation.
    sites = [x for x in G.ORIG_SITES if va - 3 <= x < va + size]
    if any(x < va or x + 4 > va + size or (x-va) % 4 or (x-va) % RECORD_SIZE not in POINTER_OFFSETS for x in sites):
        raise ValueError('unexpected relocation position')
    site_set = set(sites); elems = []; fields = []; tgts = []
    for off in range(0, size, 4):
        v = struct.unpack_from('<I', raw, off)[0]
        if va + off in site_set:
            # A resolvable address in a known image section or .data BSS tail.
            sec = G.sec_of(v); data = G.SEC['.data']
            bss = data['va'] + data['raw'] <= v < data['va'] + data['vs']
            if sec not in ('.text', '.data', '.rdata', 'CONST', '.tls') and not bss:
                raise ValueError('relocation target outside known image sections')
            elems.append(('p', v, G.TLO <= v < G.THI)); fields.append([off, '', 0]); tgts.append(v)
        elif off % RECORD_SIZE in POINTER_OFFSETS:
            if v != 0:
                raise ValueError('unrelocated nonzero pointer storage')
            elems.append(('z',))
        else:
            elems.append(('i', v))
    return dict(sym=None, name=name, va=va, size=size, type=TYPE, tc='R', n=count,
                section=section, align=4, ref=raw.hex(), kind='command-record-prefix',
                partial=True, elems=elems, fields=fields, tgts=tgts,
                evidence=r.get('evidence'), batch=r.get('batch'))


def render_entry(e, ext):
    """Return (shared struct definition, full object definition); mutate ext.

    ext maps target VA to declaration text, like gen_m3.cpp. Names identify
    storage only; source alias identity and the original full bound remain open.
    """
    rows = []
    for i in range(e['n']):
        cells = []
        for j, item in enumerate(e['elems'][i*10:(i+1)*10]):
            off = j * 4
            if item[0] == 'p':
                v = item[1]; code = item[2]
                kind = 'M3F' if code else 'M3D'
                ext[v] = ('extern "C" void %s_%08x(void);' if code else 'extern "C" char %s_%08x;') % (kind, v)
                cells.append('(%s)&%s_%08x' % ('const char*' if off in (0,4,12) else 'void*', kind, v))
            elif item[0] == 'z': cells.append('0')
            else: cells.append('0x%08xu' % item[1])
        rows.append('{%s}' % ','.join(cells))
    return STRUCT_DEFINITION, '%s %s[%d] = {\n%s\n};' % (TYPE, e['name'], e['n'], ',\n'.join(rows))

