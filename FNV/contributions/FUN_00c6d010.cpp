#include "h_74712c1d3c73.h"

extern void __cdecl FUN_00cabf50();
void __cdecl operator delete(void*, unsigned int);

struct FUN_00c6d010_Class {
    FUN_00c6d010_Class* __thiscall FUN_00c6d010(unsigned char flags);
};

FUN_00c6d010_Class* __thiscall FUN_00c6d010_Class::FUN_00c6d010(unsigned char flags)
{
    FUN_00cabf50();

    if (flags & 1) {
        ::operator delete(this, 0x3e0);
    }

    return this;
}