class S00b02640
{
public:
    void DestroyAndFreeLibraries();
};

extern "C" S00b02640 DAT_011f8270;

// @fnv 0x00fdc400
void __cdecl FUN_00fdc400()
{
    DAT_011f8270.DestroyAndFreeLibraries();
}
