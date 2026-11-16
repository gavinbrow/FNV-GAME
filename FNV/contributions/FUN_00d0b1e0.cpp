struct FUN_00d0b1e0 {
    void* unk00;
    unsigned short unk04;
    unsigned short unk06;
    void* unk08;
    void* unk0c;
    int unk10;
    struct Base { void FUN_00d0b0d0(); };
    FUN_00d0b1e0(int flags);
};
extern int DAT_0102e388;
extern int DAT_010cb1e4;
extern int DAT_010cb1c4;
extern "C" void* __cdecl FUN_00c85750();
struct CallbackInterface {
    virtual void f0();
    virtual void f1();
    virtual void callback(void*, unsigned short);
};
struct Manager {
    int unk00[4];
    CallbackInterface* interface10;
};
FUN_00d0b1e0::FUN_00d0b1e0(int flags) {
    ((Base*)((char*)this + 0x14))->FUN_00d0b0d0();
    unk0c = &DAT_010cb1c4;
    unk08 = &DAT_010cb1e4;
    unk00 = &DAT_0102e388;
    if (flags & 1) {
        Manager* manager = (Manager*)FUN_00c85750();
        manager->interface10->callback(this, unk04);
    }
}

