struct FrenzyEffectCopy : FrenzyEffectShell {
    int u00; int u04; int u08; int u0c; int u10; int u14; int u18; int u1c; int u20; int u24;
    int u28; int u2c; int u30; int u34; int u38; int u3c; int u40; int u44; int u48;
    unsigned char u4c; unsigned char u4d; unsigned char u4e; unsigned char u4f;
    FrenzyEffectCopy(void* a, void* b, void* c) { FUN_0080dbb0(a,b,c); }
};
struct EffectCloneSource : ValueModifierEffect {
    virtual void V00(); virtual void V04(); virtual void V08(); virtual void V0c();
    virtual void V10(); virtual void V14(); virtual void V18(); virtual void V1c();
    virtual void V20(); virtual void V24(); virtual void V28(); virtual void V2c();
    virtual void V30(); virtual void V34(); virtual void V38(); virtual void V3c();
    virtual void V40(); virtual void OnClone(void* clone);
    unsigned int unk04; void* unk08; void* unk0c;
    int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24;
    void* unk28;
    int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48;
    unsigned char flag4c;
    FrenzyEffectCopy* FUN_0080dbf0();
};
FrenzyEffectCopy* EffectCloneSource::FUN_0080dbf0() {
    FrenzyEffectCopy* copy = new FrenzyEffectCopy(unk28, unk08, unk0c);
    copy->u4c = flag4c;
    OnClone(copy);
    return copy;
}
