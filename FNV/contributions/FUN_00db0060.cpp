#include "h_74712c1d3c73.h"

struct FUN_00db0060_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;

    void __thiscall FUN_00db0060(int* param_2, int param_3);
};

void __thiscall FUN_00db0060_class::FUN_00db0060(int* param_2, int param_3)
{
    int value;

    value = param_2[0];
    unk00 = (((value >> 31) | 0x80000001) ^ value) >> 1;

    value = param_2[1];
    unk04 = (((value >> 31) | 0x80000001) ^ value) >> 1;

    value = param_2[2];
    unk08 = (((value >> 31) | 0x80000001) ^ value) >> 1;

    unk0C = param_3;

    value = param_2[4];
    unk10 = ((((value >> 31) | 0x80000001) ^ value) >> 1) + 1;

    value = param_2[5];
    unk14 = ((((value >> 31) | 0x80000001) ^ value) >> 1) + 1;

    value = param_2[6];
    unk18 = ((((value >> 31) | 0x80000001) ^ value) >> 1) + 1;
}