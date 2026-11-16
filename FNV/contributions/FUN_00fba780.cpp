// @fnv 0x00fba780
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdd070();
void __cdecl FUN_00fba780()
{
    atexit(&FUN_00fdd070);
}
