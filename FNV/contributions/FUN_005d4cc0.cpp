
struct SpecialActorState {
    int FUN_00401170();
    void FUN_004ff0e0(unsigned int index);
};
struct RefActor {
    SpecialActorState* FUN_007af430();
};
extern void __cdecl FUN_005accb0(
    void* parameters, const char* text,
    unsigned int* offset, RefActor* target,
    void* speaker, void* script, void* variables,
    unsigned int* outIndex);

bool __cdecl FUN_005d4cc0(
    void* parameters, const char* text, RefActor* target,
    void* speaker, void* script, void* variables,
    double* outResult, unsigned int* offset)
{
    unsigned int itemIndex = 0;
    FUN_005accb0(parameters, text, offset, target, speaker, script, variables, &itemIndex);
    if (target != 0) {
        if (target->FUN_007af430()->FUN_00401170() == 22) {
            SpecialActorState* state = target->FUN_007af430();
            state->FUN_004ff0e0(itemIndex);
        }
    }
    return true;
}
