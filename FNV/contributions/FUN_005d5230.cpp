class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern bool ExtractArgs(
    const SCRIPT_PARAMETER* parameters,
    const char* compiledParams,
    unsigned int* opcodeOffset,
    TESObjectREFR* reference,
    TESObjectREFR* container,
    Script* script,
    ScriptLocals* locals,
    ...);

struct ScriptEventManager {
    void FUN_00966a70(int eventId, bool allowConsoleEcho);
};

extern ScriptEventManager* DAT_011dea3c;
extern __declspec(thread) bool g_bConsoleEcho;

bool __cdecl FUN_005d5230(
    const SCRIPT_PARAMETER* parameters,
    const char* compiledParams,
    TESObjectREFR* reference,
    TESObjectREFR* container,
    Script* script,
    ScriptLocals* locals,
    double& result,
    unsigned int& opcodeOffset)
{
    int eventId = 0;
    if (!ExtractArgs(parameters, compiledParams, &opcodeOffset,
                     reference, container, script, locals, &eventId)) {
        return false;
    }
    if (eventId != 0) {
        DAT_011dea3c->FUN_00966a70(eventId, g_bConsoleEcho);
    }
    return true;
}