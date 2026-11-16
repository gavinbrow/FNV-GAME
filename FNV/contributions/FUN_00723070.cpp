
struct FUN_0046ffb0 {
    ~FUN_0046ffb0();
};
struct FUN_00723070 {
    virtual ~FUN_00723070();
    FUN_0046ffb0 cleanupMember;
    void FUN_007230e0();
};
void __cdecl FUN_007211c0(FUN_00723070* self);

FUN_00723070::~FUN_00723070()
{
    FUN_007230e0();
    FUN_007211c0(this);
}
