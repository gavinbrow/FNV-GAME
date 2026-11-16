struct GlobalObject_0040c150
{
    void FUN_0040c150(const char* first, const char* second);
};
extern GlobalObject_0040c150 DAT_011d0b84;
extern const char DAT_01056a44;
extern "C" int __cdecl atexit(void (__cdecl *fn)());
extern "C" void __cdecl FUN_00fd0440();

// @fnv 0x00f66520
extern "C" void __cdecl FUN_00f66520()
{
    DAT_011d0b84.FUN_0040c150(&DAT_01056a44, reinterpret_cast<const char*>(-1));
    atexit(FUN_00fd0440);
}