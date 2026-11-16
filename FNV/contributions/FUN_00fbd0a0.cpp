#include <stdlib.h>

class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d08;
extern const char DAT_010c5034[];
extern const float DAT_010223ec;
extern void FUN_00fddfc0();

// @fnv 0x00fbd0a0
void FUN_00fbd0a0()
{
    DAT_01267d08.FUN_0044f440(DAT_010c5034, DAT_010223ec);
    atexit(FUN_00fddfc0);
}
