extern int DAT_012683e8;

struct FUN_00c86720 {
    virtual ~FUN_00c86720();
};

struct FUN_00cb83f0 : FUN_00c86720 {
    void FUN_00c876a0();
    virtual ~FUN_00cb83f0();
};

FUN_00cb83f0::~FUN_00cb83f0()
{
    FUN_00c876a0();
    --DAT_012683e8;
}