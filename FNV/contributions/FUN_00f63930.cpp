struct GlobalObject_0040c150
{
    void FUN_0040c150(const char* first, const char* second);
};
extern GlobalObject_0040c150 DAT_011cf788;
extern const char DAT_010551c8;
extern "C" int __cdecl atexit(void (__cdecl *fn)());
extern "C" void __cdecl FUN_00fcf5d0();

// @fnv 0x00f63930
extern "C" void __cdecl FUN_00f63930()
{
    DAT_011cf788.FUN_0040c150(&DAT_010551c8, reinterpret_cast<const char*>(-50));
    atexit(FUN_00fcf5d0);
}