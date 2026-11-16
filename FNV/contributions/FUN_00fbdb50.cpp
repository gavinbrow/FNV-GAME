class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_012682a4;
extern const char DAT_010c73c0[];
extern const float DAT_010223ec;
extern void __cdecl FUN_00fde200();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbdb50
void __cdecl FUN_00fbdb50()
{
    DAT_012682a4.FUN_0044f440(DAT_010c73c0, DAT_010223ec);
    atexit(FUN_00fde200);
}
