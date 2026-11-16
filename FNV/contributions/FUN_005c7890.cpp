bool __cdecl FUN_005accb0(
    const SCRIPT_PARAMETER* parameters, const char* argumentData,
    unsigned int& opcodeOffset, TESObjectREFR* subject, TESObjectREFR* target,
    Script* script, ScriptLocals* locals, unsigned int* extractedValue);

bool __cdecl FUN_0059f240(
    TESObjectREFR* subject, unsigned int extractedValue, int option, double& result);

bool __cdecl FUN_005c7890(
    const SCRIPT_PARAMETER* parameters, const char* argumentData,
    TESObjectREFR* subject, TESObjectREFR* target, Script* script,
    ScriptLocals* locals, double& result, unsigned int& opcodeOffset)
{
    unsigned int extractedValue = 0;
    if (!FUN_005accb0(parameters, argumentData, opcodeOffset,
                       subject, target, script, locals, &extractedValue))
        return false;

    return FUN_0059f240(subject, extractedValue, 0, result);
}