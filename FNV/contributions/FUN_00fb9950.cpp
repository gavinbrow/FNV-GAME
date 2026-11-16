extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcca0();

// @fnv 0x00fb9950
extern "C" void FUN_00fb9950()
{
    atexit(FUN_00fdcca0);
}
