#include <xmmintrin.h>
float __cdecl FUN_00d1bad0(float* a,float* b) {
    __m128 va2 = *reinterpret_cast<__m128*>(a + 4);
    __m128 vb = *reinterpret_cast<__m128*>(b);
    __m128 va = *reinterpret_cast<__m128*>(a);
    __m128 overlap = _mm_and_ps(_mm_cmple_ps(va, vb), _mm_cmple_ps(vb, va2));
    int mask = _mm_movemask_ps(overlap);
    if ((mask & 7) == 7) return 0.0f;
    __m128 clamped = _mm_max_ps(_mm_min_ps(vb, va2), va);
    __m128 delta = _mm_sub_ps(clamped, vb);
    __m128 squared = _mm_mul_ps(delta, delta);
    __m128 y = _mm_shuffle_ps(squared, squared, 0x55);
    __m128 z = _mm_shuffle_ps(squared, squared, 0xaa);
    __m128 sum = _mm_add_ss(y, squared);
    sum = _mm_add_ss(z, sum);
    return _mm_cvtss_f32(sum);
}