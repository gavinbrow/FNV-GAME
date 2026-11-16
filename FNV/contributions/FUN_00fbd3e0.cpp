#include <new>

class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};

extern C4E7770Setting DAT_01267de0;
extern const char DAT_010c5208[];
extern const float DAT_010586fc;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde0e0();

// @fnv 0x00fbd3e0
extern "C" void FUN_00fbd3e0()
{
    new (&DAT_01267de0) C4E7770Setting(DAT_010c5208, DAT_010586fc);
    atexit(FUN_00fde0e0);
}
