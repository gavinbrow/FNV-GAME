class SCRIPT_PARAMETER;
class SCRIPT_HEADER;
class TESObjectREFR;
class Script;
class ScriptLocals;

bool __cdecl ExtractArgs(const SCRIPT_PARAMETER*, const char*, unsigned int*,
    TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);

bool __cdecl FUN_0059c010(TESObjectREFR*, unsigned int, void*, double&);

bool __cdecl FUN_005b4b80(const SCRIPT_PARAMETER* parameters, const char* scriptData,
    TESObjectREFR* container, TESObjectREFR* scriptOwner, Script* script,
    ScriptLocals* locals, double& result, unsigned int& opcodeOffset)
{
    unsigned int value = 0;
    if (!ExtractArgs(parameters, scriptData, &opcodeOffset, container, scriptOwner,
                     script, locals, &value))
        return false;
    return FUN_0059c010(container, value, 0, result);
}