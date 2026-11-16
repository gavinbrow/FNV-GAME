"""link-v2 dbgfn.py: differential tracer. Plant a breakpoint at BP, single-step the image code (system DLL calls are skipped by a return-address breakpoint) and log every entry of a function
start listed in FUNCS (json list of VAs, in THIS exe's address space). Writes the log (hex VAs) to OUT. env: BP, FUNCS, OUT, MAXFN (default 3000), IMG_LO/IMG_HI (hex, image range)."""
import ctypes, ctypes.wintypes as w, sys, os, struct, json
k = ctypes.windll.kernel32
class PI(ctypes.Structure): _fields_ = [('hp', w.HANDLE), ('ht', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]
class DBG(ctypes.Structure): _fields_ = [('ec', w.DWORD), ('pid', w.DWORD), ('tid', w.DWORD), ('pad', w.DWORD), ('u', ctypes.c_byte * 160)]
class STARTUPINFO(ctypes.Structure): _fields_ = [('cb', w.DWORD), ('a', w.LPWSTR), ('b', w.LPWSTR), ('c', w.LPWSTR), ('d', w.DWORD * 7), ('e', w.DWORD), ('f', w.WORD), ('g', w.WORD), ('h', ctypes.c_void_p), ('i', w.HANDLE), ('j', w.HANDLE), ('l', w.HANDLE)]
exe, cwd = sys.argv[1], sys.argv[2]; BP = int(os.environ['BP'], 16); FUNCS = set(json.load(open(os.environ['FUNCS']))); OUT = os.environ['OUT']; MAXFN = int(os.environ.get('MAXFN', '3000'))
LO = int(os.environ.get('IMG_LO', '400000'), 16); HI = int(os.environ.get('IMG_HI', '1300000'), 16)
sti = STARTUPINFO(); sti.cb = ctypes.sizeof(sti); pi = PI()
assert k.CreateProcessW(exe, None, None, None, False, 1, None, cwd, ctypes.byref(sti), ctypes.byref(pi)), ctypes.GetLastError()
def ctx_get(ht):
    c = (ctypes.c_ubyte * 716)(); struct.pack_into('<I', c, 0, 0x10007); k.Wow64GetThreadContext(ht, c); return c
def rd(a, n):
    b = ctypes.create_string_buffer(n); g = ctypes.c_size_t(0); k.ReadProcessMemory(pi.hp, ctypes.c_void_p(a), b, n, ctypes.byref(g)); return b.raw[:g.value]
def wr(a, data):
    old = w.DWORD(0); k.VirtualProtectEx(pi.hp, ctypes.c_void_p(a), len(data), 0x40, ctypes.byref(old)); k.WriteProcessMemory(pi.hp, ctypes.c_void_p(a), data, len(data), None); k.FlushInstructionCache(pi.hp, ctypes.c_void_p(a), len(data))
TF = 0x100; ev = DBG(); orig = None; stepping = False; log = []; pend = {}; fn = 0; steps = 0; INT3 = bytes([204])
while k.WaitForDebugEvent(ctypes.byref(ev), 120000):
    cont = 0x10002
    if ev.ec == 1:
        u = bytes(ev.u); code = struct.unpack_from('<I', u, 0)[0]; first = struct.unpack_from('<I', u, 152)[0]
        ht = k.OpenThread(0x1fffff, False, ev.tid); c = ctx_get(ht); eip = struct.unpack_from('<I', c, 184)[0]; fl = struct.unpack_from('<I', c, 192)[0]; esp = struct.unpack_from('<I', c, 196)[0]
        bpx = code in (0x80000003, 0x4000001f)
        if bpx and orig is None and not stepping: orig = rd(BP, 1); wr(BP, INT3)
        elif bpx and eip - 1 == BP and not stepping:
            wr(BP, orig); struct.pack_into('<I', c, 184, BP); struct.pack_into('<I', c, 192, fl | TF); k.Wow64SetThreadContext(ht, c); stepping = True
        elif bpx and (eip - 1) in pend:
            a2 = eip - 1; wr(a2, pend.pop(a2)); struct.pack_into('<I', c, 184, a2); struct.pack_into('<I', c, 192, fl | TF); k.Wow64SetThreadContext(ht, c)
        elif code in (0x80000004, 0x4000001e) and stepping:
            steps += 1
            if LO <= eip < HI:
                if eip in FUNCS:
                    log.append(eip); fn += 1
                    if fn >= MAXFN: break
                struct.pack_into('<I', c, 192, fl | TF); k.Wow64SetThreadContext(ht, c)
            else:
                ret, = struct.unpack('<I', rd(esp, 4))
                if LO <= ret < HI and ret not in pend:
                    pend[ret] = rd(ret, 1); wr(ret, INT3); struct.pack_into('<I', c, 192, fl & ~TF); k.Wow64SetThreadContext(ht, c)
                else: struct.pack_into('<I', c, 192, fl | TF); k.Wow64SetThreadContext(ht, c)
        elif code == 0xC0000005 and not first:
            log.append(-eip); break
        else: cont = 0x80010001
    elif ev.ec == 5: break
    k.ContinueDebugEvent(ev.pid, ev.tid, cont)
k.TerminateProcess(pi.hp, 1)
open(OUT, 'w').write('\n'.join('%x' % x if x > 0 else '-%x' % -x for x in log)); print('logged', len(log), 'steps', steps)
