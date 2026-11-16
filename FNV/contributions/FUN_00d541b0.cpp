#include <xmmintrin.h>
struct FnvCpu_FUN_00d541b0_CpuData0 {
    __m128 field00;
};
struct FnvCpu_FUN_00d541b0_CpuData1 {
    __m128 field00;
};
struct FnvCpu_FUN_00d541b0_CpuObject {
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
    void FUN_00d541b0(FnvCpu_FUN_00d541b0_CpuData0* input0, FnvCpu_FUN_00d541b0_CpuData1* input1);
};
void FnvCpu_FUN_00d541b0_CpuObject::FUN_00d541b0(FnvCpu_FUN_00d541b0_CpuData0* input0, FnvCpu_FUN_00d541b0_CpuData1* input1)
{
    this->field20 = input0->field00;
    this->field30 = input1->field00;
}
