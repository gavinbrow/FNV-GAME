
struct ActorValueMethods { void** vtable; };
struct ScriptEffectActor { ActorValueMethods* __thiscall FUN_008d8520(); };
typedef int (__thiscall* ReadActorValue)(ActorValueMethods*);
typedef void (__thiscall* ApplyActorValues)(TESObjectREFR_005d5390*, TESObjectREFR_005d5390*, int, int, int);
bool __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int&, TESObjectREFR_005d5390*, TESObjectREFR*, Script*, ScriptLocals*, TESObjectREFR_005d5390**);
bool __cdecl FUN_005cfdf0(const SCRIPT_PARAMETER* parameters, const char* script,
    TESObjectREFR_005d5390* target, TESObjectREFR* container, Script* scriptObject,
    ScriptLocals* locals, double& result, unsigned int& offset) {
    TESObjectREFR_005d5390* resolved = 0;
    if (!FUN_005accb0(parameters, script, offset, target, container,
                      scriptObject, locals, &resolved))
        return false;
    if (target->V64() && resolved && resolved->V64()) {
        ScriptEffectActor* actor = reinterpret_cast<ScriptEffectActor*>(target);
        {
            ActorValueMethods* first = actor->FUN_008d8520();
            ActorValueMethods* third = actor->FUN_008d8520();
            ActorValueMethods* second = actor->FUN_008d8520();
            reinterpret_cast<ApplyActorValues>((*(void***)resolved)[0x374 / 4])(
                resolved, reinterpret_cast<TESObjectREFR_005d5390*>(actor),
                reinterpret_cast<ReadActorValue>(second->vtable[0x4c8 / 4])(second),
                reinterpret_cast<ReadActorValue>(third->vtable[0x4d4 / 4])(third),
                reinterpret_cast<ReadActorValue>(first->vtable[0x4d0 / 4])(first));
        }
    }
    return true;
}
