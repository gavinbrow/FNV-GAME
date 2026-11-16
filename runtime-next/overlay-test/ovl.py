"""Overlay start test tool (ctypes).  Modes: find | compare | overlay | observe.
Nothing here writes outside runtime-next/overlay-test/.  Never saves live process code to disk.
"""
import sys, os, json, struct, ctypes, time, bisect, hashlib
from ctypes import wintypes as W
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REF = r'C:\Projects\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe'
PIN = r'C:\Projects\Decompilation\runtime-next\pinned-build\FalloutNV_pinned.exe'
UNITS = r'C:\Projects\Decompilation\fnv_decomp\build\units.json'
BASE = 0x400000

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)
ntdll = ctypes.WinDLL('ntdll')
PROCESS_QUERY_INFORMATION = 0x400; PROCESS_VM_READ = 0x10
PROCESS_VM_WRITE = 0x20; PROCESS_VM_OPERATION = 0x8; PROCESS_SUSPEND_RESUME = 0x800
k32.OpenProcess.restype = W.HANDLE
k32.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
k32.ReadProcessMemory.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.WriteProcessMemory.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.VirtualProtectEx.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_size_t, W.DWORD, ctypes.POINTER(W.DWORD)]
k32.FlushInstructionCache.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.c_size_t]
k32.IsWow64Process.argtypes = [W.HANDLE, ctypes.POINTER(W.BOOL)]
k32.GetExitCodeProcess.argtypes = [W.HANDLE, ctypes.POINTER(W.DWORD)]
k32.CloseHandle.argtypes = [W.HANDLE]
psapi.EnumProcessModulesEx.argtypes = [W.HANDLE, ctypes.POINTER(ctypes.c_void_p), W.DWORD, ctypes.POINTER(W.DWORD), W.DWORD]
psapi.GetModuleFileNameExW.argtypes = [W.HANDLE, ctypes.c_void_p, W.LPWSTR, W.DWORD]
ntdll.NtSuspendProcess.argtypes = [W.HANDLE]
ntdll.NtResumeProcess.argtypes = [W.HANDLE]


def open_proc(pid, access):
    h = k32.OpenProcess(access, False, pid)
    if not h:
        raise OSError('OpenProcess(pid=%d, access=0x%x) failed: WinError %d' % (pid, access, ctypes.get_last_error()))
    return h


def main_module(h):
    arr = (ctypes.c_void_p * 1024)(); need = W.DWORD()
    if not psapi.EnumProcessModulesEx(h, arr, ctypes.sizeof(arr), ctypes.byref(need), 0x03):  # LIST_MODULES_ALL
        raise OSError('EnumProcessModulesEx failed %d' % ctypes.get_last_error())
    n = need.value // ctypes.sizeof(ctypes.c_void_p)
    mods = []
    for i in range(min(n, 1024)):
        buf = ctypes.create_unicode_buffer(520)
        psapi.GetModuleFileNameExW(h, arr[i], buf, 520)
        mods.append((arr[i] or 0, buf.value))
    return mods


def rpm(h, addr, size):
    buf = (ctypes.c_char * size)(); got = ctypes.c_size_t()
    ok = k32.ReadProcessMemory(h, addr, buf, size, ctypes.byref(got))
    return bytes(buf[:got.value]), bool(ok)


def read_region(h, addr, size):
    """Read page-wise; returns (bytearray, unreadable_page_list)."""
    out = bytearray(size); bad = []
    pos = 0; CH = 0x10000
    while pos < size:
        n = min(CH, size - pos)
        d, ok = rpm(h, addr + pos, n)
        if ok and len(d) == n:
            out[pos:pos + n] = d
        else:  # fall back per 4K page
            for p in range(pos, pos + n, 0x1000):
                m = min(0x1000, size - p)
                d, ok = rpm(h, addr + p, m)
                if ok and len(d) == m: out[p:p + m] = d
                else: bad.append(p)
        pos += n
    return out, bad


class Img:
    def __init__(self, path):
        self.data = open(path, 'rb').read()
        d = self.data
        peo = struct.unpack_from('<I', d, 0x3c)[0]
        nsec, = struct.unpack_from('<H', d, peo + 6)
        optsz, = struct.unpack_from('<H', d, peo + 20)
        self.base, = struct.unpack_from('<I', d, peo + 24 + 28)
        self.sections = []
        for i in range(nsec):
            o = peo + 24 + optsz + 40 * i
            nm = d[o:o + 8].rstrip(b'\0').decode()
            vs, rva, rs, raw = struct.unpack_from('<IIII', d, o + 8)
            self.sections.append((nm, rva, vs, rs, raw))
        t = self.sections[0]
        assert t[0] == '.text', t
        self.text_rva, self.text_vs, self.text_rs, self.text_raw = t[1], t[2], t[3], t[4]

    def text(self):
        n = min(self.text_vs, self.text_rs)
        b = bytearray(self.text_vs)
        b[:n] = self.data[self.text_raw:self.text_raw + n]
        return b


