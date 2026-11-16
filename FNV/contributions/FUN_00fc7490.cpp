extern char* DAT_011f49e0;
extern const char* const DAT_0109b220;
extern char* DAT_0126f750;
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long* value);
extern "C" void __cdecl FUN_00fde370();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fc7490
void FUN_00fc7490()
{
    char* value = DAT_011f49e0;
    if (value != DAT_0109b220)
    {
        InterlockedIncrement(reinterpret_cast<volatile long*>(value) - 2);
    }
    DAT_0126f750 = DAT_011f49e0;
    atexit(FUN_00fde370);
}
