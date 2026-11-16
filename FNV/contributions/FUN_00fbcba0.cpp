struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267b10;
extern const char DAT_010c4290[];
extern const float DAT_010c42a8;
extern "C" void FUN_00fdddd0();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbcba0
void __cdecl FUN_00fbcba0()
{
    DAT_01267b10.FUN_0044f440(DAT_010c4290, DAT_010c42a8);
    atexit(&FUN_00fdddd0);
}
