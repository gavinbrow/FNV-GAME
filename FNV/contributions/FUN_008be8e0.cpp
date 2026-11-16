class FieldValues {
public:
    unsigned int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24;
    float value28;
    bool FUN_00884e90(unsigned int mask);
};
struct ValueProvider {
    virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3(); virtual void v4();
    virtual void v5(); virtual void v6(); virtual void v7(); virtual void v8(); virtual void v9();
    virtual float GetValue();
};
struct FUN_008be8e0_cls {
    unsigned int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,unk28;
    FieldValues* values2c;
    float FUN_008be8e0(ValueProvider* source);
};
float FUN_008be8e0_cls::FUN_008be8e0(ValueProvider* source)
{
    return values2c == 0
        ? 0.0f
        : (!values2c->FUN_00884e90(0x100)
            ? values2c->value28
            : source->GetValue());
}