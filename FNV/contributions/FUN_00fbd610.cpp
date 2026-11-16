typedef unsigned int (__cdecl* ValueFactory)();

extern ValueFactory DAT_00fdf048;
extern unsigned int DAT_01268108;

extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde150();

// @fnv 0x00fbd610
void FUN_00fbd610()
{
    DAT_01268108 = DAT_00fdf048();
    atexit(FUN_00fde150);
}
