struct GlobalObject;

extern GlobalObject DAT_010a58c8;
extern GlobalObject DAT_010a58a0;
extern GlobalObject* DAT_011f8ebc;

extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdc720();

// @fnv 0x00fb92a0
void FUN_00fb92a0()
{
    DAT_011f8ebc = &DAT_010a58c8;
    DAT_011f8ebc = &DAT_010a58a0;
    atexit(FUN_00fdc720);
}
