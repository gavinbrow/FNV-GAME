
struct TESForm {
    virtual void v00();
};
struct TESObjectREFR : TESForm {
    void FUN_00564db0(int flag);
};
struct Actor : TESObjectREFR {};
TESForm* __cdecl GetFormByNumericID(unsigned int id);

struct ActorListNode {
    Actor* data;
    ActorListNode* next;
    bool FUN_008256d0();
    Actor** FUN_006815c0();
    ActorListNode* FUN_00726070();
    void FUN_00726c60(Actor* const& actor);
    void FUN_00905330(Actor** data);
    void FUN_0063f7b0();
};
struct FUN_009ec400_Host {
    int unk00;
    int unk04;
    TESObjectREFR* ref;
    Actor* actor;
    int unk10;
    int unk14;
    int unk18;
    ActorListNode actors;
    TESForm* other;
    void FUN_009ec400(void* unused);
};

void FUN_009ec400_Host::FUN_009ec400(void* unused)
{
    ref = ref ? dynamic_cast<TESObjectREFR*>(GetFormByNumericID((unsigned int)ref)) : 0;
    actor = actor ? dynamic_cast<Actor*>(GetFormByNumericID((unsigned int)actor)) : 0;
    other = other ? GetFormByNumericID((unsigned int)other) : 0;
    ActorListNode* current = &actors;
    ActorListNode* previous = 0;
    while (current && !current->FUN_008256d0()) {
        Actor* entry = *current->FUN_006815c0();
        bool erase = false;
        if (entry) {
            entry = entry ? dynamic_cast<Actor*>(GetFormByNumericID((unsigned int)entry)) : 0;
            if (entry) {
                current->FUN_00726c60(entry);
            } else {
                erase = true;
            }
        } else {
            erase = true;
        }
        if (erase) {
            if (previous) {
                previous->FUN_00905330(current->FUN_006815c0());
                current = previous->FUN_00726070();
            } else {
                current->FUN_0063f7b0();
            }
        } else {
            previous = current;
            current = current->FUN_00726070();
        }
    }
    if (ref) {
        ref->FUN_00564db0(1);
    }
}
