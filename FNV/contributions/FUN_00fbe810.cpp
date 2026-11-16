typedef void* (__stdcall* Initializer)();

extern Initializer DAT_00fdf048;
extern void* DAT_012687c8;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void FUN_00fde270();

// @fnv 0x00fbe810
void FUN_00fbe810()
{
    DAT_012687c8 = DAT_00fdf048();
    atexit(FUN_00fde270);
}
