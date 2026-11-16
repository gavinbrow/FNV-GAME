extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();
struct FUN_0076bda0_class { void FUN_00aa50f0(unsigned int count); };
extern FUN_0076bda0_class DAT_011f6394;
// @fnv 0x00fb66d0
void FUN_00fb66d0()
{
    DAT_011f6394.FUN_00aa50f0(GetTickCount());
}
