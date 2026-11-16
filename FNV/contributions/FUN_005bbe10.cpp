
class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

struct ToggleTarget {
    const char* __thiscall GetName() const;
};

extern ToggleTarget* __cdecl FUN_00ec43fb(TESObjectREFR*, int, const void*, const void*, int);
extern int DAT_011841cc;
extern int DAT_011846d4;
extern const char DAT_010399b8[];
extern const char DAT_010399bc[];
extern const char DAT_01039f58[];
extern __declspec(thread) bool g_bConsoleEcho;
extern void __cdecl DebugLog(const char*, ...);

bool __cdecl FUN_005bbe10(
    const SCRIPT_PARAMETER* parameters, const char* scriptData,
    TESObjectREFR* thisObject, TESObjectREFR* container,
    Script* script, ScriptLocals* locals, double& result,
    unsigned int& opcodeOffset)
{
    ToggleTarget* target = 0;
    target = FUN_00ec43fb(thisObject, 0, &DAT_011841cc, &DAT_011846d4, 0);
    if (target != 0) {
        reinterpret_cast<bool*>(target)[0xbc] = !reinterpret_cast<bool*>(target)[0xbc];
        if (g_bConsoleEcho) {
            const char* state;
            if (reinterpret_cast<bool*>(target)[0xbc]) {
                state = DAT_010399bc;
            } else {
                state = DAT_010399b8;
            }
            DebugLog(DAT_01039f58, target->GetName(), state);
        }
    }
    return true;
}
