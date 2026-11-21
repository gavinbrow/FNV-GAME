"""M5 seed: playable regression harness.
usage: python harness.py <exe> [--run DIR] [--play SECONDS] [--tag NAME] [--save "file.fos"]
Sets up the isolated run dir (idempotent), launches, waits for the main menu, loads a save with keystrokes, plays
(walk/turn/Pip-Boy) for --play seconds, exits through the menus, checks exit code and WER/Application-log crash events,
writes <tag>_verdict.json + screenshots into direct-v1\\harness-out\\<tag>\\.
Nothing outside direct-v1 is written (Steam install and My Games are read-only sources)."""
import argparse, ctypes, ctypes.wintypes as w, json, os, re, shutil, subprocess, sys, time, glob
from datetime import datetime
from PIL import ImageGrab, Image, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
INSTALL = (__import__('os').environ.get('FNV_GAME_DIR', r'C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas'))
MYGAMES = os.environ.get('FNV_MYGAMES') or os.path.expanduser(r'~\Documents\My Games\FalloutNV')   # read only source of INIs/saves (copied into the run folder)
user32 = ctypes.windll.user32
ctypes.windll.user32.SetProcessDPIAware()
user32.GetWindowRect.argtypes = [w.HWND, ctypes.POINTER(w.RECT)]
user32.SetForegroundWindow.argtypes = [w.HWND]


def log(*a):
    print(datetime.now().strftime('%H:%M:%S'), *a, flush=True)


_GL = 'C:' + chr(92) + 'Projects' + chr(92) + 'Decompilation' + chr(92) + 'runtime-next' + chr(92) + 'direct-v1' + chr(92) + 'harness.lock'   # one game instance per PC, whatever checkout runs the harness
LOCK = os.environ.get('FNV_HARNESS_LOCK') or (_GL if os.path.isdir(os.path.dirname(_GL)) else os.path.join(HERE, 'harness.lock'))


def _pid_alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h: return False
    code = w.DWORD(); ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code)); ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and code.value == 259


def acquire_lock(max_wait=3600):
    """Exclusive lock (atomic create); waits while another live harness holds it; breaks locks older than 20 min or with a dead PID."""
    t0 = time.time()
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, ('%d %f' % (os.getpid(), time.time()) + chr(10)).encode()); os.close(fd)
            import atexit; atexit.register(release_lock); return
        except FileExistsError:
            try:
                pid_s, ts_s = open(LOCK).read().split()[:2]; pid = int(pid_s); ts = float(ts_s)
                if time.time() - ts > 1200 or not _pid_alive(pid):
                    log('breaking stale harness.lock (pid %d, age %.0fs)' % (pid, time.time() - ts)); os.remove(LOCK); continue
            except (FileNotFoundError, ValueError, IndexError, PermissionError):
                time.sleep(1); continue
            if time.time() - t0 > max_wait: raise RuntimeError('harness.lock wait timeout')
            time.sleep(5)


def release_lock():
    try:
        if open(LOCK).read().split()[0] == str(os.getpid()): os.remove(LOCK)
    except Exception: pass


