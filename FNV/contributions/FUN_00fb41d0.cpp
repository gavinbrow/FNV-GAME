class FUN_0076bda0_class
{
public:
    void FUN_00aa50f0(unsigned int value);
};

extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount();
extern FUN_0076bda0_class DAT_011f3560;

// @fnv 0x00fb41d0
void FUN_00fb41d0()
{
    DAT_011f3560.FUN_00aa50f0(GetTickCount());
}
