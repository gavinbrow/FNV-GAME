extern "C" void* __cdecl FUN_00aa1070(unsigned int size);
extern "C" void* __cdecl FUN_00ec61c0(void* buffer, int value, unsigned int count);
extern "C" int __cdecl atexit(void (__cdecl*)());
extern "C" void __cdecl FUN_00fde260();
extern unsigned int DAT_011b2194;
extern void* DAT_011b2198;
extern char DAT_011b2190;
extern char DAT_010c91c8;

// @fnv 0x00fbdff0
void __cdecl FUN_00fbdff0()
{
    void* block = FUN_00aa1070(0x94);
    unsigned int words = DAT_011b2194;
    DAT_011b2198 = block;
    FUN_00ec61c0(block, 0, words * sizeof(unsigned int));
    *reinterpret_cast<void**>(&DAT_011b2190) = &DAT_010c91c8;
    atexit(&FUN_00fde260);
}
