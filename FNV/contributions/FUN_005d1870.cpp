struct SCRIPT_PARAMETER;
class ScriptLocals;
class Script;
class TESObjectREFR;

bool __cdecl FUN_005a2a50(TESObjectREFR*, void*, void*, double&);

bool __cdecl FUN_005d1870(
    const SCRIPT_PARAMETER* apParameters,
    const char* apCompiledParams,
    TESObjectREFR* apRefObject,
    TESObjectREFR* apContainer,
    Script* apScript,
    ScriptLocals* apScriptLocals,
    double& afReturnValue,
    unsigned int& auiOffset)
{
    FUN_005a2a50(apRefObject, 0, 0, afReturnValue);
    return true;
}