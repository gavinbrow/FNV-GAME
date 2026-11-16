struct FUN_0046ffb0 {
    ~FUN_0046ffb0();
};

struct FUN_007a28c0 {
    virtual ~FUN_007a28c0();
    FUN_0046ffb0 member;
    void FUN_007a2bd0();
};

void __cdecl FUN_007211c0(FUN_007a28c0* object);

FUN_007a28c0::~FUN_007a28c0()
{
    FUN_007a2bd0();
    FUN_007211c0(this);
}
