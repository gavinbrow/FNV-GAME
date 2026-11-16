struct Callback {
    virtual void V0();
    virtual void V1();
    virtual void Notify(void* owner, unsigned short value);
    virtual void V3();
    virtual void Release(void* buffer, unsigned int size);
};
struct Manager { int unk00; int unk04; int unk08; int unk0c; Callback* callback; };
Manager* FUN_00c85750();
struct Container {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18;
    void* data1c; int count20; int state24;
    int unk28; int unk2c; int unk30; int unk34; int unk38;
    int unk3c; int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c; int unk60;
    void FUN_00dfb720();
};
struct Record : Container {
    void* data64;
    int unk68;
    int state6c;
    Record* FUN_00dfb7e0(unsigned int flags);
};
Record* Record::FUN_00dfb7e0(unsigned int flags) {
    Manager* manager = FUN_00c85750();
    Callback* callback = manager->callback;
    int size = state6c;
    unk68 = 0;
    if ((size >> 31) == 0)
        callback->Release(data64, size & 0x3fffffff);
    data64 = 0;
    state6c = 0x80000000;
    FUN_00dfb720();
    if (flags & 1) {
        manager = FUN_00c85750();
        manager->callback->Notify(this, *(unsigned short*)((char*)this + 4));
    }
    return this;
}




