#include <xmmintrin.h>
struct __declspec(align(16)) FUN_00c74ed0 {
    short channel0,channel1,channel2,channel3,channel4,channel5,channel6,channel7;
    __m128 initialVector;
    float initialValue, factor0, factor1, factor2, factor3, unk34, unk38, unk3c;
    __m128 currentPosition,currentScale,previousPosition,previousScale;
    unsigned char enabled,dirty;
    FUN_00c74ed0();
};
extern "C" float DAT_01012054;
extern "C" __m128 DAT_01267e30;
extern "C" __m128 DAT_012683b0;
FUN_00c74ed0::FUN_00c74ed0() {
    double initial = DAT_01012054;
    channel0 = -1; channel1 = -1; channel2 = -1; channel3 = -1; channel4 = -1;
    _mm_store_ps(reinterpret_cast<float*>(&initialVector), DAT_01267e30);
    initialValue = (float)initial;
    factor3=factor2=factor1=factor0=1.0f;
    currentPosition = DAT_01267e30;
    currentScale = DAT_012683b0;
    previousPosition = DAT_01267e30;
    previousScale = DAT_012683b0;
    enabled = 1; dirty = 0;
}