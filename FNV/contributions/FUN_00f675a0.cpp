struct GlobalObject_0040c150
{
    void FUN_0040c150(const char* first, const char* second);
};
extern GlobalObject_0040c150 DAT_011d1494;
extern const char DAT_010570f8;
extern "C" int __cdecl atexit(void (__cdecl *fn)());
extern "C" void __cdecl FUN_00fd09c0();

// @fnv 0x00f675a0
extern "C" void __cdecl FUN_00f675a0()
{
    DAT_011d1494.FUN_0040c150(&DAT_010570f8, reinterpret_cast<const char*>(-2));
    atexit(FUN_00fd09c0);
}