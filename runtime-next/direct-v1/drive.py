"""Concurrent key driver for dbg.py runs: waits for the menu (logo pixels), then Continue -> Yes."""
import sys, time, ctypes
sys.argv = [sys.argv[0]]
import harness as H
t0 = time.time(); h = None
while time.time() - t0 < 120:
    hs = []
    cb = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(lambda hw, l: (hs.append(hw) if H.user32.IsWindowVisible(hw) and H._title(hw) == 'Fallout: New Vegas' else None) or True)
    H.user32.EnumWindows(cb, 0)
    if hs:
        h = hs[0]
        try:
            if H.is_menu(H.snap(h)): break
        except Exception: pass
    time.sleep(2)
H.foreground(h); time.sleep(1); H.tap('down', gap=0.8); H.tap('enter', gap=2.5); H.tap('enter', gap=1)
print('driver done', flush=True)
