#include "h_74712c1d3c73.h"

struct FUN_00acea00_class {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    void* unk18;
    void* unk1c;
    void* unk20;
    int* m_pCounter24;
    void* unk28;
    void* unk2c;
    void* unk30;
    int* m_pCounter34;

    int __thiscall FUN_00acea00();
};

int FUN_00acea00_class::FUN_00acea00()
{
    --(*m_pCounter34);
    return (*m_pCounter24)++;
}