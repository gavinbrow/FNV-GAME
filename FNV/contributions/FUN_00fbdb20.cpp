class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01268298;
extern const char DAT_010c73a8[];
extern const float DAT_0101e580;
extern void __cdecl FUN_00fde1f0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbdb20
void __cdecl FUN_00fbdb20()
{
    DAT_01268298.FUN_0044f440(DAT_010c73a8, DAT_0101e580);
    atexit(FUN_00fde1f0);
}
