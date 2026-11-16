#include "h_a6f737dbf3bc.h"

struct Entry_005e4810 {
    unsigned char unk00;
    unsigned char unk01;
    unsigned short unk02;
};

struct SomeClass {
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
    unsigned int unk34;
    Entry_005e4810* unk38;
    unsigned char unk3c;

    void FUN_005e4810(unsigned short param1, unsigned char param2);
};

void SomeClass::FUN_005e4810(unsigned short param1, unsigned char param2)
{
    this->unk3c = 0;
    for (unsigned int i = 0; i < this->unk34; i++) {
        if (this->unk38[i].unk02 == param1) {
            this->unk38[i].unk00 = param2;
        }
        this->unk3c = this->unk3c | this->unk38[i].unk00;
    }
}
