class C4E7770Setting
{
public:
    void FUN_0044f440(const char* name, float value);
};

extern C4E7770Setting DAT_01267c6c;
extern const char DAT_010c4e90[];
extern float DAT_01013974;
extern void __cdecl FUN_00fddef0();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00fbce30
void FUN_00fbce30()
{
    DAT_01267c6c.FUN_0044f440(DAT_010c4e90, DAT_01013974);
    atexit(FUN_00fddef0);
}
