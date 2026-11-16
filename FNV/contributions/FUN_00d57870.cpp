#include <xmmintrin.h>
struct FnvCpu_FUN_00d57870_CpuData0 {
    __m128 field00;
};
struct FnvCpu_FUN_00d57870_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    __m128 field30;
    void FUN_00d57870(FnvCpu_FUN_00d57870_CpuData0* input0);
};
void FnvCpu_FUN_00d57870_CpuObject::FUN_00d57870(FnvCpu_FUN_00d57870_CpuData0* input0)
{
    input0->field00 = this->field30;
}
