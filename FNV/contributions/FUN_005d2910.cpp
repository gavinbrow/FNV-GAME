extern "C" bool __cdecl FUN_005a2a50(void*, int, int, double*);
extern "C" void __cdecl FUN_00703c00(const char*, ...);
extern const char DAT_0103bed4[];
extern __declspec(thread) unsigned char g_debugLoggingFlag;

extern "C" bool __cdecl FUN_005d2910(void* first, void* second, void* condition, void* fourth, void* fifth, void* sixth, double* result)
{
    bool success = FUN_005a2a50(condition, 0, 0, result);
    if (g_debugLoggingFlag) {
        FUN_00703c00(DAT_0103bed4, *result);
    }
    return success;
}