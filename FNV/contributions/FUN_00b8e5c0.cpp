extern int DAT_010b17f8;
extern int DAT_010b17d8;
extern void __cdecl FUN_00aa1460(void* object, unsigned int size);

struct FUN_00b8e5c0_class {
    void FUN_00c03a20();
    void* FUN_00b8e5c0(unsigned int flags);
};

void* FUN_00b8e5c0_class::FUN_00b8e5c0(unsigned int flags) {
    *reinterpret_cast<int**>(this) = &DAT_010b17f8;
    *reinterpret_cast<int**>(reinterpret_cast<char*>(this) + 0x6c) = &DAT_010b17d8;
    FUN_00c03a20();
    if (flags & 1) {
        FUN_00aa1460(this, 0xd0);
    }
    return this;
}