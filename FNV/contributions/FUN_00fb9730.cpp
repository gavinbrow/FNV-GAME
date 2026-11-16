extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcb60();

// @fnv 0x00fb9730
extern "C" void FUN_00fb9730()
{
    atexit(FUN_00fdcb60);
}
