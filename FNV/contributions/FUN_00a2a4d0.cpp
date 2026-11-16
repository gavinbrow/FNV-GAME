#include <string.h>
extern unsigned char DAT_011f3691;
extern unsigned char DAT_011f376b;
extern int DAT_011f3d6c, DAT_011f3c4c, DAT_011f3bbc, DAT_011f37cc;
extern void (* volatile DAT_011f3dfc)();
extern void (* volatile DAT_011f3a9c)();
extern void (* volatile DAT_011f3a0c)();
extern void (* volatile DAT_011f397c)();
extern void (* volatile DAT_011f38ec)();
extern void (* volatile DAT_011f3cdc)();
extern void (* volatile DAT_011f3b2c)();
extern void (* volatile DAT_011f385c)();
void FUN_00a2a320();
void FUN_00a2cfd0();
void FUN_00a2ab10();
void FUN_00a2a1b0();
void FUN_00a2a600();
void FUN_00a2a200();
void FUN_00a2a1a0();
void FUN_00a2a390();
int __cdecl FUN_00a2a4d0() {
    if (DAT_011f3691 != 0)
        return 0;
    DAT_011f3d6c = 0;
    DAT_011f3c4c = 0;
    DAT_011f3bbc = 0;
    DAT_011f37cc = 0;
    memset(&DAT_011f3691, 1, 1);
    DAT_011f3dfc = &FUN_00a2a320;
    DAT_011f3a9c = &FUN_00a2cfd0;
    DAT_011f3a0c = &FUN_00a2ab10;
    DAT_011f397c = &FUN_00a2a1b0;
    DAT_011f38ec = &FUN_00a2a600;
    DAT_011f376b = 0x14;
    DAT_011f3cdc = &FUN_00a2a200;
    DAT_011f3b2c = &FUN_00a2a1a0;
    DAT_011f385c = &FUN_00a2a390;
    return 1;
}
