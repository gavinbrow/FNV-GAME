#include <xmmintrin.h>
struct FnvCpu_FUN_00d54e40_CpuData0 {
    __m128 field00;
};
struct FnvCpu_FUN_00d54e40_CpuObject {
    __m128 field00;
    void FUN_00d54e40(FnvCpu_FUN_00d54e40_CpuData0* input0);
};
void FnvCpu_FUN_00d54e40_CpuObject::FUN_00d54e40(FnvCpu_FUN_00d54e40_CpuData0* input0)
{
    this->field00 = input0->field00;
}
