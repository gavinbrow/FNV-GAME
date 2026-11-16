#include "h_74712c1d3c73.h"

struct FUN_00692000_data
{
    int values[10];
};

struct FUN_00692000_class
{
    void* unk00;
    void* pBase;

    int __thiscall FUN_006925b0();
    void __thiscall FUN_00692640(void* data, int value);
    int __thiscall FUN_00692000(FUN_00692000_data* source);
};

int __thiscall FUN_00692000_class::FUN_00692000(FUN_00692000_data* source)
{
    int index = FUN_006925b0();

    FUN_00692640((char*)pBase + index * 0x28, 1);

    *((FUN_00692000_data*)((char*)pBase + index * 0x28)) = *source;

    return index;
}