struct CleanupObject;
typedef void (__stdcall* CleanupFunction)(CleanupObject* object);

extern CleanupObject DAT_011f8170;
extern CleanupFunction DAT_00fdf058;

// @fnv 0x00fdc370
void FUN_00fdc370()
{
    DAT_00fdf058(&DAT_011f8170);
}
