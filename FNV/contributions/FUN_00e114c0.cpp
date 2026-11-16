struct Subobject { virtual void Release(unsigned int flags); };
struct FUN_00e114c0_Class {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c; int unk90; int unk94; int unk98; int unk9c;
    int unkA0; int unkA4; int unkA8; int unkAC; int unkB0; int unkB4; int unkB8; int unkBC;
    int unkC0; int unkC4; int unkC8; int unkCC; int unkD0; int unkD4; int unkD8; int unkDC;
    int unkE0; Subobject* unkE4;
    void FUN_00e114c0();
};
void FUN_00e114c0_Class::FUN_00e114c0() {
    if (unkE4)
        unkE4->Release(1);
    unkE4 = 0;
}
