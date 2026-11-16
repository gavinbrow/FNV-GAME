#include <xmmintrin.h>
struct TransformData
{
    __m128 row0;
    __m128 row1;
    __m128 row2;
    __m128 sourceCopy;
    __m128 output;
    __m128 output2;
    __m128 output3;
    __m128 translation;
    __m128 transform;
    __m128 zero;
};
extern "C" void __cdecl FUN_00cf20d0(const __m128* source, TransformData* data)
{
    data->zero = _mm_setzero_ps();
    data->sourceCopy = *source;
    volatile float* savedLane = (volatile float*)((char*)data + 0x4c);
    float oldW = *savedLane;
    __m128 transform = data->transform;
    __m128 result = _mm_mul_ps(_mm_shuffle_ps(transform, transform, _MM_SHUFFLE(1, 1, 1, 1)), data->row1);
    result = _mm_add_ps(result, _mm_mul_ps(_mm_shuffle_ps(transform, transform, _MM_SHUFFLE(0, 0, 0, 0)), data->row0));
    result = _mm_add_ps(result, _mm_mul_ps(_mm_shuffle_ps(transform, transform, _MM_SHUFFLE(2, 2, 2, 2)), data->row2));
    result = _mm_add_ps(result, *source);
    data->output = result;
    *savedLane = oldW;
    data->output2 = result;
    ((float*)&data->output2)[3] = 0.0f;
    data->output3 = data->translation;
}
