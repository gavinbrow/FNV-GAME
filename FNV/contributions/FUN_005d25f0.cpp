class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern "C" bool __cdecl FUN_005a3390(TESObjectREFR*, void*, void*, double&);

void __cdecl FUN_005d25f0(const SCRIPT_PARAMETER* apParameters, const char* apCompiledParams, TESObjectREFR* apRefObject, TESObjectREFR* apContainer, Script* apScript, ScriptLocals* apScriptLocals, double& afReturnValue, unsigned int& auiOffset)
{
    FUN_005a3390(apRefObject, 0, 0, afReturnValue);
}
