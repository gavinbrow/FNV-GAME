#include <xmmintrin.h>
#include <intrin.h>

extern double DAT_010c9300;

void __cdecl FUN_00dcee10(__m128* first, __m128* second, __m128** output)
{
    __m128* destination = *output;
    destination[0] = first[0];
    destination[1] = first[1];
    destination[2] = first[2];
    destination[3] = second[0];
    destination[4] = second[1];
    destination[5] = second[2];
    _ReadWriteBarrier();
    reinterpret_cast<float*>(destination)[0] += DAT_010c9300;
    reinterpret_cast<unsigned char*>(destination)[0] = 0x1b;
    *output = destination + 6;
}