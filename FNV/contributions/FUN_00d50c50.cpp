extern int DAT_010d0b9c;
extern int DAT_0102e388;

struct RefObj {
    void removeReference();
};

struct Embedded {
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
    void Run();
};

struct FUN_00d50c50 {
    int* vtbl;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    Embedded mSub;
    RefObj** mArr;
    int mCount;
    ~FUN_00d50c50();
};

FUN_00d50c50::~FUN_00d50c50()
{
    vtbl = &DAT_010d0b9c;
    for (int i = 0; i < mCount; ++i) {
        mArr[i]->removeReference();
    }
    mSub.Run();
    vtbl = &DAT_0102e388;
}
