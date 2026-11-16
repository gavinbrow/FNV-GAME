class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_012682b0;
extern const char DAT_010c73dc[];
extern const float DAT_0101712c;
extern void __cdecl FUN_00fde210();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbdb80
void __cdecl FUN_00fbdb80()
{
    DAT_012682b0.FUN_0044f440(DAT_010c73dc, DAT_0101712c);
    atexit(FUN_00fde210);
}
