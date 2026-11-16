struct FUN_00c92b00_Entry {
    int unk00, unk04, unk08, unk0c;
    int unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c;
    int unk30, unk34, unk38, unk3c;
    int unk40, unk44;
    int value48;
    int value4c;
};

struct FUN_00c92b00_Class {
    int unk00, unk04, unk08, unk0c;
    int unk10, unk14, unk18, unk1c;
    int unk20, unk24;
    FUN_00c92b00_Entry** entries28;
    int count2c;
    int unk30;
    FUN_00c92b00_Entry** entries34;
    int count38;

    void FUN_00c92a80(int first, int second);
    void FUN_00c92b00();
};

void FUN_00c92b00_Class::FUN_00c92b00()
{
    for (int i = 0; i < count2c; ++i) {
        FUN_00c92b00_Entry* entry = entries28[i];
        FUN_00c92a80(entry->value48, entry->value4c);
    }
    for (int i = 0; i < count38; ++i) {
        FUN_00c92b00_Entry* entry = entries34[i];
        FUN_00c92a80(entry->value48, entry->value4c);
    }
}