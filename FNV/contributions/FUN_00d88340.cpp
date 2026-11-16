struct State
{
    int unk00;
    void* owner;
    int unk08;
    int eventCode;
    int unk10; int unk14; int unk18; int unk1c;
    void* resetA; int unk24;
    void* desiredA;
    void* currentA;
    void* resetB;
    int unk34;
    void* desiredB;
    void* currentB;
    int callbackFlags;
    int unk44;
    volatile float* end;
    volatile float* current;
};
void __cdecl FUN_00d8aac0(void* owner, void* current, int eventCode, int flags);
void __cdecl FUN_00d88340(State* state, int reset)
{
    if (reset == 0)
    {
        state->currentA = state->resetA;
        state->currentB = state->resetB;
    }
    volatile float* p = state->current;
    while (p < state->end)
    {
        *p = 0.0f;
        ++p;
    }
    state->current = state->end;
    if (state->currentA != state->desiredA)
        FUN_00d8aac0(state->owner, state->currentA, state->eventCode, state->callbackFlags);
    if (state->currentB != state->desiredB)
        FUN_00d8aac0(state->owner, state->currentB, state->eventCode, state->callbackFlags);
    state->currentA = state->desiredA;
    state->currentB = state->desiredB;
}
