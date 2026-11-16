#include <xmmintrin.h>
struct __declspec(align(16)) hkMatrix3_Scaled {
    __m128 col0;
    __m128 col1;
    __m128 col2;
    const __m128* __thiscall FUN_00cd4d40(const __m128* scale, const hkMatrix3_Scaled* source);
};
const __m128* hkMatrix3_Scaled::FUN_00cd4d40(const __m128* scale, const hkMatrix3_Scaled* source)
{
    col0 = _mm_mul_ps(_mm_shuffle_ps(*scale, *scale, 0), source->col0);
    col1 = _mm_mul_ps(_mm_shuffle_ps(*scale, *scale, 0), source->col1);
    col2 = _mm_mul_ps(_mm_shuffle_ps(*scale, *scale, 0), source->col2);
    return scale;
}