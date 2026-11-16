#include <xmmintrin.h>

struct GlobalVectorBlock
{
    __m128 first;
    __m128 second;
    __m128 third;
    __m128 fourth;
};

extern GlobalVectorBlock DAT_011b9240;
extern GlobalVectorBlock DAT_0126a3e0;

// @fnv 0x00fc09a0
void FUN_00fc09a0()
{
    DAT_0126a3e0.first = DAT_011b9240.first;
    DAT_0126a3e0.second = DAT_011b9240.second;
    DAT_0126a3e0.third = DAT_011b9240.third;
    DAT_0126a3e0.fourth = DAT_011b9240.fourth;
}
