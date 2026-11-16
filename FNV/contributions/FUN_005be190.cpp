class SCRIPT_PARAMETER;
class Script;
class ScriptLocals;
class ActorValueOwner {
public:
    virtual void Method0();
    virtual void Method1();
    virtual void Method2();
    virtual float GetValue(unsigned int actorValue);
};
extern bool __cdecl ExtractArgs(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);
extern bool __cdecl FUN_00406d70(unsigned int, unsigned int);
extern const char* __cdecl FUN_0066eac0(unsigned int);
extern void __cdecl FUN_00703c00(const char*, const char*);
extern const char DAT_0103a310[];
typedef void (__thiscall *ActorValueChange)(Actor*, unsigned int, float, int);
bool __cdecl FUN_005be190(const SCRIPT_PARAMETER* parameters, const char* compiledParams, TESObjectREFR* reference, TESObjectREFR* container, Script* script, ScriptLocals* locals, double& result, unsigned int& offset)
{
    unsigned int actorValue = 0;
    int newValue = 0;
    if (!ExtractArgs(parameters, compiledParams, &offset, reference, container, script, locals, &actorValue, &newValue))
        return false;
    Actor* pActor = dynamic_cast<Actor*>(reference);
    if (pActor) {
        if (!FUN_00406d70(actorValue, 0x4000)) {
            float amount = (float)((double)newValue - (double)(reinterpret_cast<ActorValueOwner*>((char*)pActor + 0xa4))->GetValue(actorValue));
            ((ActorValueChange)(*(void***)pActor)[0x3a4 / 4])(pActor, actorValue, amount, 0);
        } else if (g_tls.bDebug) {
            FUN_00703c00(DAT_0103a310, FUN_0066eac0(actorValue));
        }
    }
    return true;
}