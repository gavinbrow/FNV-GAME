struct FUN_00a0d5f0_class { FUN_00a0d5f0_class* FUN_00a0d5f0(unsigned int); };
struct InitializationState { void* begin; void* end; void* capacity; };
extern FUN_00a0d5f0_class DAT_011f32f4;
extern unsigned char DAT_011f3304;
extern unsigned char DAT_01094dfc, DAT_01094ddc, DAT_01094dbc, DAT_01094d9c;
extern "C" void __cdecl FUN_00fda000();
extern "C" int __cdecl FUN_00ec658f(void (__cdecl *)());
// @fnv 0x00fb3250
void FUN_00fb3250()
{
    InitializationState initializationState;
    DAT_011f32f4.FUN_00a0d5f0(0x101);
    *reinterpret_cast<const void**>(&DAT_011f32f4) = &DAT_01094dfc;
    *reinterpret_cast<const void**>(&DAT_011f32f4) = &DAT_01094ddc;
    DAT_011f3304 = 1;
    *reinterpret_cast<const void**>(&DAT_011f32f4) = &DAT_01094dbc;
    *reinterpret_cast<const void**>(&DAT_011f32f4) = &DAT_01094d9c;
    FUN_00ec658f(FUN_00fda000);
}