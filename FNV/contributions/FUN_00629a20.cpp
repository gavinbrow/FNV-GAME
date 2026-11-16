struct FUN_00629a20_State {
    bool value;
    int FUN_004a4840(void* owner, int input);
};
struct FUN_00629a20_Class {
    void FUN_00629f70(int result);
    void FUN_00629a20(int input);
};
void FUN_00629a20_Class::FUN_00629a20(int input) {
    FUN_00629a20_State state = {};
    FUN_00629f70(state.FUN_004a4840(this,input));
}