#include <string.h>
extern unsigned char DAT_011f3690;
extern unsigned char DAT_011f3768;
extern unsigned int DAT_011f3d60, DAT_011f3c40, DAT_011f3bb0;
extern void FUN_00a2a070(); extern void FUN_00a2a0e0(); extern void FUN_00a29cf0();
extern void FUN_00a29db0(); extern void FUN_00a2a600(); extern void FUN_00a29b10();
extern void FUN_00a29c20(); extern void FUN_00a29e00(); extern void FUN_00a29e40();
extern void (*DAT_011f3df0)(); extern void (*DAT_011f3a90)(); extern void (*DAT_011f3a00)();
extern void (*DAT_011f3970)(); extern void (*DAT_011f38e0)(); extern void (*DAT_011f3cd0)();
extern void (*DAT_011f3b20)(); extern void (*DAT_011f37c0)(); extern void (*DAT_011f3850)();
int __cdecl FUN_00a2a110()
{
    if (DAT_011f3690) return 0;
    DAT_011f3d60 = 0;
    DAT_011f3c40 = 0;
    DAT_011f3bb0 = 0;
    memset(&DAT_011f3690, 1, 1);
    DAT_011f3df0 = &FUN_00a2a070;
    DAT_011f3a90 = &FUN_00a2a0e0;
    DAT_011f3a00 = &FUN_00a29cf0;
    DAT_011f3970 = &FUN_00a29db0;
    DAT_011f38e0 = &FUN_00a2a600;
    DAT_011f3768 = 0x48;
    DAT_011f3cd0 = &FUN_00a29b10;
    DAT_011f3b20 = &FUN_00a29c20;
    DAT_011f37c0 = &FUN_00a29e00;
    DAT_011f3850 = &FUN_00a29e40;
    return 1;
}
