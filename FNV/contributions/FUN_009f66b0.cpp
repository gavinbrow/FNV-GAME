struct TESPackage { int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c; TESPackage(); ~TESPackage() {} virtual void vfunc(); };
struct NiPoint3 { float x; float y; float z; NiPoint3(); };
struct FUN_006e4080 { int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c; int unk80; int unk84; int unk88; int unk8c; int unk90; int unk94; int unk98; int unk9c; int unka0; int unka4; int unka8; int unkac; int unkb0; int unkb4; int unkb8; int unkbc; int unkc0; int unkc4; int unkc8; int unkcc; int unkd0; int unkd4; int unkd8; int unkdc; int unke0; int unke4; int unke8; FUN_006e4080(); ~FUN_006e4080() {} };
struct FUN_006dae60_shell { int unk00; void* FUN_006dae60(); };
struct FUN_009f66b0 : TESPackage {
    float unk80; int unk84; float unk88; int unk8c; float unk90;
    NiPoint3 unk94;
    int unka0; char unka4; char pad_a5; char pad_a6; char pad_a7;
    FUN_006e4080 unka8;
    FUN_006dae60_shell unk194;
    virtual void vfunc();
    FUN_009f66b0(float, float, float, int, int);
};
FUN_009f66b0::FUN_009f66b0(float a, float b, float c, int d, int e)
    : TESPackage(), unk94(), unka8() {
    unk194.FUN_006dae60();
    unk80 = 0.0f;
    unk84 = 1;
    unk88 = 0.0f;
    unk90 = 0.0f;
    unk94.y = b;
    unk94.x = a;
    unk94.z = c;
    unka0 = d;
    unka4 = 1;
    unk8c = 0;
}
