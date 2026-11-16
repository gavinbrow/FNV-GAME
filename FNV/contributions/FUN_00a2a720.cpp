#include <string.h>
extern unsigned char DAT_011f3692;
extern unsigned char DAT_011f3759;
extern int DAT_011f3d24, DAT_011f3c04, DAT_011f3b74;
void FUN_00a2a5a0();
void FUN_00a2d230();
void FUN_00a2d1e0();
void FUN_00a2cc90();
void FUN_00a2a560();
void FUN_00a2d1d0();
void FUN_00a29680();
void FUN_00a2a620();
extern void (*DAT_011f3db4)();
extern void (*DAT_011f3a54)();
extern void (*DAT_011f39c4)();
extern void (*DAT_011f3934)();
extern void (*DAT_011f38a4)();
extern void (*DAT_011f3c94)();
extern void (*DAT_011f3ae4)();
extern void (*DAT_011f3784)();
extern void (*DAT_011f3814)();
int FUN_00a2a720() {
    if (DAT_011f3692) return 0;
    DAT_011f3d24 = 0;
    DAT_011f3c04 = 0;
    DAT_011f3b74 = 0;
    memset(&DAT_011f3692, 1, 1);
    DAT_011f3db4 = FUN_00a2a5a0;
    DAT_011f3a54 = FUN_00a2d230;
    DAT_011f39c4 = FUN_00a2d1e0;
    DAT_011f3934 = FUN_00a2cc90;
    DAT_011f38a4 = FUN_00a2a600;
    DAT_011f3759 = 8;
    DAT_011f3c94 = FUN_00a2a560;
    DAT_011f3ae4 = FUN_00a2d1d0;
    DAT_011f3784 = FUN_00a29680;
    DAT_011f3814 = FUN_00a2a620;
    return 1;
}

