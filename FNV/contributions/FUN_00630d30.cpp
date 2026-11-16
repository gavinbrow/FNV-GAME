#include <xmmintrin.h>
struct FUN_00630d30_cls { __m128 m_vec; void FUN_00630d30(const __m128* a,const __m128* b); };
void FUN_00630d30_cls::FUN_00630d30(const __m128* a,const __m128* b){m_vec = _mm_add_ps(m_vec, _mm_mul_ps(*a,*b));}