struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267db0;
extern const char DAT_010c5198[];
extern const float DAT_0101df44;
extern "C" void __cdecl FUN_00fde0a0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd330
void FUN_00fbd330()
{
    DAT_01267db0.FUN_0044f440(DAT_010c5198, DAT_0101df44);
    atexit(FUN_00fde0a0);
}
