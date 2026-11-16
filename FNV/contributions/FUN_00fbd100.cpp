#include <new>

class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float value);
};

extern C4E7770Setting DAT_01267d20;
extern const char DAT_010c5064[];
extern const float DAT_010586fc;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fddfe0();

// @fnv 0x00fbd100
extern "C" void FUN_00fbd100()
{
    new (&DAT_01267d20) C4E7770Setting(DAT_010c5064, DAT_010586fc);
    atexit(FUN_00fddfe0);
}
