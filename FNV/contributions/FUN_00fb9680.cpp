// @fnv 0x00fb9680
extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdc930();

void __cdecl FUN_00fb9680()
{
    atexit(FUN_00fdc930);
}
