struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267b34;
extern const char DAT_010c42d8[];
extern const float DAT_010c42e8;
extern "C" void FUN_00fdde00();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbcc10
void __cdecl FUN_00fbcc10()
{
    DAT_01267b34.FUN_0044f440(DAT_010c42d8, DAT_010c42e8);
    atexit(&FUN_00fdde00);
}
