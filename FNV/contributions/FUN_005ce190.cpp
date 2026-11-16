struct FUN_0047eb90_Class {
    void __thiscall FUN_0047eb90(unsigned int state);
};
extern "C" unsigned char __cdecl FUN_005accb0(
    unsigned int arg1, unsigned int arg2, unsigned int last,
    unsigned int arg3, unsigned int arg4, unsigned int arg5,
    unsigned int arg6, FUN_0047eb90_Class** object, unsigned int* output);

bool __cdecl FUN_005ce190(unsigned int arg1, unsigned int arg2, unsigned int arg3,
                          unsigned int arg4, unsigned int arg5, unsigned int arg6,
                          unsigned int arg7, unsigned int arg8)
{
    FUN_0047eb90_Class* state = 0;
    unsigned int result = 0;
    if (!FUN_005accb0(arg1, arg2, arg8, arg3, arg4, arg5, arg6, &state, &result))
        return false;
    if (result)
        state->FUN_0047eb90(1);
    else
        state->FUN_0047eb90(0);
    return true;
}