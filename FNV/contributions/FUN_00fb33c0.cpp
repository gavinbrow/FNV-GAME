// @fnv 0x00fb33c0
// Initialize a global setting and register its destruction at process exit.
struct SettingInitializer
{
    void FUN_00a0d8e0(int);
};
extern "C" int __cdecl FUN_00ec658f(void (__cdecl*)());
extern "C" void __cdecl FUN_00fda190();
extern "C" unsigned int DAT_011f3358;
extern "C" unsigned int DAT_01094e7c;
void __cdecl FUN_00fb33c0()
{
    unsigned int x;
    unsigned int y;
    unsigned int z;
    reinterpret_cast<SettingInitializer*>(&DAT_011f3358)->FUN_00a0d8e0(0x25);
    DAT_011f3358 = reinterpret_cast<unsigned int>(&DAT_01094e7c);
    FUN_00ec658f(&FUN_00fda190);
}
