struct Limits {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2c;
    unsigned int unk30; unsigned int unk34; unsigned int unk38;
};
void __stdcall FUN_00e06b50(Limits* first, Limits* second, Limits* third) {
    third->unk34 = second->unk34;
    unsigned int value = third->unk38 - second->unk34 + first->unk24;
    if (value < 0x20)
        return;
    if (third->unk38 <= 2 && value < 0x100)
        return;
    if (third->unk38 < 0x20 && second->unk38 >= 0x20) {
        third->unk34 = first->unk24;
        return;
    }
    if (third->unk38 < 0x100 && second->unk38 >= 0x100) {
        third->unk34 = first->unk24;
        return;
    }
    if (third->unk38 >= 0x10000)
        return;
    if (second->unk38 >= 0x10000)
        third->unk34 = first->unk24;
}

