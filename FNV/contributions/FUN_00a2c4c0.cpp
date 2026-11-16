typedef void (__cdecl *RuntimeCallback)();

extern unsigned char DAT_011f3696;
extern unsigned char DAT_011f3767;
extern RuntimeCallback DAT_011f3d5c;
extern RuntimeCallback DAT_011f3c3c;
extern RuntimeCallback DAT_011f3bac;
extern RuntimeCallback DAT_011f3dec;
extern RuntimeCallback DAT_011f3a8c;
extern RuntimeCallback DAT_011f39fc;
extern RuntimeCallback DAT_011f396c;
extern RuntimeCallback DAT_011f38dc;
extern RuntimeCallback DAT_011f3ccc;
extern RuntimeCallback DAT_011f3b1c;
extern RuntimeCallback DAT_011f37bc;
extern RuntimeCallback DAT_011f384c;

void __cdecl FUN_00a2c420();
void __cdecl FUN_00a2c490();
void __cdecl FUN_00a2bbf0();
void __cdecl FUN_00a2be60();
void __cdecl FUN_00a2a600();
void __cdecl FUN_00a2bc60();
void __cdecl FUN_00a2bde0();
void __cdecl FUN_00a2c130();
void __cdecl FUN_00a2c1b0();

int __cdecl FUN_00a2c4c0()
{
    if (DAT_011f3696 != 0)
        return 0;

    DAT_011f3696 = 1;
    DAT_011f3d5c = 0;
    DAT_011f3c3c = 0;
    DAT_011f3bac = 0;
    DAT_011f3dec = FUN_00a2c420;
    DAT_011f3a8c = FUN_00a2c490;
    DAT_011f39fc = FUN_00a2bbf0;
    DAT_011f396c = FUN_00a2be60;
    DAT_011f38dc = FUN_00a2a600;
    DAT_011f3767 = 0x40;
    DAT_011f3ccc = FUN_00a2bc60;
    DAT_011f3b1c = FUN_00a2bde0;
    DAT_011f37bc = FUN_00a2c130;
    DAT_011f384c = FUN_00a2c1b0;
    return 1;
}
