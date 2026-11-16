#include "h_74712c1d3c73.h"

struct FUN_00501c10_Class {
    void __thiscall FUN_00501c10(int value);
};

struct FUN_0071df60_Class {
    void* __thiscall FUN_0071e0d0();
    void __thiscall FUN_00559a70(void* value);
    void __thiscall FUN_0071df60(int value);
};

void __thiscall FUN_0071df60_Class::FUN_0071df60(int value)
{
    void* result = this->FUN_0071e0d0();

    reinterpret_cast<FUN_00501c10_Class*>(
        reinterpret_cast<unsigned char*>(result) + 8)->FUN_00501c10(value);

    this->FUN_00559a70(result);
}