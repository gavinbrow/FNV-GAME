struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d74;
extern const char DAT_010c5114[];
extern "C" void __cdecl FUN_00fde050();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd250
void FUN_00fbd250()
{
    DAT_01267d74.FUN_0044f440(DAT_010c5114, 1.0f);
    atexit(FUN_00fde050);
}
