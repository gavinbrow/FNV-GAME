#include "h_74712c1d3c73.h"

struct FUN_00b71b90_VirtualObject {
    void** vtable;
};

typedef void (__thiscall *FUN_00b71b90_VirtualFunction)(FUN_00b71b90_VirtualObject*);

extern FUN_00b71b90_VirtualObject* DAT_011fdd88[0x270 / sizeof(void*)];
extern FUN_00b71b90_VirtualObject* DAT_011fda48[0x340 / sizeof(void*)];

struct FUN_00b71b90_class {
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

    void FUN_00b71b90();
    void FUN_00e814b0();
};

void FUN_00b71b90_class::FUN_00b71b90()
{
    if (unk28 != 0) {
        unsigned int i;
        for (i = 0; i < 0x270 / sizeof(void*); ++i) {
            FUN_00b71b90_VirtualObject* object = DAT_011fdd88[i];
            if (object != 0) {
                FUN_00b71b90_VirtualFunction function =
                    reinterpret_cast<FUN_00b71b90_VirtualFunction>(object->vtable[0xa0 / sizeof(void*)]);
                function(object);
            }
        }
    }

    unsigned int i;
    for (i = 0; i < 0x340 / sizeof(void*); ++i) {
        FUN_00b71b90_VirtualObject* object = DAT_011fda48[i];
        if (object != 0) {
            FUN_00b71b90_VirtualFunction function =
                reinterpret_cast<FUN_00b71b90_VirtualFunction>(object->vtable[0x88 / sizeof(void*)]);
            function(object);
        }
    }

    this->FUN_00e814b0();
}