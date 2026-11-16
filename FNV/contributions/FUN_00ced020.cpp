struct Receiver { void FUN_00cecc90(float value); };
struct State { int first; int count; int context; };
void FUN_00cebbb0(void* state, float zero, void* receiver);
int __cdecl FUN_00ced020(int owner, int context, int count, float limit, Receiver* receiver, float value) {
    State state;
    if (limit <= 0.0f) return 1;
    if (count < 1) return 1;
    state.count = count;
    state.context = context;
    state.first = owner;
    FUN_00cebbb0(&state, 0.0f, receiver);
    receiver->FUN_00cecc90(limit);
    return 0;
}

