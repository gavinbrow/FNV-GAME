class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_011f9158;
extern const char DAT_010a91c0[];
extern const float DAT_01018204;
extern void __cdecl FUN_00fdc790();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fb9520
void __cdecl FUN_00fb9520()
{
    DAT_011f9158.FUN_0044f440(DAT_010a91c0, DAT_01018204);
    atexit(FUN_00fdc790);
}
