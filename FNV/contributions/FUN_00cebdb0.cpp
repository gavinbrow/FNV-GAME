#include <xmmintrin.h>
struct MotionLike
{
    int unk00;
    float field04;
    int unk08;
    int unk0c;
    __m128 field10;
    __m128 field20;
    __m128 field30;
    __m128 field40;
    __m128 field50;
    __m128 field60;
    __m128 field70;
    __m128 field80;
    float field90;
};
void FUN_00cebdb0(const MotionLike* source, MotionLike* destination)
{
    destination->field90 = source->field04;
    destination->field80 = source->field10;
    destination->field50 = source->field20;
    destination->field60 = source->field30;
    destination->field70 = source->field40;
}
