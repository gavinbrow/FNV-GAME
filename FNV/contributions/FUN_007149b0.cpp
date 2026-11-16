#include <windows.h>

extern int __cdecl FUN_004019a0(void*);

struct FUN_007149b0_StandIn
{
    int unk00;
    int unk04;
    HANDLE unk08;

    int FUN_007149b0(unsigned int a);
};

int FUN_007149b0_StandIn::FUN_007149b0(unsigned int a)
{
    unsigned int result = WaitForSingleObject(unk08, a);

    if (result == WAIT_TIMEOUT)
        return 1;

    return FUN_004019a0(this);
}