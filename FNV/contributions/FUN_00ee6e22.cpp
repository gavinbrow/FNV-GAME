struct D3DXIMAGE_INFO;
extern "C" __declspec(dllimport) long __stdcall D3DXGetImageInfoFromFileInMemory(const void* source, unsigned int size, D3DXIMAGE_INFO* info);
long __stdcall FUN_00ee6e22(const void* source, unsigned int size, D3DXIMAGE_INFO* info)
{
    return D3DXGetImageInfoFromFileInMemory(source, size, info);
}
