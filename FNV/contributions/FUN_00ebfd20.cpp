#include "h_74712c1d3c73.h"

struct Interface_00ebfd20 {
    virtual void Unk00() = 0;
    virtual void Unk04() = 0;
    virtual unsigned long __stdcall Release() = 0;
};

struct Struct_00ebfd20 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    unsigned int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    Interface_00ebfd20** unk40;
};

struct Standin_011f6238 {
    void FUN_00aa4060(void* param_1);
};

extern Standin_011f6238 DAT_011f6238;

void __cdecl FUN_00ebfd20(Struct_00ebfd20* param_1)
{
    if (param_1->unk40 != 0) {
        for (unsigned int i = 0; i < param_1->unk20; i++) {
            if (param_1->unk40[i] != 0) {
                param_1->unk40[i]->Release();
            }
        }
        param_1->unk40 = 0;
        DAT_011f6238.FUN_00aa4060(param_1);
    }
}
