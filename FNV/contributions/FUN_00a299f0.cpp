#include <string.h>
struct CallbackTypeA;
struct CallbackTypeB;
struct CallbackTypeC;
struct CallbackTypeD;
struct NiColorKey;
struct Helper;

extern unsigned char DAT_011f367f;
extern int DAT_011f3d68;
extern int DAT_011f3c48;
extern int DAT_011f3bb8;
extern int DAT_011f37c8;
extern int DAT_011f3858;
extern void (* volatile DAT_011f3df8)(CallbackTypeA*);
extern void (* volatile DAT_011f3a98)(CallbackTypeA*);
extern void (* volatile DAT_011f3a08)(CallbackTypeB*);
extern void (* volatile DAT_011f3978)(CallbackTypeB*);
extern void (* volatile DAT_011f38e8)(NiColorKey*);
extern unsigned char DAT_011f376a;
extern int* (* volatile DAT_011f3cd8)(int, int, int, int*);
extern bool (* volatile DAT_011f3b28)(const Helper*, const Helper*);
extern void FUN_00e7cd40(CallbackTypeA*);
extern void FUN_00e7cd40(CallbackTypeB*);
extern void FUN_00a29680(CallbackTypeA*);
extern void FUN_00a29680(CallbackTypeB*);
extern void FUN_00a29680(NiColorKey*);
extern int* FUN_00a29690(int, int, int, int*);
extern bool FUN_00a299c0(const Helper*, const Helper*);

int FUN_00a299f0()
{
    if (DAT_011f367f != 0)
        return 0;
    DAT_011f3d68 = 0;
    DAT_011f3c48 = 0;
    DAT_011f3bb8 = 0;
    DAT_011f37c8 = 0;
    DAT_011f3858 = 0;
    memset(&DAT_011f367f, 1, 1);
    DAT_011f3df8 = &FUN_00e7cd40;
    DAT_011f3a98 = &FUN_00a29680;
    DAT_011f3a08 = &FUN_00a29680;
    DAT_011f3978 = &FUN_00e7cd40;
    DAT_011f38e8 = &FUN_00a29680;
    DAT_011f376a = 0x14;
    DAT_011f3cd8 = &FUN_00a29690;
    DAT_011f3b28 = &FUN_00a299c0;
    return 1;
}