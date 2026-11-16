#include <xmmintrin.h>

__m128* __stdcall FUN_00c9e3b0(int a, int b, __m128* p)
{
    const __m128 z = _mm_setzero_ps();
    p[0] = z;
    p[1] = z;
    return p;
}