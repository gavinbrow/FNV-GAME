class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267cd8;
extern const char DAT_010c4fa4[];
extern const float DAT_01017718;
extern void __cdecl FUN_00fddf80();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbcfe0
void FUN_00fbcfe0()
{
    DAT_01267cd8.FUN_0044f440(DAT_010c4fa4, DAT_01017718);
    atexit(FUN_00fddf80);
}
