#include <xmmintrin.h>
extern __declspec(align(16)) float DAT_01017d10[4];
extern float DAT_01017d00;
struct FUN_00cf08c0_VectorArray { float* values; int count; };
bool __cdecl FUN_00cf08c0(const FUN_00cf08c0_VectorArray* left, const FUN_00cf08c0_VectorArray* right)
{
    bool equal = left->count == right->count;
    if (equal) {
        int i = 0;
        if (i < left->count) {
            const __m128 absoluteMask = _mm_load_ps(DAT_01017d10);
            for (; i < left->count && equal; ++i) {
                __m128 delta = _mm_sub_ps(_mm_load_ps(left->values + 4*i), _mm_load_ps(right->values + 4*i));
                __m128 tolerance = _mm_load1_ps(&DAT_01017d00);
                __m128 absoluteDelta = _mm_and_ps(delta, absoluteMask);
                int bits = _mm_movemask_ps(_mm_cmple_ps(absoluteDelta, tolerance));
                equal = (bits & 15) == 15;
            }
        }
    }
    return equal;
}