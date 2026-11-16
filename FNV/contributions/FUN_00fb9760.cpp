extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcab0();

// @fnv 0x00fb9760
extern "C" void FUN_00fb9760()
{
    atexit(FUN_00fdcab0);
}
