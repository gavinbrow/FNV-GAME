struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267bd4;
extern const char DAT_010c4af4[];
extern const float DAT_010c4b18;
extern "C" void FUN_00fdde60();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbcd10
void __cdecl FUN_00fbcd10()
{
    DAT_01267bd4.FUN_0044f440(DAT_010c4af4, DAT_010c4b18);
    atexit(&FUN_00fdde60);
}
