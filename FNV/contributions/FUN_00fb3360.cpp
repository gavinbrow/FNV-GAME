// @fnv 0x00fb3360
extern "C" int __cdecl atexit(void (__cdecl *function)());
extern "C" void FUN_00fda150();
extern "C" unsigned int DAT_011f3348[2];

void FUN_00fb3360()
{
    DAT_011f3348[0] = 0;
    DAT_011f3348[1] = 0;
    atexit(FUN_00fda150);
}