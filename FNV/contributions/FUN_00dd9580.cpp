struct FUN_00dd9580_Interface {
    virtual void unk00();
    virtual void unk04();
    virtual void notify(void*, unsigned short);
};
struct FUN_00dd9580_Service {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00dd9580_Interface* unk10;
};
FUN_00dd9580_Service* __cdecl FUN_00c85750();
struct FUN_00dd9580_Class {
    void* vtable;
    unsigned short unk04;
    void FUN_00dd94c0();
    FUN_00dd9580_Class* FUN_00dd9580(char flags);
};
FUN_00dd9580_Class* FUN_00dd9580_Class::FUN_00dd9580(char flags) {
    FUN_00dd94c0();
    if (flags & 1) {
        FUN_00dd9580_Service* service = FUN_00c85750();
        service->unk10->notify(this, unk04);
    }
    return this;
}
