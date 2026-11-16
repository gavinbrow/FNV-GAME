#include <windows.h>
struct ID3DXBuffer;
extern "C" __declspec(dllimport) HRESULT WINAPI D3DXCreateBuffer(DWORD, ID3DXBuffer**);
HRESULT WINAPI FUN_00ee6e3a(DWORD size, ID3DXBuffer** buffer) {
    return D3DXCreateBuffer(size, buffer);
}
