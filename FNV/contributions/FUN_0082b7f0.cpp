struct SizedEffect : FUN_0082b7b0 {
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
    int unk48;
    int unk4c;
    __forceinline SizedEffect(void* target, void* value, void* other)
        : FUN_0082b7b0(target, value, other) {}
};
class FUN_0082b7f0_Owner {
public:
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10();
    virtual void v14();
    virtual void v18();
    virtual void v1c();
    virtual void v20();
    virtual void v24();
    virtual void v28();
    virtual void v2c();
    virtual void v30();
    virtual void v34();
    virtual void v38();
    virtual void v3c();
    virtual void v40();
    virtual void v44(void* value);
    void* field04;
    void* field08;
    void* field0c;
    void* field10;
    void* field14;
    void* field18;
    void* field1c;
    void* field20;
    void* field24;
    void* field28;
    FUN_0082b7b0* FUN_0082b7f0();
};
FUN_0082b7b0* FUN_0082b7f0_Owner::FUN_0082b7f0() {
    FUN_0082b7b0* effect = new SizedEffect(field28, field08, field0c);
    v44(effect);
    return effect;
}