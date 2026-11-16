struct C4E7770Setting
{
    void FUN_0044f440(const char* name, float value);
};
extern C4E7770Setting DAT_01267d68;
extern const char DAT_010c50fc[];
extern const float DAT_0101df44;
extern "C" void FUN_00fde040();
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00fbd220
void __cdecl FUN_00fbd220()
{
    DAT_01267d68.FUN_0044f440(DAT_010c50fc, DAT_0101df44);
    atexit(&FUN_00fde040);
}
