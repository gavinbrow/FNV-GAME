
struct AnimationAction {
    void FUN_00475b20();
};
AnimationAction* __cdecl FUN_00475400(unsigned int action);

struct ActorActions {
    bool FUN_00452370();
    bool FUN_00477ba0();
    unsigned int FUN_007af430(ActorActions* actor, float amount, bool repeat);
    void FUN_00579220(float amount, bool repeat);
};

void ActorActions::FUN_00579220(float amount, bool repeat) {
    if (FUN_00452370()) {
        if (!FUN_00477ba0() || repeat) {
            FUN_00475400(FUN_007af430(this, amount, repeat))->FUN_00475b20();
        }
    }
}
