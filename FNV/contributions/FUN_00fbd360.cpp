struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267dbc;
extern const char DAT_010c51b4[];
extern const float DAT_01016248;
extern "C" void __cdecl FUN_00fde0b0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd360
void FUN_00fbd360()
{
    DAT_01267dbc.FUN_0044f440(DAT_010c51b4, DAT_01016248);
    atexit(FUN_00fde0b0);
}
