#include <xmmintrin.h>
#include <emmintrin.h>
extern "C" __declspec(align(16)) const __m128 g_signClear;
struct Matrix3 {
    __m128 row0, row1, row2;
    volatile bool* FUN_00cd4e00(volatile bool* result, const Matrix3* other, float epsilon);
};
volatile bool* Matrix3::FUN_00cd4e00(volatile bool* result, const Matrix3* other, float epsilon)
{
    const __m128 limit = _mm_set1_ps(epsilon);
    bool ok = ((_mm_movemask_ps(_mm_cmple_ps(_mm_and_ps(_mm_sub_ps(row0, other->row0), g_signClear), limit)) & 7) == 7) &&
              ((_mm_movemask_ps(_mm_cmple_ps(_mm_and_ps(_mm_sub_ps(row1, other->row1), g_signClear), limit)) & 7) == 7) &&
              ((_mm_movemask_ps(_mm_cmple_ps(_mm_and_ps(_mm_sub_ps(row2, other->row2), g_signClear), limit)) & 7) == 7);
    *result=ok;
    return result;
}