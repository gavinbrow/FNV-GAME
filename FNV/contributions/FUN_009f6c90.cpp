struct FUN_0045cec0 { void* FUN_00559450(); void FUN_0066b0d0(int release); ~FUN_0045cec0(); };
struct Reference {
    virtual void slot_000();
    virtual void slot_004();
    virtual void slot_008();
    virtual void slot_00c();
    virtual void slot_010();
    virtual void slot_014();
    virtual void slot_018();
    virtual void slot_01c();
    virtual void slot_020();
    virtual void slot_024();
    virtual void slot_028();
    virtual void slot_02c();
    virtual void slot_030();
    virtual void slot_034();
    virtual void slot_038();
    virtual void slot_03c();
    virtual void slot_040();
    virtual void slot_044();
    virtual void slot_048();
    virtual void slot_04c();
    virtual void slot_050();
    virtual void slot_054();
    virtual void slot_058();
    virtual void slot_05c();
    virtual void slot_060();
    virtual void slot_064();
    virtual void slot_068();
    virtual void slot_06c();
    virtual void slot_070();
    virtual void slot_074();
    virtual void slot_078();
    virtual void slot_07c();
    virtual void slot_080();
    virtual void slot_084();
    virtual void slot_088();
    virtual void slot_08c();
    virtual void slot_090();
    virtual void slot_094();
    virtual void slot_098();
    virtual void slot_09c();
    virtual void slot_0a0();
    virtual void slot_0a4();
    virtual void slot_0a8();
    virtual void slot_0ac();
    virtual void slot_0b0();
    virtual void slot_0b4();
    virtual void slot_0b8();
    virtual void slot_0bc();
    virtual void slot_0c0();
    virtual void slot_0c4();
    virtual void slot_0c8();
    virtual void slot_0cc();
    virtual void slot_0d0();
    virtual void slot_0d4();
    virtual void slot_0d8();
    virtual void slot_0dc();
    virtual void slot_0e0();
    virtual void slot_0e4();
    virtual void NotifyOwner(void* owner);
    Reference* FUN_009611e0();
};
struct FUN_009f6c90 {
void* unk00; void* unk04; void* unk08; void* unk0c;
void* unk10; void* unk14; void* unk18; void* unk1c;
void* unk20; void* unk24; void* unk28; void* unk2c;
FUN_0045cec0 ref; ~FUN_009f6c90();
};
FUN_009f6c90::~FUN_009f6c90() {
    if (ref.FUN_00559450()) {
        if (((Reference*)ref.FUN_00559450())->FUN_009611e0()) {
            ((Reference*)ref.FUN_00559450())->FUN_009611e0()->NotifyOwner(ref.FUN_00559450());
        }
        ref.FUN_0066b0d0(0);
    }
}