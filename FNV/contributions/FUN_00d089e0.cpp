struct Base {
    void __thiscall FUN_00d08570();
};

struct Derived {
    void __thiscall FUN_00d089e0();
};

void __thiscall Derived::FUN_00d089e0()
{
    ((Base*)((char*)this - 0x18))->FUN_00d08570();
}
