extern bool __cdecl FUN_005a27e0(TESObjectREFR*, void*, void*, double&);
extern char DAT_0103b84c;

bool __cdecl FUN_005ceb90(
    const SCRIPT_PARAMETER* parameters,
    const char* scriptData,
    TESObjectREFR* thisObject,
    TESObjectREFR* container,
    Script* script,
    ScriptLocals* locals,
    double& result,
    unsigned int& opcodeOffset)
{
    if (!FUN_005a27e0(thisObject, 0, 0, result))
        return false;

    if (g_tls.bDebug)
        _DebugLog(&DAT_0103b84c, result);

    return true;
}