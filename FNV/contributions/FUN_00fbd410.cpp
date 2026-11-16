#include <new>

class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};

extern C4E7770Setting DAT_01267dec;
extern const char DAT_010c5224[];
extern const float DAT_01018180;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde0f0();

// @fnv 0x00fbd410
extern "C" void FUN_00fbd410()
{
    new (&DAT_01267dec) C4E7770Setting(DAT_010c5224, DAT_01018180);
    atexit(FUN_00fde0f0);
}
