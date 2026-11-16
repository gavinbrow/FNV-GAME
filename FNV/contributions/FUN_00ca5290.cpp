extern int DAT_012682d8;
struct FUN_00cd2de0 {
    virtual ~FUN_00cd2de0();
};
struct FUN_00ca5290 : FUN_00cd2de0 {
    virtual ~FUN_00ca5290();
    void FUN_00c876a0();
};
FUN_00ca5290::~FUN_00ca5290()
{
    FUN_00c876a0();
    --DAT_012682d8;
}