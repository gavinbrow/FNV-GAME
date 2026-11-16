extern "C" unsigned int __cdecl FUN_00ed0f89();
extern "C" void __cdecl FUN_00ede1fc(unsigned int value);
extern "C" void __cdecl FUN_00ede18d(unsigned int value);
extern "C" void __cdecl FUN_00ec7af9(unsigned int value);
extern "C" void __cdecl FUN_00ed2c6f(unsigned int value);
extern "C" void __cdecl FUN_00ede17e(unsigned int value);
extern "C" void __cdecl FUN_00eddf6c(unsigned int value);
extern "C" void __cdecl FUN_00ec5eec(unsigned int value);
extern "C" void __cdecl FUN_00ed1538(unsigned int value);
extern "C" void __cdecl FUN_00eccedb();
extern "C" unsigned int __cdecl FUN_00ed0f17(void (__cdecl* callback)());
extern unsigned int DAT_011c19c0;
// @fnv 0x00eccf0f
void FUN_00eccf0f()
{
    unsigned int value = FUN_00ed0f89();
    FUN_00ede1fc(value);
    FUN_00ede18d(value);
    FUN_00ec7af9(value);
    FUN_00ed2c6f(value);
    FUN_00ede17e(value);
    FUN_00eddf6c(value);
    FUN_00ec5eec(value);
    FUN_00ed1538(value);
    DAT_011c19c0 = FUN_00ed0f17(&FUN_00eccedb);
}
