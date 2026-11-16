extern unsigned int DAT_0126f108[256];
extern "C" int __cdecl atexit(void (__cdecl*)());
extern "C" void __cdecl FUN_00fde2e0();

// @fnv 0x00fc72e0
void __cdecl FUN_00fc72e0()
{
    for (unsigned int i = 0; i < 256; ++i)
    {
        DAT_0126f108[i] = 0;
    }
    atexit(&FUN_00fde2e0);
}
