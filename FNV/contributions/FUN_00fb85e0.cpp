extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(long volatile*);
extern "C" int __cdecl atexit(void (__cdecl*)(void));
extern "C" void __cdecl FUN_00fdc380(void);
struct Rc_00fb85e0 { int vt; long rc; };
struct File_00fb85e0 { char pad[0x158]; Rc_00fb85e0 r; };
extern File_00fb85e0* DAT_011f8188;
void __cdecl FUN_00fb85e0(void)
{
    DAT_011f8188 = 0;
    if (DAT_011f8188)
    {
        Rc_00fb85e0* r = &DAT_011f8188->r;
        InterlockedIncrement(&r->rc);
    }
    atexit(FUN_00fdc380);
}
