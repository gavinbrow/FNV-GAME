struct FUN_00522d80_virtual_object {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual char* v05();
};

struct FUN_00522d80_shell {
    unsigned char field00[0x3C];
    FUN_00522d80_virtual_object field3C;
    unsigned char field40[0x1C0];
    FUN_00522d80_virtual_object field200;

    FUN_00522d80_virtual_object* FUN_00522d80();
};

FUN_00522d80_virtual_object* FUN_00522d80_shell::FUN_00522d80() {
    FUN_00522d80_virtual_object* result = 0;

    if (field200.v05()[0] != 0) {
        result = &field200;
    }

    if (result == 0) {
        result = this ? &field3C : 0;
    }

    return result;
}