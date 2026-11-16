extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdafe0();
extern unsigned long DAT_011f49e0;
extern unsigned long DAT_0109b220;

// @fnv 0x00fb5a10
extern "C" void __cdecl FUN_00fb5a10()
{
    DAT_011f49e0 = DAT_0109b220;
    atexit(FUN_00fdafe0);
}
