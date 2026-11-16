"""Windows handle observations for a future LINK path review; not authority.

Read-only observation only: never creates outputs or launches processes. Win32
backend opens each component with OPEN_REPARSE_POINT and BACKUP_SEMANTICS,
queries volume/file index, attributes and normalized final path, then closes all
handles. This is a snapshot, not a safe creation primitive. A reviewed future
launcher must keep suitable handles and protect creation against rename/reparse,
short-name, hardlink and concurrent writers; this module must not approve LINK.
"""
import ctypes
from ctypes import wintypes
import ntpath
import os

FILE_ATTRIBUTE_DIRECTORY=0x10
FILE_ATTRIBUTE_REPARSE_POINT=0x400
ERROR_FILE_NOT_FOUND=2
ERROR_PATH_NOT_FOUND=3
INVALID_HANDLE_VALUE=ctypes.c_void_p(-1).value


def require(ok,message):
    if not ok:raise ValueError(message)


def _paths(path):
    require(type(path) is str and path and '/' not in path and ntpath.isabs(path) and
            ntpath.normpath(path)==path and not path.startswith(('\\\\?\\','\\\\.\\')), 'absolute canonical path required')
    drive,tail=ntpath.splitdrive(path)
    require(bool(drive) and tail not in ('','\\'), 'non-root path required')
    parts=[x for x in tail.split('\\') if x]
    result=[];current=drive+'\\'
    for part in parts:
        require(part not in ('.','..') and not part.endswith(('.', ' ')) and
                not any(ord(c)<32 or c in '<>:"|?*' for c in part), 'unsafe path component')
        current=ntpath.join(current,part);result.append(current)
    return result


class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
    _fields_=[('dwFileAttributes',wintypes.DWORD),('ftCreationTime',wintypes.FILETIME),
        ('ftLastAccessTime',wintypes.FILETIME),('ftLastWriteTime',wintypes.FILETIME),
        ('dwVolumeSerialNumber',wintypes.DWORD),('nFileSizeHigh',wintypes.DWORD),('nFileSizeLow',wintypes.DWORD),
        ('nNumberOfLinks',wintypes.DWORD),('nFileIndexHigh',wintypes.DWORD),('nFileIndexLow',wintypes.DWORD)]


class WindowsReadOnlyBackend:
    """Minimal Win32 handle observer; caller must separately authenticate code/runtime."""
    def __init__(self):
        require(os.name=='nt','Windows only')
        self.k=ctypes.WinDLL('kernel32',use_last_error=True)
        self.k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,
                                      wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        self.k.CreateFileW.restype=wintypes.HANDLE
        self.k.GetFileInformationByHandle.argtypes=[wintypes.HANDLE,ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION)]
        self.k.GetFileInformationByHandle.restype=wintypes.BOOL
        self.k.GetFinalPathNameByHandleW.argtypes=[wintypes.HANDLE,wintypes.LPWSTR,wintypes.DWORD,wintypes.DWORD]
        self.k.GetFinalPathNameByHandleW.restype=wintypes.DWORD
        self.k.CloseHandle.argtypes=[wintypes.HANDLE];self.k.CloseHandle.restype=wintypes.BOOL
    def open(self,path):
        # FILE_READ_ATTRIBUTES; permissive shares avoid claiming exclusion.
        handle=self.k.CreateFileW(path,0x80,0x7,None,3,0x02200000,None)
        if handle==INVALID_HANDLE_VALUE:
            error=ctypes.get_last_error()
            if error in (ERROR_FILE_NOT_FOUND,ERROR_PATH_NOT_FOUND):raise FileNotFoundError(path)
            raise OSError(error,'CreateFileW observation failed')
        return handle
    def info(self,handle):
        info=_BY_HANDLE_FILE_INFORMATION()
        if not self.k.GetFileInformationByHandle(handle,ctypes.byref(info)):
            raise OSError(ctypes.get_last_error(),'GetFileInformationByHandle failed')
        buffer=ctypes.create_unicode_buffer(32768)
        # FILE_NAME_NORMALIZED | VOLUME_NAME_GUID; unsupported network volumes fail closed.
        length=self.k.GetFinalPathNameByHandleW(handle,buffer,len(buffer),1)
        require(0<length<len(buffer),'normalized GUID final path unavailable')
        return {'volume':int(info.dwVolumeSerialNumber),
                'file_id':(int(info.nFileIndexHigh)<<32)|int(info.nFileIndexLow),
                'attributes':int(info.dwFileAttributes),'links':int(info.nNumberOfLinks),
                'final_path':buffer.value}
    def close(self,handle):
        if not self.k.CloseHandle(handle):raise OSError(ctypes.get_last_error(),'CloseHandle failed')


def observe_snapshot(protected_files, output_files, control_directory, *, backend):
    """Observe exact paths; ALWAYS returns status OBSERVED_NOT_AUTHORIZED.

    backend must be an authenticated real provider in any future use. The API
    accepts a fake for synthetic testing and therefore cannot itself authorize.
    Existing output/control leaf, reparse component, unstable duplicate identity,
    missing parents, unknown errors or unavailable final path fail closed.
    """
    require(type(protected_files) is list and protected_files and type(output_files) is list and output_files and
            type(control_directory) is str, 'exact path groups required')
    paths=protected_files+output_files+[control_directory]
    require(len({p.casefold() for p in paths})==len(paths),'duplicate declared path')
    handles=[];observed={}
    def open_info(path):
        handle=backend.open(path);handles.append(handle);row=backend.info(handle)
        require(type(row) is dict and set(row)=={'volume','file_id','attributes','links','final_path'} and
                all(type(row[k]) is int and row[k]>=0 for k in ('volume','file_id','attributes','links')) and
                row['file_id']>0 and row['links']>0 and type(row['final_path']) is str and row['final_path'],
                'invalid handle identity')
        require(not row['attributes']&FILE_ATTRIBUTE_REPARSE_POINT,'reparse component rejected')
        key=path.casefold();require(key not in observed or observed[key]==row,'path changed during observation')
        observed[key]=row
        return row
    try:
        protected=[]
        for path in protected_files:
            chain=_paths(path)
            for prefix in chain[:-1]:
                row=open_info(prefix);require(row['attributes']&FILE_ATTRIBUTE_DIRECTORY,'input parent is not directory')
            row=open_info(chain[-1]);require(not row['attributes']&FILE_ATTRIBUTE_DIRECTORY,'protected input is directory')
            protected.append((row['volume'],row['file_id']))
        parent_ids=[]
        for path in output_files+[control_directory]:
            chain=_paths(path)
            require(len(chain)>=2,'non-root output parent required')
            for prefix in chain[:-1]:
                row=open_info(prefix);require(row['attributes']&FILE_ATTRIBUTE_DIRECTORY,'output parent is not directory')
            parent_ids.append((row['volume'],row['file_id']))
            try:open_info(chain[-1])
            except FileNotFoundError:pass
            else:raise ValueError('output/control already exists')
        require(not set(protected).intersection(parent_ids),'protected input aliases output parent')
        return {'status':'OBSERVED_NOT_AUTHORIZED','protected_identities':protected,
                'output_parent_identities':parent_ids,'handles_retained':False,
                'race_free_creation_established':False,'native_link_authorized':False}
    finally:
        for handle in reversed(handles):backend.close(handle)
