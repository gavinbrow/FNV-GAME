extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdd1f0();

// @fnv 0x00fba960
extern "C" void FUN_00fba960()
{
    atexit(FUN_00fdd1f0);
}
