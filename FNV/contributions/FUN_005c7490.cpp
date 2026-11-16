class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern "C" bool __cdecl FUN_0059ec30(TESObjectREFR*, void*, void*, double&);

bool __cdecl FUN_005c7490(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)
{
    return FUN_0059ec30(apRefObject, 0, 0, afReturnValue);
}
