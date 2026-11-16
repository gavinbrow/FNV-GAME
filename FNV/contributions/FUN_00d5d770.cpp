#include <xmmintrin.h>
struct FnvCpu_FUN_00d5d770_CpuData0 {
    __m128 field00;
    __m128 field10;
    __m128 field20;
    __m128 field30;
};
struct FnvCpu_FUN_00d5d770_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    __m128 field20;
    __m128 field30;
    __m128 field40;
    __m128 field50;
    void FUN_00d5d770(FnvCpu_FUN_00d5d770_CpuData0* input0);
};
void FnvCpu_FUN_00d5d770_CpuObject::FUN_00d5d770(FnvCpu_FUN_00d5d770_CpuData0* input0)
{
    this->field20 = input0->field00;
    this->field30 = input0->field10;
    this->field40 = input0->field20;
    this->field50 = input0->field30;
}
