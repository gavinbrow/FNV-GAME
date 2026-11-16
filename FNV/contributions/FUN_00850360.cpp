#include "h_74712c1d3c73.h"

struct FUN_00850360_class : public FUN_0084ff90_shell
{
    void FUN_00850360(char* weapon, int flags);
};

extern "C" __declspec(dllimport) int __stdcall DeleteFileA(char* lpFileName);

void FUN_00850360_class::FUN_00850360(char* weapon, int flags)
{
    char path[260];

    FUN_0084ff90(weapon, path, false);
    DeleteFileA(path);
}