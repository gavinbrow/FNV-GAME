#include <xmmintrin.h>
struct FnvCpu_FUN_00df6580_CpuData0 {
    __m128 field00;
    __m128 field10;
    __m128 field20;
    __m128 field30;
};
struct FnvCpu_FUN_00df6580_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    __m128 field10;
    __m128 field20;
    __m128 field30;
    __m128 field40;
    void FUN_00df6580(FnvCpu_FUN_00df6580_CpuData0* input0);
};
void FnvCpu_FUN_00df6580_CpuObject::FUN_00df6580(FnvCpu_FUN_00df6580_CpuData0* input0)
{
    this->field10 = input0->field00;
    this->field20 = input0->field10;
    this->field30 = input0->field20;
    this->field40 = input0->field30;
}
