class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267d98;
extern const char DAT_010c5168[];
extern const float DAT_0101df44;
extern void __cdecl FUN_00fde080();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd2d0
void FUN_00fbd2d0()
{
    DAT_01267d98.FUN_0044f440(DAT_010c5168, DAT_0101df44);
    atexit(FUN_00fde080);
}
