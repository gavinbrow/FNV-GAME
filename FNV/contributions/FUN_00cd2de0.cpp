extern int DAT_012686d0;
struct FUN_00c84c50 {
    virtual ~FUN_00c84c50();
};
struct FUN_00cd2de0 : FUN_00c84c50 {
    virtual ~FUN_00cd2de0();
    void FUN_00c876a0();
};
FUN_00cd2de0::~FUN_00cd2de0()
{
    FUN_00c876a0();
    --DAT_012686d0;
}