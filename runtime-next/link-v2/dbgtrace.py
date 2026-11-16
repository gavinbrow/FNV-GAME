"""link-v2 dbgtrace.py: run exe under a debug loop; plant a breakpoint at VA BP, then single-step and keep the last N EIPs; print them at the first access violation.
env: BP=<hex va> N=<count>. usage: python -I dbgtrace.py <exe> <cwd>"""
import ctypes, ctypes.wintypes as w, sys, os, struct, collections
k = ctypes.windll.kernel32
class SI(ctypes.Structure): _fields_ = [('cb', w.DWORD)] + [('x%d' % i, ctypes.c_void_p) for i in range(17)]
class PI(ctypes.Structure): _fields_ = [('hp', w.HANDLE), ('ht', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]
class DBG(ctypes.Structure): _fields_ = [('ec', w.DWORD), ('pid', w.DWORD), ('tid', w.DWORD), ('pad', w.DWORD), ('u', ctypes.c_byte * 160)]
BP2 = {int(x, 16): None for x in os.environ.get('BP2', '').split(',') if x}
exe, cwd = sys.argv[1], sys.argv[2]; BP = int(os.environ['BP'], 16); N = int(os.environ.get('N', '60'))
si = SI(); si.cb = 68
class STARTUPINFO(ctypes.Structure): _fields_ = [('cb', w.DWORD), ('a', w.LPWSTR), ('b', w.LPWSTR), ('c', w.LPWSTR), ('d', w.DWORD * 7), ('e', w.DWORD), ('f', w.WORD), ('g', w.WORD), ('h', ctypes.c_void_p), ('i', w.HANDLE), ('j', w.HANDLE), ('l', w.HANDLE)]
sti = STARTUPINFO(); sti.cb = ctypes.sizeof(sti); pi = PI()
assert k.CreateProcessW(exe, None, None, None, False, 1, None, cwd, ctypes.byref(sti), ctypes.byref(pi)), ctypes.GetLastError()
def ctx_get(ht):
    c = (ctypes.c_ubyte * 716)(); struct.pack_into('<I', c, 0, 0x10007); k.Wow64GetThreadContext(ht, c); return c
def rd(a, n):
    b = ctypes.create_string_buffer(n); g = ctypes.c_size_t(0); k.ReadProcessMemory(pi.hp, ctypes.c_void_p(a), b, n, ctypes.byref(g)); return b.raw[:g.value]
def wr(a, data):
    old = w.DWORD(0); k.VirtualProtectEx(pi.hp, ctypes.c_void_p(a), len(data), 0x40, ctypes.byref(old)); r = k.WriteProcessMemory(pi.hp, ctypes.c_void_p(a), data, len(data), None); k.FlushInstructionCache(pi.hp, ctypes.c_void_p(a), len(data)); return r
ev = DBG(); orig = None; stepping = False; ring = collections.deque(maxlen=N); done = False; steps = 0
while not done and k.WaitForDebugEvent(ctypes.byref(ev), 60000):
    cont = 0x10002
    if os.environ.get('V'): print('ev', ev.ec, flush=True)
    ht = k.OpenThread(0x1fffff, False, ev.tid) if ev.ec == 1 else None
    if ev.ec == 1:
        u = bytes(ev.u); code = struct.unpack_from('<I', u, 0)[0]; first = struct.unpack_from('<I', u, 152)[0]; exa, = struct.unpack_from('<Q', u, 16); acc, tgt = struct.unpack_from('<QQ', u, 32)
        c = ctx_get(ht); eip = struct.unpack_from('<I', c, 184)[0]
        if os.environ.get('V'): print('exc %08x eip %08x' % (code, eip), flush=True)
        if code == 0x80000003 and orig is None and eip != BP + 1:
            if BP and not stepping:
                orig = rd(BP, 1); k.WriteProcessMemory(pi.hp, ctypes.c_void_p(BP), b'\xcc', 1, None); k.FlushInstructionCache(pi.hp, ctypes.c_void_p(BP), 1)
        elif code in (0x80000003, 0x4000001f) and eip - 1 in BP2 and stepping:
            a2 = eip - 1; wr(a2, BP2[a2]); struct.pack_into('<I', c, 184, a2); struct.pack_into('<I', c, 192, struct.unpack_from('<I', c, 192)[0] | 0x100); k.Wow64SetThreadContext(ht, c); ring.append((a2, 0))
        elif code in (0x80000003, 0x4000001f) and eip == BP + 1:
            wr(BP, orig)
            struct.pack_into('<I', c, 184, BP); struct.pack_into('<I', c, 192, struct.unpack_from('<I', c, 192)[0] | 0x100); k.Wow64SetThreadContext(ht, c); stepping = True; print('bp hit, stepping', flush=True)
            for a2 in list(BP2): BP2[a2] = rd(a2, 1); wr(a2, bytes([204]))
        elif code in (0x80000004, 0x4000001e) and stepping:
            ring.append((eip, struct.unpack_from('<I', c, 196)[0])); steps += 1
            struct.pack_into('<I', c, 192, struct.unpack_from('<I', c, 192)[0] | 0x100); k.Wow64SetThreadContext(ht, c)
        elif code == 0xC0000005 and first:
            print('first-chance AV at %08x eip %08x access %d target %08x steps %d' % (exa, eip, acc, tgt, steps), flush=True); cont = 0x80010001
        elif code == 0xC0000005:
            print('second-chance AV at %08x access %d target %08x' % (exa, acc, tgt))
            print('AV eip=%08x steps=%d' % (eip, steps)); print(' '.join('%08x:%08x' % x for x in ring)); regs = struct.unpack_from('<6I', c, 156); print('regs edi esi ebx edx ecx eax', ' '.join('%08x' % r for r in regs), 'esp %08x ebp %08x' % (struct.unpack_from('<I', c, 196)[0], struct.unpack_from('<I', c, 180)[0]))
            done = True
        else: cont = 0x80010001
    elif ev.ec == 5: print('exit', struct.unpack_from('<I', bytes(ev.u), 0)[0]); break
    k.ContinueDebugEvent(ev.pid, ev.tid, cont)
k.TerminateProcess(pi.hp, 1)
