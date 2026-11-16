struct FUN_00d2b8c0_Class;
struct RetPart { virtual void first(); virtual void second(); virtual void Release(FUN_00d2b8c0_Class* owner, unsigned int count); };
struct UnkRet { int unk00; int unk04; int unk08; int unk0c; RetPart* part10; };
struct FUN_00d2b8c0_Class {
    void* vptr00;
    unsigned short refCount;
    unsigned short unk06;
    void* vptr08;
    int unk0c;
    int unk10;
    void* vptr14;
    FUN_00d2b8c0_Class* FUN_00d2b8c0(unsigned int flags);
};
void* DAT_0102e388;
UnkRet* FUN_00c85750();
FUN_00d2b8c0_Class* FUN_00d2b8c0_Class::FUN_00d2b8c0(unsigned int flags) {
    vptr14 = &DAT_0102e388;
    vptr08 = &DAT_0102e388;
    vptr00 = &DAT_0102e388;
    if (flags & 1) {
        UnkRet* object = FUN_00c85750();
        unsigned int count = refCount;
        RetPart* part = object->part10;
        part->Release(this, count);
    }
    return this;
}
