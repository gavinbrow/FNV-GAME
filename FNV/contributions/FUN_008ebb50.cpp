struct ActorForReset : Actor {
    void __thiscall FUN_005ce9d0(bool);
    bool __thiscall FUN_004997b0();
    void __thiscall FUN_008b39f0(unsigned int);
    void __thiscall FUN_008b3a80(unsigned int);
};
struct FUN_008ebb50_Class {
    void FUN_008ebb50(ActorForReset* actor);
};
void FUN_008ebb50_Class::FUN_008ebb50(ActorForReset* actor) {
    actor->FUN_005ce9d0(true);
    if (!actor->FUN_004997b0())
        actor->FUN_00884f80();
    actor->FUN_008b39f0(0x400);
    typedef bool (__thiscall *VFunc)(FUN_008ebb50_Class*, ActorForReset*, bool);
    if ((*(VFunc*)((char*)*(void**)this + 0x7c8))(this, actor, false)) {
        if (actor->FUN_004997b0())
            actor->FUN_00884f80();
        actor->FUN_005ce9d0(false);
        actor->FUN_008b3a80(0x400);
    }
}