#include <new>

class C4E7770Setting
{
public:
    C4E7770Setting(const char* name, float initialValue) throw();
};
extern C4E7770Setting DAT_01267ce4;
extern const char DAT_010c4fc8[];
extern float DAT_01017870;
extern "C" void __cdecl FUN_00fddf90();
extern "C" int __cdecl atexit(void (__cdecl *callback)());

// @fnv 0x00fbd010
void FUN_00fbd010()
{
    new (&DAT_01267ce4) C4E7770Setting(DAT_010c4fc8, DAT_01017870);
    atexit(FUN_00fddf90);
}
