struct FUN_00401170_Mode {
    unsigned int __thiscall FUN_00401170();
};
struct FUN_0059ecc0_Ref {
    FUN_00401170_Mode* __thiscall FUN_007af430();
};
extern __declspec(thread) unsigned char traceState[];
extern const char DAT_01035260[];
void __cdecl FUN_00703c00(const char* text, double result);
bool __cdecl FUN_0059ecc0(FUN_0059ecc0_Ref* reference, void* arg1, void* arg2, double& result)
{
    result = 0.0;
    if (reference != 0) {
        if (reference->FUN_007af430()->FUN_00401170() == 0x2b) {
            result = 1.0;
        }
    }
    if (traceState[0x268] != 0) {
        FUN_00703c00(DAT_01035260, result);
    }
    return true;
}