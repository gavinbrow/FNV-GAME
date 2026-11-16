struct TalkReference : TESObjectREFR {
    TESTopic* FUN_00567790();
};

struct DialogueState {
    void FUN_00902c60();
    void FUN_00902680();
};

TESTopic* __cdecl FUN_0061a2d0(int category, int subtype);

struct DialogueProcess : MiddleHighProcess {
    void FUN_00902bd0(Actor* actor, DialogueState* state);
};

void DialogueProcess::FUN_00902bd0(Actor* actor, DialogueState* state)
{
    TESTopic* ownerTopic = FUN_0044ddc0(state);
    TESObjectREFR* reference = vfn_128();
    TESTopic* nextTopic = reference ? static_cast<TalkReference*>(reference)->FUN_00567790() : 0;
    TESTopic* referenceTopic = FUN_0061a2d0(2, 20);
    state->FUN_00902c60();
    state->FUN_00902680();
    vfn_2a4(actor, referenceTopic, false, false, true, false);
}