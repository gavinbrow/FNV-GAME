struct Part { unsigned int unk00; void FUN_00cb0c00(); };
struct FUN_00e01870_Class;
struct RetPart { virtual void first(); virtual void second(); virtual void Release(FUN_00e01870_Class* owner, unsigned int count); };
struct UnkRet { int unk00; int unk04; int unk08; int unk0c; RetPart* part10; };
struct FUN_00e01870_Class { void* vptr; unsigned short refCount; unsigned short padding; Part part08; Part part0c; Part part10; FUN_00e01870_Class* FUN_00e01870(unsigned int); };
void* DAT_0102e388;
UnkRet* FUN_00c85750();
FUN_00e01870_Class* FUN_00e01870_Class::FUN_00e01870(unsigned int flags) {
    part10.FUN_00cb0c00(); part0c.FUN_00cb0c00(); part08.FUN_00cb0c00();
    vptr = &DAT_0102e388;
    if (flags & 1) {
        UnkRet* object = FUN_00c85750();
        unsigned int count = refCount;
        RetPart* part = object->part10;
        part->Release(this, count);
    }
    return this;
}




