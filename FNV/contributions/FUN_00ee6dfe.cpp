struct D3DXMATRIX;

extern "C" __declspec(dllimport) D3DXMATRIX* __stdcall D3DXMatrixMultiplyTranspose(
    D3DXMATRIX* output, const D3DXMATRIX* first, const D3DXMATRIX* second);

D3DXMATRIX* __stdcall FUN_00ee6dfe(
    D3DXMATRIX* output, const D3DXMATRIX* first, const D3DXMATRIX* second)
{
    return D3DXMatrixMultiplyTranspose(output, first, second);
}
