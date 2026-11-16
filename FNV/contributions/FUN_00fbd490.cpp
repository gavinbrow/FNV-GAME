struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267e10;
extern const char DAT_010c5278[];
extern const float DAT_010177e8;
extern "C" void __cdecl FUN_00fde120();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbd490
void FUN_00fbd490()
{
    DAT_01267e10.FUN_0044f440(DAT_010c5278, DAT_010177e8);
    atexit(FUN_00fde120);
}
