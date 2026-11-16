#include "h_74712c1d3c73.h"

struct FUN_00a72550_Class {
    struct Item {
        int unk00;
        int unk04;
        int unk08;
    };
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    Item** unk20;
    unsigned short unk24;
    unsigned short unk26;

    int FUN_00a72550(unsigned int index, int* out);
};

int FUN_00a72550_Class::FUN_00a72550(unsigned int index, int* out)
{
    *out = 0;
    if (index >= unk26)
        return 0;

    Item* item = unk20[index];
    if (!item)
        return 0;

    *out = item->unk04;
    return item->unk08;
}
