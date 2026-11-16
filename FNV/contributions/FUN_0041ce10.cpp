#include "h_64001389b61b.h"

struct FUN_0041ce10_shell : public ExtraDataList
{
    void FUN_0041ce10(Script* apScript);
};

void FUN_0041ce10_shell::FUN_0041ce10(Script* apScript)
{
    ExtraScript* pExtra = static_cast<ExtraScript*>(GetExtraData(0x1A));
    if (pExtra != 0 && pExtra->pScript == apScript)
        pExtra->pScript = 0;
}