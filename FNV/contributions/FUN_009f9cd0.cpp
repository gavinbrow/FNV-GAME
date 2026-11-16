#include "h_74712c1d3c73.h"

extern void* (__stdcall *DAT_00fdf460)(unsigned long);
extern void (__stdcall *DAT_00fdf45c)(void*);

int __stdcall FUN_009f9bb0(void* obj, int a);

int __stdcall FUN_009f9cd0(int a)
{
    void* obj = DAT_00fdf460(0x48);
    if (obj == 0)
        return 0;

    if (FUN_009f9bb0(obj, a) < 0) {
        DAT_00fdf45c(obj);
        return 0;
    }

    return (int)obj;
}