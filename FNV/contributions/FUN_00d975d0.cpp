#include <xmmintrin.h>

extern __m128 g_010d4020;
extern __m128 g_010d4010;

union FloatBits {
    __m128 value;
    unsigned int bits[4];
};

unsigned int __cdecl FUN_00d975d0(const __m128* value) {
    FloatBits converted;
    converted.value = _mm_add_ps(_mm_mul_ps(*value, g_010d4020), g_010d4010);
    return ((converted.bits[3] & 0xffffffc0u) << 18) |
           ((converted.bits[2] & 0x3fc0u) << 10) |
           ((converted.bits[1] & 0x3fc0u) << 2) |
           ((converted.bits[0] >> 6) & 0xffu);
}
