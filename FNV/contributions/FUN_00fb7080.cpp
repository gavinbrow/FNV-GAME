// @fnv 0x00fb7080
// Initialize sentinel and state fields, then register shutdown cleanup.
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00fdb640();
extern "C" unsigned int DAT_011f6df0;
extern "C" unsigned char DAT_011f6df4;
extern "C" unsigned int DAT_011f6df8;
void __cdecl FUN_00fb7080()
{
    DAT_011f6df0 = 0xffffffffu;
    DAT_011f6df4 = 0;
    DAT_011f6df8 = 0;
    FUN_00ec658f(&FUN_00fdb640);
}
