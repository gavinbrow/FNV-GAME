#include <xmmintrin.h>

struct FnvVehicleState {
    unsigned char active;
    unsigned int flags04;
    float scalar08;
    float scalar0c;
    __m128 vectors10;
    __m128 vectors20;
    __m128 vectors30;
    __m128 vectors40;
    __m128 vectors50;
    __m128 vectors60;
    __m128 vectors70;
};

void __stdcall FUN_00e37160(int, FnvVehicleState* state)
{
    state->scalar08 = 0.0f;
    state->active = 1;
    __m128 zero = _mm_setzero_ps();
    state->vectors30 = zero;
    state->vectors10 = zero;
    state->vectors20 = zero;
    state->vectors40 = zero;
    state->vectors50 = zero;
    state->vectors60 = zero;
    state->vectors70 = zero;
}