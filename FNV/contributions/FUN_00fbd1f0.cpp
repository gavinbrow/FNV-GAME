class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d5c;
extern const char DAT_010c50dc[];
extern float DAT_01017870;
extern void __cdecl FUN_00fde030();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd1f0
void FUN_00fbd1f0()
{
    DAT_01267d5c.FUN_0044f440(DAT_010c50dc, DAT_01017870);
    atexit(FUN_00fde030);
}
