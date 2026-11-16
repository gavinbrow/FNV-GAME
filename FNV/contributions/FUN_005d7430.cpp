class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

void __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int&, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, int*);
extern "C" void __cdecl FUN_00705830(int, int, int);

bool __cdecl FUN_005d7430(const SCRIPT_PARAMETER* parameters, const char* scriptData,
                          TESObjectREFR* thisObject, TESObjectREFR* container,
                          Script* script, ScriptLocals* locals, double& result,
                          unsigned int& opcodeOffset) {
    int action = 3;
    FUN_005accb0(parameters, scriptData, opcodeOffset, thisObject,
                 container, script, locals, &action);
    FUN_00705830(0, action - 1, 0);
    return true;
}