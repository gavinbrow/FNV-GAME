extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdd010();

// @fnv 0x00fba760
void __cdecl FUN_00fba760()
{
    atexit(FUN_00fdd010);
}
