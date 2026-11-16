class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267cf0;
extern const char DAT_010c4fec[];
extern const float DAT_01017870;
extern void __cdecl FUN_00fddfa0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd040
void FUN_00fbd040()
{
    DAT_01267cf0.FUN_0044f440(DAT_010c4fec, DAT_01017870);
    atexit(FUN_00fddfa0);
}
