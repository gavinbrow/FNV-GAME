class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;
bool __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int&, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, unsigned int*, unsigned int*);
bool __cdecl FUN_005a0f90(TESObjectREFR*, unsigned int, unsigned int, double&);

bool __cdecl FUN_005cc2f0(const SCRIPT_PARAMETER* parameters, const char* scriptData,
    TESObjectREFR* reference, TESObjectREFR* container,
    Script* script, ScriptLocals* locals, double& result,
    unsigned int& opcodeOffset)
{
    result = 0.0;
    unsigned int firstIndex;
    unsigned int lastIndex;
    lastIndex = 0xFFFFFFFF;
    firstIndex = 0;
    if (!FUN_005accb0(parameters, scriptData, opcodeOffset,
        reference, container, script, locals, &firstIndex, &lastIndex))
        return false;
    if (reference)
        return FUN_005a0f90(reference, firstIndex, lastIndex, result);
    return true;
}