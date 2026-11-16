#include <stdlib.h>

class FUN_00db7ab0_class
{
public:
    void* FUN_00db7ab0(void* argument1, void* argument2, void* argument3);
};

extern unsigned char DAT_010d59b8;
extern unsigned char DAT_010cf778;
extern FUN_00db7ab0_class DAT_01268b0c;
extern "C" void FUN_00fde290();

// @fnv 0x00fbeb70
void FUN_00fbeb70()
{
    DAT_01268b0c.FUN_00db7ab0(&DAT_010d59b8, reinterpret_cast<void*>(-1), &DAT_010cf778);
    atexit(FUN_00fde290);
}
