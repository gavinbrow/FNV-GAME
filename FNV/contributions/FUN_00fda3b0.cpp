struct CleanupObject;
typedef void (__stdcall *CleanupFunction)(CleanupObject*);

extern CleanupObject DAT_011f33dc;
extern CleanupFunction DAT_00fdf058;

// @fnv 0x00fda3b0
extern "C" void __cdecl FUN_00fda3b0()
{
    DAT_00fdf058(&DAT_011f33dc);
}
