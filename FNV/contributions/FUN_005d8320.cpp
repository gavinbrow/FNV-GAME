class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern bool ExtractArgs(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);

struct UIState {
    bool FUN_005bb4d0();
    void FUN_00ad7230(bool enabled);
};

UIState* __cdecl FUN_00453a70();

bool __cdecl FUN_005d8320(const SCRIPT_PARAMETER* parameters, const char* compiled,
    TESObjectREFR* reference, TESObjectREFR* container, Script* script,
    ScriptLocals* locals, double& result, unsigned int& offset)
{
    int newState;
    if (!ExtractArgs(parameters, compiled, &offset, reference, container, script, locals, &newState))
        return false;

    if (newState != 0 && !FUN_00453a70()->FUN_005bb4d0()) {
        FUN_00453a70()->FUN_00ad7230(true);
    } else if (newState == 0 && FUN_00453a70()->FUN_005bb4d0()) {
        FUN_00453a70()->FUN_00ad7230(false);
    }
    return true;
}