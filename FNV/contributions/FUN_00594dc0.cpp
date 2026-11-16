bool __cdecl FUN_00594e40(TESObjectREFR*, unsigned int, unsigned int, double&);
bool __cdecl FUN_00594dc0(const SCRIPT_PARAMETER* parameters, const char* compiledParams,
    TESObjectREFR* reference, TESObjectREFR* container, Script* script,
    ScriptLocals* locals, double& result, unsigned int& offset)
{
    bool bResult = true;
    unsigned int iParam1 = 0;
    unsigned int iParam2 = 0;
    if (!ExtractArgs(parameters, compiledParams, &offset,
        reference, container, script, locals, &iParam1, &iParam2))
        return false;
    bResult = FUN_00594e40(reference, iParam1, iParam2, result);
    return bResult;
}