struct BaseZero {
    virtual void v0();
    int unk04;
    int unk08;
    ~BaseZero();
};
struct BaseTwelve {
    virtual void v0();
    ~BaseTwelve();
    void FUN_00406340();
};
struct FUN_0040a140 : BaseZero, BaseTwelve {
    ~FUN_0040a140();
};
FUN_0040a140::~FUN_0040a140() {
    BaseTwelve::FUN_00406340();
}