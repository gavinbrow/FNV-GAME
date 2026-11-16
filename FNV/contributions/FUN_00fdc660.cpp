void __cdecl operator delete(void* memory);

extern unsigned short DAT_011f8d84;
extern unsigned char* DAT_011f8d88;

// @fnv 0x00fdc660
void FUN_00fdc660()
{
    DAT_011f8d84 = 0;
    delete DAT_011f8d88;
    DAT_011f8d88 = 0;
}
