struct FUN_00d2dda0_class {
    virtual void finish(int);
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
    void __thiscall FUN_00d2dda0(int value);
};
extern void __cdecl FUN_00da42b0(void*, int, int, int);
void FUN_00d2dda0_class::FUN_00d2dda0(int value) {
    FUN_00da42b0(&unk30, unk0c, unk08, value);
    finish(1);
}


