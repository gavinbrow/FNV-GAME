#include <xmmintrin.h>
struct FUN_00de90f0_Class {
    __m128 rows[4];
    void FUN_00de90f0(const __m128* source);
};
void FUN_00de90f0_Class::FUN_00de90f0(const __m128* source) {
    rows[0] = source[0];
    rows[1] = source[1];
    rows[2] = source[2];
    rows[3] = source[3];
    volatile float* values = (volatile float*)this;
    values[3] = 0.0f;
    values[7] = 0.0f;
    values[11] = 0.0f;
    values[15] = 1.0f;
}
