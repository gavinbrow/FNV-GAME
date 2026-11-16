namespace fnv_00ae8f20
{
    void __cdecl _NiFreeAlias(void* buffer);
}

extern const void* DAT_011f3508;
extern void* DAT_011f350c;

extern const unsigned char DAT_0109568c;

// @fnv 0x00fda800
extern "C" void __cdecl FUN_00fda800()
{
    DAT_011f3508 = &DAT_0109568c;
    void* buffer = DAT_011f350c;
    fnv_00ae8f20::_NiFreeAlias(buffer);
}
