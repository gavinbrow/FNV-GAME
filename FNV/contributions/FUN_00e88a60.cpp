struct FUN_00e88a60_Renderer {
    virtual void f00(int, int);
    virtual void f01(int, int);
    virtual void f02(int, int);
    virtual void f03(int, int);
    virtual void f04(int, int);
    virtual void f05(int, int);
    virtual void f06(int, int);
    virtual void f07(int, int);
    virtual void f08(int, int);
    virtual void f09(int, int);
    virtual void f10(int, int);
    virtual void f11(int, int);
    virtual void f12(int, int);
    virtual void f13(int, int);
    virtual void f14(int, int);
    virtual void f15(int, int);
    virtual void f16(int, int);
    virtual void f17(int, int);
    virtual void f18(int, int);
    virtual void f19(int, int);
    virtual void f20(int, int);
    virtual void f21(int, int);
    virtual void f22(int, int);
    virtual void f23(int, int);
    virtual void f24(int, int);
    virtual void f25(int, int);
    virtual void f26(int, int);
    virtual void f27(int, int);
    virtual void f28(int, int);
    virtual void f29(int, int);
    virtual void f30(int, int);
    virtual void f31(int, int);
    virtual void f32(int, int);
    virtual void f33(int, int);
    virtual void f34(int, int);
    virtual void f35(int, int);
    virtual void f36(int, int);
    virtual void f37(int, int);
    virtual void f38(int, int);
    virtual void f39(int, int);
    virtual void f40(int, int);
    virtual void f41(int, int);
    virtual void f42(int, int);
    virtual void f43(int, int);
    virtual void f44(int, int);
    virtual void f45(int, int);
    virtual void f46(int, int);
    virtual void f47(int, int);
    virtual void f48(int, int);
    virtual void f49(int, int);
    virtual void f50(int, int);
    virtual void f51(int, int);
    virtual void f52(int, int);
    virtual void f53(int, int);
    virtual void f54(int, int);
    virtual void f55(int, int);
    virtual void f56(int, int);
    virtual void f57(int, int);
    virtual void f58(int, int);
    virtual void f59(int, int);
    virtual void f60(int, int);
    virtual void f61(int, int);
    virtual void f62(int, int);
    virtual void f63(int, int);
    virtual void f64(int, int);
    virtual void __stdcall FUN_00e88a60(int, int);
};

struct FUN_00e88a60_Class {
    char m_pad[0x10a0];
    int m_10a0[16];
    char m_pad2[0x18];
    FUN_00e88a60_Renderer* m_10f8;

    void __thiscall FUN_00e88a60(int value);
};

void __thiscall FUN_00e88a60_Class::FUN_00e88a60(int value)
{
    if (value != 0) {
        unsigned int index;
        for (index = 0; index < 16; ++index) {
            if (m_10a0[index] == value) {
                m_10a0[index] = 0;
                m_10f8->FUN_00e88a60(static_cast<int>(index), 0);
            }
        }
    }
}