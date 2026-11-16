struct Entries {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68;
    void** items;
    int count;
};
struct Owner { void FUN_00d69c10(void* item); };
struct View {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18;
    Entries* entries;
    void FUN_00d69f60();
};
void View::FUN_00d69f60() {
    if (entries) {
        for (int i = 0; i < entries->count; ++i)
            reinterpret_cast<Owner*>(reinterpret_cast<char*>(this) - 8)->FUN_00d69c10(entries->items[i]);
    }
}
