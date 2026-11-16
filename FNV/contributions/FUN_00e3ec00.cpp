#include "h_74712c1d3c73.h"

struct FUN_00e3ec00_Class {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    void* unk18;
    void* unk1c;
    void* unk20;
    void* unk24;
    FUN_00e3ec00_Class** unk28;
    int unk2c;

    int __thiscall FUN_00e3ec00();
};

int __thiscall FUN_00e3ec00_Class::FUN_00e3ec00()
{
    int total = unk2c;
    int i = 0;

    if (unk2c > 0) {
        do {
            total += unk28[i]->FUN_00e3ec00();
            ++i;
        } while (i < unk2c);
    }

    return total;
}