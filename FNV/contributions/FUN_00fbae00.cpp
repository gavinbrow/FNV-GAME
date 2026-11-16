class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_012023dc;
extern const char DAT_010bc44c[];
extern const float DAT_01022958;
extern void __cdecl FUN_00fdd370();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbae00
void FUN_00fbae00()
{
    DAT_012023dc.FUN_0044f440(DAT_010bc44c, DAT_01022958);
    atexit(FUN_00fdd370);
}