def recipe_ranges():
    u = json.load(open(UNITS))['units']
    fn, tl = [], []
    for x in u:
        for f in x['functions']:
            fn.append((int(f['address'], 16), f['size'], f['symbol']))
        for t in x.get('eh_tails', []):
            tl.append((int(t['address'], 16), t['size'], t.get('parent')))
    fn.sort(); tl.sort()
    return fn, tl


def diff_ranges(a, b):
    """Return list of (start,end) of differing runs between equal-length bytes-likes (chunk-accelerated)."""
    n = len(a); runs = []; CH = 4096
    cur = None
    for s in range(0, n, CH):
        e = min(n, s + CH)
        if a[s:e] == b[s:e]:
            continue
        for i in range(s, e):
            if a[i] != b[i]:
                if cur is not None and cur[1] == i: cur[1] = i + 1
                else:
                    if cur is not None: runs.append(tuple(cur))
                    cur = [i, i + 1]
    if cur is not None: runs.append(tuple(cur))
    return runs


def merge(runs, gap=0):
    out = []
    for s, e in sorted(runs):
        if out and s <= out[-1][1] + gap: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return [tuple(x) for x in out]


def overlap_bytes(runs, ranges):
    """bytes of runs (sorted, VA-offset) inside union of ranges (merged, sorted)."""
    starts = [r[0] for r in ranges]; tot = 0
    for s, e in runs:
        k = bisect.bisect_right(starts, s) - 1
        if k < 0: k = 0
        while k < len(ranges) and ranges[k][0] < e:
            lo = max(s, ranges[k][0]); hi = min(e, ranges[k][1])
            if hi > lo: tot += hi - lo
            k += 1
    return tot


def owner(va, fn, fa, tl, ta):
    k = bisect.bisect_right(fa, va) - 1
    if k >= 0 and fa[k] <= va < fa[k] + fn[k][1]: return 'fn %08x %s' % (fn[k][0], fn[k][2][:48])
    k = bisect.bisect_right(ta, va) - 1
    if k >= 0 and ta[k] <= va < ta[k] + tl[k][1]: return 'tail %08x' % tl[k][0]
    return 'outside-recipe'


def cmd_find():
    import subprocess
    r = subprocess.run(['powershell', '-NoProfile', '-Command',
        "Get-Process FalloutNV -ErrorAction SilentlyContinue | Select Id,Path,StartTime,MainWindowTitle,Responding,@{n='Threads';e={$_.Threads.Count}} | ConvertTo-Json"],
        capture_output=True, text=True)
    print(r.stdout)


