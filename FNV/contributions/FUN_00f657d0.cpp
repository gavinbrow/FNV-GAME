struct GlobalObject_0040c150
{
    void FUN_0040c150(const char* first, const char* second);
};
extern GlobalObject_0040c150 DAT_011d126c;
extern const char DAT_010563b4;
extern "C" int __cdecl atexit(void (__cdecl *fn)());
extern "C" void __cdecl FUN_00fcffd0();

// @fnv 0x00f657d0
extern "C" void __cdecl FUN_00f657d0()
{
    DAT_011d126c.FUN_0040c150(&DAT_010563b4, reinterpret_cast<const char*>(-20));
    atexit(FUN_00fcffd0);
}