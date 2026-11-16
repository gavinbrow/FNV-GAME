struct FUN_00d655e0_Item { int key; };
struct FUN_00d655e0_class {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    FUN_00d655e0_Item **items30;
    int count34;
    int FUN_00d655e0(int key);
};
int FUN_00d655e0_class::FUN_00d655e0(int key) {
    for (int i = 0; i < count34; ++i)
        if (items30[i]->key == key) return i;
    return -1;
}