def cmd_compare(pid, placed_path=None):
    t0 = time.time()
    h = open_proc(pid, PROCESS_QUERY_INFORMATION | PROCESS_VM_READ)
    try:
        wow = W.BOOL(); k32.IsWow64Process(h, ctypes.byref(wow))
        mods = main_module(h)
        mm = mods[0]
        res = dict(pid=pid, wow64_32bit=bool(wow.value), main_module_base='0x%x' % mm[0], main_module_path=mm[1],
                   module_count=len(mods))
        ref, pin = Img(REF), Img(PIN)
        assert ref.base == BASE and pin.base == BASE
        res['text'] = dict(rva='0x%x' % ref.text_rva, vsize='0x%x' % ref.text_vs)
        if mm[0] != BASE:
            res['stop'] = 'base != 0x400000'; json.dump(res, open(os.path.join(HERE, 'compare_result.json'), 'w'), indent=1); print(json.dumps(res, indent=1)); return
        live, bad = read_region(h, BASE + ref.text_rva, ref.text_vs)
        res['unreadable_pages_in_text'] = len(bad); res['unreadable_first'] = ['0x%x' % (BASE + ref.text_rva + p) for p in bad[:10]]
        rt, pt = ref.text(), pin.text()
        res['live_sha256_not_saved_note'] = 'live code not written to disk'
        fn, tl = recipe_ranges()
        fa = [x[0] for x in fn]; ta = [x[0] for x in tl]
        fr = merge([(a - BASE - ref.text_rva, a - BASE - ref.text_rva + s) for a, s, _ in fn])
        tr = merge([(a - BASE - ref.text_rva, a - BASE - ref.text_rva + s) for a, s, _ in tl])
        allr = merge(fr + tr)
        placed = None
        if placed_path and os.path.exists(placed_path):
            pj = json.load(open(placed_path))
            placed = merge([(a - BASE - ref.text_rva, a - BASE - ref.text_rva + s) for a, s in pj['ranges']])
            res['placed_ranges_file'] = placed_path; res['placed_bytes'] = sum(e - s for s, e in placed)
        res['recipe_union_bytes'] = sum(e - s for s, e in allr)
        for name, other in (('reference', rt), ('pinned', pt)):
            runs = diff_ranges(live, other)
            tot = sum(e - s for s, e in runs)
            r = dict(differing_bytes=tot, runs=len(runs), in_recipe_ranges=overlap_bytes(runs, allr))
            r['outside_recipe_ranges'] = tot - r['in_recipe_ranges']
            if placed is not None:
                r['in_placed_ranges'] = overlap_bytes(runs, placed); r['outside_placed_ranges'] = tot - r['in_placed_ranges']
            r['first_ranges'] = []
            for s, e in runs[:20]:
                va = BASE + ref.text_rva + s
                r['first_ranges'].append(dict(va='0x%08x' % va, len=e - s, owner=owner(va, fn, fa, tl, ta),
                                              live=bytes(live[s:min(e, s + 12)]).hex(), ref=bytes(other[s:min(e, s + 12)]).hex()))
            # size histogram of runs
            r['run_len_hist'] = {}
            for s, e in runs:
                k = e - s; k = '1' if k == 1 else '2-4' if k <= 4 else '5-16' if k <= 16 else '17-256' if k <= 256 else '>256'
                r['run_len_hist'][k] = r['run_len_hist'].get(k, 0) + 1
            # per-owner group counts
            grp = {}
            for s, e in runs:
                o = owner(BASE + ref.text_rva + s, fn, fa, tl, ta).split(' ')[0]
                grp[o] = grp.get(o, 0) + (e - s)
            r['bytes_by_owner_kind'] = grp
            res['live_vs_' + name] = r
            if name == 'reference':
                res['_runs_ref'] = runs
        # whole runs list for overlay planning (addresses only) -> compare_diffs.json (no code bytes except none)
        runs_ref = res.pop('_runs_ref')
        res['elapsed_s'] = round(time.time() - t0, 1)
        json.dump(res, open(os.path.join(HERE, 'compare_result.json'), 'w'), indent=1)
        json.dump(dict(text_va=BASE + ref.text_rva, live_vs_reference_runs=runs_ref), open(os.path.join(HERE, 'live_vs_ref_runs.json'), 'w'))
        print(json.dumps(res, indent=1))
    finally:
        k32.CloseHandle(h)



class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_void_p), ('AllocationBase', ctypes.c_void_p), ('AllocationProtect', W.DWORD),
                ('PartitionId', W.WORD), ('RegionSize', ctypes.c_size_t), ('State', W.DWORD), ('Protect', W.DWORD), ('Type', W.DWORD)]
k32.VirtualQueryEx.argtypes = [W.HANDLE, ctypes.c_void_p, ctypes.POINTER(MBI), ctypes.c_size_t]


def regions(h, lo, hi):
    out = []; a = lo
    while a < hi:
        m = MBI()
        if not k32.VirtualQueryEx(h, a, ctypes.byref(m), ctypes.sizeof(m)): raise OSError('VirtualQueryEx %d' % ctypes.get_last_error())
        s = max(a, m.BaseAddress); e = min(hi, m.BaseAddress + m.RegionSize)
        out.append((s, e, m.Protect, m.State)); a = e
    return out


def sample(pid):
    import subprocess
    r = subprocess.run(['powershell', '-NoProfile', '-Command',
        "$p=Get-Process -Id %d -ErrorAction SilentlyContinue; if($p){ $p.Refresh(); '{0}|{1}|{2}|{3}|{4}' -f $true,$p.Responding,$p.MainWindowTitle,$p.Threads.Count,[int]($p.WorkingSet64/1MB) } else {'False'}" % pid],
        capture_output=True, text=True)
    return r.stdout.strip()


