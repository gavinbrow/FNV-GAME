
struct Unknown;
struct FUN_00575650_Result {
    void FUN_0043a3c0(int first, int second);
};
struct FUN_00575650_Class : Unknown {
    virtual int v117();
    virtual int v118();
    virtual int v119();
    virtual int v120();
    virtual int v121();
    virtual int v122();
    virtual int v123();
    virtual int v124();
    virtual int v125();
    int FUN_00575ca0();
    FUN_00575650_Result* FUN_00575650(FUN_00575650_Result* target);
};
FUN_00575650_Result* FUN_00575650_Class::FUN_00575650(FUN_00575650_Result* target) {
    target->FUN_0043a3c0(this->v125(), this->FUN_00575ca0());
    return target;
}
