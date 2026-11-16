extern "C" bool __cdecl FUN_005a2440(TESObjectREFR*, int, int, double&);

bool __cdecl FUN_005cea90(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)
{
    int iValue = 0;
    if (!ExtractArgs(apParameters, apCompiledParams, &auiOffset, apRefObject, apContainer, apScript, apScriptLocals, &iValue))
        return false;
    return FUN_005a2440(apRefObject, iValue, 0, afReturnValue);
}