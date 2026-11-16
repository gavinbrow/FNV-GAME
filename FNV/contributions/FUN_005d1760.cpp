
struct ScriptFallback {
    int __thiscall FUN_007af430();
};
extern ScriptFallback* DAT_011dea3c;
bool __cdecl FUN_005accb0(int, int, int, int, int, int, int, int*, int*);
void __cdecl FUN_005a2ed0(int, int, int, double*);

bool __cdecl FUN_005d1760(int a1, int a2, int a3, int a4,
                           int a5, int a6, double* result, int a8)
{
    *result = 0.0;
    int fallback;
    {
        int parsedValue;
        parsedValue = 0;
        fallback = 0;
        if (!FUN_005accb0(a1, a2, a8, a3, a4, a5, a6, &parsedValue, &fallback)) {
            return false;
        }
        if (fallback == 0) {
            fallback = DAT_011dea3c->FUN_007af430();
        }
        FUN_005a2ed0(a3, parsedValue, fallback, result);
        return true;
    }
}
