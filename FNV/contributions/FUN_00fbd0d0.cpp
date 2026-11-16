// @fnv 0x00fbd0d0
class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};
extern "C" const float DAT_01018f7c;
extern "C" const char DAT_010c504c;
extern "C" C4E7770Setting DAT_01267d14;
extern "C" void __cdecl FUN_00fddfd0();
extern "C" int __cdecl FUN_00ec658f(void (__cdecl *)());

extern "C" void __cdecl FUN_00fbd0d0()
{
    DAT_01267d14.FUN_0044f440(&DAT_010c504c, DAT_01018f7c);
    FUN_00ec658f(FUN_00fddfd0);
}
