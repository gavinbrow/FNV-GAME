#include <xmmintrin.h>

struct GlobalVectorBlock
{
    __m128 first;
    __m128 second;
    __m128 third;
    __m128 fourth;
};

extern GlobalVectorBlock DAT_011b1c50;
extern GlobalVectorBlock DAT_01268370;

// @fnv 0x00fbdde0
void FUN_00fbdde0()
{
    DAT_01268370.first = DAT_011b1c50.first;
    DAT_01268370.second = DAT_011b1c50.second;
    DAT_01268370.third = DAT_011b1c50.third;
    DAT_01268370.fourth = DAT_011b1c50.fourth;
}
