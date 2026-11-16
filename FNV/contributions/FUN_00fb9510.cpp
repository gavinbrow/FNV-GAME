extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdc750();

// @fnv 0x00fb9510
extern "C" void FUN_00fb9510()
{
    atexit(FUN_00fdc750);
}
