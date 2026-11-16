class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d2c;
extern const char DAT_010c5078[];
extern void __cdecl FUN_00fddff0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd130
void FUN_00fbd130()
{
    DAT_01267d2c.FUN_0044f440(DAT_010c5078, 1.0f);
    atexit(FUN_00fddff0);
}
