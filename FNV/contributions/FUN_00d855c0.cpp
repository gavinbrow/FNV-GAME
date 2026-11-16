#include "h_74712c1d3c73.h"

struct FUN_00d855c0_Factory {
    virtual void FUN_00d85300_Unused() = 0;
    virtual void* FUN_00d85300(int size);
};

struct FUN_00d855c0_Manager {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d855c0_Factory* unk10;
};

struct FUN_00d855c0_Data {
    int unk00;
    unsigned short unk04;
};

extern "C" FUN_00d855c0_Manager* FUN_00c85750();
extern "C" void* __fastcall FUN_00d84bd0(void* object);
extern "C" void* FUN_00cb1260(void* destination, const void* source, unsigned int size);

void* __cdecl FUN_00d855c0(void* source)
{
    FUN_00d855c0_Manager* manager = FUN_00c85750();
    FUN_00d855c0_Data* data = static_cast<FUN_00d855c0_Data*>(
        manager->unk10->FUN_00d85300(0xB0));

    data->unk04 = 0xB0;

    void* result = FUN_00d84bd0(data);
    FUN_00cb1260(
        static_cast<unsigned char*>(result) + 0x10,
        static_cast<unsigned char*>(source) + 0x10,
        0x94);

    return result;
}