#include "h_74712c1d3c73.h"

void __cdecl FUN_00aa1460(void* object, unsigned int size);

struct FNVNiD3DPassStandIn {
    void __thiscall FUN_00be0f10();
    void* __thiscall FUN_00be2290(unsigned int flags);
};

void* __thiscall FNVNiD3DPassStandIn::FUN_00be2290(unsigned int flags)
{
    FUN_00be0f10();

    if (flags & 1)
        FUN_00aa1460(this, 0x6c);

    return this;
}