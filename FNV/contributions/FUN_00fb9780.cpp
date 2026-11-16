extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdcb90();

// @fnv 0x00fb9780
extern "C" void FUN_00fb9780()
{
    atexit(FUN_00fdcb90);
}
