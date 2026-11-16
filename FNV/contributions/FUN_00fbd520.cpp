extern "C" void* __cdecl FUN_00aa1070(unsigned int size);
extern "C" void* __cdecl FUN_00ec61c0(void* buffer, int value, unsigned int count);
extern "C" int __cdecl atexit(void (__cdecl*)());
extern "C" void __cdecl FUN_00fdde80();
extern unsigned int DAT_011b0304;
extern void* DAT_011b0308;
extern char DAT_011b0300;
extern char DAT_010c4cc4;

// @fnv 0x00fbd520
void __cdecl FUN_00fbd520()
{
    void* block = FUN_00aa1070(0x94);
    unsigned int words = DAT_011b0304;
    DAT_011b0308 = block;
    FUN_00ec61c0(block, 0, words * sizeof(unsigned int));
    *reinterpret_cast<void**>(&DAT_011b0300) = &DAT_010c4cc4;
    atexit(&FUN_00fdde80);
}
