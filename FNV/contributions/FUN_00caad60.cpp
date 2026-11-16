#include <xmmintrin.h>
struct FUN_00caad60_Class {
    __m128 unk00;
    __m128 value;
    void FUN_00caad60(const __m128* source);
};
void FUN_00caad60_Class::FUN_00caad60(const __m128* source) {
    __m128 incoming = source[0];
    __m128 current = value;
    __m128 high = _mm_unpackhi_ps(incoming, current);
    value = _mm_shuffle_ps(incoming, high, _MM_SHUFFLE(3, 0, 1, 0));
}
