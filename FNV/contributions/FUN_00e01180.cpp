struct FUN_00e01140_cls;
struct BufferManager {
    virtual void Unknown0() = 0;
    virtual void Unknown1() = 0;
    virtual void Destroy(FUN_00e01140_cls*, unsigned short) = 0;
    virtual void Unknown3() = 0;
    virtual void Release(unsigned int, unsigned int) = 0;
};
struct BufferContext {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    BufferManager* manager;
};
BufferContext* __cdecl FUN_00c85750();
void __fastcall FUN_00d24660(FUN_00e01140_cls*);

struct FUN_00e01180_cls : FUN_00e01140_cls {
    FUN_00e01180_cls* FUN_00e01180(unsigned int flags);
};
FUN_00e01180_cls* FUN_00e01180_cls::FUN_00e01180(unsigned int flags) {
    BufferContext* context = FUN_00c85750();
    BufferManager* manager = context->manager;
    unk64 = 0;
    if (!(unk68 & 0x80000000)) {
        manager->Release(unk60, (unk68 & 0x3fffffff) * 2);
    }
    unk60 = 0;
    unk68 = 0x80000000;
    FUN_00d24660(this);
    if (flags & 1) {
        BufferContext* context = FUN_00c85750();
        BufferManager* manager = context->manager;
        manager->Destroy(this, (unsigned short)unk04);
    }
    return this;
}