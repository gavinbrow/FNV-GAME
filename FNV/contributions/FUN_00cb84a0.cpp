#include <xmmintrin.h>
struct CC3320Info {
    unsigned int unk00, unk04, unk08, unk0c;
    __m128 vec10, vec20;
    float out30, out34;
};
struct CC3320Source {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    __m128 vec20,vec30;
    unsigned int unk40,unk44,unk48,unk4c;
    float value50,value54;
};
struct CC3320Base {
    int unk00;
    void __thiscall GetInfo(CC3320Info* info);
};
struct FUN_00cb84a0_cls : CC3320Base {
    int unk04;
    CC3320Source* src08;
    void FUN_00cb84a0(CC3320Info* info);
};
void FUN_00cb84a0_cls::FUN_00cb84a0(CC3320Info* info)
{
    GetInfo(info);
    CC3320Source* src = this ? src08 : 0;
    info->vec10 = src->vec20;
    info->vec20 = src->vec30;
    info->out30 = src->value50;
    info->out34 = src->value54;
}