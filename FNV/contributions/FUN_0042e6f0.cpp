#include "h_64001389b61b.h"

struct FUN_0042e6f0_shell : public BaseExtraList
{
    void FUN_00410020(BSExtraData*, bool);
    void FUN_0042e6f0();
};

void FUN_0042e6f0_shell::FUN_0042e6f0()
{
    BSExtraData* pExtra = GetExtraData(0x8E);
    if (pExtra)
        FUN_00410020(pExtra, true);
}