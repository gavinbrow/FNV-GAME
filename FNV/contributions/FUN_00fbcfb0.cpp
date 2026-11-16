// @fnv 0x00fbcfb0
struct C4E7770Setting
{
    void __thiscall FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267ccc;
extern char DAT_010c4f8c;
extern const float DAT_0101e2bc;
extern "C" void __cdecl FUN_00fddf70();
extern "C" int __cdecl FUN_00ec658f(void (__cdecl* func)());
void __cdecl FUN_00fbcfb0()
{
    DAT_01267ccc.FUN_0044f440(&DAT_010c4f8c, DAT_0101e2bc);
    FUN_00ec658f(&FUN_00fddf70);
}
