#include <new>
class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};
extern "C" unsigned char DAT_01267cb4[];
extern "C" char DAT_010c4f3c[];
extern "C" float DAT_01047228;
extern "C" void __cdecl FUN_00fddf50();
extern "C" int __cdecl atexit(void (__cdecl*)());
// @fnv 0x00fbcf50
extern "C" void __cdecl FUN_00fbcf50()
{
    new (DAT_01267cb4) C4E7770Setting(DAT_010c4f3c, DAT_01047228);
    atexit(FUN_00fddf50);
}
