"""link-v2 dbghit.py: persistent breakpoint at BP; at each hit record [esp..esp+0x14] dwords and registers; at the fatal exception print the last hits. env: BP, N(last hits)."""
import ctypes, ctypes.wintypes as w, sys, os, struct, collections
k = ctypes.windll.kernel32
class PI(ctypes.Structure): _fields_ = [('hp', w.HANDLE), ('ht', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]
class DBG(ctypes.Structure): _fields_ = [('ec', w.DWORD), ('pid', w.DWORD), ('tid', w.DWORD), ('pad', w.DWORD), ('u', ctypes.c_byte * 160)]
class STARTUPINFO(ctypes.Structure): _fields_ = [('cb', w.DWORD), ('a', w.LPWSTR), ('b', w.LPWSTR), ('c', w.LPWSTR), ('d', w.DWORD * 7), ('e', w.DWORD), ('f', w.WORD), ('g', w.WORD), ('h', ctypes.c_void_p), ('i', w.HANDLE), ('j', w.HANDLE), ('l', w.HANDLE)]
exe, cwd = sys.argv[1], sys.argv[2]; BP = int(os.environ['BP'], 16); N = int(os.environ.get('N', '8')); SKIP = int(os.environ.get('SKIP', '0'))
sti = STARTUPINFO(); sti.cb = ctypes.sizeof(sti); pi = PI()
assert k.CreateProcessW(exe, None, None, None, False, 1, None, cwd, ctypes.byref(sti), ctypes.byref(pi)), ctypes.GetLastError()
def ctx_get(ht):
    c = (ctypes.c_ubyte * 716)(); struct.pack_into('<I', c, 0, 0x10007); k.Wow64GetThreadContext(ht, c); return c
def rd(a, n):
    b = ctypes.create_string_buffer(n); g = ctypes.c_size_t(0); k.ReadProcessMemory(pi.hp, ctypes.c_void_p(a), b, n, ctypes.byref(g)); return b.raw[:g.value]
def wr(a, data):
    old = w.DWORD(0); k.VirtualProtectEx(pi.hp, ctypes.c_void_p(a), len(data), 0x40, ctypes.byref(old)); k.WriteProcessMemory(pi.hp, ctypes.c_void_p(a), data, len(data), None); k.FlushInstructionCache(pi.hp, ctypes.c_void_p(a), len(data))
ev = DBG(); orig = None; hits = collections.deque(maxlen=N); nh = 0; rearm = False; INT3 = bytes([204])
while k.WaitForDebugEvent(ctypes.byref(ev), 120000):
    cont = 0x10002
    if ev.ec == 1:
        u = bytes(ev.u); code = struct.unpack_from('<I', u, 0)[0]; first = struct.unpack_from('<I', u, 152)[0]
        ht = k.OpenThread(0x1fffff, False, ev.tid); c = ctx_get(ht); eip = struct.unpack_from('<I', c, 184)[0]; fl = struct.unpack_from('<I', c, 192)[0]; esp = struct.unpack_from('<I', c, 196)[0]
        bpx = code in (0x80000003, 0x4000001f)
        if bpx and orig is None: orig = rd(BP, 1); wr(BP, INT3)
        elif bpx and eip - 1 == BP:
            nh += 1; regs = struct.unpack_from('<6I', c, 156)
            if nh > SKIP: hits.append((nh, esp, rd(esp, 24), regs))
            wr(BP, orig); struct.pack_into('<I', c, 184, BP); struct.pack_into('<I', c, 192, fl | 0x100); k.Wow64SetThreadContext(ht, c); rearm = True
        elif code in (0x80000004, 0x4000001e) and rearm:
            wr(BP, INT3); rearm = False
        elif code == 0xC0000005 and not first:
            print('fatal AV eip=%08x hits=%d' % (eip, nh))
            for h in hits: print(h[0], '%08x' % h[1], ' '.join('%08x' % x for x in struct.unpack('<6I', h[2])), '| edi esi ebx edx ecx eax', ' '.join('%08x' % x for x in h[3]))
            break
        else: cont = 0x80010001
    elif ev.ec == 5: print('exit', nh); break
    k.ContinueDebugEvent(ev.pid, ev.tid, cont)
k.TerminateProcess(pi.hp, 1)
