void __cdecl operator delete(void*, unsigned int);

struct FUN_00c6d320_class {
    void FUN_00c8adf0();
    void* __thiscall FUN_00c6d320(char flags);
};

void* __thiscall FUN_00c6d320_class::FUN_00c6d320(char flags)
{
    FUN_00c8adf0();
    if (flags & 1) {
        operator delete(this, 0x14);
    }
    return this;
}
