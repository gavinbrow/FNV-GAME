struct CleanupObject;
typedef void (__stdcall* CleanupFunction)(CleanupObject* object);

extern CleanupObject DAT_011f8254;
extern CleanupFunction DAT_00fdf058;

// @fnv 0x00fdc3f0
void FUN_00fdc3f0()
{
    DAT_00fdf058(&DAT_011f8254);
}
