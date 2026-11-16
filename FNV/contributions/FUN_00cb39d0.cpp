struct S_00aa3e40 {
    void* __thiscall FUN_00aa3e40(int size);
};

struct S_00cb3860 {
    S_00cb3860();
};

extern S_00aa3e40 DAT_011f6238;

void* __cdecl operator new(unsigned int size, S_00aa3e40& manager,
                           unsigned int allocationSize)
{
    unsigned char* ptr = static_cast<unsigned char*>(
        manager.FUN_00aa3e40(allocationSize));
    unsigned int address = reinterpret_cast<unsigned int>(ptr);
    unsigned char alignment = static_cast<unsigned char>(
        0x10 - (address & 0x0f));
    ptr += alignment;
    ptr[-1] = alignment;
    return ptr;
}

void __cdecl operator delete(void* ptr, S_00aa3e40& manager,
                             unsigned int allocationSize)
{
}

void __cdecl FUN_00cb39d0(void* arg0, void* arg1, void* arg2, void* arg3)
{
    new (DAT_011f6238, 0x50) S_00cb3860();
}
