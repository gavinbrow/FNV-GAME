struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267dd4;
extern const char DAT_010c51ec[];
extern const float DAT_01050c48;
extern "C" void __cdecl FUN_00fde0d0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd3b0
void FUN_00fbd3b0()
{
    DAT_01267dd4.FUN_0044f440(DAT_010c51ec, DAT_01050c48);
    atexit(FUN_00fde0d0);
}
