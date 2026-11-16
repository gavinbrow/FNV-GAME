bool __cdecl FUN_005db4e0(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)
{
    unsigned int uStack_8 = 0;
    if (!ExtractArgs(apParameters, apCompiledParams, &auiOffset, apRefObject, apContainer, apScript, apScriptLocals, &uStack_8))
        return false;
    return Script::GetFactionRelationConditionFunction(apRefObject, (void*)uStack_8, 0, afReturnValue);
}