// @fnv 0x00fb5c40
extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdb060();

void __cdecl FUN_00fb5c40()
{
    atexit(FUN_00fdb060);
}
