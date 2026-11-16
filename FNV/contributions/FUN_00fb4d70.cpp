extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdadf0();
extern unsigned long DAT_011f3ec4;
extern unsigned long DAT_0109b220;

// @fnv 0x00fb4d70
extern "C" void __cdecl FUN_00fb4d70()
{
    DAT_011f3ec4 = DAT_0109b220;
    atexit(FUN_00fdadf0);
}
