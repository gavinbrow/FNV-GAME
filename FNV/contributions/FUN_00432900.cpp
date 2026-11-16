struct FNV_00432900_Data {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual ~FNV_00432900_Data();

    void FUN_00674d70(int flag);
};
struct FNV_00432900_Manager {
    bool FUN_0047c850();
    void FUN_0085a2e0(FNV_00432900_Data* data);
};
extern FNV_00432900_Manager* DAT_011de45c;

struct FUN_00432900 : public BSExtraData {
    FNV_00432900_Data* pData;
    virtual ~FUN_00432900();
};
FUN_00432900::~FUN_00432900() {
    if (pData != 0) {
        pData->FUN_00674d70(1);
        if (DAT_011de45c->FUN_0047c850()) {
            DAT_011de45c->FUN_0085a2e0(pData);
        } else {
            delete pData;
        }
    }
}