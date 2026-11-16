struct CleanupObject;
typedef void (__stdcall* CleanupFunction)(CleanupObject* object);

extern CleanupObject DAT_011f8bc4;
extern CleanupFunction DAT_00fdf058;

// @fnv 0x00fdc480
void FUN_00fdc480()
{
    DAT_00fdf058(&DAT_011f8bc4);
}
