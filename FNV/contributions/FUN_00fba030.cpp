// @fnv 0x00fba030
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdce80();
void __cdecl FUN_00fba030()
{
    atexit(&FUN_00fdce80);
}
