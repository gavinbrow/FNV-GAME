struct ResetField { void __thiscall FUN_00e10a00(); };
struct EmbeddedState {
    int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C;
    int unk50; int unk54; int unk58; int unk5C;
    int unk60; int unk64; int unk68; int unk6C;
    int unk70; int unk74; int unk78; int unk7C;
    int unk80; int unk84; int unk88; int unk8C;
    int unk90; int unk94; int unk98; int unk9C;
    int unkA0; int unkA4; int unkA8; int unkAC;
    int unkB0; int unkB4; int unkB8; int unkBC;
};
struct FUN_00de4470_class {
    float unk00; float unk04; float unk08; float unk0C;
    float unk10; float unk14; int unk18; float unk1C;
    EmbeddedState state;
    ResetField reset;
    void* __thiscall FUN_00de4470();
};
void* __thiscall FUN_00de4470_class::FUN_00de4470() {
    reset.FUN_00e10a00();
    unk08 = 0.25f;
    unk18 = 24;
    unk04 = 0.75f;
    unk00 = 1.0f;
    unk0C = 1.0f;
    unk10 = 0.5f;
    unk14 = 0.25f;
    unk1C = 1.0f;
    return this;
}
