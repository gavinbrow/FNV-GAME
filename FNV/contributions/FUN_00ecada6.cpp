struct Wrapper { unsigned char unknown[20]; unsigned int value; };
extern "C" Wrapper* __cdecl FUN_00ed11de();
// @fnv 0x00ecada6
extern "C" void __cdecl FUN_00ecada6(unsigned int value)
{
    FUN_00ed11de()->value = value;
}