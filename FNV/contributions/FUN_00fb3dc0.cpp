struct FUN_00a1c800_MapA
{
    void* vtable;
    char reserved[12];
    unsigned char initialized;
    void __thiscall FUN_00a1eaa0(int type);
};
extern FUN_00a1c800_MapA DAT_011f34e0;
extern const unsigned char DAT_010955c4;
extern const unsigned char DAT_010955a4;
extern const unsigned char DAT_01095584;
extern "C" void __cdecl DAT_00fda7c0();
extern "C" int __cdecl atexit(void (__cdecl *function)());

// @fnv 0x00fb3dc0
void FUN_00fb3dc0()
{
    int constructorLocal;
    int registrationLocal;
    int initializationLocal;
    DAT_011f34e0.FUN_00a1eaa0(37);
    DAT_011f34e0.vtable = const_cast<unsigned char*>(&DAT_010955c4);
    DAT_011f34e0.vtable = const_cast<unsigned char*>(&DAT_010955a4);
    DAT_011f34e0.initialized = 1;
    DAT_011f34e0.vtable = const_cast<unsigned char*>(&DAT_01095584);
    atexit(DAT_00fda7c0);
}