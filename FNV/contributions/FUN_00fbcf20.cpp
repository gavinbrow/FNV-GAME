struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267ca8;
extern const char DAT_010c4f20[];
extern const float DAT_010181bc;
extern "C" void FUN_00fddf40();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbcf20
void __cdecl FUN_00fbcf20()
{
    DAT_01267ca8.FUN_0044f440(DAT_010c4f20, DAT_010181bc);
    atexit(&FUN_00fddf40);
}
