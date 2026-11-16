extern float DAT_011c83c4;
extern void* DAT_011dea3c;
float* __fastcall FUN_00403e20(float*);
unsigned short __fastcall FUN_0087f9f0(void*);
struct RefLevel { unsigned int __thiscall FUN_00567e10(bool); };

int __thiscall FUN_00501270_shell::FUN_005011a0(TESObjectREFR* apRef)
{
    unsigned int result = reinterpret_cast<FUN_00501a30_shell*>(this)->FUN_00501a30(
        reinterpret_cast<Script*>(apRef));
    if (reinterpret_cast<FUN_00501250_shell*>(this)->FUN_00501250()) {
        unsigned int level = apRef
            ? reinterpret_cast<RefLevel*>(apRef)->FUN_00567e10(false)
            : FUN_0087f9f0(DAT_011dea3c);
        result += (unsigned int)((double)level * *FUN_00403e20(&DAT_011c83c4));
        if (result > 4) result = 4;
    }
    return result;
}