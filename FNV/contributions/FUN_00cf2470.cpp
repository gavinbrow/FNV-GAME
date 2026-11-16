#include <xmmintrin.h>
struct FnvCpu_FUN_00cf2470_CpuData0 {
    __m128 field00;
    __m128 field10;
};
struct FnvCpu_FUN_00cf2470_CpuObject {
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
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    __m128 fieldb0;
    __m128 fieldc0;
    void FUN_00cf2470(FnvCpu_FUN_00cf2470_CpuData0* input0);
};
void FnvCpu_FUN_00cf2470_CpuObject::FUN_00cf2470(FnvCpu_FUN_00cf2470_CpuData0* input0)
{
    input0->field00 = this->fieldb0;
    input0->field10 = this->fieldc0;
}
