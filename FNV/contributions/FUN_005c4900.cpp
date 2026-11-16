struct SCRIPT_PARAMETER;
struct TESObjectREFR;
struct Script;
struct ScriptLocals;

bool __cdecl FUN_0059d100(TESObjectREFR* reference, ScriptLocals* locals, void* unused, double& result);

bool __cdecl FUN_005c4900(
    const SCRIPT_PARAMETER* parameters,
    const char* compiledParams,
    TESObjectREFR* reference,
    TESObjectREFR* container,
    Script* script,
    ScriptLocals* locals,
    double& result,
    unsigned int& offset)
{
    return FUN_0059d100(reference, locals, 0, result);
}