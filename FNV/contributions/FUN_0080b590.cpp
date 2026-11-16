struct EffectStorage : FUN_0080b560 {
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24;
    int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48;
    EffectStorage(MagicCaster* caster, MagicItem* item, EffectItem* effect)
        : FUN_0080b560(caster, item, effect) {}
};
struct FUN_0080b590_vtable {
    void* unk00; void* unk04; void* unk08; void* unk0c; void* unk10; void* unk14;
    void* unk18; void* unk1c; void* unk20; void* unk24; void* unk28; void* unk2c;
    void* unk30; void* unk34; void* unk38; void* unk3c; void* unk40;
    void (__thiscall *ApplyEffect)(void*, FUN_0080b560*);
};
struct FUN_0080b590_object {
    FUN_0080b590_vtable* vtable;
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24;
    int unk28;
    FUN_0080b560* __thiscall FUN_0080b590();
};
FUN_0080b560* __thiscall FUN_0080b590_object::FUN_0080b590() {
    FUN_0080b560* effect = new EffectStorage((MagicCaster*)unk28, (MagicItem*)unk08, (EffectItem*)unk0c);
    vtable->ApplyEffect(this, effect); return effect;
}