def cmd_overlay(pid):
    ref, pin = Img(REF), Img(PIN)
    tb = BASE + ref.text_rva
    pj = json.load(open(os.path.join(HERE, 'placed.json')))
    placed = merge([(a, a + s) for a, s in pj['ranges']])   # VA ranges
    res = dict(pid=pid, placed_ranges_merged=len(placed), placed_bytes=sum(e - s for s, e in placed))
    h = open_proc(pid, PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_SUSPEND_RESUME)
    try:
        mm = main_module(h)[0]
        assert mm[0] == BASE, 'base'
        live, bad = read_region(h, tb, ref.text_vs); assert not bad
        rt, pt = ref.text(), pin.text()
        # (a) hook check: live vs reference over the text; (b) bytes that overlay would change
        hook = merge([(tb + s, tb + e) for s, e in diff_ranges(live, rt)])
        res['live_vs_ref_diff_runs_before'] = len(hook)
        change = [(tb + s, tb + e) for s, e in diff_ranges(live, pt)]
        skipped_ranges = []; skipped_bytes = 0
        # plan write list: placed ranges minus hook ranges
        plan = []
        for s, e in placed:
            cur = s
            for hs, he in hook:
                if he <= cur or hs >= e: continue
                if hs > cur: plan.append((cur, hs))
                skipped_bytes += min(e, he) - max(cur, hs); skipped_ranges.append((max(hs, s), min(he, e)))
                cur = max(cur, he)
            if cur < e: plan.append((cur, e))
        res['skipped_hook_bytes'] = skipped_bytes
        res['bytes_to_write'] = sum(e - s for s, e in plan)
        # restore.json: original live values of every byte the overlay would change
        chg = []
        for s, e in change:
            for a in range(s, e):
                if any(ps <= a < pe_ for ps, pe_ in plan[:0]): pass
                chg.append(a)
        pl_starts = [p[0] for p in plan]
        def in_plan(a):
            k = bisect.bisect_right(pl_starts, a) - 1
            return k >= 0 and plan[k][0] <= a < plan[k][1]
        chg = [a for a in chg if in_plan(a)]
        rest = dict(pid=pid, base=BASE, note='original live values of every byte the overlay changes; write them back to undo',
                    bytes=[dict(va='0x%08x' % a, original='%02x' % live[a - tb], pinned='%02x' % pt[a - tb]) for a in chg])
        json.dump(rest, open(os.path.join(HERE, 'restore.json'), 'w'), indent=1)
        res['bytes_that_change_value'] = len(chg)
        # ---- suspend / write / restore protection / flush / resume
        regs = regions(h, tb, tb + ref.text_vs)
        res['text_regions_before'] = [('0x%x' % s, '0x%x' % e, '0x%x' % p) for s, e, p, st in regs]
        written = 0; werr = 0
        ntdll.NtSuspendProcess(h)
        t_susp = time.time()
        try:
            olds = []
            for s, e, p, st in regs:
                old = W.DWORD()
                if not k32.VirtualProtectEx(h, s, e - s, 0x40, ctypes.byref(old)): raise OSError('VirtualProtectEx rw %d' % ctypes.get_last_error())
                olds.append((s, e, old.value))
            try:
                for s, e in plan:
                    data = bytes(pt[s - tb:e - tb]); n = ctypes.c_size_t()
                    if k32.WriteProcessMemory(h, s, data, len(data), ctypes.byref(n)) and n.value == len(data): written += len(data)
                    else: werr += 1
            finally:
                for s, e, o in olds:
                    tmp = W.DWORD(); k32.VirtualProtectEx(h, s, e - s, o, ctypes.byref(tmp))
                k32.FlushInstructionCache(h, tb, ref.text_vs)
        finally:
            ntdll.NtResumeProcess(h)
        res['suspended_ms'] = round((time.time() - t_susp) * 1000)
        res['bytes_written'] = written; res['write_errors'] = werr
        res['text_regions_after'] = [('0x%x' % s, '0x%x' % e, '0x%x' % p) for s, e, p, st in regions(h, tb, tb + ref.text_vs)]
        # verify
        live2, bad2 = read_region(h, tb, ref.text_vs)
        mism = 0
        for s, e in placed:
            if live2[s - tb:e - tb] != pt[s - tb:e - tb]:
                mism += sum(1 for i in range(s - tb, e - tb) if live2[i] != pt[i])
        res['verify_mismatch_bytes_in_placed'] = mism
        # bytes outside placed: unchanged vs ref?
        res['live_vs_pinned_after_total_diff'] = sum(e - s for s, e in diff_ranges(live2, pt))
        res['live_vs_reference_after_total_diff'] = sum(e - s for s, e in diff_ranges(live2, rt))
        json.dump(res, open(os.path.join(HERE, 'overlay_result.json'), 'w'), indent=1)
        print(json.dumps(res, indent=1), flush=True)
        samples = []
        for i in range(7):
            ec = W.DWORD(); k32.GetExitCodeProcess(h, ctypes.byref(ec))
            smp = dict(t_s=i * 10, exit_code_query=ec.value, ps=sample(pid))
            samples.append(smp); print(smp, flush=True)
            if i < 6: time.sleep(10)
        res['samples'] = samples
        json.dump(res, open(os.path.join(HERE, 'overlay_result.json'), 'w'), indent=1)
    finally:
        k32.CloseHandle(h)


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'find': cmd_find()
    elif m == 'overlay': cmd_overlay(int(sys.argv[2]))
    elif m == 'compare': cmd_compare(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None)
