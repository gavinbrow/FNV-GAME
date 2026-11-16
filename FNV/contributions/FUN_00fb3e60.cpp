extern "C" char DAT_011f3508;
extern "C" char DAT_01095684;
extern "C" void __cdecl FUN_00fda800();
extern "C" int __cdecl atexit(void (__cdecl*)());
struct FUN_00a1eeb0_class
{
    void __thiscall FUN_00a1eeb0(unsigned short first, unsigned short second);
};
// @fnv 0x00fb3e60
void __cdecl FUN_00fb3e60()
{
    unsigned int initializationState;
    reinterpret_cast<FUN_00a1eeb0_class*>(&DAT_011f3508)->FUN_00a1eeb0(0, 1);
    *reinterpret_cast<void**>(&DAT_011f3508) = &DAT_01095684;
    atexit(&FUN_00fda800);
}