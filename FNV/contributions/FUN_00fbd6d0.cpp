struct GlobalState;
typedef void (__stdcall* GlobalInitializer)(GlobalState*);

extern GlobalInitializer DAT_00fdf054;
extern GlobalState DAT_0126813c;

extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde160();

// @fnv 0x00fbd6d0
void FUN_00fbd6d0()
{
    DAT_00fdf054(&DAT_0126813c);
    atexit(FUN_00fde160);
}
