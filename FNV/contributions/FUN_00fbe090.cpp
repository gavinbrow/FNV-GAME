#include <xmmintrin.h>

inline __m128 MakeComparisonMask(unsigned int x, unsigned int y, unsigned int z, unsigned int w)
{
    __m128 result;
    result.m128_u32[0] = x;
    result.m128_u32[1] = y;
    result.m128_u32[2] = z;
    result.m128_u32[3] = w;
    return result;
}

extern __m128 DAT_01268460;
extern __m128 DAT_01268470;
extern __m128 DAT_01268480;
extern __m128 DAT_01268490;
extern __m128 DAT_012684a0;
extern __m128 DAT_012684b0;
extern __m128 DAT_012684c0;
extern __m128 DAT_012684d0;
extern __m128 DAT_012684e0;
extern __m128 DAT_012684f0;
extern __m128 DAT_01268500;
extern __m128 DAT_01268510;
extern __m128 DAT_01268520;
extern __m128 DAT_01268530;
extern __m128 DAT_01268540;
extern __m128 DAT_01268550;

// @fnv 0x00fbe090
void FUN_00fbe090()
{
    DAT_01268460 = MakeComparisonMask(0, 0, 0, 0);
    DAT_01268470 = MakeComparisonMask(~0u, 0, 0, 0);
    DAT_01268480 = MakeComparisonMask(0, ~0u, 0, 0);
    DAT_01268490 = MakeComparisonMask(~0u, ~0u, 0, 0);
    DAT_012684a0 = MakeComparisonMask(0, 0, ~0u, 0);
    DAT_012684b0 = MakeComparisonMask(~0u, 0, ~0u, 0);
    DAT_012684c0 = MakeComparisonMask(0, ~0u, ~0u, 0);
    DAT_012684d0 = MakeComparisonMask(~0u, ~0u, ~0u, 0);
    DAT_012684e0 = MakeComparisonMask(0, 0, 0, ~0u);
    DAT_012684f0 = MakeComparisonMask(~0u, 0, 0, ~0u);
    DAT_01268500 = MakeComparisonMask(0, ~0u, 0, ~0u);
    DAT_01268510 = MakeComparisonMask(~0u, ~0u, 0, ~0u);
    DAT_01268520 = MakeComparisonMask(0, 0, ~0u, ~0u);
    DAT_01268530 = MakeComparisonMask(~0u, 0, ~0u, ~0u);
    DAT_01268540 = MakeComparisonMask(0, ~0u, ~0u, ~0u);
    DAT_01268550 = MakeComparisonMask(~0u, ~0u, ~0u, ~0u);
}
