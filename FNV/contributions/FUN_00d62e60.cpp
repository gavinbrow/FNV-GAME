struct FUN_00dd9380_class { void* FUN_00dd9380(const char* name, void* factory); };
extern int DAT_01269cd0;
extern int DAT_01268fbc;
void* __cdecl FUN_00d62e20();
void __cdecl FUN_00d62e60()
{
    void* result = ((FUN_00dd9380_class*)DAT_01269cd0)->FUN_00dd9380("WeldingViewer", (void*)&FUN_00d62e20);
    DAT_01268fbc = (int)result;
}
