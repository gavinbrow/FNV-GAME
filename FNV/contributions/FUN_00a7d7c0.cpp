struct NiMemObject {
    static void* operator new(unsigned int size);
};
extern void __fastcall FUN_00a71f60(void* object);
struct FUN_00a71ec0_helper {
    void FUN_00a71ec0(void* clone, void* process);
};
extern const unsigned int DAT_0109dd0c;
struct NiPointLightLayout {
    unsigned int vtable;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    unsigned char unk9c;
    unsigned char unk9d;
    unsigned short unk9e;
    int unkA0;
    int unkA4;
    int unkA8;
    int unkAC;
    int unkB0;
    int unkB4;
    int unkB8;
    int unkBC;
    int unkC0;
    int unkC4;
    int unkC8;
    int unkCC;
    int unkD0;
    int unkD4;
    int unkD8;
    int unkDC;
    int unkE0;
    int unkE4;
    int unkE8;
    int unkEC;
    float unkF0;
    float unkF4;
    float unkF8;
};
struct FUN_00a7d7c0_Class {
    void* FUN_00a7d7c0(void* process);
};
void* FUN_00a7d7c0_Class::FUN_00a7d7c0(void* process) {
    NiPointLightLayout* clone;
    void* allocation = NiMemObject::operator new(0xfc);
    if (allocation) {
        clone = (NiPointLightLayout*)allocation;
        FUN_00a71f60(clone);
        float zero = 0.0f;
        clone->unkF0 = zero;
        clone->vtable = (unsigned int)&DAT_0109dd0c;
        clone->unk9d = 2;
        float one = 1.0f;
        clone->unkF4 = one;
        clone->unkF8 = zero;
    } else {
        clone = 0;
    }
    ((FUN_00a71ec0_helper*)this)->FUN_00a71ec0(clone, process);
    clone->unkF0 = ((NiPointLightLayout*)this)->unkF0;
    clone->unkF4 = ((NiPointLightLayout*)this)->unkF4;
    clone->unkF8 = ((NiPointLightLayout*)this)->unkF8;
    return clone;
}

