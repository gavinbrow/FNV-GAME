extern char vftable_FUN_00719390;

struct FUN_004037d0_Class
{
    void __thiscall FUN_004037d0();
};

void FUN_00719390_class::FUN_00719230()
{
    reinterpret_cast<void**>(this)[0] = reinterpret_cast<void*>(&vftable_FUN_00719390);
    reinterpret_cast<FUN_004037d0_Class*>(
        reinterpret_cast<char*>(this) + 4)->FUN_004037d0();
}