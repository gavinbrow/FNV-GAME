
struct PassBase {
    virtual void OnRelease();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    PassBase(void* owner, unsigned int mode);
};

struct FUN_00be08f0 : PassBase {
    unsigned int unk2c;
    FUN_00be08f0(void* owner);
    virtual void OnRelease();
};

FUN_00be08f0::FUN_00be08f0(void* owner)
    : PassBase(owner, 2), unk2c(0)
{
}
