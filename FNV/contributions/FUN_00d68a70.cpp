struct FUN_00d68a70_class {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int** entries;
    int count;
    int FUN_00d68a70(int key);
};
int FUN_00d68a70_class::FUN_00d68a70(int key)
{
    int limit = count;
    int index = 0;
    if (limit > 0) {
        int** entry = entries;
        do {
            if (**entry == key)
                return index;
            ++index;
            ++entry;
        } while (index < limit);
    }
    return -1;
}
