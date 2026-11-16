#include "h_74712c1d3c73.h"

void __cdecl FUN_00a28720(void*, void*);

void __cdecl FUN_00a2d690(void* a, void* b, unsigned int count)
{
    if (count <= 0)
        return;

    for (unsigned int i = count; i != 0; --i)
    {
        FUN_00a28720(a, b);
        b = static_cast<char*>(b) + 0x14;
    }
}