struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267cfc;
extern const char DAT_010c5010[];
extern "C" void FUN_00fddfb0();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbd070
void __cdecl FUN_00fbd070()
{
    DAT_01267cfc.FUN_0044f440(DAT_010c5010, 1.0f);
    atexit(&FUN_00fddfb0);
}
