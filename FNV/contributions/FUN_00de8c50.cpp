#include <xmmintrin.h>
struct Owner {
    __m128 row00;
    __m128 row10;
    __m128 row20;
    __m128 row30;
    void FUN_00de8910(float value);
    void FUN_00de8c50(const __m128* source, float value);
};
void Owner::FUN_00de8c50(const __m128* source, float value) {
    row00 = source[0];
    row10 = source[1];
    row20 = source[2];
    row30 = source[3];
    FUN_00de8910(value);
}
