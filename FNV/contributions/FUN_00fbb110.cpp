struct RuntimeObject;
typedef void (__stdcall* ObjectInitializer)(RuntimeObject* object);

extern RuntimeObject DAT_01202600;
extern ObjectInitializer DAT_00fdf054;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fdd410();

// @fnv 0x00fbb110
void FUN_00fbb110()
{
    DAT_00fdf054(&DAT_01202600);
    atexit(FUN_00fdd410);
}