# ---------------------------------------------------------------- setup
def setup_run(run, save_name):
    os.makedirs(run, exist_ok=True)
    for dll in ('steam_api.dll', 'binkw32.dll', 'libvorbis.dll', 'libvorbisfile.dll', 'GDFFalloutNV.dll', 'atimgpud.dll'):
        dst = os.path.join(run, dll)
        if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(os.path.join(INSTALL, dll)):
            shutil.copy2(os.path.join(INSTALL, dll), dst)
    open(os.path.join(run, 'steam_appid.txt'), 'w').write('22380\n')
    data = os.path.join(run, 'Data')
    if not os.path.exists(os.path.join(data, 'FalloutNV.esm')):
        if os.path.lexists(data): os.rmdir(data)  # only ever removes a (broken) junction/empty dir
        subprocess.run(['powershell', '-NoProfile', '-Command', "New-Item -ItemType Junction -Path '%s' -Target '%s' | Out-Null" % (data, os.path.join(INSTALL, 'Data'))], check=True)
    ini = os.path.join(run, 'Fallout.ini')
    if not os.path.exists(ini):
        t = open(os.path.join(MYGAMES, 'Fallout.ini'), encoding='latin1').read().replace('\r\n', '\n')
        t = t.replace('[General]\n', '[General]\nbUseMyGamesDirectory=0\n', 1)
        open(ini, 'w', encoding='latin1', newline='\r\n').write(t)
    pref = os.path.join(run, 'FalloutPrefs.ini')
    if not os.path.exists(pref):
        t = open(os.path.join(MYGAMES, 'FalloutPrefs.ini'), encoding='latin1').read()
        t = t.replace('bFull Screen=1', 'bFull Screen=0').replace('iAdapter=1', 'iAdapter=0')
        open(pref, 'w', encoding='latin1', newline='').write(t)
    sv = os.path.join(run, 'Saves'); os.makedirs(sv, exist_ok=True)
    if not glob.glob(os.path.join(sv, '*.fos')):
        src = os.path.join(MYGAMES, 'Saves', save_name) if save_name else max(
            (f for f in glob.glob(os.path.join(MYGAMES, 'Saves', 'Save *.fos'))), key=os.path.getmtime)
        shutil.copy2(src, sv)
    return os.listdir(sv)


