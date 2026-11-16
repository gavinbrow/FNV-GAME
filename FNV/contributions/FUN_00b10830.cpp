#include "h_74712c1d3c73.h"
void __cdecl FUN_00b10830(unsigned int count)
{
    if (count <= 0u) {
        count = 0;
    } else {
        if (0xffffffffu / count < 4u) {
            FUN_00b108e0_err value;
            unsigned int error = 0;
            value.FUN_00ec78f1(&error);
            value.m_vptr = (void*)DAT_010176f8;
            FUN_00ec7894(&value, DAT_01140ef8);
        }
    }
    DAT_011f6238.FUN_00aa3e40(count << 2);
}