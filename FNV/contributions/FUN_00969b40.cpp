extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount(void);
extern unsigned int DAT_011e07b4;

struct GameTimeSource {
    unsigned int* FUN_0043d4d0();
};
extern GameTimeSource DAT_011d3570;

struct TimeCounter {
    unsigned int FUN_00969b40();
};

unsigned int TimeCounter::FUN_00969b40()
{
    return DAT_011e07b4 + *DAT_011d3570.FUN_0043d4d0()
           - GetTickCount() / 1000u;
}