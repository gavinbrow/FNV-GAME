"""Exclusive build lock shared by build-all and every rebuild (runtime-next/build.lock, content 'pid unix-time owner').
  python buildlock.py acquire <owner> [--wait SECONDS] [--pid N]   waits while a live holder exists; breaks locks whose PID is dead or older than 120 min
  python buildlock.py release <owner>
  python buildlock.py status
From .cmd files: `python "%~dp0..\buildlock.py" acquire wB` ... `python "%~dp0..\buildlock.py" release wB`; the recorded PID is the parent cmd.exe (alive for the whole rebuild)."""
import os, sys, time, ctypes
_GLOBAL = 'C:' + chr(92) + 'Projects' + chr(92) + 'Decompilation' + chr(92) + 'runtime-next' + chr(92) + 'build.lock'   # machine-wide lock shared by every checkout on this PC
LOCK = os.environ.get('FNV_BUILD_LOCK') or (_GLOBAL if os.path.isdir(os.path.dirname(_GLOBAL)) else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.lock'))
STALE = 120 * 60
def alive(pid):
    k = ctypes.windll.kernel32; h = k.OpenProcess(0x1000, False, pid)
    if not h: return False
    c = ctypes.c_ulong(); ok = k.GetExitCodeProcess(h, ctypes.byref(c)); k.CloseHandle(h); return bool(ok) and c.value == 259
def read():
    try:
        t = open(LOCK).read().split(); return int(t[0]), float(t[1]), (t[2] if len(t) > 2 else '?')
    except (FileNotFoundError, ValueError, IndexError): return None
def acquire(owner, wait=7200, pid=None):
    pid = pid or os.getpid(); t0 = time.time()
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, ('%d %f %s' % (pid, time.time(), owner)).encode()); os.close(fd); return True
        except FileExistsError:
            r = read()
            if r is None: time.sleep(1); continue
            p, ts, o = r
            if not alive(p) or time.time() - ts > STALE:
                print('breaking stale build.lock held by %s (pid %d)' % (o, p), flush=True)
                try: os.remove(LOCK)
                except OSError: pass
                continue
            if time.time() - t0 > wait: return False
            print('build.lock held by %s (pid %d, %.0fs): waiting' % (o, p, time.time() - ts), flush=True); time.sleep(20)
def release(owner=None):
    r = read()
    if r and (owner is None or r[2] == owner or not alive(r[0])):
        try: os.remove(LOCK)
        except OSError: pass
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'status': print(read())
    elif c == 'acquire':
        w = int(sys.argv[sys.argv.index('--wait') + 1]) if '--wait' in sys.argv else 7200
        pid = int(sys.argv[sys.argv.index('--pid') + 1]) if '--pid' in sys.argv else os.getppid()
        sys.exit(0 if acquire(sys.argv[2], w, pid) else 1)
    elif c == 'release': release(sys.argv[2] if len(sys.argv) > 2 else None)
