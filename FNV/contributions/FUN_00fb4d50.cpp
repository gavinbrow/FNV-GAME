extern "C" int __cdecl atexit(void (__cdecl* function)());
extern void __cdecl FUN_00fdadd0();
extern unsigned int DAT_0109b220;
extern unsigned int DAT_011f3ec0;

// @fnv 0x00fb4d50
void FUN_00fb4d50()
{
    DAT_011f3ec0 = DAT_0109b220;
    atexit(FUN_00fdadd0);
}
