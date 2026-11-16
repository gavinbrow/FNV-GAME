
struct ScriptExtended { void FUN_005ac340(TESObjectREFR*); };
struct TargetContext { virtual void unused(); virtual TESObjectREFR* GetActor(ScriptLocals*); };
struct ScriptEffectShell : ScriptEffect { TargetContext* FUN_0059bb30(); void FUN_00827ac0(); };
void ScriptEffectShell::FUN_00827ac0() {
    if (pScript != 0) {
        pEffectLocals = pScript->CloneLocals();
        ((ScriptExtended*)pScript)->FUN_005ac340(FUN_0059bb30()->GetActor(pEffectLocals));
    }
}
