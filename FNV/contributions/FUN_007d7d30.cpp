struct Member_0046ffb0 {
    ~Member_0046ffb0();
};
Member_0046ffb0::~Member_0046ffb0() {}

void __cdecl FUN_007211c0(void*);

struct FUN_007d7d30 {
    Member_0046ffb0 m;
    void FUN_007d81f0();
    virtual ~FUN_007d7d30();
};

FUN_007d7d30::~FUN_007d7d30() {
    this->FUN_007d81f0();
    FUN_007211c0(this);
}
