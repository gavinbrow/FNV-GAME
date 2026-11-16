struct BSTaskletManagerCallback
{
    const void* field00;

    BSTaskletManagerCallback* FUN_00b00e40(int value);
};

extern BSTaskletManagerCallback DAT_01267b0c;
extern const unsigned char DAT_010c3b74;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fddd30();

// @fnv 0x00fbcb70
extern "C" void __cdecl FUN_00fbcb70()
{
    DAT_01267b0c.FUN_00b00e40(1);
    DAT_01267b0c.field00 = &DAT_010c3b74;
    atexit(FUN_00fddd30);
}
