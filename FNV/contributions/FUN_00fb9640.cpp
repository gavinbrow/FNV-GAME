// @fnv 0x00fb9640
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc870();
void __cdecl FUN_00fb9640()
{
    atexit(&FUN_00fdc870);
}
