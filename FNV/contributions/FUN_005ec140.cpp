struct FUN_005ec140 {
    virtual void vfn_0();
    unsigned int iIndex;
    StrMem cDisplayText;
    BSSpinLock lock;
    void FUN_005ec1f0();
    ~FUN_005ec140();
};
FUN_005ec140::~FUN_005ec140()
{
    FUN_005ec1f0();
}