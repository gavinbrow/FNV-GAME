extern "C" float DAT_011a9478;
extern "C" float DAT_011a947c;
extern "C" float DAT_011a9480;
extern "C" int DAT_010bf2ac;

struct GravityBaseCtor {
    void FUN_00c31ff0();
};

struct GravityFieldLayout {
    void* vfptr;
    unsigned int unk04, unk08, unk0c, unk10, unk14, unk18;
    unsigned int unk1c, unk20, unk24, unk28, unk2c;
    NiPoint3 originalDirection;
    NiPoint3 normalizedDirection;
};

NiPSysGravityFieldModifier* CtorHelper::FUN_00c2a9e0() {
    reinterpret_cast<GravityBaseCtor*>(this)->FUN_00c31ff0();
    GravityFieldLayout* fields = reinterpret_cast<GravityFieldLayout*>(this);
    fields->vfptr = &DAT_010bf2ac;
    NiPoint3 direction = {-DAT_011a9478, -DAT_011a947c, -DAT_011a9480};
    fields->originalDirection = direction;
    fields->normalizedDirection = direction;
    fields->normalizedDirection.UnitizeVector();
    return reinterpret_cast<NiPSysGravityFieldModifier*>(this);
}