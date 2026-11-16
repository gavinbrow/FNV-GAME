__declspec(dllimport) long __stdcall D3DXCreateCubeTextureFromFileInMemory(void*, const void*, unsigned int, void**);
long __stdcall FUN_00ee6e16(void* device, const void* data, unsigned int size, void** texture)
{
    return D3DXCreateCubeTextureFromFileInMemory(device, data, size, texture);
}