"""link-v2 dbgrun.py: start an exe under a minimal debug loop, print the first access violation (address, access type, registers) and exit. Needs the harness.lock (one game instance)."""
import ctypes, ctypes.wintypes as w, sys, os, struct
k = ctypes.windll.kernel32
class STARTUPINFO(ctypes.Structure): _fields_ = [('cb', w.DWORD), ('r', w.LPWSTR), ('d', w.LPWSTR), ('t', w.LPWSTR), ('x', w.DWORD), ('y', w.DWORD), ('xs', w.DWORD), ('ys', w.DWORD), ('xc', w.DWORD), ('yc', w.DWORD), ('fa', w.DWORD), ('fl', w.DWORD), ('sw', w.WORD), ('cb2', w.WORD), ('r2', ctypes.c_void_p), ('i', w.HANDLE), ('o', w.HANDLE), ('e', w.HANDLE)]
class PI(ctypes.Structure): _fields_ = [('hp', w.HANDLE), ('ht', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]
class EXC(ctypes.Structure): _fields_ = [('code', w.DWORD), ('flags', w.DWORD), ('rec', ctypes.c_void_p), ('addr', ctypes.c_void_p), ('n', w.DWORD), ('info', ctypes.c_void_p * 15)]
class DBG(ctypes.Structure): _fields_ = [('ec', w.DWORD), ('pid', w.DWORD), ('tid', w.DWORD), ('pad', w.DWORD), ('u', ctypes.c_byte * 160)]
exe = sys.argv[1]; cwd = sys.argv[2]
si = STARTUPINFO(); si.cb = ctypes.sizeof(si); pi = PI()
assert k.CreateProcessW(exe, None, None, None, False, 0x1, None, cwd, ctypes.byref(si), ctypes.byref(pi)), ctypes.GetLastError()
ev = DBG(); n = 0
while k.WaitForDebugEvent(ctypes.byref(ev), 30000):
    cont = 0x10002
    print('event', ev.ec, flush=True) if ev.ec not in (6,) else None
    if ev.ec == 1:
        e = EXC.from_buffer(ev.u)
        first = ctypes.c_ulong.from_buffer(ev.u, 80).value if False else None
        ex = struct.unpack_from('<II', bytes(ev.u), 0)  # code, flags
        code, flags = ex; addr = struct.unpack_from('<I', bytes(ev.u), 12)[0]
        print('exception %08x at %08x first=%d' % (code, addr, struct.unpack_from('<I', bytes(ev.u), 80)[0]), flush=True)
        if code == 0xC0000005:
            info = struct.unpack_from('<III', bytes(ev.u), 20 + 0)  # n, then info (32-bit layout: code,flags,rec,addr,n,info[])
            nparm = struct.unpack_from('<I', bytes(ev.u), 16)[0]; inf = struct.unpack_from('<II', bytes(ev.u), 20)
            print('ACCESS VIOLATION at %08x type=%d target=%08x first_chance=%d' % (addr, inf[0], inf[1], struct.unpack_from('<I', bytes(ev.u), 80)[0]))
            ctx = (ctypes.c_ubyte * 716)(); struct.pack_into('<I', ctx, 0, 0x10007)
            ht = k.OpenThread(0x1fffff, False, ev.tid); k.Wow64GetThreadContext(ht, ctx)
            c = bytes(ctx); regs = dict(zip(['edi', 'esi', 'ebx', 'edx', 'ecx', 'eax'], struct.unpack_from('<6I', c, 156))); regs.update(ebp=struct.unpack_from('<I', c, 180)[0], eip=struct.unpack_from('<I', c, 184)[0], esp=struct.unpack_from('<I', c, 196)[0])
            print({a: '%08x' % v for a, v in regs.items()})
            buf = ctypes.create_string_buffer(256); got = ctypes.c_size_t(0)
            k.ReadProcessMemory(pi.hp, ctypes.c_void_p(regs['esp']), buf, 256, ctypes.byref(got))
            print('stack', ' '.join('%08x' % x for x in struct.unpack_from('<%dI' % (got.value // 4), buf.raw, 0)))
            for spec in os.environ.get('DUMP', '').split(','):
                if not spec: continue
                a_, l_ = spec.split(':'); star = a_.startswith('*'); a_ = int(a_.lstrip('*'), 16)
                if star:
                    b4 = ctypes.create_string_buffer(4); g4 = ctypes.c_size_t(0); k.ReadProcessMemory(pi.hp, ctypes.c_void_p(a_), b4, 4, ctypes.byref(g4)); a_ = struct.unpack('<I', b4.raw)[0]
                l_ = int(l_, 16); bb_ = ctypes.create_string_buffer(l_); gg_ = ctypes.c_size_t(0)
                k.ReadProcessMemory(pi.hp, ctypes.c_void_p(a_), bb_, l_, ctypes.byref(gg_))
                print('dump %08x:' % a_, bb_.raw[:gg_.value].hex())
            bp = regs['ebp']; ch = []
            for _ in range(14):
                b2 = ctypes.create_string_buffer(8); g2 = ctypes.c_size_t(0)
                if not k.ReadProcessMemory(pi.hp, ctypes.c_void_p(bp), b2, 8, ctypes.byref(g2)): break
                nb, ra = struct.unpack('<II', b2.raw); ch.append('%08x' % ra)
                if nb <= bp: break
                bp = nb
            print('chain', ' '.join(ch))
            if struct.unpack_from('<I', bytes(ev.u), 80)[0] == 0 or True:
                n += 1
                if n >= 2 or struct.unpack_from('<I', bytes(ev.u), 80)[0] == 0: break
        cont = 0x80010001
    elif ev.ec == 5: print('exit code', struct.unpack_from('<I', bytes(ev.u), 0)[0]); break
    k.ContinueDebugEvent(ev.pid, ev.tid, cont)
k.TerminateProcess(pi.hp, 1)
