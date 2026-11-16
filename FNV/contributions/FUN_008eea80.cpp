struct FUN_008eea80_Class {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned short unk24;

    bool FUN_008eea80();
};

bool __thiscall FUN_008eea80_Class::FUN_008eea80()
{
    return (this->unk24 & 1) ? true : false;
}