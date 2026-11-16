struct FUN_00615580_Class
{
    void FUN_00615580(int mode, float value);
};

bool __cdecl FUN_005ddf10(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)
{
    int uStack_8 = 0;
    float uStack_c = 0.0f;
    int iStack_10 = 0;
    if (!ExtractArgs(apParameters, apCompiledParams, &auiOffset, apRefObject, apContainer, apScript, apScriptLocals, &iStack_10, &uStack_8, &uStack_c))
        return false;
    if (uStack_8 >= 0 && uStack_8 <= 1) {
        ((FUN_00615580_Class*)iStack_10)->FUN_00615580(uStack_8, uStack_c);
    } else {
        return false;
    }
    return true;
}