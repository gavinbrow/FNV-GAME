extern int DAT_01268154;
struct FUN_00c877b0 {
    virtual ~FUN_00c877b0();
};
struct FUN_00c87970 : FUN_00c877b0 {
    virtual ~FUN_00c87970();
    void FUN_00c876a0();
};
FUN_00c87970::~FUN_00c87970() {
    FUN_00c876a0();
    --DAT_01268154;
}