#include <xmmintrin.h>
// Builds on an earlier contributor's 2026-10-25 reconstruction of this routine.
extern float DAT_010CEB6C;
extern __m128 DAT_01268370;
void __cdecl FUN_00d41930(int, int, int, int);
void __cdecl FUN_00d32ca0(int a, int b, int c, int output)
{
    if ((*reinterpret_cast<const unsigned char*>(c + 11) & 0x20) != 0)
    {
        FUN_00d41930(a, b, c, output);
        return;
    }
    __m128* __restrict p = reinterpret_cast<__m128*>(output);
    float finalComponent = DAT_010CEB6C;
    *p = DAT_01268370;
    reinterpret_cast<float*>(p)[3] = finalComponent;
}