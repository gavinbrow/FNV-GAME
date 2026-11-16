extern int DAT_010cd45c;
struct Callback { virtual void Invoke(int value); };
struct Receiver {
    virtual void Slot00();
    virtual void Slot04();
    virtual void Slot08();
    virtual void Slot0c();
    virtual void Invoke(void* data, unsigned int size);
};
struct Manager { int unk00; int unk04; int unk08; int unk0c; int unk10; };
Manager* __cdecl FUN_00c85750();
struct FUN_00d0d0d0_cls {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    void* unk30;
    int unk34;
    int unk38;
    struct Subobject {
        int unk00; int unk04; int unk08;
        Callback* unk0c;
        void FUN_00cb1a90(void* managerValue);
        void FUN_00a29680();
    } sub3c;
    void FUN_00cf86d0();
    void FUN_00d0d0d0();
};
void FUN_00d0d0d0_cls::FUN_00d0d0d0() {
    unk00 = (int)&DAT_010cd45c;
    if (sub3c.unk0c)
        sub3c.unk0c->Invoke(1);
    sub3c.FUN_00cb1a90((void*)FUN_00c85750()->unk10);
    sub3c.FUN_00a29680();
    Manager* manager = FUN_00c85750();
    Receiver* writer = (Receiver*)manager->unk10;
    unk34 = 0;
    if ((unk38 & 0x80000000) != 0) goto skip_writer;
    writer->Invoke(unk30, (unk38 & 0x3fffffff) * 0x70);
skip_writer:
    unk30 = 0;
    unk38 = 0x80000000;
    FUN_00cf86d0();
}

