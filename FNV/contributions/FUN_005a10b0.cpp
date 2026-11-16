struct RefOps { TESForm* __thiscall FUN_007af430(); };
struct FormOps { unsigned int __thiscall FUN_00401170(); };
struct ActorOps { TESClass* __thiscall FUN_00502430(); };
struct ClassOps { bool __thiscall FUN_005f6e60(); };
extern __declspec(thread) bool tls_conditionEcho;
void __cdecl FUN_00703c00(const char* format, ...);
bool __cdecl FUN_005a10b0(TESObjectREFR* reference, void* arg1, void* arg2, double& result) {
    result = 0.0;
    if (reference) {
        TESForm* actorBase = 0;
        if (((FormOps*)((RefOps*)reference)->FUN_007af430())->FUN_00401170() == 42)
            actorBase = ((RefOps*)reference)->FUN_007af430();
        if (actorBase) {
            if (((ActorOps*)actorBase)->FUN_00502430() &&
                ((ClassOps*)((ActorOps*)actorBase)->FUN_00502430())->FUN_005f6e60())
                result = 1.0;
        }
    }
    if (tls_conditionEcho)
        FUN_00703c00("Is Guard >> %0.2f", result);
    return true;
}