"""Mini resource compiler (rc.exe is not present locally): compiles the subset used by res-src/resources.rc
(RCDATA/BITMAP/ICON/numeric-type file resources, VERSIONINFO) to a .res file. usage: rc_lite.py in.rc out.res"""
import re, struct, sys, os
LANG = 0x409
def u16(s): return s.encode('utf-16le')
def idname(x):
    return struct.pack('<HH', 0xffff, x) if isinstance(x, int) else u16(x.upper()) + b'\0\0'
def entry(typ, name, data, flags=0x30):
    hdr_core = idname(typ) + idname(name)
    hs = 8 + len(hdr_core); hdr_core += b'\0' * ((-hs) % 4); hs = 8 + len(hdr_core) + 16
    b = struct.pack('<II', len(data), hs) + hdr_core + struct.pack('<IHHII', 0, flags, LANG, 0, 0)
    return b + data + b'\0' * ((-len(data)) % 4)
def tok(s):
    return re.findall(r'"(?:[^"\\]|\\.)*"|[A-Za-z_][\w]*|0x[0-9a-fA-F]+L?|\d+L?|[,]', s)
def num(t): return int(t.rstrip('L'), 0)
def ver_block(key, children, value=b'', typ=1, vlen=None):
    k = u16(key) + b'\0\0'
    b = struct.pack('<HHH', 0, vlen if vlen is not None else (len(value) // 2 if typ == 1 else len(value)), typ) + k
    b += b'\0' * ((-len(b)) % 4); b += value
    if not children and typ == 1:  # rc.exe: leaf string blocks report their length without the trailing pad
        n = len(b); b += b'\0' * ((-len(b)) % 4); return struct.pack('<H', n) + b[2:]
    b += b'\0' * ((-len(b)) % 4)
    for c in children: b += c
    b = struct.pack('<H', len(b)) + b[2:]
    return b
def compile_rc(path):
    base = os.path.dirname(os.path.dirname(os.path.abspath(path)))  # paths in .rc are relative to direct-v1
    text = re.sub(r'//[^\n]*', '', open(path, encoding='latin1').read())
    defs = dict(re.findall(r'#define\s+(\w+)\s+(\S+)', text)); text = re.sub(r'#define[^\n]*', '', text)
    out = bytearray(entry(0, 0, b'', 0)); out = bytearray(struct.pack('<II', 0, 32) + struct.pack('<HHHH', 0xffff, 0, 0xffff, 0) + struct.pack('<IHHII', 0, 0, 0, 0, 0))
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    i = 0
    TYPES = {'RCDATA': 10, 'BITMAP': 2, 'ICON': 3}
    while i < len(lines):
        t = tok(lines[i]); name = t[0]
        name = int(defs.get(name, name)) if re.fullmatch(r'\d+|\w+', name) and (name.isdigit() or name in defs) else name
        if isinstance(name, str) and name.isdigit(): name = int(name)
        kind = t[1]
        if kind == 'VERSIONINFO':
            fixed = {}; i += 1
            while lines[i] != 'BEGIN':
                k, *v = tok(lines[i]); fixed[k] = [num(x) for x in v if x != ',']; i += 1
            fv = fixed['FILEVERSION']; pv = fixed['PRODUCTVERSION']
            fx = struct.pack('<IIIIIIIIIIIII', 0xFEEF04BD, 0x10000, (fv[0] << 16) | fv[1], (fv[2] << 16) | fv[3], (pv[0] << 16) | pv[1], (pv[2] << 16) | pv[3],
                             fixed['FILEFLAGSMASK'][0], fixed['FILEFLAGS'][0], fixed['FILEOS'][0], fixed['FILETYPE'][0], fixed['FILESUBTYPE'][0], 0, 0)
            i += 1; blocks = []
            def parse_block():
                nonlocal i
                t = tok(lines[i]); assert t[0] == 'BLOCK'; key = t[1].strip('"'); i += 1; assert lines[i] == 'BEGIN'; i += 1; ch = []
                while lines[i] != 'END':
                    t = tok(lines[i])
                    if t[0] == 'BLOCK': ch.append(parse_block())
                    else:
                        k = t[1].strip('"')
                        if t[3].startswith('"'): ch.append(ver_block(k, [], u16(t[3][1:-1]) + b'\0\0', 1))
                        else: ch.append(ver_block(k, [], b''.join(struct.pack('<H', num(x)) for x in t[3:] if x != ','), 0, vlen=4))
                        i += 1
                i += 1
                return ver_block(key, ch, b'', 1, vlen=0)
            while lines[i] != 'END': blocks.append(parse_block())
            i += 1
            data = ver_block('VS_VERSION_INFO', blocks, fx, 0, vlen=len(fx))
            out += entry(16, name, data)
            continue
        f = t[2].strip('"'); data = open(os.path.join(base, f), 'rb').read()
        if True:
            typ = TYPES.get(kind) or (int(kind) if kind.isdigit() else kind)  # unknown identifier (e.g. RT_RCDATA) = string-named type, as the original .rc did
            if kind == 'BITMAP': data = data[14:]
            if kind == 'ICON':
                cnt = struct.unpack_from('<H', data, 4)[0]; grp = struct.pack('<HHH', 0, 1, cnt); ents = []
                for n in range(cnt):
                    w, h, c, r, pl, bpp, sz, off = struct.unpack_from('<BBBBHHII', data, 6 + 16 * n)
                    ents.append((w, h, c, r, pl, bpp, sz, data[off:off + sz]))
                # rc.exe: icon images first (ids 1..n, here ids continue from 1), then the group
                for n, e in enumerate(ents): out += entry(3, n + 1, e[7])
                for n, e in enumerate(ents): grp += struct.pack('<BBBBHHIH', *e[:7], n + 1)
                out += entry(14, name, grp); i += 1; continue
            out += entry(typ, name, data)
        i += 1
    return bytes(out)
if __name__ == '__main__':
    open(sys.argv[2], 'wb').write(compile_rc(sys.argv[1])); print('wrote', sys.argv[2])
