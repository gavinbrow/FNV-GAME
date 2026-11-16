"""link-v2 lockrun.py: hold runtime-next\build.lock (atomic create, PID + timestamp, stale after 60 min or dead PID) around a command. usage: python -I lockrun.py <cmd> [args...]"""
import os, sys, time, subprocess, ctypes
LOCK = r'C:\Projects\Decompilation\runtime-next\build.lock'
def alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
    if h: ctypes.windll.kernel32.CloseHandle(h); return True
    return False
def acquire(max_wait=3600):
    t0 = time.time()
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, ('%d %d\n' % (os.getpid(), int(time.time()))).encode()); os.close(fd); return
        except FileExistsError:
            try:
                pid, ts = open(LOCK).read().split()[:2]; pid = int(pid); ts = int(ts)
                if time.time() - ts > 3600 or not alive(pid): os.remove(LOCK); continue
            except Exception: pass
            if time.time() - t0 > max_wait: raise SystemExit('build.lock wait timeout')
            time.sleep(5)
acquire()
try: rc = subprocess.call(sys.argv[1:])
finally:
    try: os.remove(LOCK)
    except OSError: pass
sys.exit(rc)
