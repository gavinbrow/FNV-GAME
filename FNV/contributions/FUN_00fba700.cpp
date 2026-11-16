// @fnv 0x00fba700
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdcfc0();
void __cdecl FUN_00fba700()
{
    atexit(&FUN_00fdcfc0);
}
