struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267d50;
extern const char DAT_010c50c0[];
extern const float DAT_01021f44;
extern "C" void FUN_00fde020();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbd1c0
void __cdecl FUN_00fbd1c0()
{
    DAT_01267d50.FUN_0044f440(DAT_010c50c0, DAT_01021f44);
    atexit(&FUN_00fde020);
}
