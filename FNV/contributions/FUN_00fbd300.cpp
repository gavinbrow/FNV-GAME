#include <new>
class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};
extern "C" unsigned char DAT_01267da4[];
extern "C" char DAT_010c517c[];
extern "C" float DAT_01016264;
extern "C" void __cdecl FUN_00fde090();
extern "C" int __cdecl atexit(void (__cdecl*)());
// @fnv 0x00fbd300
extern "C" void __cdecl FUN_00fbd300()
{
    new (DAT_01267da4) C4E7770Setting(DAT_010c517c, DAT_01016264);
    atexit(FUN_00fde090);
}