# ---------------------------------------------------------------- input
SC = {'w': 0x11, 'a': 0x1e, 's': 0x1f, 'd': 0x20, 'enter': 0x1c, 'esc': 0x01, 'tab': 0x0f, 'space': 0x39, 'down': 0xd0, 'up': 0xc8, 'y': 0x15, 'left': 0xcb, 'right': 0xcd}
EXT = {'down', 'up', 'left', 'right'}
_ROW = {'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p': 0x19, 'a': 0x1e, 's': 0x1f, 'd': 0x20, 'f': 0x21, 'g': 0x22,
        'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26, 'z': 0x2c, 'x': 0x2d, 'c': 0x2e, 'v': 0x2f, 'b': 0x30, 'n': 0x31, 'm': 0x32, ' ': 0x39,
        '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '0': 11, '`': 0x29}
SC.update({('c_' + k): v for k, v in _ROW.items()}); SC['grave'] = 0x29; SC['f5'] = 0x3f; SC['f9'] = 0x43; SC['shift'] = 0x2a


def key_down(k): user32.keybd_event(0, SC[k] & 0xff, 8 | (1 if k in EXT else 0), 0)
def key_up(k): user32.keybd_event(0, SC[k] & 0xff, 8 | 2 | (1 if k in EXT else 0), 0)


def tap(k, hold=0.08, gap=0.35):
    key_down(k); time.sleep(hold); key_up(k); time.sleep(gap)


def configured_scan_code(ini_path, action):
    """Decode a bound, non-extended keyboard scan code from isolated preferences."""
    values = []
    section = ''
    with open(ini_path, encoding='latin1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith((';', '#')): continue
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1].strip().casefold()
            elif section == 'controls' and '=' in line:
                key, value = line.split('=', 1)
                if key.strip().casefold() == action.casefold(): values.append(value.strip())
    if len(values) != 1:
        raise ValueError('missing or duplicate keyboard binding for %s' % action)
    value = values[0]
    if not re.fullmatch(r'[0-9a-fA-F]{8}', value):
        raise ValueError('missing or malformed keyboard binding for %s' % action)
    code = int(value, 16) >> 16
    if not (1 <= code <= 0x53 or 0x56 <= code <= 0x58):
        raise ValueError('unbound or unsupported keyboard binding for %s' % action)
    return code


def tap_scan(code, hold=0.08, gap=0.35):
    user32.keybd_event(0, code, 8, 0); time.sleep(hold)
    user32.keybd_event(0, code, 8 | 2, 0); time.sleep(gap)


def type_text(t, gap=0.06):
    for ch in t:
        up_ = ch.isupper(); k = 'c_' + ch.lower()
        if up_: key_down('shift')
        key_down(k); time.sleep(0.04); key_up(k)
        if up_: key_up('shift')
        time.sleep(gap)


def click(btn=1, secs=0.15):
    user32.mouse_event(2 if btn == 1 else 8, 0, 0, 0, 0); time.sleep(secs); user32.mouse_event(4 if btn == 1 else 16, 0, 0, 0, 0)


def hold(k, secs):
    key_down(k); time.sleep(secs); key_up(k)


def mouse_move(dx, dy, steps=10, delay=0.03):
    for _ in range(steps):
        user32.mouse_event(1, int(dx / steps), int(dy / steps), 0, 0); time.sleep(delay)


# ---------------------------------------------------------------- window / screenshot
def find_window(pid):
    res = []
    cb = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)(lambda h, l: (res.append(h) if _owner_pid(h) == pid and user32.IsWindowVisible(h) and _title(h) else None) or True)
    user32.EnumWindows(cb, 0)
    return res[0] if res else None


def _owner_pid(h):
    p = w.DWORD(); user32.GetWindowThreadProcessId(h, ctypes.byref(p)); return p.value


def _title(h):
    b = ctypes.create_unicode_buffer(256); user32.GetWindowTextW(h, b, 256); return b.value


def foreground(h):
    user32.keybd_event(0x12, 0, 0, 0); user32.SetForegroundWindow(h); user32.keybd_event(0x12, 0, 2, 0)  # ALT trick
    time.sleep(0.3)


def shot(h, path):
    r = w.RECT(); user32.GetWindowRect(h, ctypes.byref(r))
    if r.right - r.left < 10 or r.bottom - r.top < 10: return dict(gone=True)   # window destroyed (process exiting)
    im = ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom), all_screens=True); im.save(path)
    st = ImageStat.Stat(im.convert('L')); return dict(mean=round(st.mean[0], 1), std=round(st.stddev[0], 1), size=im.size)


def frac(path_or_im, x0, y0, x1, y1):
    import numpy as np
    im = Image.open(path_or_im) if isinstance(path_or_im, str) else path_or_im
    a = np.asarray(im.convert('RGB')).astype(int); hh, ww, _ = a.shape
    s_ = a[int(y0 * hh):int(y1 * hh), int(x0 * ww):int(x1 * ww)]
    return float(((s_[..., 0] > 200) & (s_[..., 1] > 120) & (s_[..., 1] < 200) & (s_[..., 2] < 90)).mean())


def is_menu(im):
    # Require amber in the left half of the logo as well as the full region.
    # Bright world textures can fill the right side without containing the logo.
    return frac(im, .03, .47, .34, .60) > 0.05 and frac(im, .03, .513, .185, .578) > 0.06
def _amber(im):
    """Amber UI mask at the window size used by the saved gameplay evidence."""
    import numpy as np
    a = np.asarray(im.convert('RGB').resize((1008, 786))).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 170) & (g > 85) & (b < 100) & (r > 1.13 * g) & (g > 1.4 * b)


def is_world(im):
    mask = _amber(im)
    return (int(mask[700:722, 50:310].sum()) > 500 and
            int(mask[700:722, 700:960].sum()) > 500 and not is_menu(im))


def is_pause(im):
    mask = _amber(im)
    bands = sum(int(mask[y - 8:y + 10, 870:970].sum()) > 100
                for y in (315, 352, 389, 426, 464, 502))
    return bands >= 4 and not is_world(im)


def is_console(im):
    """Recognize the observed console history and caret, excluding menu frames."""
    import numpy as np
    a = np.asarray(im.convert('RGB').resize((1008, 786))).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    white = (r > 135) & (g > 135) & (b > 130) & (abs(r - g) < 30) & (abs(g - b) < 30)
    rows = sum(int(white[y:y + 17, 25:345].sum()) > 150 for y in (675, 701, 727))
    caret = int(white[751:773, 27:33].sum()) >= 8
    amber = _amber(im)
    menu = any(int(amber[y - 8:y + 10, 870:970].sum()) > 100 for y in (315, 352, 389, 426, 464, 502))
    return rows >= 2 and caret and not menu and not is_world(im)


def snap(h):
    r = w.RECT(); user32.GetWindowRect(h, ctypes.byref(r)); return ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom), all_screens=True)


def require_world(h, proc, out, verdict, stage, timeout=60):
    """Wait for both HUD bars; only a recognized pause menu permits Escape."""
    deadline = time.monotonic() + timeout
    recovered = False
    event = None
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError('exited while waiting for world at %s' % stage)
        im = snap(h)
        if is_pause(im):
            if not recovered:
                event = dict(stage=stage, action='escape_pause', hud_restored=False)
                verdict.setdefault('recoveries', []).append(event)
                foreground(h)
                tap('esc', gap=1.5)
                recovered = True
        elif is_world(im):
            if event is not None: event['hud_restored'] = True
            return True
        time.sleep(1)
    name = 'guard_failure_%s.png' % stage
    info = shot(h, os.path.join(out, name))
    verdict['shots'].append((name, info))
    raise RuntimeError('world HUD not detected at %s; screenshot %s' % (stage, name))


def finish_console(h, proc, out, verdict, stage, timeout=60):
    """Wait for world or a confirmed console, and close that console at most once."""
    deadline = time.monotonic() + timeout
    event = None
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError('exited while waiting for console at %s' % stage)
        im = snap(h)
        if is_console(im):
            if event is None:
                event = dict(stage=stage, action='close_confirmed_console', hud_restored=False)
                verdict.setdefault('recoveries', []).append(event)
                foreground(h)
                tap('grave', gap=1.5)
        elif is_world(im):
            if event is not None: event['hud_restored'] = True
            verdict.setdefault('console_transitions', []).append(
                dict(stage=stage, action='closed_confirmed_console' if event is not None else 'world_without_toggle'))
            return True
        time.sleep(0.35)  # avoid sampling the blinking prompt at the same phase
    name = 'guard_failure_%s.png' % stage
    info = shot(h, os.path.join(out, name))
    verdict['shots'].append((name, info))
    raise RuntimeError('world HUD not detected at %s; screenshot %s' % (stage, name))


def quit_game_console(h, proc, out, verdict, timeout=30):
    """Request the game's QuitGame command and wait for actual process exit."""
    foreground(h)
    require_world(h, proc, out, verdict, 'before_quit')
    verdict['steps']['exit_method'] = 'console_quitgame'
    tap('grave', gap=1.2)
    type_text('qqq')
    tap('enter', gap=0.5)
    deadline = time.monotonic() + timeout
    while proc.poll() is None and time.monotonic() < deadline:
        time.sleep(0.5)
    return proc.poll()


def wait_for_cell(h, proc, probe, out, verdict, stage, predicate, timeout=120):
    """Wait for a stable matching cell and visible HUD, failing with a screenshot."""
    from game_state import StateUnavailable
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError('exited while waiting for cell at %s' % stage)
        try:
            cell = probe.read_cell_id()
            if cell and predicate(cell) and is_world(snap(h)):
                return cell
        except StateUnavailable:
            pass  # transient loading or unstable reads are not evidence of success
        time.sleep(0.5)
    name = 'guard_failure_%s.png' % stage
    info = shot(h, os.path.join(out, name)); verdict['shots'].append((name, info))
    raise RuntimeError('matching world cell not observed at %s; screenshot %s' % (stage, name))


def wer_events(since, exe):
    ps = ("Get-WinEvent -FilterHashtable @{LogName='Application';StartTime=[datetime]'%s'} -ErrorAction SilentlyContinue | "
          "Where-Object { $_.Message -match '%s' -and $_.ProviderName -match 'Application Error|Windows Error Reporting' } | "
          "ForEach-Object { $_.TimeCreated.ToString('o') + ' ' + $_.ProviderName + ' ' + ($_.Message -split \"`n\")[0] }" % (since.strftime('%Y-%m-%d %H:%M:%S'), os.path.basename(exe)))
    r = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.strip()]


