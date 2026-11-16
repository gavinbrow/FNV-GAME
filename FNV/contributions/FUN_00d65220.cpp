struct FUN_00d65220_Interface {
    virtual void unk00();
    virtual void unk04();
    virtual void notify(void*, unsigned short);
};
struct FUN_00d65220_Service {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d65220_Interface* unk10;
};
FUN_00d65220_Service* __cdecl FUN_00c85750();
struct FUN_00d65220_Class {
    void* vtable;
    unsigned short unk04;
    void FUN_00d64ae0();
    FUN_00d65220_Class* FUN_00d65220(char flags);
};
FUN_00d65220_Class* FUN_00d65220_Class::FUN_00d65220(char flags) {
    FUN_00d64ae0();
    if (flags & 1) {
        FUN_00d65220_Service* service = FUN_00c85750();
        service->unk10->notify(this, unk04);
    }
    return this;
}
