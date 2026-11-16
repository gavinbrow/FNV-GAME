#include "h_3213349b7f9c.h"

struct NiAVObject_004b5b00
{
    char unk00[0x34];
    void* m_pExtraDataArray;

    void* FUN_004b5b00(unsigned short index);
};

void* NiAVObject_004b5b00::FUN_004b5b00(unsigned short index)
{
    return reinterpret_cast<char*>(m_pExtraDataArray) + index * 0x30;
}