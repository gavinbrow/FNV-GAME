struct SettingState
{
    int value;
    int initializationState;
};
extern "C" SettingState DAT_011f3350;
extern "C" void __cdecl FUN_00fda170();
extern "C" int __cdecl atexit(void (__cdecl*)());
// @fnv 0x00fb3390
extern "C" void __cdecl FUN_00fb3390()
{
    DAT_011f3350.value = 0;
    DAT_011f3350.initializationState = 0;
    atexit(FUN_00fda170);
}
