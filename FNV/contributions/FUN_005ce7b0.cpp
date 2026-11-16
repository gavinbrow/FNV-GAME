extern "C" void* __cdecl FUN_00ec43fb(
    TESObjectREFR*, unsigned int, const void*, const void*, unsigned int);
extern unsigned char DAT_011841cc;
extern unsigned char DAT_011846d4;
extern char str_0103b804[];

bool __cdecl FUN_005ce7b0(
    const SCRIPT_PARAMETER* parameters, const char* compiled,
    TESObjectREFR* reference, TESObjectREFR* container,
    Script* script, ScriptLocals* locals, double& result, unsigned int& offset)
{
    FUN_005bf800_Class* action = static_cast<FUN_005bf800_Class*>(
        FUN_00ec43fb(reference, 0, &DAT_011841cc, &DAT_011846d4, 0));
    if (action) {
        result = 1.0;
        int set = 0;
        if (!ExtractArgs(parameters, compiled, &offset, reference,
                         container, script, locals, &set))
            return false;
        if (set) {
            action->FUN_005bf800(true);
        } else {
            action->FUN_005bf800(false);
        }
        if (g_tls.bDebug) {
            _DebugLog(str_0103b804, set);
        }
    }
    return true;
}
