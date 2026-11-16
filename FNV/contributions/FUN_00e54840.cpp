#include "h_74712c1d3c73.h"

int __cdecl FUN_00e54840(float** param_1, int param_2)
{
    int result = 0;

    for (int i = 0; i < param_2; ++i)
    {
        if ((*param_1)[i] != (*param_1)[i + 1])
        {
            ++result;
        }
    }

    return result + 1;
}