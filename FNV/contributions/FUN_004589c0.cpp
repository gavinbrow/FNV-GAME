#include <xmmintrin.h>
struct FUN_004589c0_cls {
    __m128 m_v;
    void FUN_004589c0(float value);
};
void FUN_004589c0_cls::FUN_004589c0(float value)
{
    m_v = _mm_set1_ps(value);
}