extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdaed0();

// @fnv 0x00fb5780
extern "C" void __cdecl FUN_00fb5780()
{
    atexit(FUN_00fdaed0);
}
