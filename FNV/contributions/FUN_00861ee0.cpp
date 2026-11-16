#include "h_4edcbf9f7517.h"

extern "C" char DAT_01081cf0[];
extern "C" void __cdecl FUN_005b5e40(char*, unsigned char, unsigned int);

struct FUN_00861ee0_Class
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    unsigned char unk80;

    void __thiscall FUN_00861ee0(unsigned char value);
};

void __thiscall FUN_00861ee0_Class::FUN_00861ee0(unsigned char value)
{
    if (value < 0x13)
        FUN_005b5e40(DAT_01081cf0, value, 0x13);

    unk80 = value;
}