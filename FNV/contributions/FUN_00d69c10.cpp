struct Callback {
    virtual void unused();
    virtual void deliver(int entry);
};
struct Entries { int* entries; int count; };
struct Record {
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
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    Entries data48;
};
struct Context {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    Record* special20;
    int unk24;
    Record** list28;
    int count2c;
    int unk30;
    Record** list34;
    int count38;
    void FUN_00c93820(Callback* ptr);
    void FUN_00c93920(int* ptr);
};
struct Dispatcher {
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
    Callback callback28;
    int data2c;
    void FUN_00d69c10(Context* context);
};
void Dispatcher::FUN_00d69c10(Context* context) {
    context->FUN_00c93820(this ? &callback28 : 0);
    context->FUN_00c93920(this ? &data2c : 0);
    for (int i = 0; i < context->count2c; ++i) {
        Entries* current = &context->list28[i]->data48;
        for (int j = 0; j < current->count; ++j) {
            callback28.deliver(current->entries[j]);
        }
    }
    for (int i = 0; i < context->count38; ++i) {
        Entries* current = &context->list34[i]->data48;
        for (int j = 0; j < current->count; ++j) {
            callback28.deliver(current->entries[j]);
        }
    }
    Record* special = context->special20;
    if (special != 0) {
        for (int j = 0; j < special->data48.count; ++j) {
            callback28.deliver(special->data48.entries[j]);
        }
    }
}
