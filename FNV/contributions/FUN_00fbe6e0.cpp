#include <xmmintrin.h>

// @fnv 0x00fbe6e0
extern "C" __m128 DAT_011b2e60;
extern "C" __m128 DAT_011b2e70;
extern "C" __m128 DAT_011b2e80;
extern "C" __m128 DAT_01268700;
extern "C" __m128 DAT_01268710;
extern "C" __m128 DAT_01268720;

extern "C" void FUN_00fbe6e0()
{
    DAT_01268700 = DAT_011b2e60;
    DAT_01268710 = DAT_011b2e70;
    DAT_01268720 = DAT_011b2e80;
}