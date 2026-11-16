struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267d44;
extern const char DAT_010c50ac[];
extern const float DAT_01013ea4;
extern "C" void FUN_00fde010();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbd190
void __cdecl FUN_00fbd190()
{
    DAT_01267d44.FUN_0044f440(DAT_010c50ac, DAT_01013ea4);
    atexit(&FUN_00fde010);
}
