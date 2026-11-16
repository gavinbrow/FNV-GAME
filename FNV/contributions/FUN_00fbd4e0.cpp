extern "C" void* __cdecl FUN_00aa1070(unsigned int size);
extern "C" void* __cdecl FUN_00ec61c0(void* buffer, int value, unsigned int count);
extern "C" int __cdecl atexit(void (__cdecl*)());
extern "C" void __cdecl FUN_00fdde70();
extern unsigned int DAT_011b02f4;
extern void* DAT_011b02f8;
extern char DAT_011b02f0;
extern char DAT_010c4c84;

// @fnv 0x00fbd4e0
void __cdecl FUN_00fbd4e0()
{
    void* block = FUN_00aa1070(0x94);
    unsigned int words = DAT_011b02f4;
    DAT_011b02f8 = block;
    FUN_00ec61c0(block, 0, words * sizeof(unsigned int));
    *reinterpret_cast<void**>(&DAT_011b02f0) = &DAT_010c4c84;
    atexit(&FUN_00fdde70);
}
