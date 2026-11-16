struct FUN_005a20b0_Standin {
    int FUN_005a20b0();
};
extern "C" void __cdecl FUN_00703c00(const char*, ...);
extern const char str_010359b4[];
__declspec(thread) unsigned char g_tlsFlag;

bool __cdecl FUN_005a2050(TESObjectREFR* reference, void* arg1, void* arg2, double& result)
{
    result = 0.0;
    result = (double)((FUN_005a20b0_Standin*)g_thePlayer)->FUN_005a20b0();
    if (g_tlsFlag)
        FUN_00703c00(str_010359b4, result);
    return true;
}