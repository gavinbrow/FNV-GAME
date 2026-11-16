struct Handler { void FUN_00d67020(int); };
struct Collection {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C; int unk50; int unk54; int unk58; int unk5C;
    int unk60; int unk64; int unk68;
    int* items;
    int count;
};
struct Owner {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18;
    Collection* collection;
    void __thiscall FUN_00d67110();
};
void __thiscall Owner::FUN_00d67110() {
    if (collection != 0) {
        int n = collection->count;
        int i = 0;
        if (0 < n) {
            do {
                ((Handler*)((char*)this - 8))->FUN_00d67020(collection->items[i]);
                i = i + 1;
            } while (i < n);
        }
    }
}

