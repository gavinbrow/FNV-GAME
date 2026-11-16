struct FUN_00528cb0_Guard {
    int value;
    FUN_00528cb0_Guard(int value);
    ~FUN_00528cb0_Guard();
    unsigned int FUN_00559450(int flag);
};
struct FUN_0044ac40_Service {
    void __thiscall FUN_0044ac40(unsigned int value);
};
extern FUN_0044ac40_Service* DAT_01202d98;
struct FUN_00906050_Class {
    virtual void v0();
    virtual void v1();
    virtual unsigned char v2(int value, FUN_00528cb0_Guard* guard);
    void __thiscall FUN_009060f0(int value);
    void __thiscall FUN_00906050(int value);
};
void FUN_00906050_Class::FUN_00906050(int value) {
    FUN_00528cb0_Guard guard(0);
    if (v2(value, &guard)) {
        FUN_009060f0(value);
        DAT_01202d98->FUN_0044ac40(guard.FUN_00559450(0));
    }
}