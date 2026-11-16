class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267c90;
extern const char DAT_010c4ee4[];
extern void __cdecl FUN_00fddf20();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbcec0
void FUN_00fbcec0()
{
    DAT_01267c90.FUN_0044f440(DAT_010c4ee4, 1.0f);
    atexit(FUN_00fddf20);
}
