#include <xmmintrin.h>
struct FUN_00c7f750_shell { void __thiscall FUN_00c7f750(float* matrix, float* vector); };
void __thiscall FUN_00c7f750_shell::FUN_00c7f750(float* matrix, float* vector)
{
    __m128 v = *(__m128*)vector;
    __m128 y = _mm_mul_ps(_mm_shuffle_ps(v, v, _MM_SHUFFLE(1,1,1,1)), *(__m128*)(matrix + 4));
    __m128 x = _mm_mul_ps(_mm_shuffle_ps(v, v, _MM_SHUFFLE(0,0,0,0)), *(__m128*)matrix);
    __m128 result = _mm_add_ps(y, x);
    __m128 z = _mm_mul_ps(_mm_shuffle_ps(v, v, _MM_SHUFFLE(2,2,2,2)), *(__m128*)(matrix + 8));
    result = _mm_add_ps(result, z);
    *(__m128*)this = result;
}
