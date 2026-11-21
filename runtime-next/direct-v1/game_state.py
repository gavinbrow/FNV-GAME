"""Read-only player owning-cell form ID probe for the x86 FNV image.

This verifies a loaded module and its PE header but does not authenticate the
executable's bytes. Callers must bind the PID/path to the launched process and
fail closed when this probe cannot obtain a stable result.
"""
import ctypes
import ctypes.wintypes as w
import os
import struct

PLAYER_GLOBAL_DATA_OFFSET = 0x0005BA3C
PLAYER_CELL_OFFSET = 0x40
CELL_FORM_ID_OFFSET = 0x0C

class StateUnavailable(RuntimeError):
    pass

class _ModuleEntry(ctypes.Structure):
    _fields_ = [('dwSize', w.DWORD), ('th32ModuleID', w.DWORD), ('th32ProcessID', w.DWORD),
                ('GlblcntUsage', w.DWORD), ('ProccntUsage', w.DWORD),
                ('modBaseAddr', ctypes.POINTER(w.BYTE)), ('modBaseSize', w.DWORD),
                ('hModule', w.HMODULE), ('szModule', w.WCHAR * 256), ('szExePath', w.WCHAR * 260)]

class _WindowsReader:
    SNAPMODULE = 0x8
    SNAPMODULE32 = 0x10
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    def __init__(self, pid):
        self.k = ctypes.WinDLL('kernel32', use_last_error=True)
        self.k.OpenProcess.argtypes = (w.DWORD, w.BOOL, w.DWORD); self.k.OpenProcess.restype = w.HANDLE
        self.k.CloseHandle.argtypes = (w.HANDLE,); self.k.CloseHandle.restype = w.BOOL
        self.k.CreateToolhelp32Snapshot.argtypes = (w.DWORD, w.DWORD); self.k.CreateToolhelp32Snapshot.restype = w.HANDLE
        self.k.Module32FirstW.argtypes = (w.HANDLE, ctypes.POINTER(_ModuleEntry)); self.k.Module32FirstW.restype = w.BOOL
        self.k.Module32NextW.argtypes = (w.HANDLE, ctypes.POINTER(_ModuleEntry)); self.k.Module32NextW.restype = w.BOOL
        self.k.ReadProcessMemory.argtypes = (w.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)); self.k.ReadProcessMemory.restype = w.BOOL
        self.pid = int(pid); self.handle = self.k.OpenProcess(self.PROCESS_QUERY_INFORMATION | self.PROCESS_VM_READ, False, self.pid)
        if not self.handle: raise StateUnavailable('OpenProcess failed: %s' % ctypes.get_last_error())

    def modules(self):
        snap = self.k.CreateToolhelp32Snapshot(self.SNAPMODULE | self.SNAPMODULE32, self.pid)
        if not snap or snap == self.INVALID_HANDLE_VALUE: raise StateUnavailable('module snapshot failed: %s' % ctypes.get_last_error())
        try:
            entry = _ModuleEntry(); entry.dwSize = ctypes.sizeof(entry)
            if not self.k.Module32FirstW(snap, ctypes.byref(entry)):
                raise StateUnavailable('module enumeration failed: %s' % ctypes.get_last_error())
            result = []
            while True:
                base = ctypes.cast(entry.modBaseAddr, ctypes.c_void_p).value
                result.append((entry.szExePath, base, entry.modBaseSize))
                if not self.k.Module32NextW(snap, ctypes.byref(entry)): break
            return result
        finally:
            self.k.CloseHandle(snap)

    def read(self, address, size):
        buf = ctypes.create_string_buffer(size); got = ctypes.c_size_t()
        ok = self.k.ReadProcessMemory(self.handle, ctypes.c_void_p(address), buf, size, ctypes.byref(got))
        if not ok or got.value != size: raise StateUnavailable('ReadProcessMemory failed or short at 0x%x' % address)
        return buf.raw

    def close(self):
        if self.handle:
            self.k.CloseHandle(self.handle); self.handle = None


def _normpath(path):
    return os.path.normcase(os.path.abspath(path))

class PlayerCellProbe:
    def __init__(self, pid, executable_path, *, _reader_factory=_WindowsReader):
        if not isinstance(executable_path, str) or not executable_path:
            raise StateUnavailable('missing executable path')
        self.reader = None
        try:
            self.reader = _reader_factory(pid)
            modules = self.reader.modules()
            # The first Toolhelp module is the main image; never silently choose a DLL.
            if not modules or _normpath(modules[0][0]) != _normpath(executable_path):
                raise StateUnavailable('main module path does not match launched executable')
            _, self.base, module_size = modules[0]
            if not self.base or module_size < 0x1000:
                raise StateUnavailable('module bounds invalid')
            dos = self._read_exact(self.base, 64)
            if dos[:2] != b'MZ': raise StateUnavailable('missing DOS header')
            peoff = struct.unpack_from('<I', dos, 0x3c)[0]
            if peoff < 64 or peoff + 26 > module_size: raise StateUnavailable('invalid PE header offset')
            pe = self._read_exact(self.base + peoff, 26)
            if pe[:4] != b'PE\0\0' or struct.unpack_from('<H', pe, 4)[0] != 0x14c or struct.unpack_from('<H', pe, 24)[0] != 0x10b:
                raise StateUnavailable('main module is not x86 PE32')
            section_count = struct.unpack_from('<H', pe, 6)[0]
            opt_size = struct.unpack_from('<H', pe, 20)[0]
            table = peoff + 24 + opt_size
            if not 0 < section_count <= 96 or opt_size < 0x60 or table + 40 * section_count > module_size:
                raise StateUnavailable('invalid PE section table')
            headers = self._read_exact(self.base + table, 40 * section_count)
            data_sections = []
            for i in range(section_count):
                row = headers[i*40:(i+1)*40]
                if row[:8].split(b'\0', 1)[0] == b'.data':
                    virtual_size, virtual_address = struct.unpack_from('<II', row, 8)
                    data_sections.append((virtual_address, virtual_size))
            if len(data_sections) != 1:
                raise StateUnavailable('missing or ambiguous .data section')
            data_rva, virtual_size = data_sections[0]
            if PLAYER_GLOBAL_DATA_OFFSET + 4 > virtual_size or data_rva + virtual_size > module_size:
                raise StateUnavailable('player global outside loaded .data virtual bounds')
            self.player_global = self.base + data_rva + PLAYER_GLOBAL_DATA_OFFSET
        except Exception:
            self.close()
            raise

    def _read_exact(self, address, size):
        try: data = self.reader.read(address, size)
        except StateUnavailable: raise
        except Exception as exc: raise StateUnavailable('process read failed') from exc
        if not isinstance(data, bytes) or len(data) != size: raise StateUnavailable('short process read')
        return data

    def _u32(self, address):
        return struct.unpack('<I', self._read_exact(address, 4))[0]

    def read_cell_id(self):
        if self.reader is None: raise StateUnavailable('probe closed')
        # Two full traversals catch common transitions; there is no atomic snapshot.
        def sample():
            player = self._u32(self.player_global)
            if not player: raise StateUnavailable('null player')
            cell = self._u32(player + PLAYER_CELL_OFFSET)
            if not cell: raise StateUnavailable('null owning cell')
            form = self._u32(cell + CELL_FORM_ID_OFFSET)
            if not form: raise StateUnavailable('zero cell form ID')
            return player, cell, form
        first = sample(); second = sample()
        if first != second: raise StateUnavailable('player/cell state changed during read')
        return first[2]

    def close(self):
        if self.reader is not None:
            reader, self.reader = self.reader, None
            reader.close()

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): self.close()
