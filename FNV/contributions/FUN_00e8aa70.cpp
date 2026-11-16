#include <d3d9.h>

extern char DAT_010efcf0[];
extern char* __cdecl FUN_00e89d50(int);
extern void __cdecl FUN_00a29680(char*, char*);

struct CubeTextureResource
{
    bool __thiscall FUN_00e8aa70();
};

bool __thiscall CubeTextureResource::FUN_00e8aa70()
{
    const D3DFORMAT format =
        *reinterpret_cast<D3DFORMAT*>(reinterpret_cast<char*>(this) + 0x20);
    IDirect3DDevice9* const device =
        *reinterpret_cast<IDirect3DDevice9**>(
            *reinterpret_cast<char**>(reinterpret_cast<char*>(this) + 0x60) + 0x288);
    IDirect3DCubeTexture9* texture = 0;
    HRESULT result = device->CreateCubeTexture(
        *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x0c),
        *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x68),
        DAT_0126f0d0 ? 0x200 : 0,
        format,
        DAT_0126f0d0 ? D3DPOOL_DEFAULT : D3DPOOL_MANAGED,
        &texture, 0);

    if (result < 0)
    {
        FUN_00a29680(DAT_010efcf0, FUN_00e89d50(result));
        return false;
    }
    *reinterpret_cast<IDirect3DCubeTexture9**>(reinterpret_cast<char*>(this) + 0x64) = texture;
    return true;
}