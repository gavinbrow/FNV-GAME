#include <new>

class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};

extern C4E7770Setting DAT_01267df8;
extern const char DAT_010c5240[];
extern const float DAT_0101622c;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fde100();

// @fnv 0x00fbd440
extern "C" void FUN_00fbd440()
{
    new (&DAT_01267df8) C4E7770Setting(DAT_010c5240, DAT_0101622c);
    atexit(FUN_00fde100);
}
