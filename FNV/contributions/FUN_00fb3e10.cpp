extern "C" int __cdecl atexit(void (__cdecl *)(void));
extern void __cdecl DAT_00fda7e0(void);

extern int DAT_01095644;
extern int DAT_01095624;
extern int DAT_01095604;
extern unsigned char DAT_011f3504;

struct FUN_00a1c800_MapB {
    int* vftable;
    void FUN_00a1ede0(int a);
};

extern FUN_00a1c800_MapB DAT_011f34f4;

// @fnv 0x00fb3e10
void FUN_00fb3e10()
{
    void* p0;
    void* p1;
    void* p2;
    DAT_011f34f4.FUN_00a1ede0(0x25);
    DAT_011f34f4.vftable = &DAT_01095644;
    DAT_011f34f4.vftable = &DAT_01095624;
    DAT_011f3504 = 1;
    DAT_011f34f4.vftable = &DAT_01095604;
    atexit(&DAT_00fda7e0);
}
