class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d38;
extern const char DAT_010c5090[];
extern float DAT_01016248;
extern void __cdecl FUN_00fde000();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd160
void FUN_00fbd160()
{
    DAT_01267d38.FUN_0044f440(DAT_010c5090, DAT_01016248);
    atexit(FUN_00fde000);
}
