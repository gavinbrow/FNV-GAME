#include "h_74712c1d3c73.h"

struct FUN_00e54ae0_class
{
    void __thiscall FUN_00e54ae0();
};

struct FUN_00e532b0_class
{
    FUN_00e54ae0_class* __thiscall FUN_00e532b0(void* buffer, void* value);
};

void __cdecl FUN_00e54ba0(void* value, FUN_00e532b0_class* object)
{
    void* buffer[4];
    object->FUN_00e532b0(buffer, value)->FUN_00e54ae0();
}