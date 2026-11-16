class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;
extern bool __cdecl ExtractArgs(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);
extern void __cdecl FUN_005f6110(unsigned int, unsigned int);
bool __cdecl FUN_005dfe30(const SCRIPT_PARAMETER* parameters, const char* scriptData, TESObjectREFR* reference, TESObjectREFR* container, Script* script, ScriptLocals* locals, double& result, unsigned int& opcodeOffset)
{
    unsigned int parsedArgument;
    unsigned int actionFlag = 1;
    if (!ExtractArgs(parameters, scriptData, &opcodeOffset, reference, container, script, locals, &parsedArgument)) {
        return false;
    }
    FUN_005f6110(parsedArgument, actionFlag);
    return true;
}