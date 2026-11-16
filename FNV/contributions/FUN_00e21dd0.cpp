#include <xmmintrin.h>
struct FUN_00e21dd0_cls { __m128 unk00; __m128 unk10; __m128 unk20; void FUN_00e21dd0(__m128* result); };
void FUN_00e21dd0_cls::FUN_00e21dd0(__m128* result) {
    __m128 a = unk10;
    __m128 b = unk20;
    __m128 lower = a;
    lower = _mm_min_ps(lower, b);
    __m128 upper = a;
    upper = _mm_max_ps(upper, b);
    result[0] = lower;
    result[1] = upper;
}
