extern "C" int DAT_0126834c;
struct CAFBase {
    virtual ~CAFBase();
};
struct FUN_00caff80 : CAFBase {
    virtual ~FUN_00caff80();
    void FUN_00c876a0();
};
FUN_00caff80::~FUN_00caff80()
{
    FUN_00c876a0();
    --DAT_0126834c;
}