extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdd220();

// @fnv 0x00fba970
extern "C" void FUN_00fba970()
{
    atexit(FUN_00fdd220);
}
