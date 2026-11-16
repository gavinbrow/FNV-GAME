extern unsigned int DAT_0109b220;
extern unsigned int DAT_011f5e9c;
extern unsigned int DAT_011f5ea0;
extern unsigned int DAT_011f5ea4;
extern unsigned int DAT_011f5ea8;

extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdb170();

// @fnv 0x00fb6270
void FUN_00fb6270()
{
    DAT_011f5e9c = DAT_0109b220;
    DAT_011f5ea0 = DAT_0109b220;
    DAT_011f5ea4 = DAT_0109b220;
    DAT_011f5ea8 = DAT_0109b220;
    atexit(FUN_00fdb170);
}