# ---------------------------------------------------------------- main
def main():
    import faulthandler; faulthandler.dump_traceback_later(int(os.environ.get('HARNESS_WATCHDOG', '600')), repeat=False, file=open(os.path.join(HERE, 'harness_watchdog.txt'), 'w'))
    ap = argparse.ArgumentParser()
    ap.add_argument('exe'); ap.add_argument('--run', default=os.path.join(HERE, 'run')); ap.add_argument('--play', type=int, default=120)
    ap.add_argument('--tag', default=None); ap.add_argument('--save', default=None)
    ap.add_argument('--extended', action='store_true'); ap.add_argument('--console-cell', default='GSProspectorSaloonInterior')
    ap.add_argument('--menu-timeout', type=int, default=120)
    ap.add_argument('--exit-keys', default='down,down,down,down,down,down,enter,down,enter')
    ap.add_argument('--exit-method', choices=('console', 'menu'), default='console')
    a = ap.parse_args()
    acquire_lock()
    exe_src = os.path.abspath(a.exe); tag = a.tag or os.path.splitext(os.path.basename(exe_src))[0]
    out = os.path.join(HERE, 'harness-out', tag); os.makedirs(out, exist_ok=True)
    V = dict(exe=exe_src, tag=tag, started=datetime.now().isoformat(), steps={}, shots=[], pass_=False)
    t_start = datetime.now()
    probe = None
    try:
        V['saves'] = setup_run(a.run, a.save)
        exe = os.path.join(a.run, os.path.basename(exe_src))
        if not os.path.exists(exe) or open(exe, 'rb').read() != open(exe_src, 'rb').read(): shutil.copy2(exe_src, exe)
        for stale in ('RendererInfo.txt',):
            pass
        proc = subprocess.Popen([exe], cwd=a.run)
        V['pid'] = proc.pid; log('launched', proc.pid)
        # --- wait for window + main menu
        t0 = time.time(); h = None
        while time.time() - t0 < a.menu_timeout:
            if proc.poll() is not None: raise RuntimeError('exited during startup code=%s' % hex(proc.returncode & 0xffffffff))
            h = h or find_window(proc.pid)
            if h and time.time() - t0 > 12: break
            time.sleep(0.5)
        if not h: raise RuntimeError('no window')
        foreground(h); time.sleep(8)
        V['steps']['window'] = dict(title=_title(h), secs=round(time.time() - t0, 1))
        s = shot(h, os.path.join(out, '01_main_menu.png')); V['shots'].append(('01_main_menu.png', s))
        # --- wait for the main menu (intros take ~25 s), then Continue -> Yes
        t1 = time.time(); menu = False
        while time.time() - t1 < a.menu_timeout:
            if proc.poll() is not None: raise RuntimeError('exited before menu code=%s' % hex(proc.returncode & 0xffffffff))
            if is_menu(snap(h)): menu = True; break
            time.sleep(2)
        V['steps']['main_menu_reached'] = menu; V['steps']['main_menu_secs'] = round(time.time() - t0, 1)
        s = shot(h, os.path.join(out, '01_main_menu.png')); V['shots'].append(('01_main_menu.png', s))
        if not menu: raise RuntimeError('main menu not detected')
        time.sleep(1); tap('down', gap=0.8); tap('enter', gap=2.5)
        s = shot(h, os.path.join(out, '02_continue_prompt.png')); V['shots'].append(('02_continue_prompt.png', s))
        tap('enter', gap=1)   # Yes
        t1 = time.time(); world = False
        while time.time() - t1 < 150:
            if proc.poll() is not None: raise RuntimeError('exited during load code=%s' % hex(proc.returncode & 0xffffffff))
            time.sleep(3)
            if is_world(snap(h)): world = True; break
        V['steps']['world_loaded'] = world; V['steps']['load_secs'] = round(time.time() - t1, 1)
        s = shot(h, os.path.join(out, '04_world.png')); V['shots'].append(('04_world.png', s))
        if not world: raise RuntimeError('world not detected after Continue')
        if a.extended:
            from game_state import PlayerCellProbe
            prefs = os.path.join(a.run, 'FalloutPrefs.ini')
            quicksave_code = configured_scan_code(prefs, 'QuickSave')
            quickload_code = configured_scan_code(prefs, 'QuickLoad')
            V['steps']['quick_bindings'] = dict(quicksave_scan=quicksave_code, quickload_scan=quickload_code)
            probe = PlayerCellProbe(proc.pid, exe)
            probe.__enter__()
        time.sleep(3)
        # --- play
        t2 = time.time(); n = 0; seq = 0
        while time.time() - t2 < a.play:
            if proc.poll() is not None: raise RuntimeError('exited during play code=%s' % hex(proc.returncode & 0xffffffff))
            foreground(h)
            require_world(h, proc, out, V, 'play_start_%d' % (n + 1))
            hold('w', 3); mouse_move(260, 0); hold('w', 2); mouse_move(-120, 30); hold('a', 1); hold('d', 1); hold('s', 1)
            tap('space', gap=0.5)
            tap('tab', gap=3)   # Pip-Boy open
            n += 1; nm = '05_pipboy_%d.png' % n; s = shot(h, os.path.join(out, nm)); V['shots'].append((nm, s))
            tap('tab', gap=2)   # close
            require_world(h, proc, out, V, 'pipboy_close_%d' % n)
            hold('w', 2); mouse_move(-200, -10)
            seq += 1
            nm = '06_world_%d.png' % seq; s = shot(h, os.path.join(out, nm)); V['shots'].append((nm, s))
            require_world(h, proc, out, V, 'play_end_%d' % seq)
        V['steps']['play_secs'] = round(time.time() - t2, 1); V['steps']['alive_after_play'] = proc.poll() is None
        if a.extended:
            sv_dir = os.path.join(a.run, 'Saves')
            for q_ in glob.glob(os.path.join(sv_dir, 'quicksave*.fos')): os.remove(q_)   # run-folder copy only; the quicksave must be created by this run
            n0 = len(glob.glob(os.path.join(sv_dir, '*.fos'))); E = V['steps']['extended'] = {}
            def S(nm):
                s_ = shot(h, os.path.join(out, nm)); V['shots'].append((nm, s_)); return s_
            def world_ok(timeout=60):
                t_ = time.time()
                while time.time() - t_ < timeout:
                    if proc.poll() is not None: raise RuntimeError('exited code=%s' % hex(proc.returncode & 0xffffffff))
                    if is_world(snap(h)): return True
                    time.sleep(2)
                return False
            def console(cmd, wait=2.0, timeout=60):
                require_world(h, proc, out, V, 'console_before_' + cmd.split()[0])
                tap('grave', gap=1.2); type_text(cmd); tap('enter', gap=wait)
                # Loading may close or retain the console; act only on a recognized state.
                finish_console(h, proc, out, V, 'console_after_' + cmd.split()[0], timeout)
            # 1) new save at a known stable cell, using the isolated configured binding.
            foreground(h); require_world(h, proc, out, V, 'before_quicksave')
            saved_cell = probe.read_cell_id()
            if not saved_cell: raise RuntimeError('saved cell is unavailable')
            E['cell_before_save'] = saved_cell
            tap_scan(quicksave_code, hold=0.1, gap=6); S('10_after_quicksave.png')
            E['cell_after_save'] = wait_for_cell(h, proc, probe, out, V, 'after_quicksave', lambda cell: cell == saved_cell, 60)
            n1 = len(glob.glob(os.path.join(sv_dir, '*.fos'))); E['saves_before'] = n0; E['saves_after'] = n1; E['new_save_written'] = n1 > n0
            E['saves'] = sorted(os.path.basename(x) for x in glob.glob(os.path.join(sv_dir, '*.fos')))
            # 2) cell change via console command
            console('coc ' + a.console_cell, wait=4, timeout=90)
            E['cell_after_coc'] = wait_for_cell(h, proc, probe, out, V, 'after_coc', lambda cell: cell != saved_cell, 90)
            E['world_after_coc'] = True; E['cell_changed'] = E['cell_after_coc'] != saved_cell; time.sleep(5); S('15_new_cell.png')
            # 3) walk, draw weapon, fire
            foreground(h); require_world(h, proc, out, V, 'before_weapon'); hold('w', 3); mouse_move(300, 0); hold('w', 2); tap('c_r', gap=2); S('16_weapon_drawn.png'); click(); time.sleep(0.5); click(); time.sleep(1); S('17_fired.png')
            # 4) pass game time (console)
            console('set gamehour to 20', wait=2); time.sleep(5); S('18_time_changed.png'); E['world_after_time'] = world_ok(30)
            # 5) quickload is proven only when the saved cell is observed again.
            foreground(h); require_world(h, proc, out, V, 'before_quickload')
            E['cell_before_load'] = probe.read_cell_id()
            if E['cell_before_load'] != E['cell_after_coc']: raise RuntimeError('cell changed unexpectedly before quickload')
            tap_scan(quickload_code, hold=0.1, gap=3)
            E['cell_after_load'] = wait_for_cell(h, proc, probe, out, V, 'after_quickload', lambda cell: cell == saved_cell, 120)
            E['world_after_load'] = True; E['cell_restored'] = E['cell_after_load'] == saved_cell; time.sleep(3); S('22_after_quickload.png')
            V['steps']['extended_ok'] = all(E.get(k) for k in ('new_save_written', 'world_after_coc', 'world_after_time', 'world_after_load', 'cell_changed', 'cell_restored'))
        # --- request a normal game exit; retain the menu route for UI debugging
        if a.exit_method == 'console':
            quit_game_console(h, proc, out, V)
        else:
            V['steps']['exit_method'] = 'menu'
            # --- exit: Esc -> pause menu; keys come from --exit-keys (default derived by exploration)
            foreground(h); tap('esc', gap=2); s = shot(h, os.path.join(out, '07_pause.png')); V['shots'].append(('07_pause.png', s))
            for i, k in enumerate([x for x in a.exit_keys.split(',') if x]):
                tap(k, gap=2.5); nm = '08_exit_%d_%s.png' % (i, k); s = shot(h, os.path.join(out, nm)); V['shots'].append((nm, s))
                if proc.poll() is not None: break
            t3 = time.time()
            while proc.poll() is None and time.time() - t3 < 12: time.sleep(1)
            # fallbacks when a menu step was swallowed (menu focus quirks): quit-dialog Exit Game, then main-menu Quit
            for attempt, seq in enumerate((['down', 'enter'], ['down', 'down', 'enter'], ['esc', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'enter', 'down', 'enter'])):
                if proc.poll() is not None: break
                V['steps']['exit_fallback_%d' % attempt] = seq
                for k in seq:
                    tap(k, gap=1.5)
                    if proc.poll() is not None: break
                t3 = time.time()
                while proc.poll() is None and time.time() - t3 < 10: time.sleep(1)
        V['steps']['exit_code'] = None if proc.poll() is None else proc.returncode
        V['steps']['exited_cleanly'] = proc.poll() is not None and proc.returncode == 0
    except Exception as e:
        V['error'] = '%s: %s' % (type(e).__name__, e); log('ERROR', V['error'])
    finally:
        if probe is not None:
            try: probe.__exit__(None, None, None)
            except Exception as e: V['error'] = 'probe cleanup failed: %s' % e
        try:
            if proc.poll() is None:
                V['steps']['forced_kill'] = True; proc.kill()
        except Exception: pass
        time.sleep(3)
        V['wer_events'] = wer_events(t_start, a.exe)
        V['pass_'] = (V['steps'].get('extended_ok', True)) and bool(V['steps'].get('exited_cleanly')) and not V['wer_events'] and not V['steps'].get('forced_kill') and 'error' not in V and V['steps'].get('alive_after_play')
        V['finished'] = datetime.now().isoformat()
        json.dump(V, open(os.path.join(out, 'verdict.json'), 'w'), indent=1, default=str)
        log('VERDICT', 'PASS' if V['pass_'] else 'FAIL', json.dumps(V['steps']), V.get('error', ''), V['wer_events'])
    sys.exit(0 if V['pass_'] else 1)


if __name__ == '__main__':
    main()
