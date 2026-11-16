"""Minimal Win32 debugger (64-bit python -> 32-bit WOW64 target).
usage: python dbg.py exe cwd [seconds] [--trace] [--keep]
 Prints first real exception (regs, stack return candidates, ebp chain) then kills the process.
 --trace logs file/registry/process APIs via int3 breakpoints on SysWOW64 exports."""
import ctypes, ctypes.wintypes as w, sys, struct, time, os, pefile
k = ctypes.WinDLL('kernel32', use_last_error=True)
k.ReadProcessMemory.argtypes = [w.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k.WriteProcessMemory.argtypes = [w.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k.FlushInstructionCache.argtypes = [w.HANDLE, ctypes.c_void_p, ctypes.c_size_t]
k.OpenThread.restype = w.HANDLE
k.GetFinalPathNameByHandleW.argtypes = [w.HANDLE, w.LPWSTR, w.DWORD, w.DWORD]


class SI(ctypes.Structure):
    _fields_ = [('cb', w.DWORD), ('a', w.LPWSTR), ('b', w.LPWSTR), ('c', w.LPWSTR), ('d', w.DWORD), ('e', w.DWORD), ('f', w.DWORD), ('g', w.DWORD), ('h', w.DWORD), ('i', w.DWORD), ('j', w.DWORD), ('fl', w.DWORD), ('sw', w.WORD), ('r', w.WORD), ('r2', ctypes.c_void_p), ('in', w.HANDLE), ('out', w.HANDLE), ('err', w.HANDLE)]


class PI(ctypes.Structure):
    _fields_ = [('hp', w.HANDLE), ('ht', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]


class EXR(ctypes.Structure):
    _fields_ = [('code', w.DWORD), ('flags', w.DWORD), ('rec', ctypes.c_void_p), ('addr', ctypes.c_void_p), ('n', w.DWORD), ('info', ctypes.c_size_t * 15)]


class EXI(ctypes.Structure):
    _fields_ = [('rec', EXR), ('first', w.DWORD)]


class DE(ctypes.Structure):
    _fields_ = [('code', w.DWORD), ('pid', w.DWORD), ('tid', w.DWORD), ('pad', w.DWORD), ('u', ctypes.c_byte * 160)]


class CTX(ctypes.Structure):
    _fields_ = [('flags', w.DWORD), ('dr', w.DWORD * 6), ('fsave', w.BYTE * 112), ('gs', w.DWORD), ('fs', w.DWORD), ('es', w.DWORD), ('ds', w.DWORD), ('edi', w.DWORD), ('esi', w.DWORD), ('ebx', w.DWORD), ('edx', w.DWORD), ('ecx', w.DWORD), ('eax', w.DWORD), ('ebp', w.DWORD), ('eip', w.DWORD), ('cs', w.DWORD), ('efl', w.DWORD), ('esp', w.DWORD), ('ss', w.DWORD), ('ext', w.BYTE * 512)]


exe, cwd = sys.argv[1], sys.argv[2]
run = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 30
TRACE = '--trace' in sys.argv
si = SI(); si.cb = ctypes.sizeof(si); pi = PI()
assert k.CreateProcessW(exe, None, None, None, False, 1 | 0x10, None, cwd, ctypes.byref(si), ctypes.byref(pi)), ctypes.get_last_error()


def rd(a, n):
    b = ctypes.create_string_buffer(n); g = ctypes.c_size_t()
    k.ReadProcessMemory(pi.hp, a, b, n, ctypes.byref(g)); return b.raw[:g.value]


def wr(a, d):
    g = ctypes.c_size_t(); k.WriteProcessMemory(pi.hp, a, d, len(d), ctypes.byref(g)); k.FlushInstructionCache(pi.hp, a, len(d))


def cstr(a, wide=False):
    if not a: return '<null>'
    b = rd(a, 520)
    if wide: return b.decode('utf-16le', 'replace').split('\x00')[0]
    return b.split(b'\x00')[0].decode('latin1')


FUNCS = {'CreateFileA': 'a', 'CreateFileW': 'w', 'FindFirstFileA': 'a', 'FindFirstFileW': 'w', 'GetFileAttributesA': 'a', 'GetFileAttributesW': 'w',
         'LoadLibraryA': 'a', 'LoadLibraryW': 'w', 'LoadLibraryExW': 'w', 'LoadLibraryExA': 'a', 'RegOpenKeyExA': 'r', 'RegQueryValueExA': 'q',
         'CreateProcessA': 'a', 'CreateProcessW': 'w', 'ShellExecuteA': 's', 'MessageBoxA': 'm', 'MessageBoxW': 'mw', 'CreateMutexA': 'mu',
         'OutputDebugStringA': 'a', 'CreateDirectoryA': 'a', 'FindWindowA': 'f', 'DeleteFileA': 'a', 'MoveFileA': 'a', 'TerminateProcess': 't', 'RaiseException': 't', 'UnhandledExceptionFilter': 't'}
bps = {}; step = None


def thread_ctx(tid, flags=0x10007):
    h = k.OpenThread(0x1fffff, False, tid); cx = CTX(); cx.flags = flags; k.Wow64GetThreadContext(h, ctypes.byref(cx)); return h, cx


def on_dll(base, path):
    name = os.path.basename(path).lower()
    if TRACE and name in ('kernelbase.dll', 'kernel32.dll', 'user32.dll', 'shell32.dll', 'advapi32.dll'):
        try:
            pe = pefile.PE(r'C:\Windows\SysWOW64\%s' % name, fast_load=True); pe.parse_data_directories([0])
            for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if e.name and e.name.decode() in FUNCS and not e.forwarder:
                    a = base + e.address; ob = rd(a, 1)
                    if ob and ob != b'\xcc': bps[a] = (ob, e.name.decode(), name); wr(a, b'\xcc')
        except Exception as ex:
            print('dll err', name, ex)


t0 = time.time(); de = DE()
print('pid', pi.pid, flush=True)
buf = ctypes.create_unicode_buffer(520)
while time.time() - t0 < run:
    if not k.WaitForDebugEvent(ctypes.byref(de), 300): continue
    cont = 0x10002
    if de.code == 3:
        print('image base loaded at', hex(struct.unpack_from('<Q', bytes(de.u), 24)[0]), flush=True)
    if de.code == 6:
        hf, base = struct.unpack_from('<QQ', bytes(de.u), 0)[0:2]
        if hf and k.GetFinalPathNameByHandleW(hf, buf, 520, 0): on_dll(base, buf.value)
    elif de.code == 1:
        ex = EXI.from_buffer(de.u); c = ex.rec.code; ea = ex.rec.addr or 0
        if c in (0x80000003, 0x4000001f) and ea in bps:
            ob, name, m = bps[ea]; h, cx = thread_ctx(de.tid)
            ret = struct.unpack('<I', rd(cx.esp, 4))[0]; a = [struct.unpack('<I', rd(cx.esp + 4 + 4 * i, 4))[0] for i in range(4)]
            kind = FUNCS[name]; s = ''
            if kind in ('a', 'mu'): s = cstr(a[0])
            elif kind == 'w': s = cstr(a[0], True)
            elif kind == 's': s = cstr(a[2])
            elif kind == 'm': s = '%s | %s' % (cstr(a[1]), cstr(a[2]))
            elif kind == 'mw': s = cstr(a[1], True)
            elif kind in ('r', 'q'): s = cstr(a[1])
            elif kind == 'f': s = '%s %s' % (cstr(a[0]), cstr(a[1]))
            print('API %s(%s) ret=%08x' % (name, s, ret), flush=True)
            if kind == 't':
                st_ = rd(cx.esp, 0x600); cc = []
                for i_ in range(0, len(st_) - 3, 4):
                    v_ = struct.unpack_from('<I', st_, i_)[0]
                    if 0x401000 <= v_ < 0x2000000 and (rd(v_ - 5, 1) == bytes([0xe8]) or rd(v_ - 2, 1) == bytes([0xff]) or rd(v_ - 6, 2) == bytes([0xff, 0x15])): cc.append('%08x' % v_)
                eb_ = cx.ebp; ch_ = []
                for _ in range(16):
                    f_ = rd(eb_, 8)
                    if len(f_) < 8: break
                    nb_, rt_ = struct.unpack('<II', f_); ch_.append('%08x' % rt_)
                    if nb_ <= eb_: break
                    eb_ = nb_
                print('  ebp chain:', ' '.join(ch_), flush=True)
            wr(ea, ob); cx.eip = ea; cx.efl |= 0x100; k.Wow64SetThreadContext(h, ctypes.byref(cx)); step = (ea, de.tid)
        elif c in (0x80000004, 0x4000001e) and step and step[1] == de.tid:
            wr(step[0], b'\xcc'); step = None
        elif c in (0x80000003, 0x4000001e, 0x4000001f, 0x406d1388, 0x40010006, 0x4001000a, 0x80000004): pass
        elif c == 0xe06d7363: print('C++ exception thrown at', hex(ea), flush=True); cont = 0x80010001
        else:
            h, cx = thread_ctx(de.tid)
            print('EXCEPTION %08x at %08x first=%d info=%s' % (c, cx.eip, ex.first, [hex(x) for x in ex.rec.info[:ex.rec.n]]))
            print(' '.join('%s=%08x' % (r, getattr(cx, r)) for r in 'eax ebx ecx edx esi edi ebp esp'.split()))
            st = rd(cx.esp, 0x400); print('code@eip', rd(cx.eip, 12).hex())
            cands = []
            for i in range(0, len(st) - 3, 4):
                v = struct.unpack_from('<I', st, i)[0]
                if 0x401000 <= v < 0xfde000 and (rd(v - 5, 1) == b'\xe8' or rd(v - 2, 1) == b'\xff' or rd(v - 6, 2) == b'\xff\x15'): cands.append((i, v))
            print('ret cands:', ' '.join('+%x:%08x' % (i, v) for i, v in cands[:24]))
            ebp = cx.ebp; ch = []
            for _ in range(14):
                f = rd(ebp, 8)
                if len(f) < 8: break
                nb, ret = struct.unpack('<II', f); ch.append(ret)
                if nb <= ebp: break
                ebp = nb
            print('ebp chain:', ' '.join('%08x' % x for x in ch))
            k.TerminateProcess(pi.hp, 0xdead); sys.exit(1)
        if c not in (0x80000003, 0x80000004, 0x4000001e, 0x4000001f, 0xe06d7363, 0x406d1388, 0x40010006, 0x4001000a): cont = 0x80010001
    elif de.code == 5:
        print('process exited code', hex(struct.unpack_from('<I', bytes(de.u), 0)[0])); sys.exit(2)
    k.ContinueDebugEvent(de.pid, de.tid, cont)
print('ran %ds without crash; pid %d' % (run, pi.pid))
if '--keep' not in sys.argv: k.TerminateProcess(pi.hp, 0)
