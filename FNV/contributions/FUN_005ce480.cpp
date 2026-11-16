
struct ValueContext {
    int FUN_0084e3a0();
};
extern void __cdecl FUN_005acc70(int* value, double* result);
extern void __cdecl FUN_00703c00(const char* label, int value);
extern char DAT_0103b76c;
typedef ValueContext* (__thiscall *ActorContextMethod)(Actor*);
bool __cdecl FUN_005ce480(const SCRIPT_PARAMETER* parameters, const char* compiled, TESObjectREFR* object,
    TESObjectREFR* container, Script* script, ScriptLocals* locals, double& result, unsigned int& offset) {
    result = 0.0;
    Actor* actor = dynamic_cast<Actor*>(object);
    int value = 0;
    if (actor) {
        ValueContext* context = reinterpret_cast<ActorContextMethod>((*reinterpret_cast<void***>(actor))[0x42c / 4])(actor);
        if (context) {
            value = context->FUN_0084e3a0();
            FUN_005acc70(&value, &result);
        }
    }
    if (tlsData.bConsoleEcho)
        FUN_00703c00(&DAT_0103b76c, value);
    return true;
}
