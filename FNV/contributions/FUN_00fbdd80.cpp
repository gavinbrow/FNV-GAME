typedef void* (__stdcall* Initializer)();

extern Initializer DAT_00fdf048;
extern void* DAT_0126835c;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void FUN_00fde250();

// @fnv 0x00fbdd80
void FUN_00fbdd80()
{
    DAT_0126835c = DAT_00fdf048();
    atexit(FUN_00fde250);
}
