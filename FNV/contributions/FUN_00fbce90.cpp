// @fnv 0x00fbce90
struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};

extern "C" char DAT_01267c84;
extern "C" char DAT_010c4ec4;
extern "C" void FUN_00fddf10();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fbce90()
{
    reinterpret_cast<C4E7770Setting*>(&DAT_01267c84)->FUN_0044f440(
        &DAT_010c4ec4, 0.0f);
    atexit(&FUN_00fddf10);
}