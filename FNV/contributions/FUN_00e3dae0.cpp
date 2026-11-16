#include <xmmintrin.h>
struct FUN_00d21410_Obj {
    void __thiscall FUN_00d21410(int a1, int a2);
};

extern int DAT_010eba5c;
extern int DAT_010eba3c;
extern float DAT_01012068;

struct FUN_00e3dae0_Class {
    void* unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    void* unk10;
    unsigned int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    float unk28;
    volatile unsigned char unk2C;
    unsigned char unk2D;
    unsigned short unk2E;
    unsigned int volatile unk30;
    unsigned int volatile unk34;
    unsigned int volatile unk38;
    unsigned int volatile unk3C;
    unsigned int volatile unk40;
    unsigned int volatile unk44;
    unsigned int volatile unk48;
    unsigned int volatile unk4C;
    unsigned int volatile unk50;
    unsigned int volatile unk54;
    unsigned int volatile unk58;
    unsigned int volatile unk5C;
    unsigned int volatile unk60;
    unsigned int volatile unk64;
    unsigned int volatile unk68;
    unsigned int volatile unk6C;
    unsigned int volatile unk70;
    unsigned int volatile unk74;
    unsigned int volatile unk78;
    unsigned int volatile unk7C;
    unsigned int volatile unk80;
    unsigned int volatile unk84;
    unsigned int volatile unk88;
    unsigned int volatile unk8C;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9C;
    unsigned int unkA0;
    unsigned int unkA4;
    unsigned int unkA8;
    unsigned int unkAC;
    unsigned int unkB0;
    unsigned int unkB4;
    unsigned int unkB8;
    unsigned int unkBC;
    unsigned int volatile unkC0;
    unsigned short volatile unkC4;
    unsigned short volatile unkC6;
    unsigned int volatile unkC8;
    unsigned int volatile unkCC;
    unsigned int volatile unkD0;
    unsigned int unkD4;
    unsigned int unkD8;
    unsigned int unkDC;
    float unkE0;
    float unkE4;
    float unkE8;
    float unkEC;

    FUN_00e3dae0_Class* __thiscall FUN_00e3dae0(float value);
};

FUN_00e3dae0_Class* __thiscall FUN_00e3dae0_Class::FUN_00e3dae0(float value)
{
    reinterpret_cast<FUN_00d21410_Obj*>(this)->FUN_00d21410(0x10, 6);

    unk28 = value;
    unk00 = &DAT_010eba5c;
    unk10 = &DAT_010eba3c;
    unk18 = 0x11;
    unk1C = 0x12;
    unk20 = 0x3FFFF;
    unk24 = 0x1FFFF;
    __m128 constantVector = _mm_set1_ps(DAT_01012068);

    unk30 = 0;
    unk34 = 0;
    unk38 = 0x80000000;
    unk3C = 0;
    unk40 = 0;
    unk44 = 0x80000000;
    unk48 = 0;
    unk4C = 0;
    unk50 = 0x80000000;
    unk54 = 0;
    unk58 = 0;
    unk5C = 0x80000000;
    unk60 = 0;
    unk64 = 0;
    unk68 = 0x80000000;
    unk6C = 0;
    unk70 = 0;
    unk74 = 0x80000000;
    unk78 = 0;
    unk7C = 0;
    unk80 = 0x80000000;
    unk84 = 0;
    unk88 = 0;
    unk8C = 0x80000000;

    unkC0 = 0;
    unkC4 = 0;
    unkC6 = 0;
    unkC8 = 0;
    unkCC = 0;
    unkD0 = 0x80000000;

    unk2C = 6;
    *reinterpret_cast<__m128*>(&unkE0) = constantVector;

    return this;
}
