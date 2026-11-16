struct BSTaskletManagerCallback
{
    const void* field00;

    BSTaskletManagerCallback* FUN_00b00e40(int value);
};

extern BSTaskletManagerCallback DAT_0126782c;
extern const unsigned char DAT_010c3b68;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fddd20();

// @fnv 0x00fbcb40
extern "C" void __cdecl FUN_00fbcb40()
{
    DAT_0126782c.FUN_00b00e40(0);
    DAT_0126782c.field00 = &DAT_010c3b68;
    atexit(FUN_00fddd20);
}
