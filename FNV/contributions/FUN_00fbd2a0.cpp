// @fnv 0x00fbd2a0
struct C4E7770Setting
{
    void __thiscall FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267d8c;
extern char DAT_010c5144;
extern const float DAT_010c5164;
extern "C" void __cdecl FUN_00fde070();
extern "C" int __cdecl FUN_00ec658f(void (__cdecl* func)());
void __cdecl FUN_00fbd2a0()
{
    DAT_01267d8c.FUN_0044f440(&DAT_010c5144, DAT_010c5164);
    FUN_00ec658f(&FUN_00fde070);
}
