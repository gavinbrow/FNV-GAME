struct D3DXPLANE;
struct D3DXMATRIX;

extern "C" __declspec(dllimport) D3DXPLANE* __stdcall D3DXPlaneTransform(
    D3DXPLANE* output, const D3DXPLANE* plane, const D3DXMATRIX* matrix);

D3DXPLANE* __stdcall FUN_00ee6dc8(
    D3DXPLANE* output, const D3DXPLANE* plane, const D3DXMATRIX* matrix)
{
    return D3DXPlaneTransform(output, plane, matrix);
}
